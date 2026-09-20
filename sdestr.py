import time
import requests

MESSAGE = "Your preset message here"

WEBHOOKS = [
    "https://discord.com/api/webhooks/1551164982593462282/srpFQ2AvOGBRFi_YwkbM38K42s8DdveLwHqg4Lj5sHwZawAtt6sqpYc6zP85SJ-8S7MB?thread_id=1478772480867958825",
    "https://discord.com/api/webhooks/1551164982593462282/srpFQ2AvOGBRFi_YwkbM38K42s8DdveLwHqg4Lj5sHwZawAtt6sqpYc6zP85SJ-8S7MB?thread_id=1476213013630418975",
]

INTERVAL = 60  # seconds


def send_message(webhook):
    try:
        response = requests.post(
            webhook,
            json={"content": MESSAGE},
            timeout=10
        )

        if response.status_code in (200, 204):
            print("Sent successfully")
        else:
            print(f"Failed: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Connection error: {e}")


while True:
    for webhook in WEBHOOKS:
        send_message(webhook)

    print(f"Waiting {INTERVAL} seconds...")
    time.sleep(INTERVAL)