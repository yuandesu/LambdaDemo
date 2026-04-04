# Lambda Demo

Three AWS Lambda (Python) functions showing different approaches to integrating OpenAI with Datadog monitoring, with a focus on PII (Personally Identifiable Information) handling.

## Functions

| File | Description |
|---|---|
| `HelloWorldDemo.py` | Minimal Lambda function — a clean template to start from |
| `MockPIIAPI.py` | Returns mock user data (with PII) and sends metrics to Datadog via UDP; no SDK required |
| `MockPIIAPI_Tracer.py` | Full Datadog SDK integration using `@tracer.wrap()` and `@datadog_lambda_wrapper` |

## Prerequisites

- AWS account with CLI configured (`aws configure`)
- [Datadog](https://app.datadoghq.com) account and API key
- OpenAI API key

## Deploy to AWS Lambda

### 1. Package and upload

```bash
zip function.zip MockPIIAPI_Tracer.py
aws lambda update-function-code \
  --function-name <your-function-name> \
  --zip-file fileb://function.zip
```

### 2. Attach the Datadog Lambda Layers

In the Lambda console, add these layers for your region:

```
arn:aws:lambda:<region>:464622532012:layer:Datadog-Python311:<version>
arn:aws:lambda:<region>:464622532012:layer:Datadog-Extension:<version>
```

Find the latest layer versions at [docs.datadoghq.com/serverless](https://docs.datadoghq.com/serverless/libraries_integrations/extension/).

### 3. Set environment variables in the Lambda console

| Variable | Value |
|---|---|
| `DD_API_KEY` | Your Datadog API key |
| `DD_SITE` | `datadoghq.com` |
| `DD_SERVICE` | `lambda-demo` |
| `DD_ENV` | `production` |
| `OPENAI_API_KEY` | Your OpenAI API key |

### 4. Invoke and verify

```bash
# Generate 1 mock user record
aws lambda invoke --function-name <your-function-name> out.json && cat out.json

# Generate 10 records
aws lambda invoke \
  --function-name <your-function-name> \
  --payload '{"queryStringParameters": {"count": "10"}}' \
  --cli-binary-format raw-in-base64-out \
  out.json && cat out.json
```

Open [Datadog APM → Traces](https://app.datadoghq.com/apm/traces) to see the traces.

## Local Testing

```bash
pip install datadog ddtrace openai datadog-lambda
python HelloWorldDemo.py
```

## AWS SAM (optional)

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  LambdaDemoFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: MockPIIAPI_Tracer.lambda_handler
      Runtime: python3.11
      Timeout: 30
      MemorySize: 256
```
