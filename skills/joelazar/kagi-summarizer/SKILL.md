---
name: kagi-summarizer
description: 使用 Kagi 的通用摘要 API 可以对任何 URL 或文本进行摘要生成。该 API 支持多种摘要引擎（包括企业级的高级 Muriel 模型），能够生成带项目符号的要点总结，并支持将输出内容翻译成 28 种语言。当您需要对文章、论文、视频字幕或任何文档进行高质量摘要时，可以使用该工具。
---
# Kagi通用摘要工具

使用[Kagi的通用摘要API](https://help.kagi.com/kagi/api/summarizer.html)对任何URL或文本块进行摘要处理。支持文章、论文、PDF文件、视频字幕、论坛帖子等多种类型的内容。该工具支持多种摘要引擎，并可将输出结果翻译成28种语言。

该工具采用Go语言编写，启动速度快且运行时无需依赖任何外部库。您可以直接下载预编译好的二进制文件，也可以从源代码进行编译。

## 设置

使用该工具前，需要创建一个已启用API访问权限的Kagi账户。请使用与其他kagi-*工具相同的`KAGI_API_KEY`。

1. 在https://kagi.com/signup注册一个账户。
2. 进入“设置” → “高级” → “API门户”（https://kagi.com/settings/api）。
3. 生成API令牌。
4. 在https://kagi.com/settings/billing_api页面完成资金充值。
5. 将以下代码添加到您的shell配置文件（`~/.profile`或`~/.zprofile`）中：
   ```bash
   export KAGI_API_KEY="your-api-key-here"
   ```
6. 查看[安装指南](#installation)以了解如何安装该工具。

## 价格

采用令牌计费方式，按处理的1,000个令牌收费。缓存请求是免费的。

| 计划类型 | 每1,000个令牌的价格 |
|------|---------------------|
| 标准计划（Cecil / Agnes） | **0.030美元** |
| Kagi Ultimate订阅用户 | **0.025美元**（自动生效） |
| Muriel（企业级） | 价格更高——请查看[API定价页面](https://kagi.com/settings?p=api) |

## 使用方法

```bash
# Summarize a URL
{baseDir}/kagi-summarizer.sh https://example.com/article

# Summarize raw text
{baseDir}/kagi-summarizer.sh --text "Paste your article text here..."

# Pipe text from stdin
cat paper.txt | {baseDir}/kagi-summarizer
echo "Long text..." | {baseDir}/kagi-summarizer.sh --type takeaway

# Choose engine
{baseDir}/kagi-summarizer.sh https://arxiv.org/abs/1706.03762 --engine muriel

# Get bullet-point takeaways instead of prose
{baseDir}/kagi-summarizer.sh https://example.com/article --type takeaway

# Translate summary to another language
{baseDir}/kagi-summarizer.sh https://example.com/article --lang DE
{baseDir}/kagi-summarizer.sh https://example.com/article --lang JA

# JSON output
{baseDir}/kagi-summarizer.sh https://example.com/article --json

# Combined options
{baseDir}/kagi-summarizer.sh https://arxiv.org/abs/1706.03762 --engine muriel --type takeaway --lang EN --json
```

### 参数说明

| 参数 | 说明 |
|------|-------------|
| `--text <文本>` | 对原始文本进行摘要处理，而非URL |
| `--engine <引擎名称>` | 使用的摘要引擎（默认为`cecil`） |
| `--type <输出类型>` | 输出格式：`summary`（纯文本）或`takeaway`（项目符号列表） |
| `--lang <语言代码>` | 将输出结果翻译成指定语言（例如`EN`、`DE`、`FR`、`JA`） |
| `--json` | 以JSON格式输出结果 |
| `--no-cache` | 跳过缓存结果 |
| `--timeout <秒>` | HTTP请求超时时间（默认为120秒） |

### 可用的摘要引擎

| 引擎名称 | 描述 |
|--------|-------------|
| `cecil` | 生成简洁、易于理解的摘要（默认引擎） |
| `agnes` | 生成正式、技术性强的摘要 |
| `muriel` | 企业级高级模型，质量最高，但处理速度较慢 |

### 支持的语言代码

常见语言代码：`EN`（英语）· `DE`（德语）· `FR`（法语）· `ES`（西班牙语）· `IT`（意大利语）· `PT`（葡萄牙语）· `JA`（日语）· `KO`（韩语）· `ZH`（简体中文）· `ZH-HANT`（繁体中文）· `RU`（俄语）· `AR`（阿拉伯语）

完整语言代码列表：`BG`（保加利亚语）· `CS`（捷克语）· `DA`（丹麦语）· `DE`（德语）· `EL`（希腊语）· `EN`（英语）· `ES`（西班牙语）· `ET`（爱沙尼亚语）· `FI`（芬兰语）· `FR`（法语）· `HU`（匈牙利语）· `ID`（印度尼西亚语）· `IT`（意大利语）· `JA`（日语）· `KO`（韩语）· `LT`（立陶宛语）· `LV`（拉脱维亚语）· `NB`（挪威语）· `NL`（荷兰语）· `PL`（波兰语）· `PT`（葡萄牙语）· `RO`（罗马尼亚语）· `RU`（俄语）· `SK`（斯洛伐克语）· `SL`（斯洛文尼亚语）· `SV`（瑞典语）· `TR`（土耳其语）· `UK`（英语）· `ZH`（中文）· `ZH-HANT`（繁体中文）

如果未指定语言，输出结果将使用文档原始语言。

## 输出结果

### 默认输出（纯文本）

摘要内容会输出到标准输出（stdout），令牌使用情况和API剩余余额会输出到标准错误输出（stderr）：

```
The paper "Attention Is All You Need" introduces the Transformer architecture,
a novel approach to sequence transduction tasks that relies entirely on
attention mechanisms, dispensing with recurrence and convolutions...

[API Balance: $9.9800 | tokens: 1243]
```

### JSON格式（使用`--json`选项）

```json
{
  "input": "https://arxiv.org/abs/1706.03762",
  "output": "The paper introduces the Transformer...",
  "tokens": 1243,
  "engine": "muriel",
  "type": "takeaway",
  "meta": {
    "id": "abc123",
    "node": "us-east",
    "ms": 4821,
    "api_balance": 9.98
  }
}
```

## 使用场景

- 当您拥有URL或文档，但希望快速获取简洁摘要时，可以使用`kagi-summarizer`。
- 对于研究论文、长篇文章或会议记录等需要结构化摘要的情况，建议使用`--type takeaway`选项。
- 当对摘要质量要求较高时（如长文档、学术论文或技术报告），可以选择`--engine muriel`。
- 如果需要将摘要翻译成其他语言，可以使用`--lang`参数。
- 如果需要从多个来源通过实时网络搜索合成信息，可以使用`kagi-fastgpt`。
- 如果需要原始搜索结果以便进一步分析或比较，可以使用`kagi-search`。

## 安装方法

### 方法一：下载预编译的二进制文件（无需Go语言环境）

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)        ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

TAG=$(curl -fsSL "https://api.github.com/repos/joelazar/kagi-skills/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
BINARY="kagi-summarizer_${TAG}_${OS}_${ARCH}"

mkdir -p {baseDir}/.bin
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/${BINARY}" \
  -o {baseDir}/.bin/kagi-summarizer
chmod +x {baseDir}/.bin/kagi-summarizer

# Verify checksum (recommended)
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/checksums.txt" | \
  grep "${BINARY}" | sha256sum --check
```

预编译的二进制文件适用于Linux和macOS（amd64及arm64架构）以及Windows（amd64架构）。

### 方法二：从源代码编译（需要Go 1.26及以上版本）

```bash
cd {baseDir} && go build -o .bin/kagi-summarizer .
```

或者，您可以直接运行`{baseDir}/kagi-summarizer.sh`。如果系统中已安装Go语言，该脚本会在首次运行时自动完成编译。

该工具没有任何外部依赖项，仅依赖Go标准库。