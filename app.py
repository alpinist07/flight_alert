from flask import Flask, request, render_template
import json, os
from scheduler import check_all

app = Flask(__name__)
DATA_FILE = "conditions.json"

def load_conditions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_conditions(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new = {
            "origin": request.form['origin'],
            "dests": request.form['dests'].split(','),
            "dates": request.form['dates'].split(','),
            "price": int(request.form['price']),
            "email": request.form['email']
        }
        data = load_conditions()
        data.append(new)
        save_conditions(data)
        return "조건 저장 완료!"
    return render_template('form.html')

@app.route('/check')
def trigger():
    check_all()
    return "조건 확인 완료!"

if __name__ == '__main__':
    app.run()
