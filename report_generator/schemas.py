from pydantic import BaseModel, Field
from typing import Optional

class ReportRequest(BaseModel):
    title: str = Field(..., description="사업 아이템 및 프로젝트명", example="AI 기반 맞춤형 리포트 자동 생성기")
    category: str = Field(default="government", description="리포트 유형 (government: 정부지원사업용, ir: 투자유치용, market: 시장분석용)")
    target_customer: str = Field(..., description="타겟 고객층", example="1인 기업가, 소상공인, 예비창업자")
    core_features: str = Field(..., description="주요 기능 및 경쟁력", example="자동화된 PDF 렌더링, 3분 내 사업계획서 완성")
    budget: str = Field(default="10,000,000원", description="예산 및 목표 매출")
    program_type: str = Field(default="packages_15p", description="지원사업 프로그램 규격 (packages_15p, cheongsa_12p, rnd_25p, export_8p, local_5p)")
    access_key: Optional[str] = Field(default=None, description="1회용 구매 인증 코드")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API 키 (선택사항)")

class ReportResponse(BaseModel):
    success: bool
    title: str
    category_name: str
    markdown_content: str
    html_content: str
    generated_at: str
