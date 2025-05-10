import json
from search import search_flights
from notifier import send_email, send_telegram

def load_conditions():
    with open("conditions.json") as f:
        return json.load(f)

def check_all():
    conditions = load_conditions()
    for cond in conditions:
        for dest in cond['dests']:
            for date in cond['dates']:
                matches = search_flights(cond['origin'], dest, date, cond['price'])
                if matches:
                    msg = "\n".join(matches)
                    send_email(cond['email'], "항공권 발견!", msg)
                    send_telegram(f"[항공권 알림]\n{msg}")
