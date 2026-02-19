---
name: raon-os
version: 0.7.10
description: "这是一款由人工智能驱动的初创企业辅助工具，专为韩国创业者设计。它能够评估商业计划书，帮助创业者匹配政府提供的资金支持计划（如TIPS/DeepTech/Global TIPS），并与3,972家获得TIPS资助的初创企业建立联系，同时提供投资者的推荐意见。此外，该工具还支持与Kakao i OpenBuilder的集成。其主要功能包括：智能的问答系统（支持HyDE、多查询、CRAG等模式）、结构化数据提取技术，以及财务数据匹配功能（Track B）。"
metadata:
  openclaw:
    env:
      - name: GEMINI_API_KEY
        description: "Google Gemini API key (recommended for embeddings + LLM)"
        required: false
      - name: OPENROUTER_API_KEY
        description: "OpenRouter API key (multi-model access)"
        required: false
      - name: ANTHROPIC_API_KEY
        description: "Anthropic Claude API key"
        required: false
      - name: OPENAI_API_KEY
        description: "OpenAI API key"
        required: false
      - name: KAKAO_CALLBACK_SECRET
        description: "Kakao i OpenBuilder webhook HMAC secret (optional)"
        required: false
      - name: RAON_API_URL
        description: "Managed API endpoint (optional, for SaaS mode)"
        required: false
      - name: RAON_API_KEY
        description: "Managed API key (optional, for SaaS mode)"
        required: false
    requires:
      bins: ["python3", "node"]
    notes: "At least one LLM API key (GEMINI, OPENROUTER, ANTHROPIC, or OPENAI) is recommended. Falls back to local Ollama if no keys are set. API keys are stored in ~/.openclaw/.env (user-managed, chmod 600 recommended). The skill includes a local HTTP server (port 8400) and crawlers for public government data collection."
---
# Raon OS — 启动伴侣（v0.7.10）

## 安装要求

- **Python 3.9+**（macOS 已内置，无需额外安装）
- **Node.js 18+**（用于执行 `npx @yeomyeonggeori/raon-os`）
- **LLM API 密钥**（以下选项之一，按优先级排序）：

| 环境变量 | 说明 | 备注 |
|----------|------|------|
| `OPENROUTER_API_KEY` | **优先级1** — 支持所有 OpenClaw 模型 | 推荐 |
| `GEMINI_API_KEY` | **优先级2** — Google Gemini + 嵌入式功能 | |
| `ANTHROPIC_API_KEY` | **优先级3** — Claude | |
| `OPENAI_API_KEY` | **优先级4** — GPT + 嵌入式功能 | |
- **Ollama 本地版** | 无密钥时自动检测 | 可选 — 使用 `raon.sh install-model` 安装 |

- **向量搜索**：如果配置了 `GEMINI_API_KEY` 或 `OPENAI_API_KEY`，则自动启用向量搜索功能；否则使用 BM25 关键词搜索。

## 快速入门

```bash
# 1. OpenClaw 설치
npm install -g openclaw

# 2. 스킬 설치
openclaw skill install @yeomyeonggeori/raon-os

# 3. API 키 설정 (권장: OpenRouter)
echo "OPENROUTER_API_KEY=sk-or-..." >> ~/.openclaw/.env
chmod 600 ~/.openclaw/.env  # 보안: 소유자만 읽기/쓰기

# 4. 모델 override (선택) — 기본은 프로바이더별 최적 모델 자동 선택
echo "RAON_MODEL=anthropic/claude-opus-4-5" >> ~/.openclaw/.env

# 5. 연결 테스트
python3 scripts/raon_llm.py --detect
```

## LLM 配置（`raon_llm.py`）

所有 API 密钥均存储在 `~/.openclaw/.env` 文件中（优先使用环境变量设置）：

```bash
# ~/.openclaw/.env 예시
OPENROUTER_API_KEY=sk-or-v1-xxxx   # 1순위 (추천)
GEMINI_API_KEY=AIzaSy-xxxx          # 2순위 + 임베딩
ANTHROPIC_API_KEY=sk-ant-xxxx       # 3순위
OPENAI_API_KEY=sk-xxxx              # 4순위 + 임베딩
RAON_MODEL=google/gemini-2.5-flash  # 모델 강제 지정 (선택)
RAON_LLM_PROVIDER=openrouter       # 프로바이더 강제 지정 (선택)
```

Raon OS 是一款专为创业团队设计的辅助工具，可帮助您将商业想法转化为实际项目。

## 功能介绍

### 1. **biz-plan** — 商业计划书评估
分析商业计划书（PDF/文本格式），并提供评分及改进建议。

**评估内容：**
- 问题定义与解决方案的适用性
- 市场规模与竞争分析
- 商业模式的合理性
- 团队能力
- 财务规划
- 技术竞争力

**输出结果：** 总分（100分制）+ 各项评分 + 具体改进建议

### 2. **gov-funding** — 政府扶持项目匹配
根据创业团队的资料，推荐合适的政府扶持项目。

**可申请的扶持计划：** TIPS、K-Startup Grand Challenge、创业成长技术开发项目、预备创业包、初期创业包等

### 3. **investor-match** — 投资者匹配（未来版本将实现）
根据创业团队的发展阶段和行业特点，推荐合适的投资者。

```bash
# 투자자 추천
{baseDir}/scripts/raon.sh investor-match --stage "pre-a" --industry "AI" --amount "1M"
```

## PDF 文件处理说明

**重要提示：**  
如果用户直接上传 PDF 文件，文件内容会超出系统允许的token限制。  
**必须先提取文本内容再进行评估。**

**处理流程：**
- 如果 PDF 文件包含 OpenClaw 的附件：  
  1. PDF 文件会被保存到 `media/inbound/` 目录中。  
  2. 请勿直接在命令行中插入 PDF 文件（否则会导致 token 耗尽）。  
  3. 使用 `execute.py --file <文件路径>` 命令进行评估。  
  4. 将评估结果反馈给用户。

## 使用流程

**典型的创业团队使用流程：**

```
1. "내 사업계획서 평가해줘" → biz-plan evaluate
2. "어떻게 고치면 돼?" → biz-plan improve
3. "이걸로 지원할 수 있는 정부사업 있어?" → gov-funding match
4. "TIPS 지원서 초안 만들어줘" → gov-funding draft
5. "투자자도 연결해줘" → investor-match
```

## 投资者匹配功能

**投资者视角的分析：**
从投资者的角度分析商业计划书，并生成投资吸引力报告：  
- **Deal Summary**（1分钟简要总结）  
- **目标投资者类型**（种子轮/Pre-A轮/行业）  
- **投资亮点与风险提示**  
- ** pitching 提示**  

## HTTP API 服务器

支持部署本地 REST API 服务器，以便与 Web 聊天工具或外部服务集成：

**API 端点：**  
- `GET /health` — 系统状态检查  
- `GET /v1/modes` — 支持的模式列表  
- `POST /v1/evaluate` — 商业计划书评估  
- `POST /v1/improve` — 商业计划书优化  
- `POST /v1/match` — 政府扶持项目匹配  
- `POST /v1/draft` — 支持申请草稿（需提供项目信息）  
- `POST /v1/checklist` — 支持申请准备情况检查（需提供项目信息）  
- `POST /v1/investor` — 投资者资料分析  

**请求示例：**  
（具体请求格式请参考相关文档）

**CORS 支持**：支持与 Web 前端系统的跨域请求集成。

## API 集成说明

当前版本采用本地 LLM（基于 RAG 技术）进行评估。  
如需集成 K-Startup AI API，请配置相应的环境变量：

```bash
export RAON_API_URL="https://api.k-startup.ai"
export RAON_API_KEY="your-api-key"
```

如果未配置 API，系统将回退到本地 LLM + RAG 处理流程。

## 评估标准参考

政府扶持项目的评审标准请参考 `references/` 目录下的文件：  
- `references/tips-criteria.md` — TIPS 评审标准  
- `references/gov-programs.md` — 主要政府扶持项目列表及申请要求