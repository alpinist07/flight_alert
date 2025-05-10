from flask import Flask, request, render_template
import json, os
from search import search_flights  # 기존 search.py에서 가져옴

app = Flask(__name__)
DATA_FILE = "conditions.json"

def load_conditions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_conditions(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            origin = request.form.get('origin')
            dests = request.form.get('dests', '').split(',')
            dates = request.form.get('dates', '').split(',')
            price = int(request.form.get('price', '0'))
            email = request.form.get('email')

            # 조건 저장
            new = {
                "origin": origin,
                "dests": dests,
                "dates": dates,
                "price": price,
                "email": email
            }
            data = load_conditions()
            data.append(new)
            save_conditions(data)

            # 항공권 가격 실시간 조회
            results = []
            for dest in dests:
                for date in dates:
                    dest = dest.strip()
                    date = date.strip()
                    if dest and date:
                        matches = search_flights(origin, dest, date, price)
                        results.extend(matches)

            return render_template('result.html', results=results)

        except Exception as e:
            return f"오류 발생: {e}", 500

    return render_template('form.html')
