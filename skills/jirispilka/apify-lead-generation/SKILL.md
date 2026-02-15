---
name: apify-lead-generation
description: 通过抓取谷歌地图、网站、Instagram、TikTok、Facebook、LinkedIn、YouTube和谷歌搜索的结果来生成B2B/B2C潜在客户信息。适用于用户需要寻找潜在客户、建立潜在客户列表、丰富联系人信息或抓取用于销售推广的资料时的场景。
---

# 生成潜在客户（Lead Generation）

使用 Apify Actors 从多个平台抓取潜在客户信息。

## 前提条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6 或更高版本（以支持 `--env-file` 参数）
- `mcpc` CLI 工具（用于获取 Actor 的配置信息）

## 工作流程

请复制此任务清单并跟踪进度：

```
Task Progress:
- [ ] Step 1: Determine lead source (select Actor)
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the lead finder script
- [ ] Step 5: Summarize results
```

### 第一步：确定潜在客户来源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 适用场景 |
|-----------|----------|----------|
| 本地企业 | `compass/crawler-google-places` | 餐厅、健身房、商店等 |
| 联系信息抓取 | `vdrmota/contact-info-scraper` | 从 URL 中提取电子邮件和电话号码 |
| Instagram 账号信息 | `apify/instagram-profile-scraper` | 发现 Instagram 博主 |
| Instagram 帖子/评论 | `apify/instagram-scraper` | 帖子、评论、标签、地点信息 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 发现地点、用户和标签 |
| TikTok 视频/标签 | `clockworks/tiktok-scraper` | 全面提取 TikTok 数据 |
| TikTok 标签/账号信息 | `clockworks/free-tiktok-scraper` | 免费的 TikTok 数据提取工具 |
| TikTok 用户搜索 | `clockworks/tiktok-user-search-scraper` | 通过关键词查找用户 |
| TikTok 账号信息 | `clockworks/tiktok-profile-scraper` | 与 TikTok 创作者联系 |
| TikTok 关注者/被关注者信息 | `clockworks/tiktok-followers-scraper` | 分析受众群体 |
| Facebook 页面 | `apify/facebook-pages-scraper` | 企业联系人信息 |
| Facebook 页面联系人 | `apify/facebook-page-contact-information` | 提取电子邮件、电话号码和地址 |
| Facebook 群组 | `apify/facebook-groups-scraper` | 收集购买意向信息 |
| Facebook 活动 | `apify/facebook-events-scraper` | 用于活动交流和合作 |
| Google 搜索 | `apify/google-search-scraper` | 广泛获取潜在客户信息 |
| YouTube 频道 | `streamers/youtube-scraper` | 与 YouTube 创作者合作 |
| Google 地图中的电子邮件 | `poidata/google-maps-email-extractor` | 直接提取电子邮件地址 |

### 第二步：获取 Actor 的配置信息

使用 `mcpc` 动态获取 Actor 的输入参数和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为实际选择的 Actor（例如：`compass/crawler-google-places`）。

此操作会返回：
- Actor 的描述和 README 文件
- 必需和可选的输入参数
- 可用的输出字段

### 第三步：询问用户偏好

在运行脚本之前，请询问用户以下内容：
1. **输出格式**：
   - **快速响应**：在聊天中显示前几条结果（不保存文件）
   - **CSV**：包含所有字段的完整导出文件
   - **JSON**：以 JSON 格式导出所有数据
2. **结果数量**：根据具体使用场景确定

### 第四步：运行脚本

**快速响应（在聊天中显示结果，不保存文件）：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV 格式导出：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.csv \
  --format csv
```

**JSON 格式导出：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.json \
  --format json
```

### 第五步：总结结果

完成后，请报告以下内容：
- 找到的潜在客户数量
- 文件的位置和名称
- 可用的关键字段
- 建议的下一步操作（如筛选、数据 enrichment）

## 错误处理

- **“APIFY_TOKEN 未找到”**：请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
- **“mcpc 未找到”**：请用户安装 `npm install -g @apify/mcpc`
- **“Actor 未找到”**：请检查 Actor ID 的拼写是否正确
- **“脚本运行失败”**：请用户查看错误输出中的 Apify 控制台链接
- **“超时”**：尝试减小输入数据量或增加 `--timeout` 参数的值