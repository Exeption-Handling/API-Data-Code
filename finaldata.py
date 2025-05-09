from multiprocessing import Process, Manager
import threading
import time
import data, data2, data4, data5 # 
from flask import Flask, render_template
import pymysql

app = Flask(__name__)
merged = {}  # 전역 변수: 갱신된 데이터를 계속 여기에 저장
# MySQL 연결 정보
conn = None

def create_connection():
    global conn
    conn = pymysql.connect(
        host="localhost",
        user="1324554",
        password="xxxxx",
        db="weather_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

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
        
        return merged_data
    
# 🔹 일반 함수: 백그라운드에서 사용
def save_to_db(data):
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO weather_table 
                     (temp, maxtemp, mintemp, humidity, rain, rainchance, pm10Value, pm25Value) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                data['temp'],
                data['maxtemp'],
                data['mintemp'],
                data['humidity'],
                data['rain'],
                data['rainchance'],
                data['pm10Value'],
                data['pm25Value']
            ))
        conn.commit()
        print("✅ 저장 성공")
    except Exception as e:
        print("❌ 저장 실패:", e)

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
def load_latest_data_from_db():
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM weather_table ORDER BY id DESC LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchone()
        return render_template("finalindex.html", weather=result)
    except Exception as e:
        return f"❌ 불러오기 오류: {e}"
    
@app.route("/all")
def show_all_data():
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM weather_table ORDER BY id DESC;"
            cursor.execute(sql)
            results = cursor.fetchall()
        return render_template("finalindexall.html", data=results)
    except Exception as e:
        return f"❌ 불러오기 오류: {e}"

@app.route("/save")
def save_data():
    try:
        save_to_db(merged)
        return "✅ 저장 성공"
    except Exception as e:
        return f"❌ 오류 발생: {e}"

if __name__ == "__main__":
    create_connection()
    # 백그라운드에서 주기적인 데이터 갱신 시작
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()

    # Flask 앱 실행
    app.run(debug=True, host="0.0.0.0")
