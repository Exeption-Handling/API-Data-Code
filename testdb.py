import sqlite3

conn = sqlite3.connect("./OpenSourceBasicProj_Ass/teamproj/weather_data.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("테이블 목록:", cur.fetchall())

cur.execute("SELECT * FROM weather")
rows = cur.fetchall()
print("저장된 데이터:")
for row in rows:
    print(row)

conn.close()
