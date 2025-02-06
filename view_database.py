import sqlite3

# データベースに接続
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# subjects テーブルのデータを表示
cursor.execute("SELECT * FROM subjects")
subjects_rows = cursor.fetchall()
print("Subjects Table:")
print("科目ID | 科目名 | 単位数")
for row in subjects_rows:
    print(row)

# students テーブルのデータを表示
cursor.execute("SELECT * FROM users")
users_rows = cursor.fetchall()
print("\nStudents Table:")
print("学籍番号 | 氏名 | パスワード | GPA | 学年順位 | 取得単位数 | 不足単位数")
for row in users_rows:
    print(row)

# students テーブルのデータを表示
cursor.execute("SELECT * FROM enrollments")
enrollments_rows = cursor.fetchall()
print("\nEnrollments Table:")
print("履修ID | 学籍番号 | 科目番号 | 得点 | 評価")
for row in enrollments_rows:
    print(row)

# 接続を閉じる
conn.close()
