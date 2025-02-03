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