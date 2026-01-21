import json
import random
import socket
import time

# Datadog Extensionのアドレス
DD_HOST = "127.0.0.1"
DD_PORT = 8125

# --- 1. ダミーデータベースを準備 (Mock Database) ---
# Fakerパッケージをインストールできないため、シンプルな辞書を自作
FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "David", "Elizabeth"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "company.com", "aws.com"]
ROLES = ["Admin", "User", "Viewer", "Editor"]
STATUSES = ["Active", "Inactive", "Banned", "Pending"]

def send_metric(name, value, tags):
    """ Datadog ExtensionにUDPパケットを手動送信 """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tag_str = ",".join(tags)
        # フォーマット: metric_name:value|c|#tags (cはCounter)
        payload = f"{name}:{value}|c|#{tag_str}"
        sock.sendto(payload.encode('utf-8'), (DD_HOST, DD_PORT))
        sock.close()
        print(f"? Metric Sent: {payload}")
    except Exception as e:
        print(f"Metric Error: {e}")

def generate_one_user():
    """ ダミーユーザーを生成するロジック """
    f_name = random.choice(FIRST_NAMES)
    l_name = random.choice(LAST_NAMES)
    
    # Emailを組み立てる: james.smith@gmail.com
    email = f"{f_name.lower()}.{l_name.lower()}@{random.choice(DOMAINS)}"
    
    # 年齢を18~65でランダム生成
    age = random.randint(18, 65)
    
    return {
        "id": random.randint(1000, 9999),
        "name": f"{f_name} {l_name}",
        "email": email,
        "age": age,
        "role": random.choice(ROLES),
        "status": random.choice(STATUSES),
        "created_at": int(time.time())
    }

def lambda_handler(event, context):
    # --- 2. URLパラメータを解析 ---
    # デフォルトは1件生成、?count=5で数量を指定可能
    count = 1
    
    # パラメータがあるか確認（Function URLのevent構造）
    query_params = event.get("queryStringParameters")
    if query_params and "count" in query_params:
        try:
            count = int(query_params["count"])
            # 安全制限、一度に生成しすぎないように
            if count > 100: count = 100
        except:
            pass # 変換に失敗したら1を維持

    print(f"リクエストを受信、{count}件のダミーデータを生成中...")
    # Logを辞書にしてからdump、Datadogが自動でフィールドを解析
    print(json.dumps({
        "level": "INFO",
        "message": f"リクエストを受信、{count}件のダミーデータを生成中",
        "request_id": context.aws_request_id, # 追跡しやすいように
        "count": count
    }))

    # --- 3. 生成開始 ---
    users = []
    for _ in range(count):
        user = generate_one_user()
        users.append(user)

    # --- 4. Datadog監視メトリクスを送信 ---
    # 生成した人数を記録（Counter）
    send_metric("mock_api.users.generated", count, ["env:lambda-demo"])
    
    # このリクエストで生成したデータ量を記録（Histogram/Distribution）- ここでは簡単にGaugeで模擬
    # これはパフォーマンス指標と仮定
    send_metric("mock_api.batch_size", count, ["env:lambda-demo"])

    # --- 5. HTTPレスポンスを返す（API標準形式に準拠）---
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "meta": {
                "count": count,
                "source": "AWS Lambda Mock Generator"
            },
            "data": users
        })
    }