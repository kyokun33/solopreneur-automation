import webview

def main():
    url = "http://localhost:8000"
    print(f"Launching Native Desktop Window for AI Report Generator SaaS: {url}")
    
    window = webview.create_window(
        title="🚀 [마이크로 SaaS] AI 사업계획서 & 보고서 자동 생성기 (report_generator)",
        url=url,
        width=1150,
        height=880,
        resizable=True,
        on_top=True
    )
    webview.start()

if __name__ == "__main__":
    main()
