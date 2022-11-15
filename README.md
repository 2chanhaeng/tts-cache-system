# TTS Cache System
 원티드 5차 백엔드 프리온보딩 코스 5차 과제

- [TTS Cache System](#tts-cache-system)
  - [API Docs](#api-docs)

## API Docs

| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | /api/v1/project | 프로젝트 생성 |
| GET | /api/v1/project/<int:project_id>/?page=<int:page_num> | 프로젝트 특정 페이지 내 텍스트 조회 |
| PUT | /api/v1/audio/<int:audio_id>/ | 텍스트 수정 |
| POST | /api/v1/audio/<int:audio_id>/ | 텍스트 추가  |
| DELETE | /api/v1/audio/<int:audio_id>/ | 텍스트 삭제 |
| DELETE | /api/v1/project/<int:project_id>/ | 프로젝트 삭제 |
| GET | /api/v1/audio/<int:audio_id>/download/ | 오디오파일 송신 |
