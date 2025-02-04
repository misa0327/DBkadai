import sqlite3

# 学生IDを使って必要な情報をデータベースから取得する関数
def get_student_info(student_id, password):
    """
    学生IDとパスワードを使って学生の基本情報を取得する
    """
    # データベースに接続
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    # 学生の情報を取得（成績評価、GPA、順位、取得単位数、不足単位数）
    # student_idに対応するパスワードをデータベースから取得
    cursor.execute('''
    SELECT name, gpa, rank, total_credits, remaining_credits 
    FROM users
    WHERE student_id = ? AND password = ?
    ''', (student_id, password))

    student_info = cursor.fetchone()
    return (name, grade, gpa, rank, total_credits, remaining_credits)

  if student_info:
        # 成績評価を取得する（履修したすべての科目の評価を取得）
        cursor.execute('''
        SELECT s.subject_name, e.score 
        FROM enrollments e
        JOIN subjects s ON e.subject_id = s.subject_id
        WHERE e.student_id = ?
        ''', (student_id,))
        scores = cursor.fetchall()

        # 成績を評価に変換（欠席の場合も処理）
        grades = {subject_name: get_grade(score) for subject_name, score in scores}
        return student_info, grades  # 学生情報と科目ごとの成績評価を返す
    
    connection.close()
    return None  # 情報が見つからない場合


def main():
    # ユーザからIDとパスワードを入力
    student_id = input("Enter student ID: ")
    password = input("Enter password: ")  

    # パスワードが適切か確認
    student_info = get_student_info(student_id, password)

    if student_info:
        name, gpa, rank, total_credits, remaining_credits = student_info
        print(f"Student Name: {name}")
        print(f"GPA: {gpa:.2f}")
        print(f"Rank: {rank}")
        print(f"Total Credits: {total_credits}")
        print(f"Remaining Credits for Graduation: {remaining_credits}")
    else:
        print("Invalid student ID or password!")

if __name__ == "__main__":
    main()
