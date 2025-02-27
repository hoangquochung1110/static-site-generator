Setting Up CloudFront with Custom Domain and SSL Certificate

## Step 1: Request an SSL Certificate from AWS Certificate Manager

Access AWS Console: Navigate to the AWS Management Console and go to the AWS Certificate Manager (ACM) in the us-east-1 region.

**us-east-1 region** is a must because https://stackoverflow.com/questions/37289994/aws-certificate-manager-do-regions-matter

Request a Public Certificate: Click on "Request a certificate" and select "Request a public certificate."

Add Domain Names: Enter your domain name (e.g., example.com) and any subdomains you want covered (e.g., *.example.com).

Choose Validation Method: Select DNS validation.

Create CNAME Records:

After requesting the certificate, ACM will provide you with CNAME records to validate your domain ownership.

Go to your Namecheap account, open the Advanced DNS tab for your domain, and add these CNAME records.

## Step 2: Set Up CloudFront Distribution
Access CloudFront Console: Navigate to the AWS CloudFront console.

Create Distribution:

Click on "Create Distribution" and choose "Get Started."

For static websites hosted on S3, enter your S3 bucket URL as the Origin Domain Name; otherwise, use another origin like API Gateway or EC2 if applicable.

Configure Settings:

Set Origin Protocol Policy to "Match Viewer."

Add Alternate Domain Names (CNAMEs) that match your domain (e.g., example.com, www.example.com).

Set Viewer Protocol Policy to "Redirect HTTP to HTTPS."

Allow all necessary HTTP methods (GET, HEAD, etc.) based on your application needs.

Select Custom SSL Certificate:

Choose the custom SSL certificate created in Step 1.

## Step 3: Configure DNS Records in Namecheap
Open Advanced DNS Tab: In Namecheap's dashboard for your domain, go to Advanced DNS settings.

Add New Record:

Create a new record of type CNAME for each subdomain or root domain pointing directly at CloudFront's distribution URL (e.g., d123456789.cloudfront.net).

Important Notes
The ACM certificate must be requested in us-east-1 for use with CloudFront distributions.

Do not remove original validation CNAME records unless no longer needed by any active certificates.