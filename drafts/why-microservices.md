## - What is serverless about ?

* there are never instances, operating systems, or servers to manage. AWS handles everything required to run and scale your application. By building serverless applications, your developers can focus on the code that makes your business unique.
* An application that can automatically scale, inherently highly available and run without provisioning or managing an EC2 host is known as a Serverless Application.

Benefits:

- scalability
- deployment speed (no server management)
- automated high availability
- benefit of shifting operational engineering focus to tasks that better differentiate the business.
- reduced cost of idle capacity.
    * utilization of servers
    * operational costs: all of the stuff that's involved in managing and provisioning and securing servers
- Faster time to market:
    * When you move from a world where you have to provision servers up front, to a serverless world, it becomes trivial to deploy a highly scalable application in a very short amount of time.
    * So you can get a prototype of a simple web service that's capable of scaling up and handling thousands or more requests per second in a day or two in a lot of cases.

## Event-based architecture
In event-driven architectures, events are the primary mechanism for sharing information across services. These events are observable, such as a new message in a log file, rather than directed, such as a command to specifically do something. Events initiate actions and communication between decoupled services

An event can be a change in state, a user request, or an update, like an item being placed in a shopping cart in an e-commerce website. When an event occurs, the information is published for other services to consume it.
#### Producers, routers, consumers

## AWS Serverless stack

## Lambda: compute service
#### Benefits:
- You can run code without provisioning or maintaining servers.
- It initiates functions for you in response to events.
- It scales automatically.
- It provides built-in code monitoring and logging via Amazon CloudWatch

#### Synchronous invocation:
- Lambda runs the function and waits for a response. When the function completes, Lambda returns the response from the function's code
- there are no built-in retries. You must manage your retry strategy within your application code.
- The following AWS services invoke Lambda synchronously:
* Amazon API Gateway
* Amazon Cognito
* AWS CloudFormation
* Amazon Alexa
* Amazon Lex
* Amazon CloudFront

#### Asynchronous invocation
- When you invoke a function asynchronously, events are queued and the requestor doesn't wait for the function to complete. This model is appropriate when the client doesn't need an immediate response.
- With the asynchronous model, you can make use of destinations. Use destinations to send records of asynchronous invocations to other services. (Select the Destinations tab for more information.)

- A destination can send records of asynchronous invocations to other services. You can configure separate destinations for events that fail processing and for events that process successfully. You can configure destinations on a function, a version, or an alias, similarly to how you can configure error handling settings. With destinations, you can address errors and successes without needing to write more code.

- The following AWS services invoke Lambda asynchronously:
* Amazon SNS
* Amazon S3
* Amazon EventBridge

#### Polling invocation

#### Lambda execution environment
- Init phase split into three sub-phases:
    * Extension init - starts all extensions: downloads the code for the function, dependencies and all layers.
    * Runtime init - bootstraps the runtime
    * Function init - runs the function's static code (the code outside the main handler)
- Invoke phase: In this phase, Lambda invokes the function handler. After the function runs to completion, Lambda prepares to handle another function invocation.
- Shutdown phase: runtime shutdown then extension shutdown

#### Performance optimization
**Cold and warm starts**
Cold start: a new execution environment is required to run a Lambda function.

Warm start: the Lambda service retains the environment instead of destroying it immediately. This allows the function to run again within the same execution environment. This saves time by not needing to initialize the environment.

![AWS Lambda execution environment lifecycle](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/aws-lambda-exec-env-lifecycle.png)

**Best practice: Write functions to take advantage of warm starts**
- Store and reference dependencies locally.
- Limit re-initialization of variables.
- Add code to check for and reuse existing connections.
- Use tmp space as transient cache.
- Check that background processes have completed.

#### AWS Lambda Function Permissions
There are two sides that define the necessary scope of permissions – permission to invoke the function, and permission of the Lambda function itself to act upon other services.

**IAM resource-based policy**: define permissions to invoke the function
**The execution role**: gives your function permissions to interact with other services.

To learn more:
- Viewing resource-based IAM policies in Lambda: https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html
- Viewing and updating permissions in the execution role: https://docs.aws.amazon.com/lambda/latest/dg/permissions-executionrole-update.html

Tips:
    - Remember to use the principle of least privilege when creating IAM policies and roles. Always start with the most restrictive set of permissions and only grant further permissions as required for the function to run.
    - You can also use IAM Access Analyzer to help identify the required permissions for the IAM execution role.

Quiz: What IAM entities must be included in an execution role for a Lambda function to interact with other services, such as DynamoDB? (Select TWO.)

Answer:
    - IAM policy that defines the actions that can be taken within DynamoDB
    - Trust policy that grants "AssumeRole" permission to Lambda to act on DynamoDB

#### Configuring Your Lambda Functions
When building and testing a function, you must specify three primary configuration settings: memory, timeout, and concurrency

#### Monitoring and Troubleshooting
- Main tool: Amazon CloudWatch: helps you monitor your code when it runs, Lambda automatically tracks the following:
    * Number of requests
    * Invocation duration per request
    * Number of requests that result in an error

- Additional tool: AWS X-Ray, to identify the call flow of Lambda functions and API calls. We can use this tool for:
    * fine-tune performance
    * Trace path and timing of an invocation to locate bottlenecks and failures

- Other monitoring and troubleshooting tools:
    * AWS CloudTrail helps audit your application by recording all the API actions made against the application. These logs can be exported to the analysis tool of your choice for additional analysis
    * Dead-letter queue: help us to capture and analyze application errors that must receive a response for follow-up or code corrections.
        - For e.g an ecommerce application that processes orders. If an order fails, you cannot ignore that order error. You move that error into the dead-letter queue and manually look at the queue and fix the problems.
        - Dead-letter queues are available for asynchronous and non-stream polling events.
        - A dead-letter queue can be an Amazon Simple Notification Service (Amazon SNS) topic or an Amazon Simple Queue Service (Amazon SQS) queue.

Read more:
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html


## Security and Observability for Serverless Applications
### Shared responsibility model
One benefit of serverless architectures is that when you rely on AWS managed services, you shift more parts of the AWS shared responsibility model toward AWS. You have the same security issues, but AWS manages more of them on your behalf.

### Three security best practices
- Follow the principle of least privilege.
- Protect data at rest and in transit.
- Audit your system for changes, unexpected access, unusual patterns, or errors.


### Limiting access to APIs
You have three options for authorizing access to your APIs through API Gateway: AWS Identity and Access Management (IAM), Amazon Cognito, and Lambda authorizers
- IAM: is best for clients that are within your AWS environment or can otherwise retrieve IAM temporary credentials to access your environment.
- Amazon Cognito: gives you a managed service that can support sign-in/sign-up capabilities or act as an identity provider (IdP) in a federated identity scenario.
- Lambda authorizers: When a client makes a request your API's method, API Gateway calls your Lambda authorizer. The Lambda authorizer takes the caller's identity as the input and returns an IAM policy as the output.
    * Best for securing APIs using custom business logic: Use a Lambda authorizer to implement a custom authorization scheme. Your scheme can use request parameters to determine the caller's identity or use a bearer token authentication strategy such as OAuth or SAML.
    * Implementation details: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html

![Lambda Authorizer Authorization Workflow](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/lambda-authorizer-authorization-workflow.png)

### Protect your data in transit and at rest

#### Encrypt data in transit
- Encrypt the client-side payload
- Encrypt data before processing
- Do not send, log or store unencrypted sensitive data

#### Protect data at rest
- Encryption uses AWS KMS

### Serverless data protection best practices
- Make yourself aware of how you can take advantage of AWS managed services to reduce your security management burden.
- Think about security end to end at each integration point in your distributed architecture.
- Use narrowly scoped IAM permissions and roles to protect access to your Lambda functions and other AWS services.
- Create smaller Lambda functions that perform scoped activities, and don’t share IAM roles between functions.
- To pass data in a Lambda function, use environment variables, AWS Systems Manager Parameter Store, or AWS Secrets Manager.

**Passing data to AWS Lambda**
- Env variables: scoped to a single function
- Parameter Store or Secrets Manager: values can be stored across multiple applications
- Secret Manager: allows for secret rotation and cross-account access.

### The three pillars of observability
- Monitor: Metrics collected through monitoring provide data about **the performance of your systems**. You can think of a metric as a single variable that is used to monitor an aspect of your system. When you combine all these individual metrics, you are able to see how your application is performing over time.
- Trace: How to identify where an error or a bottleneck might be occurring ? To do this, you can use a trace. A trace will follow requests as they travel through the individual services and resources that make up your application, providing an end-to-end view of how it is performing. You can use this trace to follow the path of an individual request as it passes through each service or tier in your application so that you can pinpoint where issues are occurring.
- Log: time-stamped records of events that include failures, errors, state transformations, or even who accessed your system at a certain time.

### Monitoring serverless applications

**CloudWatch metrics**: helps you to monitor your service health and to alarm on error cases.
- Business metrics: measure your application performance against business goals. Examples: Orders placed, debit and credit card operations, flights purchased.
- Customer experience metrics:
    * Examples:
        - Perceived latency
        - Time it takes to add an item to a basket or checkout
        - Page load times
- System metrics: Percentage of HTTP errors/success, Memory utilization, Function duration/error/throttling, Queue length, etc.
- Operational metrics:CI/CD pipeline statistics, such as successful or failed deployments, feedback time, cycle and lead time.

**CloudWatch Logs**: create business-level metrics with CloudWatch Logs metric filters.

**CloudWatch Logs Insights**: you can use prebuilt or custom queries on your logs to provide aggregated views and reporting

### Tracing serverless applications
One of the challenges of microservice-based, distributed architectures is how you can get insight into all of your different integration points. When a transaction fails, or completes slower than expected, you need to have a way to determine where, in the flow of services, it failed.

Additional resources:
- Visualize Lambda function invocations using AWS X-Ray: https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html

### Auditing serverless applications
**CloudTrail** and **AWS Config**

#### CloudTrail
CloudTrail to answer question like: "Who modified the resource?"
    * Provides full details about the API action, such as the identity of the requestor, time of the API call, request parameters, and response elements returned by the service
    * Records actions by IAM user or role or other AWS services
    * Records events initiated via console, CLI, SDK or API.
    * **Is enabled when you create an account**

Important concepts:
- CloudTrail events:
    * When activity occurs in your AWS account, that activity is recorded in a CloudTrail event, and you can see recent events in the event history.
    * viewable, searchable, and downloadable record of the past 90 days
- CloudTrail Trails:
    * a configuration that enables the delivery of CloudTrail events to an Amazon Simple Storage Service (Amazon S3) bucket, Amazon CloudWatch Logs, and Amazon CloudWatch Events in case you need to maintain a longer history of events.
    * When you create a trail, it tracks events performed on or within resources in your AWS account and writes them to an S3 bucket that you specify.

#### AWS Config
AWS Config to answer question like: "Does this modification comply with our rules?"

- View a snapshot of how resources are configured
- Create rules that enforce compliant state -> flag out rule violation and notify you via SNS
- Can use AWS Config to standardize development:
    * Runtime environment
    * Handler name
    * Memory allocation
    * Timeout settings

Both CloudTrail and AWS Config help you to monitor and manage changes so that you can give your developers the room to innovate, but prevent undesirable changes from sneaking into your applications.

### Scaling Serverless Architectures
Scaling considerations:

To successfully scale your serverless architecture, you need to know the capabilities and service limits of the services that you’re integrating. Also, select patterns that optimize your application for the scale you need to support. Key considerations include the following:

- Timeouts
- Retry behaviors
- Throughput
- Payload size

#### Scaling considerations for Lambda
- Concurrency limits: to help avoid unexpected consequences if you have a "function gone wild" scenario. For example, a runaway function could incur very high costs, and impact the performance of downstream resources
- Burst behavior: When you get a burst of requests, Lambda will immediately increase concurrency up to the "Immediate Concurrency Increase" level for the AWS Region where your Lambda function is running. Then, it will add 500 more invocations each minute, until it either has enough to process the burst, or hits the function or account concurrency limit.
- Memory configuration: Functions that are assigned more memory may actually be cheaper to run because they’ll run faster. When you configure functions, there is only one setting that can impact performance—memory. However, both CPU and I/O scale linearly with memory configuration. For example, a function with 256 MB of memory has twice the CPU and I/O as a 128 MB function.

## Designing Event-Driven Architectures
### Serverless Event Submission Patterns
#### Amazon SQS integration with Lambda
By introducing the SQS queue in front of Lambda, you create an asynchronous connection between the API request and Lambda. This allows you to satisfy the API request without regard for how long the Lambda function (or other backend services) will run.
![SQS in front of Lambda](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/sqs-in-front-of-lambda.png)

#### Workflow orchestration with AWS Step Functions
- Keep orchestration out of lambda
- Automatically trigger and track each step
- Log each step

## Deploying Serverless Applications
### Understanding Serverless Deployments
**AWS SAM**: an open source framework you can use to build your serverless applications. It provides you with a shorthand syntax to express your functions, APIs, databases, and event source mappings.
    - SAM templates: an extension of the AWS CloudFormation templates, with some additional components that make them easier for you to work with.
    - SAM CLI: Helps you test your code and emulate the Lambda environment locally
    - SAM package: Creates a deployment package for your template
    - SAM deploy: Deploys your template into an AWS CloudFormation stack

**Sharing Configuration Data**:
As a best practice, never hardcode secrets or configurations into your deployment package, as you may accidentally expose that information. Always separate your configurations and secrets from your code, to prevent accidental check-ins to public source control.
When working with Lambda, you can use:
- **environment variables** to store configuration settings separate from your code.:
    * Pros:
        - simple to set up
        - no dependencies on other services
    * Cons:
        - However, environment variables are specific to a particular Lambda function, so it can be difficult to share configurations across your Lambda functions and projects.
        - When the configurations in your environment variables change, you will need to update them for every Lambda function that uses them. That can be difficult to track down in a large-scale environment.
- **AWS Systems Manager Parameter Store**: a free, fully managed, centralized storage system for configuration data and secret management. This data can be stored in plaintext or also encrypted with KMS.
    * Pros:
        - a free, fully managed, centralized storage system for configuration data and secret management
        - Each Lambda function only having access to the configuration data that it needs
        - Parameter Store tracks all parameter changes through versioning, so if you need to roll back your deployment, you can also choose to use an earlier version of your configuration data to use.
        - Parameter Store provides hierarchical key/value storage. You could create a hierarchy for each of your environments (dev, stage, and prod), and then have the API keys that you need for each environment.
    * Cons:
        - may incur additional cold-start latency when executed, as the function needs to retrieve and decrypt the secret from parameter storage. (you can store it in a global variable. Once you pull the configuration data from parameter storage, your function code can check to see if you need to pull or update the parameter. This will not improve the latency when you first call your Lambda function, but it may reduce the latency for subsequent calls)

### Deployment strategies
Deployment strategies define how you want to deliver your software. Organizations follow different deployment strategies based on their business model. Some choose to deliver software that is fully tested, and others might want their users to provide feedback and let their users evaluate under development features (such as Beta releases). The following section discusses various deployment strategies.

**All-at-once deployment**: means all traffic is shifted from the original environment to the replacement environment all at once.

**Canary deployment**: you deploy your new version of your application code and shift a small percentage of production traffic to point to that new version. After you have validated that this version is safe and not causing errors, you direct all traffic to the new version of your code. Read more: [Implement Lambda canary deployments using a weighted alias
](https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html)

**Linear deployment**: similar to canary deployment. In this strategy, you direct a small amount of traffic to your new version of code at first. After a specified period of time, you automatically increment the amount of traffic that you send to the new version until you’re sending 100 percent of production traffic.

![Deployment preferences with SAM](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/deployment-preference-with-sam.png)

### Creating a deployment pipeline
When you check a piece of code into source control, you don’t want to wait for a human to manually approve it or have each piece of code run through different quality checks. A CI/CD pipeline can help automate the steps required to release your software deployment and standardize on a core set of quality checks. Here is an example of a deployment pipeline:

![Example deployment pipeline](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/example-deployment-pipeline.png)

A CI/CD pipeline is mainly made up of four steps: Source, Build, Test, Production. CI/CD can be pictured as a pipeline, where new code is submitted on one end, tested over a series of stages (source, build, test, staging, and production), and then published as production-ready code.

AWS offers a tool for each phase of the pipeline. These tools include:
- AWS CodeCommit for Source
- AWS CodeBuild for Build and Test
- AWS CodeDeploy for Production
- AWS CodePipeline for fully managed continuous delivery

#### Implement Lambda canary deployments using a weighted alias
You can use a **weighted alias to split traffic between two different versions of the same function**. With this approach, you can test new versions of your functions with a small percentage of traffic and quickly roll back if necessary. This is known as a canary deployment. Canary deployments differ from blue/green deployments by exposing the new version to only a portion of requests rather than switching all traffic at once.

You can point an alias to a maximum of two Lambda function versions. The versions must meet the following criteria:
- Both versions must have the same execution role.
- Both versions must have the same dead-letter queue configuration, or no dead-letter queue configuration.
- Both versions must be published. The alias cannot point to $LATEST.

Details: https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html

#### Automate deployment with weighted aliases while rolling capabilities are enabled
Use **AWS CodeDeploy** and **AWS Serverless Application Model (AWS SAM)** to create a rolling deployment that automatically detects changes to your function code, deploys a new version of your function, and gradually increase the amount of traffic flowing to the new version. The amount of traffic and rate of increase are parameters that you can configure.

Details: https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html#lambda-rolling-deployments

## Amazon API Gateway for Serverless Applications
After this section, you should be able to:
- Identify initial use cases where API Gateway and Lambda can decouple a larger monolith.
- Identify a plan for your application for managing APIs that includes endpoint selection, caching configurations, - authorization methods, usage plans, and deployment stages.
- Identify how to build real-time messaging communication applications using WebSocket APIs.
- Use the API Gateway console to create an API from scratch, test it with a mock endpoint, and deploy it using an available authorization option.
- Use Amazon CloudWatch to analyze the traffic on your deployed API and identify opportunities or improvements, validations, responses, and mapping.
- Use API Gateway as an event source for a Lambda function using Lambda Aliases and API Gateway Stage Variables.

### Introduction to API Gateway
API Gateway is a service that facilitates the creation, publishing, maintenance, monitoring, and security of your APIs at any scale. API Gateway handles all your tasks around accepting and processing hundreds of thousands of concurrent API calls. This includes handling traffic management, Cross Origin Resource Sharing (CORS) support, authorization and access control, throttling, monitoring, and API version management.

### API Gateway features
- Developer features in API Gateway
    * Run multiple versions of API at the same time:
    * Quick SDK generation: If you’re using REST APIs, API Gateway can generate client Software Development Kits (SDKs) for several platforms, which you can use to quickly test new APIs from your applications and distribute SDKs to third-party developer. You can use AWS Command Line Interface (AWS CLI) to generate and download an SDK of an API for a supported platform by calling the **get-sdk** command.
    * Transform and validate request-response data
- Features for managing API access
    * Reduce latency and throttle traffic:
API Gateway provides end users with the lowest possible latency for API requests and responses by taking advantage of the Amazon CloudFront global network of edge locations. With this service, you also can throttle traffic and authorize API calls to ensure that backend operations withstand traffic spikes and backend systems are not unn
    * Built-in flexible authorization options: AWS Identity and Access Management (IAM) and Amazon Cognito. If you use OAuth tokens, API Gateway also offers native OpenID Connect (OIDC) and OAuth 2 support.

### API Gateway architecture
This architecture provides an example overview of the concepts and features you can use with API Gateway. These will be discussed in further depth as you proceed through the lessons. Select each hotspot to learn more about this architecture.

![API Gateway architecture](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/api-gw-architecture.png)

### Selecting the best API type for your use case
- REST API:
    * All-inclusive set of features needed to build, manage, and publish APIs at a single price point
    * Building APIs that use certificates for backend authentication, AWS WAF, or resource policies
    * Workloads that need an edge-optimized or private API type
- HTTP API:
    * Building modern APIs that are equipped with native OIDC and OAuth 2 authorization
    * Building proxy APIs for Lambda or any HTTP endpoint
    * APIs for latency-sensitive workloads
    * do not currently offer API management functionality.
- Websocket API:
    * Bidirectional communication that lets clients and services independently send messages to each other
    * Richer client-to-service interactions because services can push data to clients without requiring clients to make an explicit request.
    * APIs that require real-time messaging

### Real-time message communication with WebSocket APIs
#### Benefits and use cases of WebSocket APIs
PI Gateway WebSocket APIs are designed for bidirectional communication between your client and backend architecture. You can do this by using any WebSockets client such as a mobile app, chat app, AWS IOT device, or application dashboard.

When you connect the client to API Gateway, API Gateway will manage the persistence and state needed to connect it to your clients. Unlike a REST API, which receives and responds to requests, a WebSocket API supports two-way communication between your client applications and your backend.

WebSocket APIs are often used in real-time application use cases such as:
• Chat applications
• Streaming dashboards
• Real-time alerts and notifications
• Collaboration platforms
• Multiplayer games
• Financial trading platforms

Pricing considerations for WebSocket APIs

There are three different aspects to consider:
- Flat charge: charge for the messages you send and receive. For WebSocket APIs, the API Gateway free tier currently includes one million messages (sent or received) and 750,000 connection minutes for up to 12 months.
- Connection minutes: In addition to paying for the messages you send and receive, you are also charged for the total number of connection minutes.
- Additional charges: You may also incur additional charges if you use API Gateway in conjunction with other AWS services or transfer data out of AWS.

### Designing REST APIs
API Gateway REST APIs use a request-response model, where a client sends a request to a service and the service responds back synchronously. This kind of model is suitable for many different kinds of applications that depend on synchronous communication.

#### API Gateway REST API endpoint types
- Regional endpoint: is designed to reduce latency when calls are made from the same AWS Region as the API. In this model, API Gateway does not deploy its own CloudFront distribution in front of your API. Instead, traffic destined for your API will be directed straight at the API endpoint in the Region where you’ve deployed it.
    * gives you lower latency for applications that are invoking your API from within the same Region (for example, an API that is going to be accessed from EC2 instances within the same Region)
    * provides you with the flexibility to deploy your own CloudFront distribution or content delivery network (CDN) in front of API Gateway and control that distribution using your own settings for customized scenarios. An example of this might be to design for disaster recovery scenarios or implement load balancing in a very customized way.
- edge-optimized endpoint: is designed to help you reduce client latency from anywhere on the internet
    * a fully managed CloudFront distribution is automatically configured to provide lower latency access to your API.
    * This endpoint-type setup reduces your first hit latency for your API. An additional benefit of using a managed CloudFront distribution is that you don’t have to pay for or manage a CDN separately from API Gateway.
- Private endpoint: is designed for applications that have very secure workloads, such as healthcare or financial data that cannot be exposed publicly on the internet.
    * This endpoint type is still managed by API Gateway, but requests are only routable and can only originate from within a single virtual private cloud (VPC) that you control.
    * There are no data transfer-out charges for private APIs. However, AWS PrivateLink charges apply when using private APIs in API Gateway.

Although it is important to consider your current and future needs when creating your REST API endpoint in API Gateway, it is possible to change the endpoint type. Changing your API endpoint type requires you to update the API's configuration. You can change an existing API type using the API Gateway console, the AWS CLI, or an AWS SDK for API Gateway. The following endpoint type changes are supported:
1. From edge-optimized to regional or private
2. From regional to edge-optimized or private
3. From private to regional

#### API Gateway optional cache
- Why:
    * It **reduces overall latency** for serving requests.
    * It minimizes the number of requests that need to be made to your backend.
- Configure caching per API stage: Configuration choices for stage caching include the following.
    * Provision between 0.5 GB and 237 GB of cache
    * Set TTL in seconds
    * Turn on encryption of cache data
    * Only GET methods will be cached
    * Configure per method: You can override stage-level settings for individual methods. Turn caching on or off for specific methods, increase or decrease the TTL, or turn encryption on or off for cached responses.
- Managing API cache:
    * Caching is charged at an hourly rate, dependent on the cache size you select, regardless of the number of API calls being cached.

#### Pricing considerations for REST APIs
- Flat charge: you only pay when your APIs are in use at a set cost per million requests.
- Data transfer out: You may incur additional charges if you use API Gateway in conjunction with other AWS services or transfer data out of AWS. Private API endpoints don’t have data transfer-out charges. Instead, PrivateLink charges apply.
- Optional cache

### Building and Deploying APIs with API Gateway
#### API Gateway integration types
- Lambda function: When you are using API Gateway as the gateway to a Lambda function, you’ll use the Lambda integration. This will result in requests being proxied to Lambda with request details available to your function handler in the event parameter, supporting a streamlined integration setup. The setup can evolve with the backend without requiring you to tear down the existing setup.
- HTTP endpoint: useful for public web applications where you want clients to interact with the endpoint. This type of integration lets an API expose HTTP endpoints in the backend.
- AWS Service: an integration type that lets an API expose AWS service actions. For example, you might drop a message directly into an Amazon Simple Queue Service (Amazon SQS) queue.
- Mock
- VPC Link: connect to a VPC Link that allows access to resources within VPCs via a Network Load Balancer (NLB).

#### Test your API methods
Test results:
    - Request: Request is the resource's path that was called for the method.
    - Status: Status is the response's HTTP status code.
    - Latency: Latency is the time between the receipt of the request from the caller and the returned response.
    - Response Body: Response Body is the HTTP response body.
    - Response Headers: Response Headers are the HTTP response header.

Response logs
Test results include simulated CloudWatch logs. No data is actually written to CloudWatch when testing.

The output shows the state changes from the method request to the integration request, and from the integration response to the method response.

This can be useful for troubleshooting any mapping errors that cause the request to fail. In this example, no mapping transformations were applied.

#### API stages
When you are ready to make your API callable for your users, you need to deploy your API to a stage.

A stage is a snapshot of the API and represents a unique identifier for a version of a deployed API.

With stages, you can have multiple versions and roll back versions. Anytime you update anything about the API, you need to redeploy it to an existing stage or to a new stage that you create as part of the deploy action.

**Building and deploying best practices**
Use API Gateway stages with Lambda aliases

To highlight something that was mentioned in the previous example, Lambda and API Gateway are both designed to support flexible use of versions. You can do this by using aliases in Lambda and stages in API Gateway. When you couple that with stage variables, you don't have to hard-code components, which leads to having a smooth and safe deployment.
- In Lambda, enable versioning and use aliases to reference.
- In API Gateway, use stages for environments.
- Point API Gateway stage variables at the Lambda aliases.

### Managing API Access
#### Authorization for API Gateway
- Authorizing with IAM:
    * If you have an internal service or a restricted number of customers, IAM is a great choice for authorization, especially for applications that use IAM to interact with other AWS services using IAM roles
    * No additional cost
- Lambda Authorizers
    * You also need to consider what you already have in place that should be used. If you are using an OAuth strategy as an organization, you may want to consider Lambda Authorizer
    * Lambda Authorizer is simply a Lambda function that you can write to perform any custom authorization that you need. There are two types of Lambda Authorizers you should be aware of: Token and Request.
    * ![Lambda Authorizer](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/lambda-authorizer.jpg)
- Cognito Authorizers: As an alternative to using IAM or Lambda authorizers, you can use Amazon Cognito and a Cognito User Pool to control access to your APIs.

#### Permissions
Three main types of permissions:
- Execute permission
- Manage permission
- Resource policy

To learn more:
- How API Gateway resource policies affect authorization workflow: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-authorization-flow.html

#### Throttling and usage plans
Beyond just allowing or denying access to your APIs, API Gateway also helps you manage the volume of API calls that are processed through your API endpoint.

With API Gateway, you can set throttle and quota limits on your API consumers. This can useful for things such as preventing one consumer from using all of your backend system’s capacity or to ensure that your downstream systems can manage the number of requests you send through.

**Usage plans**:
You can set up usage plans for:
- API Key Throttling per second and burst
- API Key Quota by day, week, or month
- API Key Usage by daily usage records
![API Gateway usage plan](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/api-gw-usage-plan.jpg)

**Token bucket algorithm**
The method by which the limits are measured and throttled is based on the token bucket algorithm, which is a widely used algorithm for checking that network traffic conforms to set limits. A token, in this case, counts as a request and the burst is the maximum bucket size.

Requests that come into the bucket are fulfilled at a steady rate. If the rate at which the bucket is being filled causes the bucket to fill up and exceed the burst value, a 429 Too Many Requests error would be returned.

API Gateway sets a limit on a steady-state rate and a burst of request submissions per account and per Region. At the account level, by default, API Gateway limits the steady-state request rate to 10,000 requests per second. It limits the burst to 5,000 requests across all APIs within an AWS account. However, as discussed earlier, you can use usage plans to manage limits at a more granular level.

**Throttling settings hierarchy**
The type and level of throttling applied to a request is dependent on all of the limits involved and are applied in this order:
1. Per-client, per-method throttling limits that you set for an API stage in a usage plan
2. Per-client throttling limits that you set in a usage plan
3. Default per-method limits and individual per-method limits that you set in API stage settings
The account level limit

### CloudWatch Metrics for API Gateway
- Count: Total number of API requests in a period
- Latency: Time between when API Gateway receives a request from a client and when it returns a response to the client; this includes the integration latency and other API Gateway overhead
- IntegrationLatency: Time between when API Gateway relays a request to the backend and when it receives a response from the backend
- 4xxError: Client-side errors captured in a specified period
- 5xxError: Server-side errors captured in a specified period
- CacheHitCount: Number of requests served from the API cache in a given period
- CacheMissCount: Number of requests served from the backend in a given period, when API caching is turned on

With these metrics, you can monitor details such as the following:

• How often your APIs are being called
• The number of invocations to your API
• The latency of the API responses
• If there are any errors, and if so, whether they are 400 errors or 500 errors
• Whether your cache is being hit or how many times the backend needed to be called while caching was enabled

Calculating API Gateway overhead: Two key metrics that are used to calculate the API Gateway overhead of deployed APIs are the Latency and IntegrationLatency CloudWatch Metrics.
- The latency metric gives you details about how long it takes for a full round-trip response, from the second your customer invokes your API to when your API responds with the results. This is a full round-trip duration of an API request through API Gateway.
- Integration latency is how long it takes for API Gateway to make the invocation to your backend and receive the response.

The difference between these two metrics gives you your API Gateway overhead. Together, these metrics can help you fine-tune your applications and see where the bottlenecks are.

### CloudWatch Logs for API Gateway
- Execution Logging:
    * logs what’s happening on the roundtrip of a request
    * You can see all the details from when the request was made, the other request parameters, everything that happened between the requests, and what happened when API Gateway returned the results to the client that’s calling the service.
    * can be useful to troubleshoot APIs, but can result in logging sensitive data. Because of this, it is recommended you don't enable Log full requests/responses data for production APIs. In addition, there is a cost component associated with logging your APIs.
- Access logging:
    * provides details about who's invoking your API.
    * includes everything including IP address, the method used, the user protocol, and the agent that's invoking your API.
    * Access logging is fully customizable using JSON formatting. If you need to, you can publish them to a third-party resource to help you analyze them.

### Monitoring with X-Ray and CloudTrail
- AWS X-Ray
    * to trace and analyze user requests as they travel through your Amazon API Gateway APIs to the underlying services
    * to identify and troubleshoot the root cause of performance issues and errors
    * gives you an end-to-end view of an entire request, so you can analyze latencies and errors in your APIs and their backend services
- AWS CloudTrail
    * captures all API calls for API Gateway as events.
        - IP address, requester, and time of request are included.
        - Event history can be reviewed.
        - Create a trail to send events to an Amazon Simple Storage Service (Amazon S3) bucket.

### Data Mapping and Request Validation
In API Gateway, an API's method request can take a payload in a different format from the corresponding integration request payload as required by your backend and the reverse.

Mapping templates can be added to the integration request to transform the incoming request to the format required by the backend of the application or to transform the backend payload to the format required by the method response.

Key variables for transformations


| Variable | Use Case|
|----------|-------------|
| \$input	 | Body, json, params, path |
| \$stageVariables | Any stage variable name |
| \$util | escapeJavaScript(), parseJson(), urlEncode/Decode(), base64Encode/Decode() |

### Offloading request validation to API Gateway
In conjunction with data transformation and customized Gateway Responses, you can also let API Gateway handle some of your basic validations, rather than making the call or building that validation into the backend.

Details: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html