import unittest
from unittest.mock import MagicMock, patch
# 상대 경로 사용 (패키지 구조에 따라 수정 필요)
from src.services.blog_publisher import NaverAdapter, TistoryAdapter

class TestBlogPublishing(unittest.TestCase):
    
    def setUp(self):
        # 테스트용 Mock 파일 생성 (실제 환경에서는 임시 파일을 만들어야 합니다.)
        self.mock_file_path = "temp_test_article.md" 
        with open(self.mock_file_path, 'w', encoding='utf-8') as f:
            f.write("# 테스트용 원고 제목\n\n이것은 데이터 무결성 관련 핵심 내용입니다.")

    def tearDown(self):
        # 테스트 후 파일 정리
        import os
        if os.path.exists(self.mock_file_path):
             os.remove(self.mock_file_path)


    @patch('src.services.blog_publisher.open', new=MagicMock()) # 실제 file open 호출을 목킹
    def test_content_loader(self):
        # load_and_parse_content가 파일을 성공적으로 읽고 데이터를 반환하는지 테스트
        from src.services.blog_publisher import BlogPublisherService
        service = BlogPublisherService(content_file_path=self.mock_file_path)
        try:
            raw, title, tags = service.load_and_parse_content()
            self.assertIsInstance(raw, str)
            self.assertTrue("데이터 무결성" in raw) # 내용 확인
        except Exception as e:
            self.fail(f"Content loading failed unexpectedly: {e}")

    def test_naver_adapter_format(self):
        # Naver 포맷팅 로직이 예상대로 작동하는지 테스트
        adapter = NaverAdapter()
        raw_content = "테스트 원고 내용입니다."
        formatted = adapter.format_content(raw_content)
        self.assertIn("BEGIN NAVER Optimized Content", formatted)
        self.assertIn("naver-body", formatted)

    @patch('src.services.blog_publisher.print') # print 함수 호출까지 Mocking하여 부수 효과 검증 가능
    def test_tistory_adapter_format(self, mock_print):
        # Tistory 포맷팅 로직이 예상대로 작동하는지 테스트
        adapter = TistoryAdapter()
        raw_content = "테스트 원고 내용입니다."
        formatted = adapter.format_content(raw_content)
        self.assertIn("BEGIN TISTORY Optimized Content", formatted)
        self.assertIn("## 콘텐츠 분석 결과", formatted)

# 실행 예시: python -m unittest tests.test_blog_publisher