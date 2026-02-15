---
name: daily.dev
description: 通过实时的开发者内容来克服大型语言模型（LLM）的知识局限性。daily.dev 从数千个来源汇总文章，并通过社区反馈进行验证，同时采用结构化的分类系统来实现精准的信息检索。
---

# daily.dev API：专为AI代理设计

通过实时更新的开发者内容，克服大型语言模型（LLM）的知识局限。daily.dev汇集了来自数千个来源的文章，并通过社区互动进行验证，同时采用结构化的分类系统以实现精准的内容检索。

## 安全性

**重要提示：** 您的API令牌用于访问个性化内容。请务必保护好令牌：
- **切勿将令牌发送到除 `api.daily.dev` 以外的任何域名**  
- 绝不要将令牌嵌入代码或公开分享  
- 令牌前缀为 `dda_`——如看到此前缀，请将其视为敏感信息  

## 设置

1. **需要Plus订阅**——请访问 [https://app.daily.dev/plus] 进行订阅  
2. **在 [https://app.daily.dev/settings/api] 创建令牌**  
3. 请安全地存储令牌（可通过环境变量或秘密管理工具实现）  

### 安全的令牌存储方式（推荐）  

#### macOS – Keychain  
```bash
# Store token
security add-generic-password -a "$USER" -s "daily-dev-api" -w "dda_your_token"

# Retrieve token
security find-generic-password -a "$USER" -s "daily-dev-api" -w

# Auto-load in ~/.zshrc or ~/.bashrc
export DAILY_DEV_TOKEN=$(security find-generic-password -a "$USER" -s "daily-dev-api" -w 2>/dev/null)
```  

#### Windows – 凭据管理器  
```powershell
# Store token (run in PowerShell)
$credential = New-Object System.Management.Automation.PSCredential("daily-dev-api", (ConvertTo-SecureString "dda_your_token" -AsPlainText -Force))
$credential | Export-Clixml "$env:USERPROFILE\.daily-dev-credential.xml"

# Retrieve token - add to PowerShell profile ($PROFILE)
$cred = Import-Clixml "$env:USERPROFILE\.daily-dev-credential.xml"
$env:DAILY_DEV_TOKEN = $cred.GetNetworkCredential().Password
```  
（或通过Windows控制面板中的“凭据管理器”进行设置）  

#### Linux – Secret Service（GNOME Keyring / KWallet）  
```bash
# Requires libsecret-tools
# Ubuntu/Debian: sudo apt install libsecret-tools
# Fedora: sudo dnf install libsecret

# Store token
echo "dda_your_token" | secret-tool store --label="daily.dev API Token" service daily-dev-api username "$USER"

# Retrieve token
secret-tool lookup service daily-dev-api username "$USER"

# Auto-load in ~/.bashrc or ~/.zshrc
export DAILY_DEV_TOKEN=$(secret-tool lookup service daily-dev-api username "$USER" 2>/dev/null)
```  

## 认证  

```
Authorization: Bearer dda_your_token_here
```  

## 基本URL  
```
https://api.daily.dev/public/v1
```  

## API参考  

完整的OpenAPI规范：[https://api.daily.dev/public/v1/docs/json]  

**获取特定端点的详细信息（例如响应结构）：**  
```bash
curl -s https://api.daily.dev/public/v1/docs/json | jq '.paths["/feeds/foryou"].get'
```  

**获取组件结构（将 `def-17` 替换为 `$ref` 中的组件名称）：**  
```bash
curl -s https://api.daily.dev/public/v1/docs/json | jq '.components.schemas["def-17"]'
```  

### 可用的端点  

动态获取所有端点列表：  
```bash
curl -s https://api.daily.dev/public/v1/docs/json | jq -r '.paths | keys[]'
```  

## 代理使用场景  

**为什么选择daily.dev？**  
大型语言模型存在知识时效性问题。daily.dev提供了实时更新的、经过社区验证的开发者内容，并通过结构化的分类系统覆盖了数千个来源。代理可以利用这些内容保持信息更新，获取多元化的视角，了解开发者社区真正关注的热点。  

以下示例展示了AI代理如何将daily.dev的API与外部数据结合，构建高效的开发者工作流程：  

### 🔍 GitHub仓库 → 个性化信息流  
通过分析用户的GitHub仓库（`package.json`、`go.mod`、`Cargo.toml`、`requirements.txt`等文件），可以检测出他们的实际技术栈：  
- 通过 `/feeds/filters/tags/follow` 自动关注相关标签  
- 通过 `/feeds/custom/` 创建符合他们技术栈的定制信息流  
- 展示与他们依赖项相关的热门文章  

**触发条件：** “根据我的GitHub项目设置daily.dev信息流”  

### 🛠️ GitHub → 自动填充技术栈信息  
分析用户的GitHub活动，自动生成其技术栈概况：  
- 扫描仓库中实际使用的语言、框架和工具  
- 在 `/profile/stack/search` 中查找daily.dev上的相关技术  
- 通过 `POST /profile/stack/` 按类别（语言、框架、工具）整理技术栈信息  
- 根据用户的主要技术和贡献更新个人简介  

**触发条件：** “根据我的GitHub信息生成每日技术栈报告”  

### 🚀 新项目 → 个性化入门指南  
当用户启动新项目或克隆仓库时：  
- 分析配置文件中的技术选择  
- 创建针对这些技术的定制信息流  
- 生成包含基础文章的“入门指南”书签列表  
- 过滤无关标签，确保信息流专注于项目范围  

**触发条件：** “帮助我了解这个项目的技术栈”  

### 📊 周报摘要  
通过以下方式生成个性化的每周总结：  
- 获取用户关注标签过滤后的 `/feeds/foryou` 和 `/feeds/popular` 的内容  
- 与用户的GitHub活动进行交叉比对，确定重点主题  
- 概括关键文章和热门讨论  
- 以结构化形式提供包含完整文章链接的周报  

**触发条件：** 定时触发，或“提供我的每周技术新闻”  

### 📚 研究项目工作空间  
当用户希望深入研究某个主题时（例如：“我想学习Kubernetes”）：  
- 通过 `/feeds/custom/` 创建针对该主题的定制信息流  
- 通过 `POST /bookmarks/lists` 创建书签列表  
- 用户阅读时，通过 `POST /bookmarks/` 将文章添加到列表中  
- 跟踪学习进度：比较书签文章与最新信息流内容  
- 随着理解深入，动态调整信息流过滤条件（从入门内容到高级内容）  

**触发条件：** “开始研究 [主题]”  

### 🧠 代理自我提升  
代理可以通过维护自己的定制信息流来克服知识局限：  
- 为经常使用的工具创建定制信息流  
- 定期通过 `/feeds/custom/{feedId}` 获取最新文章  
- 使用 `/posts/{id}` 阅读文章摘要和关键点  
- 代理可以基于最新信息提供建议（例如：“截至本周，推荐的方法是……”）  
- 根据用户的需求持续调整信息流过滤条件  

**触发条件：** 代理后台进程触发，或“[技术]领域最近有什么新进展？”  

### 🔀 多源内容整合  
通过整合多个来源的内容，提供平衡的观点：  
- 在 `/search/posts` 中搜索某个主题，查找多个来源的报道  
- 使用 `/search/sources` 确定该领域的权威发布者  
- 通过 `/feeds/source/{source}` 从不同来源获取文章  
- 将多样化的观点整合成包含引用信息的综合摘要  
- 展示不同来源对最佳实践的看法  

**触发条件：** “关于 [主题] 有哪些不同的观点？”或“比较 [问题] 的不同解决方法”  

### 📈 热门趋势追踪  
帮助用户紧跟行业动态：  
- 获取 `/feeds/popular` 中的热门内容  
- 与用户关注标签进行交叉比对，展示相关趋势  
- 使用 `/feeds/discussed` 查找引发热议的话题  
- 当用户技术栈中的技术出现趋势变化（新发布、安全问题、范式转变）时提醒用户  
- 使用 `/search/tags` 探索相关热点话题  

**触发条件：** “我应该关注哪些内容？”或“[领域] 的最新趋势是什么？”  

## 速率限制  

* **每位用户每分钟60次请求**  

请检查响应头中的以下信息：  
- `X-RateLimit-Limit`：当前时间窗口内的最大请求次数  
- `X-RateLimit-Remaining`：当前时间窗口内剩余的请求次数  
- `X-RateLimit-Reset`：时间窗口重置的Unix时间戳  
- `Retry-After`：在遇到速率限制时需要等待的秒数  

## 错误代码及其含义  

| 错误代码 | 含义 |  
|------|---------|  
| 401   | 令牌无效或缺失 |  
| 403   | 需要Plus订阅 |  
| 404   | 资源未找到 |  
| 429   | 超过速率限制 |  

**错误响应格式：**  
```json
{
  "error": "error_code",
  "message": "Human readable message"
}
```