<create_file path="f:\1인기업\_company_agents\developer\specs\tos_hard_stop_spec.md"># 🛑 TOS Hard Stop 로직 개발 스펙 문서 (v1.0)

## 1. 개요
**프로젝트명**: 고고플랙스 (Solopreneur Automation System)  
**문서 버전**: v1.0  
**작성일**: 2026-08-30  
**주요 목적**: 법적 승인 전까지 결제 및 데이터 수집 플로우를 강제로 차단하는 'Hard Stop' 로직 구현 가이드라인

---

## 2. 핵심 요구사항
### 2.1 조건부 진입 (Conditional Entry)
*   **조건**: `TOS_Status`가 `'APPROVED'` 또는 `'EXEMPTED'(예외 승인)` 상태일 때만 플로우 진입 허용.
*   **반대 조건**: `'PENDING'`(검토 중), `'REJECTED'`(거부), `'DRAFT'`(초안) 상태 시 시스템 진입 차단.

### 2.2 Hard Stop 구현 위치
1.  **API Gateway Level (백엔드)**: 모든 결제 요청 (Payment API) 및 데이터 수집 API 엔드포인트 앞에 `TOS_Gateway_Middleware` 를 전방 배치.
    *   헤더 `x-tos-status`를 확인하여 상태가 `'APPROVED'`가 아님 즉시 403 Forbidden 반환.
2.  **Frontend Level (클라이언트)**: 결제 버튼 클릭 시 비동기로 TOS API 상태를 먼저 확인하고, UI 레벨에서 에러 토스트 (Toaster) 나 모달을 띄워 차단.

---

## 3. 구현 세부 사항 (Implementation Details)

### 3.1 Backend Gateway Middleware (Python/FastAPI Example)
```python
from fastapi import Request, HTTPException
from typing import Optional
import requests

class TOSHardStopMiddleware:
    def __init__(self, api_base_url: str, tos_api_key: str):
        self.api_base_url = api_base_url
        self.tos_api_key = tos_api_key

    async def check_tos_status(self) -> str:
        """TOS 상태 조회 API 호출 (External Service 또는 Internal DB)"""
        # 실제 구현은 환경 변수나 내부 DB 로 대체 가능
        url = f"{self.api_base_url}/tos/status"
        headers = {"Authorization": f"Bearer {self.tos_api_key}"}
        response = requests.get(url, headers=headers)
        return response.json().get("status")

    async def process_request(self, request: Request):
        # 결제/회원가입 등 민감 API 로직
        if not "/payment" in request.url and not "/signup" in request.url:
            return  # 비민감 엔드포인트는 통과
        
        status = await self.check_tos_status()
        
        if status != "APPROVED":
            raise HTTPException(
                status_code=403, 
                detail="Legal Review Pending. System Hard Stop Activated."
            )
```

### 3.2 Frontend Utility (React/TypeScript Example)
```tsx
// hooks/useTosStatus.ts
const useTosHardStop = () => {
    const [status, setStatus] = useState('PENDING'); // 초기값: PENDING (Block Mode)

    useEffect(() => {
        fetchTosStatus(); // API 호출 로직 구현
    }, []);

    if (status !== 'APPROVED') {
        return <ErrorOverlay message="법적 검토 중입니다. 결제 기능이 일시 중지되었습니다." />;
    }
    
    return null; // 정상 상태 시 렌더링 중단
};
```

---

## 4. 개발 체크리스트 (Developer TODO)
*   [ ] `TOS_Gateway_Middleware` 클래스 구현 및 API 테스트 (`pytest`).
*   [ ] Frontend 의 `useTosStatus` 훅 작성 및 에러 핸들링 UI (모달/토스트) 제작.
*   [ ] 환경 변수 `.env` 에 `TOS_API_BASE_URL` 및 키 저장 (.gitignore 등록 필수).
*   [ ] CI/CD 파이프라인에 코드 리뷰 단계 추가 (법무 팀 승인 여부 확인 체크).

---

## 5. 법무팀 연동 프로토콜
*   **상태 업데이트 API**: `/api/legal/tos/status`
    *   `PUT`: 상태 변경 (Draft -> Review -> Approved) 시 자동 배포 트리거 필요.
    *   `POST`: 리뷰 의견 제출 시 백엔드 로직 수정 로그 남기기.

> **주의사항**: 이 스펙은 법적 승인 전까지 'Simulation Mode'로 유지됩니다. 실제 운영 전환 시 `.env` 설정값을 `SIMULATION_MODE=false`로 변경해야 합니다.