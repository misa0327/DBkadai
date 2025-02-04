#database_setup.py
import sqlite3

def create_database():
    #DB設計
    #subjects:      科目の基本情報（科目Id、科目名、単位数）
    #users:         生徒の基本情報（生徒ID、氏名、パスワード、GPA、順位、取得単位、不足単位）
    #enrollments:   生徒が履修した科目の情報（生徒ID、科目ID、スコア、評価）
    
    
    # データベースファイルのパス
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()


    #sublects
    #科目情報: 科目ごとにIDを設定し、科目名や単位数を統一
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY,  -- 科目ID(主キー)
        subject_name TEXT NOT NULL,      -- 科目名
        credits INTEGER NOT NULL         -- 単位数  
    );
    ''')

    #users
    #生徒情報: 生徒の基本情報（GPAや順位を含む）を保存し、履修情報とは分ける。
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        student_id TEXT PRIMARY KEY,  -- 学生ID (主キー)
        name TEXT NOT NULL,           -- 氏名
        password TEXT NOT NULL,       -- パスワード
        gpa REAL,                     -- GPA
        rank INTEGER,                 -- 順位
        total_credits INTEGER DEFAULT 0, -- 取得単位数
        remaining_credits INTEGER DEFAULT 124 -- 不足単位数
    );
    ''')    

    #enrollmets
    #履修情報: 生徒ごとに履修した科目の情報（成績・評価）を保存する。
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 履修ID(主キー)
        student_id TEXT NOT NULL,  -- 生徒ID(外部キー)
        subject_id INTEGER NOT NULL, -- 科目ID(外部キー)
        score INTEGER,              -- 成績（点数）
        grade TEXT,                 -- 評価（秀、優、良、可、不可、欠席）
        FOREIGN KEY (student_id) REFERENCES users(student_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    );
    """)
    
    
    # 必要に応じて他のテーブルを作成する処理を追加
    #変更を保存
    connection.commit()
    #データベース接続のクローズ
    connection.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
