import sqlite3

def get_grade(score):
    """
    得点に基づいて評価を決定
    """
    if score >= 90:
        return "秀"
    elif score >= 80:
        return "優"
    elif score >= 70:
        return "良"
    elif score >= 60:
        return "可"
    elif score >= 50:
        return "不可"
    else:
        return "欠席"  # 得点が50未満の場合は欠席とみなす

def calculate_gpa(student_id):
#指定された学生IDのGPA、取得単位数、不足単位数を計算
#GPA=履修した各科目のGP*単位数の合計/履修登録した単位数の合計
#GP＝（科目の得点-50）/10
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    # 学生IDに関連する全ての科目情報を取得
    #subjectsテーブルから、欠席でない科目の得点と単位数を取得
    cursor.execute('''SELECT credits, score FROM subjects WHERE student_id = ? AND grade != '欠席' ''', (student_id,))
    subjects = cursor.fetchall()

    total_weighted_score = 0 #GPA計算に使用する加重スコア
    total_credits = 0 #学生が履修した層単位数
    total_earned_credits = 0 # 取得単位数


    for subject in subjects:
        credits, score = subject
        grade = get_grade(score)
        
        # 欠席の場合はGPA計算に含めない
        if grade != "欠席":
            gp = (score - 50) / 10 if score >= 60 else 0  # GP計算
            total_weighted_score += gp * credits
            total_credits += credits
            total_earned_credits += credits  # 取得単位数を加算

    # GPA計算
    if total_credits > 0:
        gpa = total_weighted_score / total_credits
    else:
        gpa = 0

    connection.close()
    return gpa
    # GPA計算後に順位を更新する処理
    calculate_and_update_rank()




    # 不足単位数の計算
    required_credits = 124
    remaining_credits = required_credits - total_earned_credits

    # 取得したGPA、取得単位数、残り単位数をusersテーブルに更新
    cursor.execute('''UPDATE users SET gpa = ?, total_credits = ?, remaining_credits = ? WHERE student_id = ?''', 
                   (gpa, total_earned_credits, remaining_credits, student_id))
    connection.commit()

    connection.close()
    return gpa, total_earned_credits, remaining_credits


def calculate_and_update_rank():
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

if __name__ == "__main__":
    student_id = input("Enter student ID: ")
    gpa, earned_credits, remaining_credits = calculate_gpa_and_credits(student_id)
    print(f"GPA for student {student_id}: {gpa:.2f}")
    print(f"Earned Credits: {earned_credits}")
    print(f"Remaining Credits for Graduation: {remaining_credits}")