---
name: agentic-paper-digest-skill
description: 该工具用于获取并汇总最近的arXiv论文和Hugging Face论文，并通过“Agentic Paper Digest”功能对这些论文进行整理。当用户需要论文摘要、最近论文的JSON数据列表，或运行arXiv/Hugging Face相关的处理流程时，可以使用该工具。
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
- 安装 Python 3 并具备网络访问权限。
- 通过 `OPENAI_API_KEY` 访问 OpenAI 模型，或通过 `LITELLM_API_BASE` 和 `LITELLM_API_KEY` 使用 OpenAI 兼容的代理服务。
- 可以使用 `git` 来初始化项目；如果没有 `git`，则可以使用 `curl`/`wget`（或 Python）来下载项目代码。

## 获取代码并安装
- 建议使用初始化辅助脚本。该脚本会在可用时使用 `git`，否则会切换为下载压缩包（zip 文件）。

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

## 运行（可选：使用 API）

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
- 使用 CLI 命令 `--json` 可以输出 `run_id`、`seen`、`kept`、`window_start` 和 `window_end` 等信息。
- 数据存储在 `data/papers.sqlite3` 文件中（位于 `PROJECT_DIR` 目录下）。
- API 支持的接口包括：`POST /api/run`、`GET /api/status`、`GET /api/papers`、`GET/POST /api/topics`、`GET/POST /api/settings`。

## 配置文件
配置文件位于 `PROJECT_DIR/config` 目录下。环境变量可以通过 shell 或 `.env` 文件进行设置。这里的脚本会自动从 `PROJECT_DIR` 目录下加载 `.env` 文件（也可以通过 `ENV_FILE=/path/to/.env` 来覆盖配置文件）。

**环境变量（.env 或外部文件）**
- `OPENAI_API_KEY`：用于访问 OpenAI 模型（litellm 会读取此变量）。
- `LITELLM_API_BASE`、`LITELLM_API_KEY`：指定使用 OpenAI 兼容的代理服务。
- `LITELLM_MODEL_RELEVANCE`、`LITELLM_MODEL_SUMMARY`：用于选择相关性和摘要生成的模型（如果未设置，默认使用相关性模型）。
- `LITELLM_TEMPERATURE_RELEVANCE`、`LITELLM_temPERATURE_SUMMARY`：调整模型的输出确定性。
- `LITELLM_MAX_RETRIES`：LLM 调用的最大重试次数。
- `LITELLM_DROP_PARAMS=1`：忽略不支持的参数以避免代理服务错误。
- `WINDOW_HOURS`、`APP_TZ`：设置结果的时间窗口和时区。
- `ARXIV_CATEGORIES`：以逗号分隔的类别列表（默认包含 `cs.CL,cs.AI,cs.LG,stat.ML,cs.CR`）。
- `ARXIV_API_BASE`、`HF_API_BASE`：用于覆盖源数据的 API 地址。
- `ARXIV_MAX_results`、`ARXIV_PAGE_SIZE`：arXiv 的分页限制。
- `MAX_CANDIDATES_PER_SOURCE`：每个数据源的最大候选论文数量。
- `FETCH_TIMEOUT_S`、`REQUEST_TIMEOUT_S`：数据源获取和每个请求的超时时间。
- `ENABLE_PDF_TEXT=1`：在摘要中包含论文的第一页文本（需要安装 `PyMuPDF`：`pip install pymupdf`）。
- `DATA_DIR`：存储 `papers.sqlite3` 文件的目录。
- `CORS_ORIGINS`：API 服务器允许的来源域名列表（用于 UI）。
- 其他路径配置：`TOPICS_PATH`、`SETTINGS_PATH`、`AFFILIATION_BOOSTS_PATH`。

**配置文件示例**
- `config/topics.json`：包含论文主题的列表，包括 `id`、`label`、`description`、`max_per_topic` 和 `keywords`。相关性分类器必须严格按照这里的格式输出主题 ID。当 `apply_topic_caps=1` 时，`max_per_topic` 也会影响 `GET /api/papers` 的返回结果数量。
- `config/settings.json`：用于修改数据获取的配置参数（如 `arxiv_max_results`、`arxiv_page_size`、`fetch_timeout_s`、`MAX_CANDIDATES_PER_SOURCE`）。可以通过 `POST /api/settings` 更新这些配置。
- `config/affiliations.json`：包含基于子字符串匹配的论文来源权重设置。权重总和不能超过 1.0。请确保文件格式正确（不要在文件末尾添加逗号）。

## 必须遵循的工作流程
1. **首先，请从以下 GitHub 仓库下载配置文件并阅读其中的配置：https://github.com/matanle51/agentic_paper_digest**：
   - 加载 `config/topics.json`、`config/settings.json` 和 `config/affiliations.json`（如果存在的话）。
   - 在请求用户修改配置之前，先了解当前的主题 ID、数量限制等设置。
2. **向用户询问以下配置信息（提供帮助）**：
   - **感兴趣的主题** → 更新 `config/topics.json` 中的主题信息（`topics[].id/label/description/keywords`、`max_per_topic`）。
     显示当前默认值，并询问用户是否需要修改。
   - **时间窗口（小时）** → 设置 `WINDOW_HOURS`（或者通过 `--window-hours` 参数传递给 CLI）；如果用户不关心这个设置，保持默认值 24 小时。
   - **其他配置参数** → 询问用户以下参数，并解释其用途：`ARXIV_CATEGORIES`、`ARXIV_MAX_results`、`ARXIV_PAGE_SIZE`、`MAX_CANDIDATES_PER_SOURCE`。
     显示当前默认值，并询问用户是否需要修改。
   - **模型/代理服务** → 设置 `OPENAI_API_KEY` 或 `LITELLM_API_KEY`（如果使用代理服务，还需设置 `LITELLM_API_BASE`），以及 `LITELLM_MODEL_RELEVANCE`/`LITELLM_MODEL_SUMMARY`。
   - **默认情况下不要询问以下参数**：时区设置、质量与成本的权衡、超时设置、是否包含 PDF 文本、来源偏好设置等。除非用户提出要求，否则使用默认值。
3. **确认工作目录**：询问用户希望将项目克隆或运行的位置。如果用户没有特别要求，默认目录为 `PROJECT_DIR="$HOME/agentic_paper_digest"`。切勿硬编码 `/Users/...` 类型的路径。
4. **初始化项目**：运行初始化脚本（除非项目已经存在且用户表示不需要重新初始化）。
5. **创建或更新 `.env` 文件**：
   - 如果没有 `.env` 文件，可以从仓库中的 `.env.example` 文件创建一个，然后让用户填写必要的配置参数。
   - 在运行程序之前，确保至少设置了 `OPENAI_API_KEY` 或 `LITELLM_API_KEY` 中的一个。
6. **应用配置更改**：
   - 直接编辑 JSON 文件；或者通过 `POST /api/topics` 和 `POST /api/settings` 来更新配置。
7. **运行流程**：
   - 对于一次性生成 JSON 结果的情况，建议使用 `scripts/run_cli.sh` 脚本。
   - 如果用户需要 UI 或 API 接口功能，或者需要轮询任务，可以使用 `scripts/run_api.sh`。
8. **报告结果**：
   - 如果结果数量较少，建议增加 `WINDOW_HOURS`、`ARXIV_MAX_results` 或扩展搜索主题范围。

## 获得良好结果的建议
- 帮助用户明确并确保主题的针对性，以便分类器能够准确选择论文 ID。
- 如果对结果质量有较高要求，可以使用更强大的模型进行摘要生成。
- 如果使用 OpenAI 的模型，建议默认使用 gpt-5-mini 以获得良好的性能平衡。
- 当结果较少时，可以增加 `WINDOW_HOURS` 或 `ARXIV_MAX_results`；如果结果过于杂乱，可以减小这些参数的值。
- 根据研究领域调整 `ARXIV_CATEGORIES` 的设置。
- 如果论文摘要太简短，可以启用 PDF 文本显示功能（`ENABLE_PDF_TEXT=1`）。
- 适当设置来源权重，以平衡搜索结果的相关性和多样性。
- 积极帮助用户调整配置参数，以获得更好的搜索效果！

## 常见问题解决方法
- 如果端口 8000 被占用，可以运行 `bash "{baseDir}/scripts/stop_api.sh` 命令，或者通过 `--port` 参数传递给 API 命令。
- 如果结果为空，可以增加 `WINDOW_HOURS` 的值，或者检查 `.env` 文件中的 API 密钥是否正确。
- 如果出现 API 密钥相关的错误，请在运行程序之前在 shell 中设置 `OPENAI_API_KEY` 或 `LITELLM_API_KEY`。