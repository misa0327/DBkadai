import sqlite3

# データベースに接続（存在しない場合は新規作成）
conn = sqlite3.connect('university.db')

# カーソルを作成
cursor = conn.cursor()

# テーブルのデータを削除
cursor.execute("DELETE FROM users;")

# 変更を保存
conn.commit()

# 接続を閉じる
conn.close()
