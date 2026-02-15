---
name: apify-lead-generation
description: 通过抓取谷歌地图、网站、Instagram、TikTok、Facebook、LinkedIn、YouTube和谷歌搜索的结果来生成B2B/B2C潜在客户信息。适用于用户需要寻找潜在客户、建立潜在客户列表、丰富联系人信息或抓取用于销售推广的资料的情况。
version: 1.0.1
source: https://github.com/apify/agent-skills
homepage: https://apify.com
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - node
        - mcpc
    primaryEnv: APIFY_TOKEN
    install:
      - kind: node
        package: "@apify/mcpc"
        bins: [mcpc]
---

# 生成潜在客户（Lead Generation）

使用 Apify 的演员（Actors）从多个平台抓取潜在客户信息。

## 先决条件

- 在 OpenClaw 设置中配置了 `APIFY_TOKEN`
- Node.js 20.6 或更高版本
- `mcpc` CLI（通过技能元数据自动安装）

## 输入数据清洗规则

在将任何值替换到 bash 命令中之前，请确保：
- **ACTOR_ID**：必须是技术名称（例如 `owner/actor-name`，由字母、数字、连字符和点组成）或原始 ID（恰好 17 个字母数字字符，例如 `oeiQgfg5fsmIJB7Cn`）。拒绝包含 shell 元字符（`; | & $ ` ( ) { } < > ! \n`）的值。
- **SEARCH_KEYWORDS**：仅接受纯文本单词。拒绝包含 shell 元字符的输入。
- **JSON_INPUT**：必须是有效的 JSON 格式，并且不能包含单引号（请使用转义的双引号）。在使用前验证其结构。
- **输出文件名**：必须符合 `YYYY-MM-DD_descriptive-name.{csv,json}` 的格式。文件名中不能包含路径分隔符（`/`, `..`）、空格或特殊字符。

## 工作流程

请复制此检查清单并跟踪进度：

```
Task Progress:
- [ ] Step 1: Determine lead source (select Actor)
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the lead finder script
- [ ] Step 5: Summarize results
```

### 第一步：确定潜在客户来源

根据用户需求选择合适的演员：

| 用户需求 | 演员 ID | 适用场景 |
|-----------|----------|----------|
| 本地企业 | `compass/crawler-google-places` | 餐厅、健身房、商店 |
| 联系信息获取 | `vdrmota/contact-info-scraper` | 从 URL 中提取电子邮件和电话号码 |
| Instagram 账号信息 | `apify/instagram-profile-scraper` | 发现影响者 |
| Instagram 帖子/评论 | `apify/instagram-scraper` | 帖子、评论、标签、地点信息 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 发现地点、用户和标签 |
| TikTok 视频/标签 | `clockworks/tiktok-scraper` | 全面提取 TikTok 数据 |
| TikTok 标签/账号信息 | `clockworks/free-tiktok-scraper` | 免费的 TikTok 数据提取工具 |
| TikTok 用户搜索 | `clockworks/tiktok-user-search-scraper` | 根据关键词查找用户 |
| TikTok 账号信息 | `clockworks/tiktok-profile-scraper` | 联系创作者 |
| TikTok 关注者/被关注者信息 | `clockworks/tiktok-followers-scraper` | 分析受众 |
| Facebook 页面 | `apify/facebook-pages-scraper` | 企业联系人信息 |
| Facebook 页面联系人 | `apify/facebook-page-contact-information` | 提取电子邮件、电话号码和地址 |
| Facebook 群组 | `apify/facebook-groups-scraper` | 获取购买意向信号 |
| Facebook 活动 | `apify/facebook-events-scraper` | 用于建立联系和合作 |
| Google 搜索 | `apify/google-search-scraper` | 广泛获取潜在客户信息 |
| YouTube 频道 | `streamers/youtube-scraper` | 与创作者建立合作 |
| Google 地图中的电子邮件 | `poidata/google-maps-email-extractor` | 直接提取电子邮件地址 |

### 第二步：获取演员的输入格式

使用 `mcpc` 动态获取所选演员的输入格式和详细信息：

```bash
mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为实际选择的演员名称（例如 `compass/crawler-google-places`）。

这将返回：
- 演员的描述和 README 文件
- 必需和可选的输入参数
- 可用的输出字段

### 第三步：询问用户偏好

在运行脚本之前，请询问用户以下信息：
1. **输出格式**：
   - **快速响应**：在聊天中显示前几条结果（不保存文件）
   - **CSV**：包含所有字段的完整导出文件
   - **JSON**：以 JSON 格式导出所有数据
2. **结果数量**：根据具体使用场景确定

### 第四步：运行脚本

**快速响应（在聊天中显示结果，不保存文件）：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT'
```

**CSV 格式输出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.csv' \
  --format csv
```

**JSON 格式输出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.json' \
  --format json
```

### 第五步：总结结果

完成后，报告以下信息：
- 找到的潜在客户数量
- 文件的位置和名称
- 可用的关键字段
- 建议的下一步操作（如筛选、数据 enrichment）

## 安全性与数据隐私

该技能指导代理选择 Apify 演员，通过 `mcpc` 获取其输入格式并运行抓取任务。所包含的脚本仅与 `api.apify.com` 进行通信，并将输出结果写入当前工作目录下的文件；它不会访问其他系统文件或环境变量。

Apify 演员仅抓取公开可用的数据，不会收集目标平台上公开可见之外的私人或个人身份信息。为确保更高的安全性，您可以通过查询 `https://api.apify.com/v2/acts/:actorId` 来检查演员的权限级别：`LIMITED_PERMISSIONS` 表示演员在受限环境中运行，而 `FULL_PERMISSIONS` 表示具有更广泛的系统访问权限。有关详细信息，请参阅 [Apify 的通用条款和条件](https://docs.apify.com/legal/general-terms-and-conditions)。

## 错误处理

- **未找到 APIFY_TOKEN**：请用户在 OpenClaw 设置中配置 `APIFY_TOKEN`。
- **未找到 mcpc**：运行 `npm install -g @apify/mcpc`。
- **未找到对应的演员**：检查演员 ID 的拼写是否正确。
- **运行失败**：请用户查看错误输出中的 Apify 控制台链接。
- **超时**：减小输入数据量或增加 `--timeout` 参数的值。