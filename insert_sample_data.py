#insert_sample.py
import sqlite3
from gpa_calculation import calculate_gpa_and_credits #gpa_calculationのインポート
from utils import get_grade  # get_grade を適切にインポート
from database_setup import remove_duplicates


def insert_sample_data():
    # データベース接続
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()



    # 科目情報の挿入
    subjects = [
        (1, 'データベース', 2),
        (2, '電子商取引論', 2),
        (3, '線形代数学', 1),
        (4, '人工知能', 2),
        (5, '英語', 1)
    ]
    
    # 重複を防ぐために INSERT OR IGNORE を使う
    cursor.executemany('''INSERT OR IGNORE INTO subjects (subject_id, subject_name, credits) VALUES (?, ?, ?)''', subjects)



    # 生徒情報の挿入 (評価、取得単位、不足単位は計算で決定されるのでNoneを設定)
    ## GPA、total_credits、remaining_creditsは計算後に設定されるため、データ挿入時に None にしておく
    students = [
        ('g2342001', '田中太郎', 'password123', None, None, None, None),  # GPA、取得単位、不足単位は計算
        ('g2242014', '佐藤花子', 'password456', None, None, None, None),  # GPA、取得単位、不足単位は計算
        ('g2342078', '鈴木一郎', 'password789', None, None, None, None),  # GPA、取得単位、不足単位は計算
        ('g2341008', '青山輝樹', 'password321', None, None, None, None)
    ]
    
    cursor.executemany('''INSERT OR IGNORE INTO users (student_id, name, password, gpa, rank, total_credits, remaining_credits) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', students)

    # 履修情報の挿入
    enrollments = [
        ('g2342001', 1, 80, None),  # 田中太郎: データベース
        ('g2342001', 2, 75, None),  # 田中太郎: 電子商取引論
        ('g2342001', 3, 60, None),  # 田中太郎: 線形代数学
        ('g2242014', 1, 70, None),  # 佐藤花子: データベース
        ('g2242014', 2, 85, None),  # 佐藤花子: 電子商取引論
        ('g2242014', 4, 55, None), # 佐藤花子: 人工知能
        ('g2342078', 1, None, None),  # 鈴木一郎: データベース
        ('g2342078', 3, 80, None),  # 鈴木一郎: 線形代数学
        ('g2342078', 5, 90, None),   # 鈴木一郎: 英語
        ('g2341008', 2, 95, None),
        ('g2341008', 4, 85, None),
        ('g2341008', 5, 90, None)
    ]
    
    # 成績を計算して `grade` カラムにセット
    enrollments_with_grades = [(student_id, subject_id, score, get_grade(score)) for student_id, subject_id, score, _ in enrollments]
    
    cursor.executemany('''INSERT OR IGNORE INTO enrollments (student_id, subject_id, score, grade) 
                           VALUES (?, ?, ?, ?)''', enrollments_with_grades)

    # 変更を保存
    connection.commit()

    # 各学生のGPAや取得単位数、順位を計算して更新
    for student in students:
        student_id = student[0]
        calculate_gpa_and_credits(student_id)  # GPAと単位数の計算

     # 重複データを削除
    remove_duplicates(connection)

    connection.close()
    
if __name__ == "__main__":
    insert_sample_data()
    print("Sample data inserted successfully.")