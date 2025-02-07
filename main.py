import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from insert_sample_data import insert_sample_data  # insert_sample_data関数をインポート

class StudentApp:
    def __init__(self, root):
        # 最初にサンプルデータを挿入
        insert_sample_data()

        self.root = root
        self.root.title("Student Login")
        self.root.geometry("400x250")
        self.root.configure(bg="#2C3E50")
        
        tk.Label(root, text="Student ID:", fg="white", bg="#2C3E50", font=("Arial", 12)).pack(pady=5)
        self.student_id_entry = tk.Entry(root, font=("Arial", 12))
        self.student_id_entry.pack()
        
        tk.Label(root, text="Password:", fg="white", bg="#2C3E50", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(root, show="*", font=("Arial", 12))
        self.password_entry.pack()
        
        tk.Button(root, text="Login", command=self.login, font=("Arial", 12), bg="#3498DB", fg="white").pack(pady=10)
        
    def login(self):
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        
        student_info = self.get_student_info(student_id, password)
        
        if student_info:
            self.root.destroy()
            MainApp(student_id, student_info)
        else:
            messagebox.showerror("Login Failed", "Invalid student ID or password!")
    
    def get_student_info(self, student_id, password):
        connection = sqlite3.connect('university.db')
        cursor = connection.cursor()
        
        cursor.execute(''' 
        SELECT name, gpa, rank, total_credits, remaining_credits 
        FROM users
        WHERE student_id = ? AND password = ?
        ''', (student_id, password))
        
        student_info = cursor.fetchone()
        
        if student_info:
            cursor.execute(''' 
            SELECT subjects.subject_name, enrollments.grade
            FROM enrollments
            JOIN subjects ON enrollments.subject_id = subjects.subject_id
            WHERE enrollments.student_id = ?
            ''', (student_id,))
            grades = cursor.fetchall()
            connection.close()
            return student_info + (grades,)
        
        connection.close()
        return None

class MainApp:
    def __init__(self, student_id, student_info):
        self.root = tk.Tk()
        self.root.title("Student Dashboard")
        self.root.geometry("600x400")
        self.root.configure(bg="#34495E")
        
        self.student_id = student_id
        self.student_info = student_info
        self.language = "jp"
        
        self.label_welcome = tk.Label(self.root, text=f"ようこそ, {student_info[0]}", fg="white", bg="#34495E", font=("Arial", 16, "bold"))
        self.label_welcome.pack(pady=10)
        
        button_frame = tk.Frame(self.root, bg="#34495E")
        button_frame.pack(expand=True)
        
        self.btn_gpa_rank = tk.Button(button_frame, text="GPA・順位を見る", command=self.show_gpa_rank, font=("Arial", 14), bg="#1ABC9C", fg="white", width=20, height=2)
        self.btn_gpa_rank.pack(pady=5)
        
        self.btn_credits = tk.Button(button_frame, text="単位数を見る", command=self.show_credits, font=("Arial", 14), bg="#1ABC9C", fg="white", width=20, height=2)
        self.btn_credits.pack(pady=5)
        
        self.btn_grades = tk.Button(button_frame, text="成績を見る", command=self.show_grades, font=("Arial", 14), bg="#1ABC9C", fg="white", width=20, height=2)
        self.btn_grades.pack(pady=5)
        
        self.btn_language = tk.Button(self.root, text="English", command=self.toggle_language, font=("Arial", 12), bg="#F39C12", fg="white")
        self.btn_language.place(relx=0.9, rely=0.05, anchor="ne")
        
        self.btn_logout = tk.Button(self.root, text="ログアウト", command=self.logout, font=("Arial", 12), bg="#E74C3C", fg="white")
        self.btn_logout.place(relx=0.9, rely=0.9, anchor="se")
        
        self.root.mainloop()
    
    def toggle_language(self):
        if self.language == "jp":
            self.language = "en"
            self.label_welcome.config(text=f"Welcome, {self.student_info[0]}")
            self.btn_gpa_rank.config(text="View GPA & Rank")
            self.btn_credits.config(text="View Credits")
            self.btn_grades.config(text="View Grades")
            self.btn_language.config(text="日本語")
            self.btn_logout.config(text="Logout")  # ログアウトボタンのテキストを英語に変更
        else:
            self.language = "jp"
            self.label_welcome.config(text=f"ようこそ, {self.student_info[0]}")
            self.btn_gpa_rank.config(text="GPA・順位を見る")
            self.btn_credits.config(text="単位数を見る")
            self.btn_grades.config(text="成績を見る")
            self.btn_language.config(text="English")
            self.btn_logout.config(text="ログアウト")  # ログアウトボタンのテキストを日本語に変更
    
    def show_gpa_rank(self):
        window = tk.Toplevel(self.root)
        window.title("GPA & Rank")
        window.geometry("300x150")
        window.configure(bg="#2C3E50")
        
        tree = ttk.Treeview(window, columns=("item", "value"), show="headings")
        tree.heading("item", text="項目" if self.language == "jp" else "Item")
        tree.heading("value", text="値" if self.language == "jp" else "Value")
        
        tree.insert("", "end", values=("GPA", f"{self.student_info[1]:.2f}"))
        tree.insert("", "end", values=("順位" if self.language == "jp" else "Rank", self.student_info[2]))
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def show_credits(self):
        window = tk.Toplevel(self.root)
        window.title("Credits")
        window.geometry("300x150")
        window.configure(bg="#2C3E50")
        
        tree = ttk.Treeview(window, columns=("item", "value"), show="headings")
        tree.heading("item", text="項目" if self.language == "jp" else "Item")
        tree.heading("value", text="値" if self.language == "jp" else "Value")
        
        tree.insert("", "end", values=("取得単位数" if self.language == "jp" else "Earned Credits", self.student_info[3]))
        tree.insert("", "end", values=("不足単位数" if self.language == "jp" else "Remaining Credits", self.student_info[4]))
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def show_grades(self):
        grades_window = tk.Toplevel(self.root)
        grades_window.title("Grades")
        grades_window.geometry("500x300")
        grades_window.configure(bg="#2C3E50")
        
        tree = ttk.Treeview(grades_window, columns=("subject", "grade"), show="headings")
        tree.heading("subject", text="科目" if self.language == "jp" else "Subject")
        tree.heading("grade", text="成績" if self.language == "jp" else "Grade")
        
        for subject, grade in self.student_info[5]:
            tree.insert("", "end", values=(subject, grade))
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        StudentApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
