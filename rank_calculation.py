# rank_calculation.py
import sqlite3

def calculate_and_update_rank():
    """
    学生のGPAに基づいて、学年・学科ごとに順位を計算し、更新
    """
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    # すべての学生情報を取得
    cursor.execute('''SELECT student_id, gpa FROM users''')
    students = cursor.fetchall()

    # 学籍番号の先頭5文字ごとにグループ化
    student_groups = {}
    for student_id, gpa in students:
        if len(student_id) < 5:
            continue  # IDが不正な場合はスキップ
        
        group_key = student_id[:5]  # 例: "g2342"（学籍番号の先頭5文字）

        if group_key not in student_groups:
            student_groups[group_key] = []
        
        student_groups[group_key].append((student_id, gpa))

    # 各グループごとに順位を計算し、更新
    for group, group_students in student_groups.items():
        sorted_students = sorted(group_students, key=lambda x: x[1] if x[1] is not None else 0, reverse=True)
        rank = 1
        for student_id, _ in sorted_students:
            cursor.execute('''UPDATE users SET rank = ? WHERE student_id = ?''', (rank, student_id))
            rank += 1


    # 変更を保存
    connection.commit()
    connection.close()
