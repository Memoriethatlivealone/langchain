import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

print("base_url:", base_url)

url = base_url.rstrip("/") + "/models"
headers = {"Authorization": f"Bearer {api_key}"}

resp = requests.get(url, headers=headers, timeout=30)
print("status:", resp.status_code)
data = resp.json()
models = data.get("data", [])
print("model count:", len(models))
print("-" * 50)
all_ids = []
for m in models:
    mid = m.get("id", "")
    all_ids.append(mid)

# 优先打印包含 5.6 / sol / gpt 的
hits = [x for x in all_ids if ("5.6" in x) or ("sol" in x.lower())]
print(">>> 可能的目标模型:")
for h in hits:
    print("   ", h)
print("-" * 50)
print(">>> 全部模型:")
for x in all_ids:
    print(x)
