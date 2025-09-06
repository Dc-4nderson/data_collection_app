from flask import Flask, render_template_string, request, redirect
import sqlite3
import random

app = Flask(__name__)

DB_PATH = 'data.db'

FIELDS = [
    'saving_amount', 'monthly_income', 'monthly_bills', 'monthly_entertainment',
    'sales_skills', 'age', 'dependents', 'assets', 'risk_level',
    'confidence', 'business_difficulty'
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(f"{field} INTEGER" for field in FIELDS)},
            readiness_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def generate_scenario():
    return {
        'saving_amount': random.randint(0, 50000),
        'monthly_income': random.randint(1000, 20000),
        'monthly_bills': random.randint(500, 10000),
        'monthly_entertainment': random.randint(0, 3000),
        'sales_skills': random.randint(1, 10),
        'age': random.randint(18, 70),
        'dependents': random.randint(0, 5),
        'assets': random.randint(0, 100000),
        'risk_level': random.randint(1, 10),
        'confidence': random.randint(1, 10),
        'business_difficulty': random.randint(1, 10)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        scenario = {field: int(request.form[field]) for field in FIELDS}
        readiness_score = int(request.form['readiness_score'])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f'''
            INSERT INTO scenarios ({', '.join(FIELDS)}, readiness_score)
            VALUES ({', '.join('?' for _ in FIELDS)}, ?)
        ''', [scenario[field] for field in FIELDS] + [readiness_score])
        conn.commit()
        conn.close()
        return redirect('/thanks')
    else:
        scenario = generate_scenario()
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Financial Readiness Scenario</title>
                <style>
                    body {
                        background: #f4f6f8;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        max-width: 500px;
                        margin: 40px auto;
                        background: #fff;
                        border-radius: 12px;
                        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                        padding: 32px 28px;
                    }
                    h1 {
                        text-align: center;
                        color: #2d3e50;
                        margin-bottom: 18px;
                    }
                    .scenario-list {
                        margin-bottom: 24px;
                    }
                    .scenario-item {
                        display: flex;
                        justify-content: space-between;
                        padding: 8px 0;
                        border-bottom: 1px solid #eee;
                    }
                    .scenario-item:last-child {
                        border-bottom: none;
                    }
                    label {
                        font-weight: 500;
                        color: #34495e;
                    }
                    .readiness-input {
                        width: 60px;
                        padding: 6px;
                        border-radius: 4px;
                        border: 1px solid #ccc;
                        margin-left: 10px;
                    }
                    .submit-btn {
                        display: block;
                        width: 100%;
                        background: #2d89ef;
                        color: #fff;
                        border: none;
                        border-radius: 6px;
                        padding: 12px;
                        font-size: 1.1em;
                        font-weight: bold;
                        cursor: pointer;
                        margin-top: 18px;
                        transition: background 0.2s;
                    }
                    .submit-btn:hover {
                        background: #1b5fa7;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Financial Readiness Scenario</h1>
                    <form method="post">
                        <div class="scenario-list">
                            {% for field, value in scenario.items() %}
                                <div class="scenario-item">
                                    <label>{{ field.replace('_', ' ').title() }}</label>
                                    <input type="hidden" name="{{ field }}" value="{{ value }}">
                                    <span>{{ value }}</span>
                                </div>
                            {% endfor %}
                        </div>
                        <div style="text-align:center; margin-bottom:16px;">
                            <label for="readiness_score">How ready is this person financially? (1-10):</label>
                            <input class="readiness-input" type="number" name="readiness_score" min="1" max="10" required>
                        </div>
                        <button class="submit-btn" type="submit">Submit Rating</button>
                    </form>
                </div>
            </body>
            </html>
        ''', scenario=scenario)

@app.route('/thanks')
def thanks():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Thank You!</title>
            <style>
                body {
                    background: #f4f6f8;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 420px;
                    margin: 80px auto;
                    background: #fff;
                    border-radius: 14px;
                    box-shadow: 0 2px 16px rgba(44, 62, 80, 0.12);
                    padding: 36px 30px;
                    text-align: center;
                }
                .thank-icon {
                    font-size: 54px;
                    color: #2d89ef;
                    margin-bottom: 18px;
                }
                h2 {
                    color: #2d3e50;
                    margin-bottom: 12px;
                }
                p {
                    color: #34495e;
                    font-size: 1.1em;
                    margin-bottom: 0;
                }
                .home-link {
                    display: inline-block;
                    margin-top: 22px;
                    padding: 10px 22px;
                    background: #2d89ef;
                    color: #fff;
                    border-radius: 6px;
                    text-decoration: none;
                    font-weight: 500;
                    transition: background 0.2s;
                }
                .home-link:hover {
                    background: #1b5fa7;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="thank-icon">🎉</div>
                <h2>Thank You!</h2>
                <p>Your response has been recorded.<br>
                We appreciate your feedback on financial readiness.</p>
                <a class="home-link" href="/">Rate Another Scenario</a>
            </div>
        </body>
        </html>
    ''')

@app.route('/view')
def view_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT * FROM scenarios")
    rows = c.fetchall()
    conn.close()
    columns = ['ID'] + [field.replace('_', ' ').title() for field in FIELDS] + ['Financial Readiness']
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Stored Scenarios</title>
            <style>
                body {
                    background: #f4f6f8;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 900px;
                    margin: 40px auto;
                    background: #fff;
                    border-radius: 12px;
                    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                    padding: 32px 28px;
                }
                h1 {
                    text-align: center;
                    color: #2d3e50;
                    margin-bottom: 18px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #eee;
                    padding: 8px 6px;
                    text-align: center;
                }
                th {
                    background: #2d89ef;
                    color: #fff;
                }
                tr:nth-child(even) {
                    background: #f4f6f8;
                }
                .home-link {
                    display: inline-block;
                    margin-top: 22px;
                    padding: 10px 22px;
                    background: #2d89ef;
                    color: #fff;
                    border-radius: 6px;
                    text-decoration: none;
                    font-weight: 500;
                    transition: background 0.2s;
                }
                .home-link:hover {
                    background: #1b5fa7;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Stored Financial Scenarios</h1>
                <table>
                    <tr>
                        {% for col in columns %}
                            <th>{{ col }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in rows %}
                        <tr>
                            {% for item in row %}
                                <td>{{ item }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </table>
                <a class="home-link" href="/">Back to Scenario</a>
            </div>
        </body>
        </html>
    ''', rows=rows, columns=columns)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)