# alert_sender.py — 경보 목록을 n8n Webhook 으로 전송
import os
import sys
from datetime import datetime

import requests  # pip install requests

# ── 설정 (본인 값으로 바꿀 것) ─────────────────────────
STUDENT = "clover"          # 채점 증적 — 반드시 본인 것으로 변경
# 본인 n8n Webhook 의 Production URL. 환경변수 N8N_WEBHOOK_URL 로 설정하거나,
# 아래 기본값을 로컬에서만 직접 채워 쓰고 커밋하지 않는다.
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/여기에-본인-webhook-경로")
TIMEOUT = 10   # 초

# 레벨 10 이상 = 거부(deny) 대상, 10 미만 = 허용(allow) 대상
alerts = [
    {"ip": "10.0.0.5",   "level": 12, "rule": "brute_force_login"},   # 거부 대상
    {"ip": "192.168.0.7", "level": 8,  "rule": "port_scan"},          # 허용 대상
    {"ip": "203.0.113.9", "level": 15, "rule": "sql_injection_attempt"},  # 거부 대상
]


def send_alerts(url, student, rows):
    """alerts 를 n8n Webhook 으로 POST. 성공 시 True, 실패해도 프로그램은 죽지 않는다."""
    payload = {
        "student": student,
        "generated_at": datetime.now().isoformat(),
        "alerts": rows,
    }
    try:
        res = requests.post(url, json=payload, timeout=TIMEOUT)
        print(f"[n8n] POST {url} -> {res.status_code}")
        res.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[n8n] 전송 실패: {e}", file=sys.stderr)
        return False


def main():
    ok = send_alerts(N8N_WEBHOOK_URL, STUDENT, alerts)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
