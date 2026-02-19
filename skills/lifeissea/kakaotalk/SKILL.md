---
name: kakaotalk
version: 1.0.0
description: "KakaoTalk频道Webhook桥梁AI助手：通过与Kakao i OpenBuilder的集成，实现与Raon AI助手的对话。支持Ollama（qwen3:8b）作为备用方案；具备会话管理功能，并支持自动传输长达900个字符的消息。"
author: Yeomyeonggeori Inc. <iam@dawn.kim>
license: MIT
metadata:
  openclaw:
    env:
      - name: GEMINI_API_KEY
        description: "Google Gemini 2.5 Flash Lite API 키 (Ollama 실패 시 fallback)"
        required: false
      - name: KAKAO_CALLBACK_SECRET
        description: "카카오 오픈빌더 웹훅 서명 검증 시크릿 (선택, 보안 강화)"
        required: false
      - name: KAKAOTALK_PORT
        description: "웹훅 서버 포트 (기본 8401)"
        required: false
      - name: OLLAMA_HOST
        description: "Ollama 서버 주소 (기본 http://localhost:11434)"
        required: false
    requires:
      bins: ["python3"]
    notes: "Ollama가 로컬에 설치되어 있고 qwen3:8b 모델이 pull되어 있어야 합니다. GEMINI_API_KEY는 Ollama 실패 시 자동 fallback에 사용됩니다."
---
# kakaotalk — 卡卡聊AI助手技能

这是一个可以在卡卡聊（KakaoTalk）频道中与Raon AI助手进行对话的OpenClaw技能。  
需要将该技能注册为Kakao i OpenBuilder中的“回退区块（Fallback Block）”才能使用。

## 架构

```
카카오톡 채널
     ↓
카카오 i 오픈빌더 (폴백 블록 → 스킬 서버)
     ↓ POST /kakao
Python 웹훅 서버 (포트 8401)
     ↓
Ollama qwen3:8b (90초, 로컬) → 실패 시 Gemini 2.5 Flash Lite
     ↓
카카오 v2 응답 (simpleText + quickReplies)
```

---

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `GEMINI_API_KEY` | Gemini 2.5 Flash Lite API密钥（Ollama备用） | — |
| `KAKAO_CALLBACK_SECRET` | Webhook签名验证密钥（可选） | — |
| `KAKAOTALK_PORT` | 服务器端口 | `8401` |
| `OLLAMA_HOST` | Ollama地址 | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama模型 | `qwen3:8b` |
| `KAKAOTALK_PERSONA_NAME` | AI名称（显示在欢迎/处理中消息中） | `AI助手` |
| `KAKAOTALK_SYSTEM_PROMPT` | 系统提示语（可替换默认提示语） | — |
| `KAKAOTALK_LOG_DIR` | 日志存储路径 | `~/.openclaw/logs` |

```bash
# ~/.openclaw/.env 에 추가
GEMINI_API_KEY=내_API_키
KAKAO_CALLBACK_SECRET=오픈빌더_시크릿  # 선택
KAKAOTALK_PERSONA_NAME=라온            # AI 이름 커스텀
# KAKAOTALK_SYSTEM_PROMPT=당신은 ...   # 프롬프트 완전 교체 시
```

---

## 安装与运行

### 1. 准备Ollama模型

```bash
ollama pull qwen3:8b
```

### 2. 注册服务（launchd — 在macOS启动时自动运行）

```bash
bash scripts/install-service.sh
```

- launchd标签：`com.yeomyeonggeori.kakaotalk`
- 日志文件：`/Users/tomas/.openclaw/workspace/logs/kakaotalk.log`

### 3. 手动运行（测试用）

```bash
python3 scripts/server.py
# 기본 포트 8401, Ctrl+C로 종료
```

---

## 卡卡聊OpenBuilder设置步骤

1. **创建Kakao Business账户** — 访问https://business.kakao.com注册账户
2. **进入Kakao i OpenBuilder** — 登录https://i.kakao.com → 创建机器人
3. **注册技能**  
   在左侧菜单中选择**技能** → **添加技能** → 输入技能服务器URL：
   ```
   https://<ngrok_URL_or_server>/kakao
   ```
4. **连接回退区块**  
   在**场景** → **回退区块** → **技能**选项卡中选择之前创建的技能 → 保存设置
5. （可选）**连接卡卡聊频道**  
   通过卡卡聊频道管理器连接机器人

---

## 本地测试（使用ngrok）

```bash
# ngrok 터널 생성 + URL 자동 출력
bash scripts/ngrok-setup.sh

# 출력된 URL을 카카오 오픈빌더 스킬 서버 URL에 입력
# 예: https://abc123.ngrok.io/kakao
```

### 使用curl进行直接测试

```bash
curl -s -X POST http://localhost:8401/kakao \
  -H "Content-Type: application/json" \
  -d '{
    "userRequest": {
      "utterance": "TIPS 신청 방법 알려줘",
      "user": {"id": "test_user_001"}
    },
    "bot": {"id": "test_bot"},
    "intent": {"name": "폴백 블록"}
  }' | python3 -m json.tool
```

**健康检查**：
```bash
curl http://localhost:8401/health
```

---

## 响应机制

| 情况 | 响应方式 |
|------|------|
| LLM在4.5秒内响应 | 立即返回答案 |
| LLM响应超时（超过4.5秒） | 显示“Raon正在思考中…”并继续生成回答 |
| 点击“重新提问” | 返回缓存的已完成回答 |
| 点击“首次提问” | 重置会话并显示欢迎消息 |

---

## 服务管理

```bash
# 중지
launchctl unload ~/Library/LaunchAgents/com.yeomyeonggeori.kakaotalk.plist

# 시작
launchctl load ~/Library/LaunchAgents/com.yeomyeonggeori.kakaotalk.plist

# 로그 실시간 확인
tail -f /Users/tomas/.openclaw/workspace/logs/kakaotalk.log

# 상태 확인
launchctl list | grep kakaotalk
```

---

## 文件结构

```
skills/kakaotalk/
├── SKILL.md                  # 이 파일
├── package.json              # ClawHub 배포 메타
├── scripts/
│   ├── server.py             # 웹훅 서버 (Python stdlib)
│   ├── install-service.sh    # launchd 서비스 등록
│   └── ngrok-setup.sh        # ngrok 터널 도우미
└── references/
    └── kakao-api.md          # 카카오 오픈빌더 v2 API 레퍼런스
```