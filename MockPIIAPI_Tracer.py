import json
import random
import time

# --- Datadog Layerからの強力なサポート ---
from ddtrace import tracer
from datadog_lambda.metric import lambda_metric
# 1. この重要なWrapperをインポート（親Spanが見つからない問題を解決）
from datadog_lambda.wrapper import datadog_lambda_wrapper

# ダミーデータベース
FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "company.com"]

# ---------------------------------------------------------
# ? 特徴 1: 自動トレーシング (Tracing)
# @tracer.wrap() デコレータを使用すると、Datadogがこの関数の実行時間を自動計測
# ---------------------------------------------------------
@tracer.wrap(name="function.generate_user", service="mock-data-generator", resource="gen_one")
def generate_one_user():
    # 計算遅延をシミュレート（フレームグラフを見やすくするため）
    time.sleep(random.uniform(0.01, 0.05))
    
    f_name = random.choice(FIRST_NAMES)
    l_name = random.choice(LAST_NAMES)
    
    return {
        "id": random.randint(1000, 9999),
        "name": f"{f_name} {l_name}",
        "email": f"{f_name.lower()}.{l_name.lower()}@{random.choice(DOMAINS)}",
        "created_at": int(time.time())
    }

# ---------------------------------------------------------
# 2. このデコレータを追加して、DatadogにLambdaのライフサイクル全体を管理させる
# これでtracer.current_span()が最外層の親Spanを取得できるようになる
# ---------------------------------------------------------
@datadog_lambda_wrapper
def lambda_handler(event, context):
    # 現在のTraceにRequest IDを手動でタグ付け、デバッグしやすくする
    # Wrapperを追加したので、ここでSpanを確実に取得できる
    current_span = tracer.current_span()
    if current_span:
        current_span.set_tag("request.id", context.aws_request_id)

    # 1. パラメータを解析（デフォルトは1件生成）
    count = 1
    query_params = event.get("queryStringParameters")
    if query_params and "count" in query_params:
        try:
            count = int(query_params["count"])
            if count > 50: count = 50 # 安全上限
        except:
            pass
            
    if current_span:
        current_span.set_tag("generation.count", count)

    print(f"リクエストを受信、{count}件のダミーデータを生成中...")
    
    # 2. 生成ロジックを実行
    users = []
    for _ in range(count):
        user = generate_one_user()
        users.append(user)

    # ---------------------------------------------------------
    # ? 特徴 2: 公式SDKでメトリクスを送信 (Metrics)
    # 自分でsocketを書く必要なし！この一行で接続、フォーマット、タイムスタンプを自動処理
    # ---------------------------------------------------------
    lambda_metric(
        metric_name='mock_api.users.generated', # メトリクス名
        value=count,                            # 数値
        tags=['env:production', 'version:v2_sdk'] # タグ
    )

    # 3. 結果を返す
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "meta": {
                "count": count,
                "method": "Datadog SDK (Auto)"
            },
            "data": users
        })
    }