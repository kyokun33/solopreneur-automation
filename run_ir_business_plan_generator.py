# ==============================================================================
# 3분 정부지원 IR AI 사업계획서 보고서 생성기 (PRO 정식 승인 버전 런처)
# ==============================================================================
import os
import webbrowser

html_path = r"C:\Users\sude3\OneDrive\바탕 화면\1인기업\3분_정부지원_IR_AI_사업계획서_생성기.html"

if not os.path.exists(html_path):
    html_path = r"C:\Users\sude3\OneDrive\바탕 화면\3분_정부지원_IR_AI_사업계획서_생성기.html"

webbrowser.open_new_tab(f"file:///{html_path.replace('\\', '/')}")
print("3-Minute IR AI Business Plan Generator PRO Web App Opened Successfully!")