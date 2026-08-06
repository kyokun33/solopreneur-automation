import os
import sys
import webview

def main():
    html_path = os.path.abspath(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ebook_reader.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    print(f"Launching Native Desktop Window for: {file_url}")
    
    # Create desktop app window forced on top
    window = webview.create_window(
        title="💡 [비밀 치트키] 1인 기업 AI 프롬프트 100선 가이드",
        url=file_url,
        width=1100,
        height=850,
        resizable=True,
        on_top=True
    )
    webview.start()

if __name__ == "__main__":
    main()
