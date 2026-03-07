---
name: talent-scout
description: “挖走竞争对手最优秀的人才：通过 LinkedIn 搜索候选人，利用人工智能对候选人进行排名，然后通过一条命令生成个性化的联系信息（私信）。”
user-invocable: true
allowed-tools: Bash, Read, Write, Glob
argument-hint: "<linkedin-company-people-url> --title <job-title>"
---
# Talent Scout — 竞争对手人才情报

您可以使用 `talent-scout` 命令行工具。该工具会抓取 LinkedIn 上公司的员工页面，根据目标职位进行筛选，利用人工智能对候选人进行排名，并生成个性化的联系信息（DM）以及关于竞争对手团队结构的报告。

## 可用命令

### 1. Full Scout（推荐）
通过一个命令完成抓取、人工智能排名、联系信息生成和 PDF 文件生成。
```bash
talent-scout scout \
  --url "https://www.linkedin.com/company/google/people/" \
  --title "Senior Software Engineer" \
  --output report.json \
  --pdf talent_brief.pdf
```

### 2. Extract Only（仅提取原始数据，不使用人工智能）
```bash
talent-scout extract \
  --url "https://www.linkedin.com/company/stripe/people/" \
  --title "Product Manager" \
  --output raw_candidates.json
```

### 3. Deterministic Only（仅使用确定性方法，不使用人工智能）
```bash
talent-scout scout \
  --url "https://www.linkedin.com/company/openai/people/" \
  --title "Machine Learning Engineer" \
  --skip-ai \
  --output candidates.json
```

### 4. 从现有 JSON 文件生成 PDF
```bash
talent-scout pdf --file report.json --output brief.pdf
```

### 5. 从本地文件运行（跳过抓取步骤）
```bash
talent-scout scout \
  --file raw_candidates.json \
  --title "Senior Software Engineer" \
  --output report.json
```

## 可选参数
- `--limit N` — 最多获取的候选人数量（默认：全部）
- `--skip-ai` — 跳过人工智能排名和联系信息生成
- `--output path.json` — 将报告保存为 JSON 文件
- `--pdf path.pdf` — 生成 PDF 格式的人才报告

## 自动更新（每周一次）

在运行之前，系统会自动检查工具包是否需要更新（每 7 天检查一次）：
```bash
python3 - <<'EOF'
import os, time
from pathlib import Path

repo = Path.home() / "ai-native-toolkit"
stamp = repo / ".last_updated"

if repo.exists():
    last = float(stamp.read_text().strip()) if stamp.exists() else 0
    if time.time() - last > 7 * 86400:
        os.system(f"cd {repo} && git pull --quiet && pip install -e . -q")
        stamp.write_text(str(time.time()))
EOF
```

## 使用说明

1. **检查系统要求**
   - 输入 `which talent-scout`，如果未找到该命令，提示用户运行 `pip install ai-native-toolkit` 或 `pip install -e .`
   - 需要的参数：`APIFY_API_KEY` 以及 `GEMINI_API_KEY`、`OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 中的其中一个。

2. **确定用户的需求**：
   - 输入公司名称和职位名称：`scout --url ... --title ...`
   - 如果用户已有原始 JSON 数据：`scout --file ... --title ...`
   - 如果用户仅需要原始数据：`extract`

3. **询问缺失的信息**：
   - “需要哪个公司的 LinkedIn 人员页面？”（页面地址必须以 `/people/` 结尾）
   - “您目标的是哪个职位？”（例如：“高级软件工程师”）
   - “最多需要多少名候选人？”（可选，对应于 `--limit` 参数）

4. **展示 report.json 文件中的结果**：
   - 执行摘要（1 段）
   - 前 5 名排名最高的候选人（姓名、职位、所在地区、为何是目标人选）
   - 个性化联系信息草稿（可直接发送）
   - 关于竞争对手团队结构的分析

5. **分析完成后生成 PDF 报告**：`talent-scout pdf --file report.json --output brief.pdf`

## 输出结构

JSON 报告包含以下内容：
- `companyUrl` — 被抓取的公司页面 URL
- `targetTitle` — 使用的职位筛选条件
- `totalCandidatesFound` — 找到的匹配员工总数
- `candidates[]` — 经过处理的候选人列表（姓名、职位、所在地区、个人资料链接）
- `top5[]` — 经人工智能排名的前 5 名候选人（包含排名原因和联系建议）
- `outreachDrafts[]` — 个性化的联系信息草稿（主题和内容不超过 300 字）
- `teamInsights[]` — 关于竞争对手的 3-5 条分析信息
- `executiveSummary` — 2-3 句的执行摘要