---
name: comfyui_antigravity_automation
description: ComfyUI & Antigravity Automation Pipeline skill using LLM Bridge, API Nodes, and Scene Camera Action for workflow and image/video generation.
---

# 🎨 ComfyUI & Antigravity Automation Pipeline Skill

본 스킬은 ComfyUI와 안티그래비티(Antigravity) AI 에이전트 간의 자동화 파이프라인 구축, 워크플로우(workflow.json) 생성/검증, OpenAI 호환 API 노드 연동 및 2D/3D 카메라 연출 씬 생성을 전담하는 커스텀 스킬 가이드입니다.

---

## 📌 핵심 파이프라인 3대 연동 지침

### 1. 🌉 ComfyUI LLM Bridge (`huikku/comfyui-llm-bridge`)
- ComfyUI의 로컬 API Server (`http://127.0.0.1:8188`)와 직접 통신 시 본 어댑터를 활용한다.
- 대표님이 워크플로우(`workflow.json`) 생성을 요청하거나 수정을 원할 때 무작위 추론 작성을 금지한다.
- LLM Bridge의 경량 노드 스키마 구조 (`@NodeName +required:TYPE -output:TYPE`)를 참조하여 **실제 로컬 ComfyUI에 설치된 노드 ID 및 입력/출력 타입 연결 정보를 100% 검증 후 JSON을 자동 생성**한다.

### 2. 🔑 Antigravity API Nodes (`Jint8888/Comfyui-Antigravity-apinodes`)
- ComfyUI 캔버스 내부에서 안티그래비티 / OpenAI 규격 API (`gemini-3-pro-image`, LLM, Audio, Multimodal)를 직접 호출하는 노드가 필요한 경우 본 커스텀 노드를 파이프라인에 배치한다.
- 텍스트 프롬프트 생성 및 스타일/시드 제어 파라미터를 해당 API 노드 입력값으로 자동 매핑한다.

### 3. 🎥 Scene Camera Action (`arturitu/ComfyUI-scene-camera-action`)
- 2D/3D 연출, 카메라 연출, 씬(Scene) 제어가 포함된 스프라이트/이미지/비디오 생성을 수행할 때 카메라 제어 노드 (`SceneNode`, `ActingNode`, `DirectingNode`) 파라미터를 동적으로 제어한다.
- TPV, FPV, Wide, Side 카메라 각도 및 WASD 모션 궤적 캡처 셋업을 연동한다.

---

## ⚡ 실행 프로토콜

- 사용자가 ComfyUI 워크플로우 생성, 노드 연결, 이미지/비디오 자동화, 3D 카메라 연출을 요청할 시 **위 3가지 도구와 검증된 스키마 구조를 최우선 적용하여 코드 및 JSON을 작성**한다.

---

## 🌐 ComfyUI 기본 리소스 정보 (참조용)

- **ComfyUI 공식 저장소**: `https://github.com/comfy-org/comfyui` (설치 및 코어 로직 참조)
- **ComfyUI-Manager**: `https://github.com/comfy-org/ComfyUI-Manager` (커스텀 노드 패키지 관리 시 참조)
- **Comfy-Org HuggingFace**: `https://huggingface.co/Comfy-Org` (공식 AI 모델 및 경량화 파일 다운로드 시 참조)

ComfyUI 환경 구축이나 모델/노드 설치 명령을 수행할 때 위 3대 리소스 주소를 최우선으로 활용한다.

