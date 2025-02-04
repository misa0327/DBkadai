#utils.py
def get_grade(score):
    """
    得点に基づいて評価を決定
    """
    if score is None:
        return "欠席"
    elif score >= 90:
        return "秀"
    elif score >= 80:
        return "優"
    elif score >= 70:
        return "良"
    elif score >= 60:
        return "可"
    else:
        return "不可"  # 60点未満は不可