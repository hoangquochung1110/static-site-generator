---
title: How to Set Up Amazon CloudFront with S3: A Complete Security Guide for 2025
date: 2025-02-12 17:00
description: Learn how to securely configure Amazon CloudFront distribution with S3 bucket using Origin Access Control (OAC). This step-by-step guide covers everything from blocking public access to implementing proper bucket policies for enhanced security.
category: blog
tags:
    - aws
---

# How to Set Up Amazon CloudFront with S3: A Complete Security Guide for 2025

Learn how to securely configure Amazon CloudFront distribution with S3 bucket using Origin Access Control (OAC). This step-by-step guide covers everything from blocking public access to implementing proper bucket policies for enhanced security.

## What You'll Learn
- How to secure S3 buckets by blocking public access
- Setting up Origin Access Control (OAC) for CloudFront
- Creating optimized CloudFront distributions for Asia-Pacific regions
- Implementing secure bucket policies for CloudFront access
- Verifying your CloudFront and S3 configuration

## Prerequisites
Before starting this tutorial, ensure you have:
- AWS CLI installed and configured on your system
- An existing S3 bucket
- Access to AWS Console with appropriate permissions
- Basic understanding of AWS services
- Commands configured for Singapore region (ap-southeast-1)

## Step 1: Secure Your S3 Bucket
First, we'll block all public access to your S3 bucket to ensure maximum security:

```bash
BUCKET_NAME="your-bucket-name"

aws s3api put-public-access-block \
  --bucket ${BUCKET_NAME} \
  --public-access-block-configuration '{
    "BlockPublicAcls": true,
    "IgnorePublicAcls": true,
    "BlockPublicPolicy": true,
    "RestrictPublicBuckets": true
  }'
```

## Step 2: Configure Bucket Domain Name
Retrieve your S3 bucket's domain name for CloudFront configuration:

```bash
BUCKET_DOMAIN=$(aws s3api get-bucket-location \
  --bucket ${BUCKET_NAME} \
  --query 'join(``, [`'${BUCKET_NAME}'.s3.`, `ap-southeast-1`, `.amazonaws.com`])' \
  --output text)

echo "Bucket domain name: $BUCKET_DOMAIN"
```

## Step 3: Set Up Origin Access Control (OAC)
Create an Origin Access Control for secure CloudFront-to-S3 communication:

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
```

## Step 4: Deploy CloudFront Distribution
Create an optimized CloudFront distribution with security best practices:

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

## Step 5: Implement Secure Bucket Policy
Create and apply a least-privilege bucket policy:

```bash
# Get Distribution ID and Account ID
DIST_ID=$(aws cloudfront list-distributions \
  --query 'DistributionList.Items[?Origins.Items[?Id==`S3-'${BUCKET_NAME}'`]].Id' \
  --output text)

ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# Create and apply bucket policy
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

aws s3api put-bucket-policy \
  --bucket ${BUCKET_NAME} \
  --policy file://bucket-policy.json
```

## Step 6: Verify Your Setup
Ensure all components are correctly configured:

```bash
# Verify distribution status
aws cloudfront get-distribution \
  --id $DIST_ID \
  --query 'Distribution.{Status:Status,DomainName:DomainName}' \
  --output table

# Check bucket policy
aws s3api get-bucket-policy \
  --bucket ${BUCKET_NAME} \
  --output text | jq '.'

# Confirm public access block
aws s3api get-public-access-block \
  --bucket ${BUCKET_NAME}
```

## Key Features and Benefits
- **Enhanced Security**:
  - Complete public access blocking
  - Origin Access Control implementation
  - HTTPS enforcement
  - Least-privilege bucket policies
- **Optimized Performance**:
  - 24-hour default cache duration
  - 365-day maximum cache duration
  - Automatic compression
  - HTTP/2 and IPv6 support
- **Asia-Pacific Optimization**:
  - PriceClass_200 configuration
  - Singapore region edge locations
  - Optimal latency for APAC users

## Important Notes
1. Distribution deployment typically takes 15-20 minutes
2. Content is only accessible through CloudFront, not directly via S3
3. Replace `your-bucket-name` with your actual S3 bucket name
4. Remember to clean up temporary files after setup:
   ```bash
   rm -f bucket-policy.json
   ```

## Troubleshooting Tips
- If distribution status shows "InProgress" for more than 30 minutes, check CloudFront console for errors
- Verify bucket policy syntax if CloudFront access is denied
- Ensure all public access blocks are enabled for maximum security
- Check CloudWatch metrics for distribution performance

## Conclusion
By following this guide, you've created a secure, optimized CloudFront distribution for your S3 bucket. This setup ensures your content is delivered efficiently while maintaining strong security controls. Remember to regularly review your configuration and update settings as needed to maintain optimal performance and security.
