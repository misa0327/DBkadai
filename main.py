from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from insert_sample_data import insert_sample_data  # insert_sample_data.pyから関数をインポート

app = Flask(__name__)

# アプリケーション起動時にサンプルデータを挿入
insert_sample_data()  # main.pyが起動した際にサンプルデータを挿入

# 学生情報を取得する関数
def get_student_info(student_id, password=None):
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()
    
    if password:
        cursor.execute(''' 
        SELECT name, gpa, rank, total_credits, remaining_credits 
        FROM users
        WHERE student_id = ? AND password = ? 
        ''', (student_id, password))
    else:
        cursor.execute(''' 
        SELECT name, gpa, rank, total_credits, remaining_credits 
        FROM users
        WHERE student_id = ? 
        ''', (student_id,))
    
    student_info = cursor.fetchone()
    
    if student_info:
        cursor.execute(''' 
        SELECT subjects.subject_name, enrollments.grade
        FROM enrollments
        JOIN subjects ON enrollments.subject_id = subjects.subject_id
        WHERE enrollments.student_id = ? 
        ''', (student_id,))
        grades = cursor.fetchall()
        connection.close()
        return student_info + (grades,)
    
    connection.close()
    return None

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form["student_id"]
        password = request.form["password"]
        
        student_info = get_student_info(student_id, password)
        if student_info:
            return redirect(url_for("dashboard", student_id=student_id))
        else:
            return "ログインに失敗しました。学生IDまたはパスワードが間違っています。"
    
    return render_template("login.html")

@app.route("/dashboard/<student_id>")
def dashboard(student_id):
    student_info = get_student_info(student_id, password=None)  # パスワードなし
    if student_info:
        return render_template("dashboard.html", 
                               student_name=student_info[0], 
                               gpa=student_info[1], 
                               rank=student_info[2],
                               earned_credits=student_info[3], 
                               remaining_credits=student_info[4],
                               grades=student_info[5])
    else:
        return "データが見つかりませんでした"

if __name__ == "__main__":
    app.run(debug=True)
