from multiprocessing import Process, Manager
import threading
import time
import data, data2, data4, data5 # 
from flask import Flask, render_template
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
merged = {}  # 전역 변수: 갱신된 데이터를 계속 여기에 저장

def load_data():
    """multiprocessing으로 데이터 수집"""
    with Manager() as manager:
        shared_list = manager.list()

        jobs = [
            Process(target=data.finalarr, args=(shared_list,)),
            Process(target=data2.finalarr, args=(shared_list,)),
            Process(target=data4.finalarr, args=(shared_list,)),
            Process(target=data5.finalarr, args=(shared_list,))
        ]

        for job in jobs:
            job.start()
        for job in jobs:
            job.join()

        cleaned = []
        for item in shared_list:
            if isinstance(item, list):
                cleaned.extend(item)
            else:
                cleaned.append(item)

        merged_data = {}
        for d in cleaned:
            merged_data.update(d)
        time = datetime.now()
        time = time.strftime("%Y%m%d%H%M%S")
        merged_data['time'] = time

        return merged_data
    
DB_PATH = "./OpenSourceBasicProj_Ass/teamproj/weather_data.db"

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT,
                    temp TEXT,
                    maxtemp TEXT,
                    mintemp TEXT,
                    humidity TEXT,
                    rain TEXT,
                    rainchance TEXT,
                    pm10Value TEXT,
                    pm25Value TEXT
                )
            """)
            conn.commit()

def save_to_db(data):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather (time, temp, maxtemp, mintemp, humidity, rain, rainchance, pm10Value, pm25Value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("time"),
            data.get("temp"),
            data.get("maxtemp"),
            data.get("mintemp"),
            data.get("humidity"),
            data.get("rain"),
            data.get("rainchance"),
            data.get("pm10Value"),
            data.get("pm25Value")
        ))
        conn.commit()

def background_updater():
    global merged
    while True:
        print("🔄 주기적으로 데이터 갱신 중...")
        try:
            merged = load_data()
            print("데이터 갱신 완료:", merged)
            save_to_db(merged)
        except Exception as e:
            print("데이터 갱신 실패:", e)
        time.sleep(1800)  # 300초 = 5분마다 갱신

@app.route("/")
def home():
    if merged:
        return render_template("finalindex.html", weather=merged)
    else:
        return "데이터를 불러올 수 없습니다."

if __name__ == "__main__":
    init_db()
    # 백그라운드에서 주기적인 데이터 갱신 시작
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()

    # Flask 앱 실행
    app.run(debug=True)
