from multiprocessing import Process, Manager
import threading
import time
import data, data2, data3, data4, data5, data6 # 
from flask import Flask, render_template
import pymysql
from datetime import datetime

app = Flask(__name__)
merged = {}  # 전역 변수: 갱신된 데이터를 계속 여기에 저장
# MySQL 연결 정보
conn = None

def create_connection():
    global conn
    conn = pymysql.connect(
        host="localhost",
        user="1324554",
        password="1111",
        db="weather_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def load_data():
    """multiprocessing으로 데이터 수집"""
    with Manager() as manager:
        shared_list = manager.list()
        shared_list2 = manager.list()

        jobs = [
            Process(target=data.finalarr, args=(shared_list,)),
            Process(target=data2.finalarr, args=(shared_list,)),
            Process(target=data3.finalarr, args=(shared_list2,)),         
            Process(target=data4.finalarr, args=(shared_list,)),
            Process(target=data5.finalarr, args=(shared_list,)),
            Process(target=data6.finalarr, args=(shared_list2,))
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
        
        organized_data = {}
        for d in shared_list2:
            for key, value in d.items():
                if key not in organized_data:
                    organized_data[key] = []
                organized_data[key].extend(value)

        if int(organized_data['lightning'][0][1]) > 0 and float(merged_data['rain']) > 0.0:
            s = 1
        elif int(organized_data['lightning'][0][1]) > 0 and float(merged_data['rain']) == 0.0:
            s = 2
        elif float(merged_data['rain']) > 0.0 and organized_data['sky'][0][1] in ['2', '3']:
            s = 3
        elif float(merged_data['rain']) > 0.0:
            s = 4
        elif int(merged_data['cloud']) >= 5 and int(merged_data['rainchance']) >= 50:
            s = 5
        elif int(merged_data['cloud']) >= 5:
            s = 6
        elif float(merged_data['wind']) > 8.0:
            s = 7
        else:
            s = 0
        merged_data['icon'] = s

        organized_data['icon'] = []
        for i in range(81):
            if i < 6:
                if int(organized_data['raintype'][i][1]) > 0 and int(organized_data['lightning'][i][1]) > 0:
                    t = 1
                elif int(organized_data['raintype'][i][1]) < 0 and int(organized_data['lightning'][i][1]) > 0:
                    t = 2
                elif organized_data['raintype'][i][1] in ['2', '3']:
                    t = 3
                elif organized_data['raintype'][i][1] in ['1', '4']:
                    t = 4
                elif int(organized_data['sky'][i][1]) == 4:
                    t = 5
                elif int(organized_data['sky'][i][1]) == 3:
                    t = 6
                elif float(organized_data['wind'][i][1]) > 8.0:
                    t = 7
                else:
                    t = 0
            else:
                if organized_data['raintype'][i][1] in ['2', '3']:
                    t = 3
                elif organized_data['raintype'][i][1] in ['1', '4']:
                    t = 4
                elif int(organized_data['sky'][i][1]) == 4:
                    t = 5
                elif int(organized_data['sky'][i][1]) == 3:
                    t = 6
                elif float(organized_data['wind'][i][1]) > 8.0:
                    t = 7
                else:
                    t = 0
                organized_data['icon'].append([organized_data['temp'][i][0], t])
            #print(organized_data['icon'])
        return merged_data, organized_data
    
# 🔹 일반 함수: 백그라운드에서 사용
def save_to_db(data, data2):
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO weather_table 
                    (temp, maxtemp, mintemp, humidity, rain, rainchance, pm10Value, pm25Value, cloud, wind, icon) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                data['temp'],
                data['maxtemp'],
                data['mintemp'],
                data['humidity'],
                data['rain'],
                data['rainchance'],
                data['pm10Value'],
                data['pm25Value'],
                data['cloud'],
                data['wind'],
                data['icon']
            ))
        
        for category, entries in data2.items():  # data는 위에서 말한 dict
            #print(entries)
            for entry in entries:
                #print(entry)
                time_str, value = entry
                # time_str은 '202505081400' 같은 문자열이라고 가정
                time_obj = datetime.strptime(time_str, "%Y%m%d%H%M")

                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO weather_table_f (category, time, value) VALUES (%s, %s, %s)",
                        (category, time_obj, float(value))
                    )

        conn.commit()
        print("✅ 저장 성공")
    except Exception as e:
        print("❌ 저장 실패:", e)

def background_updater():
    global merged
    while True:
        print("🔄 주기적으로 데이터 갱신 중...")
        try:
            merged, organized = load_data()
            print("데이터 갱신 완료:", merged, organized['icon'])
            save_to_db(merged, organized)
        except Exception as e:
            print("데이터 갱신 실패:", e)
            time.sleep(1800)  # 300초 = 5분마다 갱신

@app.route("/")
def load_latest_data_from_db():
    try:
        with conn.cursor() as cursor:
            # weather_table에서 최신 1개
            cursor.execute("SELECT * FROM weather_table ORDER BY id DESC LIMIT 1;")
            weather = cursor.fetchone()

            # weather_table_f에서 가장 최근 created_at 시간 구하기
            cursor.execute("SELECT MAX(created_at) AS latest FROM weather_table_f;")
            result = cursor.fetchone()
            latest_created = result['latest'] if result and 'latest' in result else None
            if not latest_created:
                return "❌ created_at 기준 데이터가 없습니다."
            # 해당 created_at을 가진 모든 데이터 가져오기
            cursor.execute("""
                SELECT * FROM weather_table_f 
                WHERE created_at = %s 
                ORDER BY time, category;
            """, (latest_created,))
            weather_f_list = cursor.fetchall()
            if not weather_f_list:
                return "❌ weather_table_f에 해당 created_at 값의 데이터가 없습니다."

        return render_template("finalindex.html", weather=weather, weather_f_list=weather_f_list)

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
