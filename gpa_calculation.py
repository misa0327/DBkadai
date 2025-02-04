#gpa_calculation.py
import sqlite3
from rank_calculation import calculate_and_update_rank  # 順位計算をインポート

def calculate_gpa_and_credits(student_id):
"""
指定された学生IDのGPA、取得単位数、不足単位数を計算
GPA=履修した各科目のGP*単位数の合計/履修登録した単位数の合計
GP=(科目の得点-50)/10
"""
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    #学生IDに関連する全ての科目情報を取得
    #enrollmentsテーブルから、欠席でない科目の得点と単位数を取得
    cursor.execute('''SELECT s.credits, e.score 
                      FROM enrollments e
                      JOIN subjects s ON e.subject_id = s.subject_id
                      WHERE e.student_id = ? AND e.grade != '欠席' ''', (student_id,))
    enrollments = cursor.fetchall()

    total_weighted_score = 0    #GPA計算用
    total_credits = 0           #履修単位数
    total_earned_credits = 0    #取得単位数

    for credits, score in enrollments:
        gp = (score - 50) / 10 if score >= 60 else 0  # GPAの計算
        total_weighted_score += gp * credits
        total_credits += credits
        if score >= 60:
            total_earned_credits += credits  # 取得単位数を加算
    
     # GPA計算
    gpa = (total_weighted_score / total_credits) if total_credits > 0 else 0


    # 不足単位の計算
    required_credits = 124  # 卒業に必要な単位数
    remaining_credits = required_credits - total_earned_credits


    # GPA・取得単位数・不足単位数をデータベースに更新
    cursor.execute('''UPDATE users SET gpa = ?, total_credits = ?, remaining_credits = ? WHERE student_id = ?''', 
                   (gpa, total_earned_credits, remaining_credits, student_id))
    

    # データベースに変更を反映
    connection.commit()
    connection.close()

    # 順位を更新
    calculate_and_update_rank()

    return gpa, total_earned_credits, remaining_credits

