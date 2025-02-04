#insert_sample.py
import sqlite3

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
    
    cursor.executemany('''INSERT INTO subjects (subject_name, credits) VALUES (?, ?)''', subjects)

    # 生徒情報の挿入 (評価、取得単位、不足単位は計算で決定されるのでNoneを設定)
    students = [
        ('S12345', '田中太郎', 'password123', None, None, None, None),  # GPA、取得単位、不足単位は計算
        ('S12346', '佐藤花子', 'password456', None, None, None, None),  # GPA、取得単位、不足単位は計算
        ('S12347', '鈴木一郎', 'password789', None, None, None, None),  # GPA、取得単位、不足単位は計算
    ]
    
    cursor.executemany('''INSERT INTO users (student_id, name, password, gpa, rank, total_credits, remaining_credits) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', students)

    # 履修情報の挿入
    enrollments = [
        ('S12345', 1, 80, '優'),  # 田中太郎: データベース
        ('S12345', 2, 75, '優'),  # 田中太郎: 電子商取引論
        ('S12345', 3, 60, '可'),  # 田中太郎: 線形代数学
        ('S12346', 1, 70, '良'),  # 佐藤花子: データベース
        ('S12346', 2, 85, '秀'),  # 佐藤花子: 電子商取引論
        ('S12346', 4, 55, '不可'), # 佐藤花子: 人工知能
        ('S12347', 1, 65, '可'),  # 鈴木一郎: データベース
        ('S12347', 3, 80, '優'),  # 鈴木一郎: 線形代数学
        ('S12347', 5, 90, '秀')   # 鈴木一郎: 英語
    ]
    
    cursor.executemany('''INSERT INTO enrollments (student_id, subject_id, score, grade) 
                           VALUES (?, ?, ?, ?)''', enrollments)

    # 変更を保存
    connection.commit()
    connection.close()

    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
