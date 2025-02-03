# rank_calculation.py
import sqlite3

def calculate_and_update_rank():
    """
    全学生のGPAに基づいて順位を計算し、更新
    """
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    # すべての学生のGPAを降順に並べて取得
    cursor.execute('''SELECT student_id, gpa FROM users ORDER BY gpa DESC''')
    students = cursor.fetchall()

    # 順位を計算してusersテーブルを更新
    rank = 1
    for student in students:
        student_id = student[0]
        # 順位を更新
        cursor.execute('''UPDATE users SET rank = ? WHERE student_id = ?''', (rank, student_id))
        rank += 1

    # 変更を保存
    connection.commit()
    connection.close()
