# Setting up CloudFront Distribution for S3 Bucket [^1]

This guide demonstrates how to set up a CloudFront distribution for an S3 bucket with proper security
configurations and Origin Access Control (OAC).

## Prerequisites
• AWS CLI installed and configured
• An existing S3 bucket
• Running these commands from Singapore region

## Initial Setup

Set your bucket name as a variable: [^2]
```bash
BUCKET_NAME="XXXXXXXXXXXXXXXX"
```


## 1. Block Public Access to S3 Bucket

First, ensure the S3 bucket is properly secured by blocking all public access:

```bash
aws s3api put-public-access-block \
  --bucket ${BUCKET_NAME} \
  --public-access-block-configuration '{
    "BlockPublicAcls": true,
    "IgnorePublicAcls": true,
    "BlockPublicPolicy": true,
    "RestrictPublicBuckets": true
  }'
```


## 2. Get Bucket Domain Name

Get the S3 bucket domain name for CloudFront origin configuration, replace `ap-southeast-1` with your region:

bash
```
echo "Bucket domain name: $BUCKET_DOMAIN"
BUCKET_DOMAIN=$(aws s3api get-bucket-location \
  --bucket ${BUCKET_NAME} \
  --query 'join(``, [`'${BUCKET_NAME}'.s3.`, `ap-southeast-1`, `.amazonaws.com`])' \
  --output text)

echo "Bucket domain name: $BUCKET_DOMAIN"
```

## 3. Create Origin Access Control

Create an OAC for secure access between CloudFront and S3:

```bash
OAC_ID=$(aws cloudfront create-origin-access-control \
  --origin-access-control-config '{
    "Name": "OAC-'${BUCKET_NAME}'",
    "Description": "OAC for '${BUCKET_NAME}'",
    "SigningProtocol": "sigv4",
    "SigningBehavior": "always",
    "OriginAccessControlOriginType": "s3"
  }' \
  --query 'OriginAccessControl.Id' \
  --output text)

echo "Created OAC ID: $OAC_ID"
```

## 4. Create CloudFront Distribution

Create the CloudFront distribution with optimal settings for Singapore:

```bash
aws cloudfront create-distribution \
  --distribution-config '{
    "CallerReference": "'$(date +%s)'",
    "Origins": {
      "Quantity": 1,
      "Items": [
        {
          "Id": "S3-'${BUCKET_NAME}'",
          "DomainName": "'${BUCKET_DOMAIN}'",
          "S3OriginConfig": {
            "OriginAccessIdentity": ""
          },
          "OriginAccessControlId": "'${OAC_ID}'"
        }
      ]
    },
    "DefaultCacheBehavior": {
      "TargetOriginId": "S3-'${BUCKET_NAME}'",
      "ViewerProtocolPolicy": "redirect-to-https",
      "AllowedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"],
        "CachedMethods": {
          "Quantity": 2,
          "Items": ["GET", "HEAD"]
        }
      },
      "ForwardedValues": {
        "QueryString": false,
        "Cookies": {
          "Forward": "none"
        }
      },
      "MinTTL": 0,
      "DefaultTTL": 86400,
      "MaxTTL": 31536000,
      "Compress": true
    },
    "Enabled": true,
    "Comment": "Distribution for '${BUCKET_NAME}'",
    "PriceClass": "PriceClass_200",
    "HttpVersion": "http2",
    "IsIPV6Enabled": true
  }'
```


## 5. Configure S3 Bucket Policy

Create and apply the bucket policy to allow CloudFront access:

```bash
# Get Distribution ID and Account ID
DIST_ID=$(aws cloudfront list-distributions \
  --query 'DistributionList.Items[?Origins.Items[?Id==`S3-'${BUCKET_NAME}'`]].Id' \
  --output text)

ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# Create bucket policy

cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::'${BUCKET_NAME}'/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::'${ACCOUNT_ID}':distribution/'${DIST_ID}'"
                }
            }
        }
    ]
}
EOF

# Apply the bucket policy
aws s3api put-bucket-policy \
  --bucket ${BUCKET_NAME} \
  --policy file://bucket-policy.json
```


## 6. Verify Configuration

Verify all components are properly configured:

```bash
# Check distribution status
aws cloudfront get-distribution \
  --id $DIST_ID \
  --query 'Distribution.{Status:Status,DomainName:DomainName}' \
  --output table

# Verify bucket policy
aws s3api get-bucket-policy \
  --bucket ${BUCKET_NAME} \
  --output text | jq '.'

# Verify public access block
aws s3api get-public-access-block \
  --bucket ${BUCKET_NAME}
```

## Configuration Details

• **Price Class**: PriceClass_200 (optimal for Singapore, includes Asia edge locations)
• **Security**:
  • Public access blocked
  • Origin Access Control enabled
  • HTTPS enforced
  • Least privilege bucket policy
• **Cache Behavior**:
  • Default TTL: 24 hours (86400 seconds)
  • Maximum TTL: 365 days (31536000 seconds)
  • Compression enabled
  • Only GET and HEAD methods allowed
• **Protocol Support**:
  • HTTP/2 enabled
  • IPv6 enabled
  • HTTPS redirect enabled

## Notes

1. Before running the commands, set your bucket name:
  bash
   BUCKET_NAME="XXXXXXXXXXXXXXXX"

2. Distribution deployment takes approximately 15-20 minutes
3. The CloudFront domain name will be provided in the distribution details
4. Direct S3 access is blocked; content is only accessible through CloudFront
5. Clean up temporary files after setup:
  bash
   rm -f bucket-policy.json


[^1]: https://stackoverflow.com/questions/73899494

[^2]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
