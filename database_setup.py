import sqlite3

def create_database():
    # データベースファイルのパス
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()

    # ユーザー情報テーブルの作成
    #学生ID:　プライマリーキー
    #氏名
    #パスワード
    #GPA:　実数（REAL型）で保持
    #順位:　整数（INTEGER型）
    #取得単位数
    #不足単位
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        student_id TEXT PRIMARY KEY,    
                        name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        gpa REAL,
                        rank INTEGER,
                        total_credits INTEGER,
                        remaining_credits INTEGER)''')

    # 科目情報テーブルの作成
    #科目ID:　プライマリーキー
    #学生ID:　usersテーブルのstudent_idとリレーション　
    #FOREIGN KEYを使いsubjectsテーブルのstudent_idがusersテーブルのstudent_idと一致するようにしている
    #科目名
    #単位数:　整数型
    #科目の得点(60未満は0として計算)
    #成績評価:　TEXT型
    cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                        subject_id INTEGER PRIMARY KEY,
                        student_id TEXT,
                        subject_name TEXT NOT NULL,
                        credits INTEGER NOT NULL,
                        score INTEGER,   -- 得点を格納
                        grade TEXT,      -- 評価を格納（「秀」「優」「良」「可」「不可」「欠席」）
                        FOREIGN KEY (student_id) REFERENCES users(student_id))''')
    
    
    # 必要に応じて他のテーブルを作成する処理を追加
    #変更を保存
    connection.commit()
    #データベース接続のクローズ
    connection.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
