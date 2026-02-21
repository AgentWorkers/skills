---
name: raon-os
version: 0.7.10
description: "这是一款专为韩国创业者设计的、由人工智能驱动的创业辅助工具。它能够帮助企业评估商业计划书，匹配政府提供的资金支持计划（如TIPS/DeepTech/Global TIPS），帮助创业者与3,972家获得TIPS资助的初创企业建立联系，获取投资建议，并实现与Kakao i OpenBuilder平台的集成。该工具具备以下功能：智能问答系统（Agentic RAG，包括HyDE、Multi-Query、CRAG），结构化数据提取技术，以及财务数据匹配功能（Track B）。"
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

- **Python 3.9+**（macOS 默认已安装，无需额外安装）
- **Node.js 18+**（用于执行 `npx @yeomyeonggeori/raon-os` 命令）
- **LLM API 密钥**（以下选项之一，按优先级排序）：

| 环境变量 | 说明 | 备注 |
|----------|------|------|
| `OPENROUTER_API_KEY` | **优先级1** — 支持所有 OpenClaw 模型 | 推荐 |
| `GEMINI_API_KEY` | **优先级2** — Google Gemini + 内置模型 | |
| `ANTHROPIC_API_KEY` | **优先级3** — Claude | |
| `OPENAI_API_KEY` | **优先级4** — GPT + 内置模型 | |
- **Ollama 本地模型**：在未设置密钥时自动检测 | 可选 — 使用 `raon.sh install-model` 命令安装 |

- **向量搜索**：如果设置了 `GEMINI_API_KEY` 或 `OPENAI_API_KEY`，则自动启用向量搜索功能；否则将使用 BM25 关键词搜索。

## 快速入门

```bash
# 1. OpenClaw 설치
npm install -g openclaw

# 2. 스킬 설치
openclaw skill install @yeomyeonggeori/raon-os

# 3. API 키 설정 (권장: OpenRouter)
echo "OPENROUTER_API_KEY=your-openrouter-key" >> ~/.openclaw/.env
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
OPENROUTER_API_KEY=<your-key>   # 1순위 (추천)
GEMINI_API_KEY=<your-key>          # 2순위 + 임베딩
ANTHROPIC_API_KEY=<your-key>       # 3순위
OPENAI_API_KEY=<your-key>              # 4순위 + 임베딩
RAON_MODEL=google/gemini-2.5-flash  # 모델 강제 지정 (선택)
RAON_LLM_PROVIDER=openrouter       # 프로바이더 강제 지정 (선택)
```

Raon OS 是一个专为创业团队设计的智能助手，可协助将创意转化为实际业务。

## 功能

### 1. **biz-plan** — 商业计划书评估
分析商业计划书（PDF/文本格式），并提供评分及改进建议。

```bash
# PDF 평가
{baseDir}/scripts/raon.sh biz-plan evaluate --file /path/to/plan.pdf

# 텍스트 평가
{baseDir}/scripts/raon.sh biz-plan evaluate --text "사업 아이디어 설명..."

# JSON 형식 출력
{baseDir}/scripts/raon.sh biz-plan evaluate --file /path/to/plan.pdf --json

# 결과를 파일로 저장
{baseDir}/scripts/raon.sh biz-plan evaluate --file /path/to/plan.pdf --output result.md

# 두 사업계획서 비교 분석
{baseDir}/scripts/raon.sh biz-plan evaluate --file plan_a.pdf --file plan_b.pdf

# 개선안 생성
{baseDir}/scripts/raon.sh biz-plan improve --file /path/to/plan.pdf

# 평가 히스토리 조회
{baseDir}/scripts/raon.sh history
```

**评估内容**：
- 问题定义与解决方案的适用性
- 市场规模与竞争分析
- 商业模式的合理性
- 团队能力
- 财务规划
- 技术竞争力

**输出结果**：总分（100分）+ 各项得分 + 具体改进建议

### 2. **gov-funding** — 政府扶持项目匹配
根据创业团队的资料，推荐合适的政府扶持项目。

```bash
# 매칭 (사업계획서 기반)
{baseDir}/scripts/raon.sh gov-funding match --file /path/to/plan.pdf

# 매칭 (키워드 기반)
{baseDir}/scripts/raon.sh gov-funding match --industry "AI/SaaS" --stage "early" --region "서울"

# 지원사업 상세 정보
{baseDir}/scripts/raon.sh gov-funding info --program "TIPS"

# 지원서 초안 생성
{baseDir}/scripts/raon.sh gov-funding draft --program "TIPS" --file /path/to/plan.pdf

# 지원 준비 체크리스트
{baseDir}/scripts/raon.sh gov-funding checklist --program "TIPS" --file /path/to/plan.pdf
```

**支持项目**：
- TIPS（韩国科技创业支持计划）
- K-Startup 大挑战赛
- 创业成长技术开发项目
- 预创企业支持包
- 初创企业支持包等

### 3. **investor-match** — 投资者匹配（后续功能）
根据创业团队的阶段和行业，推荐合适的投资者。

```bash
# 투자자 추천
{baseDir}/scripts/raon.sh investor-match --stage "pre-a" --industry "AI" --amount "1M"
```

## PDF 处理（重要提示）

**注意**：如果用户直接上传 PDF 文件，可能会导致令牌消耗过快。**必须先提取文本再进行评估**。

**处理流程**：
- 如果 PDF 文件包含 OpenClaw 的附件：
  1. PDF 文件会被保存在 `media/inbound/` 目录中。
  2. **切勿将 PDF 文件直接嵌入到评估请求中**，以避免令牌耗尽。
  3. 使用 `exec` 命令执行 `evaluate.py --file <文件路径>` 进行评估。
  4. 将评估结果反馈给用户。

## 使用流程

**典型的创业团队使用流程**：

```
1. "내 사업계획서 평가해줘" → biz-plan evaluate
2. "어떻게 고치면 돼?" → biz-plan improve
3. "이걸로 지원할 수 있는 정부사업 있어?" → gov-funding match
4. "TIPS 지원서 초안 만들어줘" → gov-funding draft
5. "투자자도 연결해줘" → investor-match
```

## Investor Match**

**从投资者角度分析商业计划书，并生成吸引力分析报告：**
- **交易摘要**（1分钟总结）
- **目标投资者类型**（种子轮/Pre-A 轮/行业）
- **投资亮点与风险提示**
- ** pitching 提示**

## HTTP API 服务器

可以启动本地 REST API 服务器，以便与 Web 聊天工具或其他外部服务集成：

```bash
raon.sh serve           # 기본 포트 8400
raon.sh serve 9000      # 커스텀 포트
```

**API 端点**：
- `GET /health` — 系统健康检查
- `GET /v1/modes` — 支持的模式列表
- `POST /v1/evaluate` — 评估商业计划书
- `POST /v1/improve` — 优化商业计划书
- `POST /v1/match` — 匹配政府扶持项目
- `POST /v1/draft` — 提交扶持申请（需提供项目信息）
- `POST /v1/checklist` — 检查扶持申请准备情况（需提供项目信息）
- `POST /v1/investor` — 分析投资者资料

**请求示例**：
```bash
curl -X POST http://localhost:8400/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"text": "사업계획서 내용..."}'
```

**支持 CORS**（允许 Web 前端进行接口调用）。

## API 集成

当前版本基于本地分析（使用 LLM 和 RAG 技术）。如需集成 K-Startup AI API，请配置相应的环境变量：

```bash
export RAON_API_URL="https://api.k-startup.ai"
export RAON_API_KEY="your-api-key"
```

如果未设置 API，系统会回退到本地 LLM 和 RAG 的处理流程。

## 评估标准参考

有关政府扶持项目的评估标准，请参考 `references/` 目录下的文件：
- `references/tips-criteria.md` — TIPS 评估标准
- `references/gov-programs.md` — 主要政府扶持项目列表及申请条件

---

## ⚠️ 安全性与数据流

### 凭据保护
- 所有 API 密钥均存储在 `~/.openclaw/.env` 文件中（建议设置 `chmod 600` 权限）。
- **请注意**：实际密钥值不会包含在软件包中。

### 数据传输
- **默认模式（本地运行）**：所有数据在本地处理（使用 Ollama LLM 和本地 RAG 系统）。
- **SaaS 模式**（设置 `RAON_API_URL` 时）：评估请求和 PDF 文本会被发送到指定服务器。
  - **仅允许连接到可信的服务器**。
- **Supabase 模式**（设置 `SUPABASE_URL` 时）：反馈数据和使用量数据会存储在该服务器上。
  - **注意**：`SUPABASE_SERVICE_KEY` 是高权限密钥，需谨慎配置。

### 服务器安全
- `/api/keys/*` 端点仅限 **localhost** 使用（管理员专用 API）。
- 如需对外部服务开放，请使用 Nginx 反向代理并进行访问控制。
- **Kakao Webhook**：必须返回 HTTP 200 状态码，以符合 Kakao 平台的要求（防止请求重复发送）。