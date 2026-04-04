[English](#english) | [日本語](#日本語) | [繁體中文](#繁體中文)

---

## English

# Lambda Demo

Three AWS Lambda (Python) functions showing different approaches to integrating OpenAI with Datadog monitoring, with a focus on PII (Personally Identifiable Information) handling.

### Functions

| File | Description |
|---|---|
| `HelloWorldDemo.py` | Minimal Lambda function — a clean template to start from |
| `MockPIIAPI.py` | Returns mock user data (with PII) and sends metrics to Datadog via UDP; no SDK required |
| `MockPIIAPI_Tracer.py` | Full Datadog SDK integration using `@tracer.wrap()` and `@datadog_lambda_wrapper` |

### Prerequisites

- AWS account with CLI configured (`aws configure`)
- [Datadog](https://app.datadoghq.com) account and API key
- OpenAI API key

### Deploy to AWS Lambda

**1. Package and upload**

```bash
zip function.zip MockPIIAPI_Tracer.py
aws lambda update-function-code \
  --function-name <your-function-name> \
  --zip-file fileb://function.zip
```

**2. Attach the Datadog Lambda Layers**

In the Lambda console, add these layers for your region:

```
arn:aws:lambda:<region>:464622532012:layer:Datadog-Python311:<version>
arn:aws:lambda:<region>:464622532012:layer:Datadog-Extension:<version>
```

Find the latest layer versions at [docs.datadoghq.com/serverless](https://docs.datadoghq.com/serverless/libraries_integrations/extension/).

**3. Set environment variables in the Lambda console**

| Variable | Value |
|---|---|
| `DD_API_KEY` | Your Datadog API key |
| `DD_SITE` | `datadoghq.com` |
| `DD_SERVICE` | `lambda-demo` |
| `DD_ENV` | `production` |
| `OPENAI_API_KEY` | Your OpenAI API key |

**4. Invoke and verify**

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

### Local Testing

```bash
pip install datadog ddtrace openai datadog-lambda
python HelloWorldDemo.py
```

### AWS SAM (optional)

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

---

## 日本語

# Lambda デモ

OpenAI と Datadog モニタリングを統合するさまざまなアプローチを示す、3 つの AWS Lambda（Python）関数です。PII（個人を特定できる情報）の取り扱いに焦点を当てています。

### 関数一覧

| ファイル | 説明 |
|---|---|
| `HelloWorldDemo.py` | 最小構成の Lambda 関数 — スタートテンプレートとして活用できる |
| `MockPIIAPI.py` | PII を含むモックユーザーデータを返し、UDP 経由で Datadog にメトリクスを送信（SDK 不要） |
| `MockPIIAPI_Tracer.py` | `@tracer.wrap()` と `@datadog_lambda_wrapper` を使った Datadog SDK のフル統合 |

### 前提条件

- AWS アカウントと CLI 設定済み（`aws configure`）
- [Datadog](https://app.datadoghq.com) アカウントと API キー
- OpenAI API キー

### AWS Lambda へのデプロイ

**1. パッケージ化とアップロード**

```bash
zip function.zip MockPIIAPI_Tracer.py
aws lambda update-function-code \
  --function-name <your-function-name> \
  --zip-file fileb://function.zip
```

**2. Datadog Lambda Layer を追加**

Lambda コンソールで、お使いのリージョン向けに以下のレイヤーを追加してください:

```
arn:aws:lambda:<region>:464622532012:layer:Datadog-Python311:<version>
arn:aws:lambda:<region>:464622532012:layer:Datadog-Extension:<version>
```

最新のレイヤーバージョンは [docs.datadoghq.com/serverless](https://docs.datadoghq.com/serverless/libraries_integrations/extension/) で確認できます。

**3. Lambda コンソールで環境変数を設定**

| 変数 | 値 |
|---|---|
| `DD_API_KEY` | Datadog API キー |
| `DD_SITE` | `datadoghq.com` |
| `DD_SERVICE` | `lambda-demo` |
| `DD_ENV` | `production` |
| `OPENAI_API_KEY` | OpenAI API キー |

**4. 実行して確認**

```bash
# モックユーザーデータを 1 件生成
aws lambda invoke --function-name <your-function-name> out.json && cat out.json

# 10 件生成
aws lambda invoke \
  --function-name <your-function-name> \
  --payload '{"queryStringParameters": {"count": "10"}}' \
  --cli-binary-format raw-in-base64-out \
  out.json && cat out.json
```

[Datadog APM → Traces](https://app.datadoghq.com/apm/traces) でトレースを確認してください。

### ローカルテスト

```bash
pip install datadog ddtrace openai datadog-lambda
python HelloWorldDemo.py
```

### AWS SAM（任意）

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

---

## 繁體中文

# Lambda 示範

三個 AWS Lambda（Python）函式，展示整合 OpenAI 與 Datadog 監控的不同方式，並聚焦於 PII（個人可識別資訊）的處理。

### 函式說明

| 檔案 | 說明 |
|---|---|
| `HelloWorldDemo.py` | 最小化的 Lambda 函式 — 乾淨的起始範本 |
| `MockPIIAPI.py` | 回傳含 PII 的模擬使用者資料，並透過 UDP 傳送指標至 Datadog（無需 SDK） |
| `MockPIIAPI_Tracer.py` | 使用 `@tracer.wrap()` 與 `@datadog_lambda_wrapper` 的完整 Datadog SDK 整合 |

### 前置需求

- AWS 帳號並完成 CLI 設定（`aws configure`）
- [Datadog](https://app.datadoghq.com) 帳號與 API 金鑰
- OpenAI API 金鑰

### 部署至 AWS Lambda

**1. 打包並上傳**

```bash
zip function.zip MockPIIAPI_Tracer.py
aws lambda update-function-code \
  --function-name <your-function-name> \
  --zip-file fileb://function.zip
```

**2. 附加 Datadog Lambda Layer**

在 Lambda 主控台中，為您所在的 Region 新增以下 Layer：

```
arn:aws:lambda:<region>:464622532012:layer:Datadog-Python311:<version>
arn:aws:lambda:<region>:464622532012:layer:Datadog-Extension:<version>
```

最新 Layer 版本請參考 [docs.datadoghq.com/serverless](https://docs.datadoghq.com/serverless/libraries_integrations/extension/)。

**3. 在 Lambda 主控台設定環境變數**

| 變數 | 值 |
|---|---|
| `DD_API_KEY` | 您的 Datadog API 金鑰 |
| `DD_SITE` | `datadoghq.com` |
| `DD_SERVICE` | `lambda-demo` |
| `DD_ENV` | `production` |
| `OPENAI_API_KEY` | 您的 OpenAI API 金鑰 |

**4. 執行並確認**

```bash
# 產生 1 筆模擬使用者資料
aws lambda invoke --function-name <your-function-name> out.json && cat out.json

# 產生 10 筆
aws lambda invoke \
  --function-name <your-function-name> \
  --payload '{"queryStringParameters": {"count": "10"}}' \
  --cli-binary-format raw-in-base64-out \
  out.json && cat out.json
```

開啟 [Datadog APM → Traces](https://app.datadoghq.com/apm/traces) 確認 traces 是否出現。

### 本機測試

```bash
pip install datadog ddtrace openai datadog-lambda
python HelloWorldDemo.py
```

### AWS SAM（選用）

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
