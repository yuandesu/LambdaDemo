# AWS Lambda デモプロジェクト

AWS Lambda関数のデモプロジェクトです。Datadog監視統合の実装例を含みます。

## ? ファイル構成

| ファイル | 説明 |
|---------|------|
| `HelloWorldDemo.py` | 基本的なLambda関数のサンプル |
| `MockPIIAPI.py` | UDPでDatadogメトリクスを手動送信するモックAPI |
| `MockPIIAPI_Tracer.py` | Datadog SDK自動トレーシング付きの拡張版 |

## ? 機能詳細

### HelloWorldDemo.py

最もシンプルなLambda関数の例です。

```python
# レスポンス例
{
    "statusCode": 200,
    "body": {
        "message": "Hello World!",
        "request_id": "<aws_request_id>"
    }
}
```

### MockPIIAPI.py

ダミーユーザーデータを生成するモックAPIです。

**特徴:**
- ランダムなユーザー情報（名前、メール、年齢、役割、ステータス）を生成
- UDP経由でDatadog Extensionにメトリクスを手動送信
- URLパラメータ `?count=N` で生成件数を指定可能（最大100件）

**送信メトリクス:**
- `mock_api.users.generated` - 生成したユーザー数
- `mock_api.batch_size` - バッチサイズ

### MockPIIAPI_Tracer.py

Datadog公式SDKを使用した高度な監視機能付きバージョンです。

**特徴:**
- `@tracer.wrap()` デコレータによる自動トレーシング
- `@datadog_lambda_wrapper` によるLambdaライフサイクル管理
- `lambda_metric()` による公式SDKメトリクス送信
- カスタムSpanタグ（`request.id`, `generation.count`）

## ? Datadog統合

### 必要なDatadog Lambda Layer

```
arn:aws:lambda:<region>:464622532012:layer:Datadog-Python<version>:<layer_version>
arn:aws:lambda:<region>:464622532012:layer:Datadog-Extension:<layer_version>
```

### 環境変数

| 変数名 | 説明 |
|--------|------|
| `DD_API_KEY` | Datadog APIキー |
| `DD_SITE` | Datadogサイト（例: `datadoghq.com`） |
| `DD_SERVICE` | サービス名 |
| `DD_ENV` | 環境名（production, staging等） |
| `DD_TRACE_ENABLED` | トレース有効化（`true`/`false`） |

## ?? デプロイ方法

### AWS CLIを使用する場合

```bash
# ZIPファイルを作成
zip function.zip MockPIIAPI_Tracer.py

# Lambda関数を更新
aws lambda update-function-code \
    --function-name <function-name> \
    --zip-file fileb://function.zip
```

### AWS SAMを使用する場合

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MockPIIAPIFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: MockPIIAPI_Tracer.lambda_handler
      Runtime: python3.11
      Timeout: 30
      MemorySize: 256
```

## ? 使用例

### Function URLでの呼び出し

```bash
# 1件のダミーデータを生成
curl https://<function-url>/

# 10件のダミーデータを生成
curl "https://<function-url>/?count=10"
```

### レスポンス例

```json
{
    "meta": {
        "count": 1,
        "method": "Datadog SDK (Auto)"
    },
    "data": [
        {
            "id": 1234,
            "name": "James Smith",
            "email": "james.smith@gmail.com",
            "created_at": 1705849200
        }
    ]
}
```

## ? ライセンス

MIT License
