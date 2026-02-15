# safe-web

使用 **PromptGuard** 进行安全的网页内容获取和搜索，并对其进行扫描。

## 状态

✅ 可用

## 目的

在将网页内容返回给 AI 之前，保护系统免受隐藏在网页中的注入攻击。该工具会对网页内容的获取和搜索过程进行安全扫描。

## 安装

需要 [PromptGuard](https://clawhub.ai/seojoonkim/prompt-guard) 以及 Python 相关依赖库：

```bash
# Install PromptGuard first
cd /home/linuxbrew/.openclaw/workspace/skills/prompt-guard
pip3 install --break-system-packages -e .

# Install web dependencies (if not present)
pip3 install --break-system-packages requests beautifulsoup4
```

## 使用方法

### 获取网页内容

获取一个 URL 并扫描其内容：

```bash
# Basic fetch
safe-web fetch https://example.com/article

# Save to file
safe-web fetch https://example.com --output article.txt

# JSON output for automation
safe-web fetch https://example.com --json

# Strict mode (block on MEDIUM)
safe-web fetch https://example.com --strict
```

### 进行网页搜索

搜索网页并扫描搜索结果：

```bash
# Basic search
safe-web search "AI safety research"

# More results
safe-web search "stock market news" --count 10

# JSON output
safe-web search "machine learning" --json
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 - 内容/结果无问题 |
| 1 | 错误（网络问题、解析问题等） |
| 2 | 检测到威胁 - 内容被屏蔽 |

## 配置

### 环境变量

- `BRAVE_API_KEY` - Brave Search 的 API 密钥（可选，用于搜索功能）
  - 可在以下地址获取：https://brave.com/search/api/

### 建立符号链接（推荐）

创建一个系统级的符号链接，以便在任何目录下都能直接使用 `safe-web`：

```bash
sudo ln -s /home/linuxbrew/.openclaw/workspace/skills/safe-web/scripts/safe-web.py /usr/local/bin/safe-web
```

创建符号链接后，无需指定完整路径即可直接使用 `safe-web`。

## 工作原理

### 获取网页内容的过程
1. 使用 `requests` 下载网页内容。
2. 使用 `BeautifulSoup` 提取文本（同时移除脚本和样式）。
3. 使用 PromptGuard 对提取的文本进行扫描。
4. 返回干净的内容，或在检测到威胁时屏蔽相关内容，并附上详细的报告。

### 进行网页搜索的过程
1. 调用 Brave Search API（需要 API 密钥）。
2. 扫描每个搜索结果的标题和描述。
3. 过滤掉可疑的结果。
4. 仅返回干净的结果。

## 安全机制

- **失败处理机制**：如果 PromptGuard 无法加载或扫描失败，工具会报告错误，而不会返回未经验证的内容。
- **内容净化**：在扫描之前会对 HTML 进行解析，并移除脚本和样式，以减少误报。
- **禁止执行**：该工具仅用于获取和扫描网页内容，不会执行其中的 JavaScript 代码或任何命令。

## 示例输出

### 清洁的获取结果
```
Fetching: https://site.com/article
Fetched 1523 characters
Scanning with PromptGuard...

Article content here...
```

### 被屏蔽的内容
```
Fetching: https://suspicious-site.com
Fetched 2048 characters
Scanning with PromptGuard...
============================================================
🛡️  SAFE-WEB SECURITY ALERT
============================================================
Source: https://suspicious-site.com
Severity: CRITICAL
Action: BLOCK_NOTIFY
Patterns Matched: 8

Detected Patterns:
  - instruction_override_en
  - role_manipulation_en
  - system_impersonation_en
============================================================

Content from https://suspicious-site.com has been blocked.
```

### 搜索结果
```
Searching: AI research
Found 5 results, scanning...

Showing 3 clean results:

1. Latest AI Research Papers
   URL: https://arxiv.org/list/ai/recent
   Recent submissions in artificial intelligence...

2. AI Safety Institute
   URL: https://www.safe.ai/
   Research and development for safe AI systems...
```

## 适用场景

- 从不可信的 URL 获取内容时。
- 用于抓取网页数据进行分析时。
- 在将网页结果传递给 AI 处理时。
- 任何可能进入 AI 界面的网页内容。

**注意**：
- 对于以下场景，请使用标准的 `web_fetch`/`web_search` 工具：
  - 来自受信任的、已知安全的域名。
  - 内部文档网站。
  - 明确希望绕过安全扫描的情况。

## 与原生工具的比较

| 功能 | 原生 `web_fetch` | `safe-web` |
|---------|-------------------|------------------|
| 获取 HTML 内容 | ✅ | ✅ |
| 提取文本 | ✅ | ✅ |
| 检查注入攻击 | ❌ | ✅ |
| 输出 JSON 格式 | ✅ | ✅ |
| 保存到文件 | ❌ | ✅ |
| 错误代码 | 0/1 | 0/1/2（表示安全状态） |

## 所需依赖库

- Python 3.8 及以上版本
- [PromptGuard 3.1.0 及以上版本](https://clawhub.ai/seojoonkim/prompt-guard)（需在工作区安装）
- `requests` 库
- `beautifulsoup4` 库
- Brave Search 的 API 密钥（用于搜索功能）

## 限制条件

- 搜索功能需要 Brave Search 的 API 密钥（免费 tier 可用）。
- 该工具不会执行 JavaScript 代码（仅处理静态 HTML）。
- 大型网页在提取文本时可能会被截断。
- 网络超时默认设置为 30 秒。