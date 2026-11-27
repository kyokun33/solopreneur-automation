import os
from typing import Protocol, List
from abc import ABC, abstractmethod
# ⚠️ 실제 API 호출을 시뮬레이션하기 위한 모듈입니다.
# 여기에 Naver와 Tistory의 SDK 또는 HTTP 클라이언트 로직이 들어갈 예정입니다.

class PlatformAdapter(ABC):
    """
    플랫폼별 배포 규격에 맞춰 콘텐츠를 변환하고 게시하는 추상 기반 클래스 (Adapter Pattern)
    모든 플랫폼 어댑터는 이 인터페이스를 따라야 합니다.
    """
    PLATFORM_NAME: str = "ABSTRACT"

    @abstractmethod
    def format_content(self, content: str) -> str:
        """
        표준 Markdown/Rich Text 콘텐츠를 해당 플랫폼이 요구하는 최종 HTML 또는 텍스트 포맷으로 변환합니다.
        예: Naver는 특정 div 구조가 필요할 수 있음. Tistory는 다른 마크다운 파싱을 선호할 수 있음.
        """
        raise NotImplementedError("Subclass must implement format_content")

    @abstractmethod
    def publish(self, formatted_html: str, title: str, tags: List[str]) -> dict:
        """
        최종 포맷팅된 콘텐츠를 실제 플랫폼 API를 통해 게시합니다.
        성공/실패 여부와 고유 URL을 반환해야 합니다.
        """
        raise NotImplementedError("Subclass must implement publish")

# ------------------------------------------------------
# ⭐️ Naver Blog Adapter 구현체
# ------------------------------------------------------
class NaverAdapter(PlatformAdapter):
    PLATFORM_NAME = "NaverBlog"

    def format_content(self, content: str) -> str:
        print(f"[DEBUG] {self.PLATFORM_NAME}: 표준 콘텐츠를 Naver 최적화 HTML로 변환 중...")
        # 실제로는 복잡한 HTML 구조 재작성 로직이 들어갑니다.
        return f"<!-- BEGIN NAVER Optimized Content -->\n<h1>{content[:20]}...</h1><div class='naver-body'>{content}</div><!-- END NAVER Optimized Content -->"

    def publish(self, formatted_html: str, title: str, tags: List[str]) -> dict:
        print(f"[DEBUG] {self.PLATFORM_NAME}: API 호출 시뮬레이션... 제목: '{title}'")
        # 여기에 Naver Blog Open API를 사용한 인증 및 포스팅 로직이 들어갑니다. (OAuth 2.0 등)
        return {"status": "SUCCESS", "url": f"https://blog.naver.com/temp/{hash(formatted_html)}", "platform": self.PLATFORM_NAME}

# ------------------------------------------------------
# ⭐️ Tistory Adapter 구현체
# ------------------------------------------------------
class TistoryAdapter(PlatformAdapter):
    PLATFORM_NAME = "Tistory"

    def format_content(self, content: str) -> str:
        print(f"[DEBUG] {self.PLATFORM_NAME}: 표준 콘텐츠를 Tistory 최적화 마크다운/HTML로 변환 중...")
        # 실제로는 Tistory의 특정 마크다운 파싱 또는 HTML 구조가 필요합니다.
        return f"<!-- BEGIN TISTORY Optimized Content -->\n## 콘텐츠 분석 결과\n{content}\n<!-- END TISTORY Optimized Content -->"

    def publish(self, formatted_html: str, title: str, tags: List[str]) -> dict:
        print(f"[DEBUG] {self.PLATFORM_NAME}: API 호출 시뮬레이션... 제목: '{title}'")
        # 여기에 Tistory API를 사용한 인증 및 포스팅 로직이 들어갑니다.
        return {"status": "SUCCESS", "url": f"https://tistory.com/temp/{hash(formatted_html)}", "platform": self.PLATFORM_NAME}

# ------------------------------------------------------
# ⭐️ 메인 실행 서비스 클래스
# ------------------------------------------------------
class BlogPublisherService:
    def __init__(self, content_file_path: str):
        if not os.path.exists(content_file_path):
            raise FileNotFoundError(f"Error: Specified content file not found at {content_file_path}")
        self.content_file_path = content_file_path

    def load_and_parse_content(self) -> tuple[str, str, List[str]]:
        """
        1. 파일에서 콘텐츠를 읽고 (Markdown/Rich Text).
        2. 제목과 태그를 추출합니다. (이 부분은 정규식 또는 별도 파서를 사용해야 합니다.)
        """
        print(f"⚙️ {self.__class__.__name__}: 로컬 파일을 분석하여 원고 내용을 로드합니다.")
        try:
            with open(self.content_file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            # 임시 파싱 로직 (실제 환경에서는 더 복잡한 NLP/RegEx가 필요함)
            title = "AI 저작권 폭탄 피하기: 데이터 출처 증명이 곧 사업 생존권인 이유" # 개요 1 제목 사용
            tags = ["AI저작권", "데이터프로비넌스", "법적책임"]

            return raw_content, title, tags

        except Exception as e:
            print(f"❌ 콘텐츠 로드 중 치명적인 오류 발생: {e}")
            raise

    def run_automation(self, adapter: PlatformAdapter) -> dict:
        """
        선택된 어댑터를 사용하여 전체 배포 과정을 실행합니다.
        """
        try:
            # 1. 원고 로드 및 파싱 (핵심 데이터 추출)
            raw_content, title, tags = self.load_and_parse_content()

            # 2. 플랫폼별 포맷 변환 (추상화된 핵심 비즈니스 로직)
            formatted_html = adapter.format_content(raw_content)

            # 3. 실제 배포 실행
            result = adapter.publish(formatted_html, title, tags)

            print("✅ 모든 단계가 성공적으로 완료되었습니다.")
            return result

        except FileNotFoundError as e:
            return {"status": "FAILED", "reason": str(e)}
        except Exception as e:
            # 실패 시, 어디서, 왜 깨졌는지 로그를 남깁니다. (Debugging Focus)
            print(f"🚨 자동화 프로세스 중 예기치 않은 오류 발생: {type(e).__name__} - {e}")
            return {"status": "CRITICAL_FAILURE", "reason": str(e)}

# ------------------------------------------------------
# 테스트 실행 블록 (실제 사용 시에는 주석 처리)
# if __name__ == "__main__":
#     # 가상의 원고 파일 경로를 지정합니다.
#     MOCK_FILE_PATH = "/path/to/your/article.md" 
    
#     if os.path.exists(MOCK_FILE_PATH):
#         service = BlogPublisherService(content_file_path=MOCK_FILE_PATH)

#         # Naver 테스트 실행
#         naver_adapter = NaverAdapter()
#         naver_result = service.run_automation(naver_adapter)
#         print("\n--- Naver 배포 결과 ---")
#         print(naver_result)

#         # Tistory 테스트 실행
#         tistory_adapter = TistoryAdapter()
#         tistory_result = service.run_automation(tistory_adapter)
#         print("\n--- Tistory 배포 결과 ---")
#         print(tistory_result)
#     else:
#         print("실행 실패: 더미 파일 경로를 실제 원고 파일 경로로 수정해주세요.")