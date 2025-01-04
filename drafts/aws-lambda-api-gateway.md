
- Two types:
    - REST API:
        * Protocols: REST and WebSocket
        * Full-featured
    - HTTP API: REST only, simple interface
- API endpoint types:
    - Regional: services are spun un in a specific region, let's say ap-southeast-1. If you're calling it from Berlin, it's a bit longer of a call.
    - Edge-optimized: could help in cases where your clients are geographically distributed
    - Private
- Understanding RPS and burst
    - Requests per second (RPS):
    - Burst: The number of concurrent starts API Gateway supports (hard maximum of 5K)
- Integration types:
    - Lambda function - proxy: Requests come at API Gateway are wrapped with metadata and passed to backend
- Authorization:
    - Open: No authentication or authorization
    - IAM permissions: Use IAM policies and AWS creds to grant access
    - JWT authorizers: Use JSON Web Tokens. Part of OIDC and OAuth 2.0 frameworks
    - Lambda authorizers
- Caching
- Default throttling: All APIs share a throttling limit of 10K requests per second and 5K burst per account per Region
- Configure custom domains: SSL cert, DNS records (CNAME, A, ...)
- Logging
    - Add cloudwatch permissions
    - Add api gw service as trusted entity
- Swagger/OpenAPI import and export
- CI/CD
- HTTP proxy integration
- CORS policy: https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
- Http headers: https://docs.aws.amazon.com/apigateway/latest/developerguide/request-response-data-mappings.html
- Export REST API


### DEBUG:
#### AWS
- Forgot to comment out the running of the handler function at the end of my Lambda function that I use to run locally for testing during development. This caused two instances of the function to run causing this error: https://github.com/alixaxel/chrome-aws-lambda/issues/69
- Reserved environment variables in AWS Lambda: https://cloudash.dev/blog/aws-lambda-default-environment-variables
- AWS Lambda has restrictions on writing to the file system. By default, the file system in AWS Lambda is read-only except for a specific directory,
/tmp, which acts as ephemeral storage. Common issues:
    * https://repost.aws/questions/QUyYQzTTPnRY6_2w71qscojA/read-only-file-system-aws-lambda
- Misc:
    * https://stackoverflow.com/questions/65366479/http-api-returns-undefined-value-outside-aws-lambda-test-environment
    * How to config DNS on Cloudflare to connect a domain to API Gateway: https://medium.com/@amirhosseinsoltani7/connect-cloudflare-to-aws-api-gateway-c64f0713b5e9

#### Vercel & Nextjs
- Vercel throws 504 error (timeout) when making requests to AWS API Gateway. Solutions:
    * may adjust timeout of vercel serverless function
    * may adjust function region (~ 45s)

- In Nextjs, there're a few challenges to set metadata for Open Graph if we'd like to use Dynamic Routing. Common issues:
    * metadata for open graph: https://github.com/vercel/next.js/discussions/57251
