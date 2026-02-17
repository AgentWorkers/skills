---
name: ucm
description: "AI代理的API市场——通过一个API密钥即可使用100项服务（包括网络搜索、图像生成、代码沙箱、文本转语音（TTS）、NASA数据查询、食谱查询、宝可梦相关服务等，共计90多项服务）。"
homepage: https://github.com/ucmai/skills
metadata: {"openclaw": {"emoji": "🛒", "requires": {"env": ["UCM_API_KEY"], "anyBins": ["curl", "node"]}, "primaryEnv": "UCM_API_KEY", "install": [{"id": "node", "kind": "node", "package": "@ucm/mcp-server", "bins": ["ucm-mcp"], "label": "Install UCM MCP Server (node)"}]}}
---
# UCM — 通用商业市场平台

您可以通过一个API密钥让您的代理访问100项API服务，其中87项服务是完全免费的。

## 设置

### 选项1：MCP服务器（推荐）

如果您的环境支持MCP，请配置UCM MCP服务器：

```json
{
  "mcpServers": {
    "ucm": {
      "command": "npx",
      "args": ["-y", "@ucm/mcp-server@0.3.3"],
      "env": {
        "UCM_API_KEY": "ucm_key_..."
      }
    }
  }
}
```

还没有API密钥？在连接后使用`ucm_register`工具进行注册——该工具会自动为您生成一个API密钥，且无需支付任何费用（仅需1.00美元的免费信用额度）。

### 选项2：HTTP API（适用于所有环境）

```bash
# Register (free)
curl -X POST https://registry.ucm.ai/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-openclaw-agent"}'
# Returns: { "api_key": "ucm_key_...", "credits": { "balance": "1.00" } }
```

将`UCM_API_KEY`保存为环境变量：

```bash
export UCM_API_KEY="ucm_key_..."
```

### 选项3：mcporter

如果您已安装了mcporter，请按照相关说明进行配置：

```bash
mcporter call ucm.ucm_register name=my-agent
mcporter call ucm.ucm_discover query="search the web"
mcporter call ucm.ucm_call service_id=ucm/web-search endpoint=search query="AI news"
```

## 使用方法

### 查找所需服务

根据您的需求找到相应的API服务：

```bash
curl -X POST https://registry.ucm.ai/v1/discover \
  -H "Content-Type: application/json" \
  -d '{"query": "generate an image from text"}'
```

### 调用服务

```bash
curl -X POST https://registry.ucm.ai/v1/call \
  -H "Authorization: Bearer $UCM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "ucm/web-search",
    "endpoint": "search",
    "body": {"query": "OpenClaw tutorials"}
  }'
```

### 查看余额

```bash
curl -H "Authorization: Bearer $UCM_API_KEY" \
  https://registry.ucm.ai/v1/credits
```

## 可用服务（共100项）

### 收费服务（每次调用费用为0.01–0.05美元）

| 服务 | 功能 | 价格 |
|---------|-------------|-------|
| ucm/web-search | 在网络上进行搜索（Tavily） | 0.01美元 |
| ucm/web-scrape | 抓取网页内容（Firecrawl） | 0.02美元 |
| ucm/image-generation | 从文本生成图片（Together AI） | 0.05美元 |
| ucm/code-sandbox | 在沙箱环境中执行代码（E2B） | 0.03美元 |
| ucm/text-to-speech | 将文本转换为音频（Kokoro） | 0.01美元 |
| ucm/speech-to-text | 将音频转录为文本（Whisper） | 0.01美元 |
| ucm/email | 发送电子邮件（Resend） | 0.01美元 |
| ucm/doc-convert | 转换文档格式（Firecrawl） | 0.02美元 |
| ucm/us-stock | 美国股市数据（Finnhub） | 0.01美元 |
| ucm/cn-finance | 中国金融数据（Tushare） | 0.01美元 |
| ucm/translate | 文本翻译（MyMemory） | 0.01美元 |
| ucm/qr-code | 生成二维码 | 0.01美元 |
| ucm/news | 最新新闻（NewsData） | 0.01美元 |

### 免费服务（87项，费用为0.00美元）

- 天气信息 |
- 维基百科 |
- 货币兑换 |
- 国家信息 |
- 假日信息 |
- 字典查询 |
- 书籍查询 |
- 地理编码 |
- 数学计算 |
- IP地址定位 |
- 地址查询 |
- 学术论文 |
- 营养信息 |
- 加密货币价格 |
- 时区信息 |
- 域名查询 |
- Hacker News新闻 |
- 随机数据 |
- 诗歌内容 |
- 电影信息 |
- 单词关联查询 |
- 大学信息 |
- 邮政编码查询 |
- 小知识 |
- 笑话 |
- 建议 |
- 消遣活动建议 |
- 圣经经文 |
- 查克·诺里斯相关内容 |
- 食谱 |
- 鸡尾酒信息 |
- 食品信息 |
- 日出/日落时间查询 |
- 狗的图片 |
- 猫的相关信息 |
- 头像生成 |
- 颜色选择 |
-Lorem Ipsum文本 |
- NASA相关信息 |
- SpaceX信息 |
- 国际空间站（ISS）信息 |
- 太空新闻 |
- arXiv学术论文 |
- 地震信息 |
- 世界银行数据 |
- FDA数据 |
- 碳排放强度信息 |
- 海拔高度信息 |
- 年龄/性别/国籍预测 |
- 英国邮政编码查询 |
- 车辆信息 |
- 纽约大都会艺术博物馆（Met Museum）信息 |
- 芝加哥艺术学院（Art Institute of Chicago）信息 |
- 电视节目信息 |
- 动漫信息 |
- iTunes音乐资源 |
- 广播电台信息 |
- 免费游戏 |
- 游戏优惠信息 |
- 宝可梦相关内容 |
- D&D游戏相关资源 |
- 梗图（memes） |
- ISBN查询 |
- 条形码生成 |
- Wayback Machine网站 |
- npm包管理（npm） |
- PyPI仓库信息 |
- GitHub仓库信息 |
- 国家旗帜信息 |
- 扑克牌信息 |
- 《星球大战》相关内容 |
- xkcd漫画 |
- 《瑞克和莫蒂》（Rick & Morty）相关内容 |
- 诺贝尔奖相关信息 |
- 历史事件信息 |
- 卡尼耶（Kanye）名言 |
- Rust编程语言相关资源 |
- Docker Hub信息 |
- Lichess棋盘游戏信息 |
- 周期表信息 |
- 机场信息 |
- 随机狐狸图片 |

## 安全性与隐私

### 数据流

您的代理发出的所有API请求都会通过UCM注册中心（`registry.ucm.ai`）进行中转，然后由该注册中心将请求转发给第三方服务提供商。您的代理永远不会直接与第三方API进行通信，也不会存储它们的API密钥。

```
Your Agent → registry.ucm.ai → Third-party API (Tavily, Firecrawl, etc.)
```

### 从您的设备传输的数据

| 数据类型 | 目的地 | 用途 |
|---------|-------------|---------|
| API密钥（`ucm_key_...`） | `registry.ucm.ai` | 用于身份验证 |
| 服务调用参数（如搜索查询、URL） | `registry.ucm.ai` → 第三方服务提供商 | 用于执行API请求 |
| 代理名称（注册时提供） | `registry.ucm.ai` | 用于账户识别 |

### 保留在本地的数据

- 您的OpenClaw配置信息及对话历史记录 |
- API调用返回的结果（仅存储在您的代理本地） |
- 本技能文件本身（仅包含使用说明；可选的MCP服务器作为独立进程运行）

### 被调用的外部端点

| 端点 | 调用时机 |
|---------|--------|
| `https://registry.ucm.ai/v1/agents/register` | 一次性注册 |
| `https://registry.ucm.ai/v1/call` | 每次API服务调用时 |
| `https://registry.ucm.ai/v1/discover` | 服务搜索时 |
| `https://registry.ucm.ai/v1/services` | 浏览服务目录时 |
| `https://registry.ucm.ai/v1/credits` | 查看余额时 |

所有数据传输都采用HTTPS协议。此技能不会访问其他外部域名。

### 信任与安全保障

- **无嵌入脚本**：本技能文件仅包含使用说明和HTTP调用示例；可选的MCP服务器（`@ucm/mcp-server`）是一个公开的npm包，在安装前您可以对其进行审计。
- **保护API密钥**：UCM在服务器端管理所有API密钥。
- **记录所有调用日志**：每次API调用都会被记录下来，包括交易ID和时间戳。
- **自动退款**：如果第三方服务出现故障（如5xx、429、422错误），系统会自动退还您的信用额度。
- **费用限制**：系统设置费用上限，防止费用过度支出（初始信用额度为1.00美元）。
- **经过全面测试**：该技能已通过684项安全、认证及功能测试。

## 链接

- 官网：https://ucm.ai
- 文档：https://ucm.ai/docs
- 仪表盘：https://dashboard.ucm.ai
- npm包：https://www.npmjs.com/package/@ucm/mcp-server
- GitHub仓库：https://github.com/ucmai/skills