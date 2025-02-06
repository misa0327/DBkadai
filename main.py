import sqlite3

# 学生IDを使って必要な情報をデータベースから取得する関数
def get_student_info(student_id, password):
    
    #学生IDとパスワードを使って学生の基本情報を取得する
    
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
    connection.close()

    if student_info:
        return student_info
    return None  # 情報が見つからない場合


def main():
    while True:
        # ユーザからIDとパスワードを入力
        student_id = input("Enter student ID: ")
        password = input("Enter password: ")  

        # パスワードが適切か確認
        student_info = get_student_info(student_id, password)

        if student_info:
            name, gpa, rank, total_credits, remaining_credits = student_info
            print(f"{name} さん")
            print(f"GPA: {gpa:.2f}")
            print(f"順位: {rank}")
            print(f"取得単位数: {total_credits}")
            print(f"不足単位数: {remaining_credits}")
            break  # 有効な情報が入力された場合、ループを終了
        else:
            print("Invalid student ID or password!")
            print("Please try again.")

if __name__ == "__main__":
    main()
