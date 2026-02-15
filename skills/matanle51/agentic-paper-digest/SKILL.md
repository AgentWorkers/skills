---
name: agentic-paper-digest-skill
description: 该工具用于获取并汇总最近的arXiv和Hugging Face论文，并提供“Agentic Paper Digest”作为摘要。适用于用户需要论文摘要、最近论文的JSON数据流，或运行arXiv/Hugging Face相关流程的场景。
homepage: https://github.com/matanle51/agentic_paper_digest
compatibility: Requires Python 3, network access, and either git or curl/wget for bootstrap. LLM access via OPENAI_API_KEY or LITELLM_API_KEY (OpenAI-compatible).
metadata: {"clawdbot":{"requires":{"anyBins":["python3","python"]}}}
---

# Agentic Paper Digest

## 使用场景
- 从 arXiv 和 Hugging Face 获取最新的论文摘要。
- 为下游代理生成 JSON 格式的输出数据。
- 在需要轮询任务时，运行本地 API 服务器。

## 先决条件
- Python 3 及网络访问权限。
- 通过 `OPENAI_API_KEY` 访问 OpenAI 模型，或通过 `LITELLM_API_BASE` 和 `LITELLM_API_KEY` 访问兼容 OpenAI 的服务提供商。
- 可选：使用 `git` 进行项目初始化；否则可以使用 `curl`/`wget`（或 Python）来下载项目代码库。

## 获取代码并安装
- 建议使用初始化辅助脚本。该脚本会在可用时使用 `git`，否则会切换到 zip 文件下载方式。

```bash
bash "{baseDir}/scripts/bootstrap.sh"
```

- 通过设置 `PROJECT_DIR` 来覆盖克隆路径。

```bash
PROJECT_DIR="$HOME/agentic_paper_digest" bash "{baseDir}/scripts/bootstrap.sh"
```

## 运行（推荐使用 CLI）

```bash
bash "{baseDir}/scripts/run_cli.sh"
```

- 根据需要传递 CLI 参数。

```bash
bash "{baseDir}/scripts/run_cli.sh" --window-hours 24 --sources arxiv,hf
```

## 运行（可选：通过 API）

```bash
bash "{baseDir}/scripts/run_api.sh"
```

- 触发任务并读取结果。

```bash
curl -X POST http://127.0.0.1:8000/api/run
curl http://127.0.0.1:8000/api/status
curl http://127.0.0.1:8000/api/papers
```

- 如有需要，停止 API 服务器。

```bash
bash "{baseDir}/scripts/stop_api.sh"
```

## 输出结果
- 使用 CLI 命令 `--json` 可输出 `run_id`、`seen`、`kept`、`window_start` 和 `window_end`。
- 数据存储在 `data/papers.sqlite3` 文件中（位于 `PROJECT_DIR` 目录下）。
- API 支持的请求方法包括：`POST /api/run`、`GET /api/status`、`GET /api/papers`、`GET/POST /api/topics`、`GET/POST /api/settings`。

## 配置
配置文件位于 `PROJECT_DIR/config` 目录下。环境变量可以通过 shell 或 `.env` 文件进行设置。这里的脚本会自动从 `PROJECT_DIR` 下加载 `.env` 文件（可以通过 `ENV_FILE=/path/to/.env` 来覆盖配置文件）。

**环境变量（.env 文件或环境变量）**
- `OPENAI_API_KEY`：用于 OpenAI 模型（litellm 会读取此变量）。
- `LITELLM_API_BASE`、`LITELLM_API_KEY`：指定使用哪个 OpenAI 兼容的代理或服务提供商。
- `LITELLM_MODEL_RELEVANCE`、`LITELLM_MODEL_SUMMARY`：用于相关性分析和摘要生成的模型（如果未设置，则使用默认的相关性模型）。
- `LITELLM_TEMPERATURE_RELEVANCE`、`LITELLM_TEMPERATURE_SUMMARY`：影响输出结果的确定性；数值越低，结果越确定。
- `LITELLM_MAX_RETRIES`：LLM 调用的最大重试次数。
- `LITELLM_DROP_PARAMS=1`：忽略不支持的参数以避免服务提供商错误。
- `WINDOW_HOURS`、`APP_TZ`：指定时间窗口和时区。
- `ARXIV_CATEGORIES`：以逗号分隔的类别（默认包含 `cs.CL,cs.AI,cs.LG,stat.ML,cs.CR`）。
- `ARXIV_API_BASE`、`HF_API_BASE`：用于指定 arXiv 和 Hugging Face 的 API 端点。
- `ARXIV_MAX-results`、`ARXIV_PAGE_SIZE`：arXiv 的分页限制。
- `MAX_CANDIDATES_PER_SOURCE`：每个来源的最大候选论文数量。
- `FETCH_TIMEOUT_S`、`REQUEST_TIMEOUT_S`：数据获取和每个请求的超时时间。
- `ENABLE_PDF_TEXT=1`：在摘要中包含论文的第一页文本（需要安装 `PyMuPDF`：`pip install pymupdf`）。
- `DATA_DIR`：存储 `papers.sqlite3` 文件的路径。
- `CORS_ORIGINS`：API 服务器允许的来源域名列表（用于 UI）。
- 路径覆盖选项：`TOPICS_PATH`、`SETTINGS_PATH`、`AFFILIATION_BOOSTS_PATH`。

**配置文件**
- `config/topics.json`：包含论文主题的列表，包括 `id`、`label`、`description`、`max_per_topic` 和 `keywords`。相关性分类器必须严格按照这里的定义输出主题 ID。当 `apply_topic_caps=1` 时，`max_per_topic` 也会限制 `GET /api/papers` 请求的结果数量。
- `config/settings.json`：用于修改数据获取的参数（如 `arxiv_max_results`、`arxiv_page_size`、`fetch_timeout_s`、`max_candidates_per_source`）。可以通过 `POST /api/settings` 更新这些配置。
- `config/affiliations.json`：包含基于子字符串匹配的应用权重信息（每个模式的权重之和不超过 1.0）。无效的 JSON 格式会禁用权重设置，请确保文件格式正确（不要在文件末尾添加逗号）。

## 必须遵循的工作流程
1. **读取现有配置**：
   - 加载 `config/topics.json`、`config/settings.json` 和 `config/affiliations.json`（如果存在的话）。
   - 在请求用户修改配置之前，先了解当前的主题 ID、数量限制和获取限制。
2. **根据用户需求调整配置**：
   - **感兴趣的主题** → 更新 `config/topics.json` 中的主题信息（`topics[].id/label/description/keywords`、`max_per_topic`）。
     显示当前默认值，并询问用户是否需要修改。
   - **时间窗口（以小时为单位）** → 仅当用户需要时设置 `WINDOW_HOURS`（或通过 `--window-hours` 参数传递）；否则使用默认值。
   - **搜索范围** → 设置 `ARXIV_CATEGORIES`、`ARXIV_MAX-results`、`ARXIV_PAGE_SIZE`、`MAX_CANDIDATES_PER_SOURCE`。
     询问用户是否需要修改这些设置，并显示当前值。
   - **模型/服务提供商** → 设置 `OPENAI_API_KEY` 或 `LITELLM_API_KEY`（如果使用代理，则还需设置 `LITELLM_API_BASE`），以及 `LITELLM_MODEL_RELEVANCE`/`LITELLM_MODEL_SUMMARY`。
   - **API UI 访问** → 仅当用户明确要求使用不同的 API 端点时设置 `CORS_ORIGINS`。
   - **默认情况下不询问以下参数**：时区、质量与成本的权衡、超时设置、PDF 文本显示、来源偏好设置等。除非用户请求修改，否则使用默认值。
3. **确认工作目录**：询问用户希望将项目克隆或运行的位置。如果用户没有特别要求，默认路径为 `PROJECT_DIR="$HOME/agentic_paper_digest"`。切勿硬编码 `/Users/...` 等路径。
4. **初始化项目代码库**：运行初始化脚本（除非代码库已经存在且用户表示跳过此步骤）。
5. **创建或验证 `.env` 文件**：
   - 如果缺少 `.env` 文件，可以从代码库中的 `.env.example` 文件生成它，然后询问用户填写相关参数和自定义设置。
   - 在运行程序之前，确保至少设置了 `OPENAI_API_KEY` 或 `LITELLM_API_KEY` 中的一个。
6. **应用配置更改**：
   - 直接编辑 JSON 文件（或通过 `POST /api/topics` 和 `POST /api/settings` 来更新配置）。
7. **运行流程**：
   - 对于一次性生成 JSON 结果，建议使用 `scripts/run_cli.sh` 脚本。
   - 仅当用户明确要求使用 UI 或 API 接口、或需要轮询功能时，使用 `scripts/run_api.sh`。
8. **报告结果**：
   - 统计运行结果（`seen`、`kept`、`window` 等指标）。
   - 如果结果数量较少，建议增加 `WINDOW_HOURS`、`ARXIV_MAX_results` 或扩展搜索范围。

## 获得优质结果的建议
- 确保主题范围明确且互斥，以便分类器能够准确选择论文 ID。
- 如果对结果质量有较高要求，可以使用更强大的模型进行摘要生成。
- 当结果较少时，增加 `WINDOW_HOURS` 或 `ARXIV_MAX_results`；如果结果过于杂乱，可以减小这些值。
- 根据研究领域调整 `ARXIV_CATEGORIES` 的设置。
- 如果论文摘要内容过于简短，可以启用 PDF 文本显示功能（`ENABLE_PDF_TEXT=1`）。
- 使用适当的权重来调整排名结果，同时避免影响相关性评估。

## 常见问题解决方法
- 如果端口 8000 被占用，可以运行 `bash "{baseDir}/scripts/stop_api.sh` 命令，或通过 `--port` 参数调整 API 的端口。
- 如果结果为空，可以增加 `WINDOW_HOURS` 值，或检查 `.env` 文件中的 API 密钥是否正确。
- 如果出现 API 密钥错误，可以在运行程序前在 shell 中导出 `OPENAI_API_KEY` 或 `LITELLM_API_KEY`。