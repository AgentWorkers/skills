---
name: kagi-fastgpt
description: 您可以通过 Kagi 的 FastGPT API 提出问题，并获得由 AI 合成的答案，这些答案会基于实时的网络搜索结果进行生成。系统会返回带有引用来源的直接答案。当您需要快速且权威的答案时（而非原始的搜索结果），可以使用此功能。
---
# Kagi FastGPT

使用[Kagi的FastGPT API](https://help.kagi.com/kagi/api/fastgpt.html)获取带有引用来源的AI生成答案。FastGPT会在后台执行完整的网页搜索，并将结果整合成简洁的答案——非常适合用于事实性问题、API查询以及当前事件相关的查询。

该工具使用Go语言编写的二进制文件，启动速度快且没有运行时依赖项。该二进制文件可以预先下载，也可以从源代码编译获得。

## 设置

需要一个已启用API访问权限的Kagi账户。使用的`KAGI_API_KEY`与`kagi-search`工具相同。

1. 在https://kagi.com/signup创建一个账户。
2. 转到设置 → 高级 → API门户：https://kagi.com/settings/api
3. 生成API令牌。
4. 在https://kagi.com/settings/billing_api充值资金。
5. 将以下代码添加到您的shell配置文件（`~/.profile`或`~/.zprofile`）中：
   ```bash
   export KAGI_API_KEY="your-api-key-here"
   ```
6. 查看下面的[安装说明](#installation)来安装二进制文件。

## 价格

每次查询费用为1.5美分（1000次查询共计15美元）。缓存后的响应是免费的。

## 使用方法

```bash
{baseDir}/kagi-fastgpt.sh "query"                        # Ask a question (default)
{baseDir}/kagi-fastgpt.sh "query" --json                 # JSON output
{baseDir}/kagi-fastgpt.sh "query" --no-refs              # Answer only, no references
{baseDir}/kagi-fastgpt.sh "query" --no-cache             # Bypass response cache
{baseDir}/kagi-fastgpt.sh "query" --timeout 60           # Custom timeout (default: 30s)
```

### 参数选项

| 参数 | 描述 |
|------|-------------|
| `--json` | 以JSON格式输出结果（详见下文） |
| `--no-refs` | 在文本输出中省略引用信息 |
| `--no-cache` | 跳过缓存结果（适用于时效性强的查询） |
| `--timeout <sec>` | HTTP超时时间（秒，默认值：30秒） |

## 输出结果

### 默认输出（文本格式）

输出整合后的答案，后面会附上编号的参考文献列表：

```
Python 3.11 was released on October 24, 2022 and introduced several improvements...

--- References ---
[1] What's New In Python 3.11 — Python 3.11.3 documentation
    https://docs.python.org/3/whatsnew/3.11.html
    The headline changes in Python 3.11 include significant performance improvements...
[2] ...
```

令牌使用情况和API余额会显示在标准错误输出（stderr）中。

### JSON格式（使用`--json`选项）

返回一个JSON对象，包含以下内容：
- `query`：原始查询内容
- `output`：整合后的答案
- `tokens`：消耗的令牌数量
- `references[]`：一个包含`{ title, url, snippet }`对象的数组
- `meta`：API元数据（`id`, `node`, `ms`）

## 使用场景

- **使用kagi-fastgpt**：当您需要从网页来源直接获取答案时（例如：“上个月发布了X的哪个版本？”、“如何配置Y？”）
- **使用kagi-search**：当您需要原始搜索结果以便自行浏览、比较或提取数据时
- **使用网页浏览器**：当您需要与网页交互或页面内容依赖于JavaScript时

## 安装方法

### 选项A：下载预编译的二进制文件（无需Go语言环境）

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)        ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

TAG=$(curl -fsSL "https://api.github.com/repos/joelazar/kagi-skills/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
BINARY="kagi-fastgpt_${TAG}_${OS}_${ARCH}"

mkdir -p {baseDir}/.bin
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/${BINARY}" \
  -o {baseDir}/.bin/kagi-fastgpt
chmod +x {baseDir}/.bin/kagi-fastgpt

# Verify checksum (recommended)
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/checksums.txt" | \
  grep "${BINARY}" | sha256sum --check
```

预编译的二进制文件适用于Linux和macOS（amd64 + arm64）以及Windows（amd64）系统。

### 选项B：从源代码编译（需要Go 1.26及以上版本）

```bash
cd {baseDir} && go build -o .bin/kagi-fastgpt .
```

或者，您可以直接运行`{baseDir}/kagi-fastgpt.sh`脚本——如果系统中安装了Go语言，该脚本会在首次运行时自动进行编译。

该二进制文件没有外部依赖项，仅依赖Go标准库。