import webview

def main():
    url = "http://127.0.0.1:8090"
    print(f"Launching Native Desktop Window for Sales Portal: {url}")
    
    window = webview.create_window(
        title="🔥 [1인기업 무인 판매 포털] AI 업무 자동화 프롬프트 100선 전자책",
        url=url,
        width=1150,
        height=880,
        resizable=True,
        on_top=True
    )
    webview.start()

if __name__ == "__main__":
    main()
