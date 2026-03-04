---
name: skill-guard
description: 在安装 ClawHub 技能之前，使用 Lakera Guard 对这些技能进行扫描，以检测是否存在提示注入（prompt injection）或恶意内容。该扫描功能可以自动在用户尝试安装某项技能时触发，也可以根据需求（通过技能的 slug 或搜索查询）来手动执行，以便对任何技能进行安全审计。
metadata: {"openclaw": {"requires": {"env": ["APIFY_TOKEN", "LAKERA_API_KEY", "OPENCLAW_WEBHOOK_URL", "OPENCLAW_HOOKS_TOKEN"]}, "primaryEnv": "APIFY_TOKEN", "emoji": "🛡️", "homepage": "https://apify.com/numerous_hierarchy/skill-guard-actor"}}
---# SkillGuard  
在技能被安装到您的 OpenClaw 工作区之前，它会扫描 ClawHub 上的技能，以检测是否存在提示注入、越狱尝试或恶意指令。  

## 何时使用此技能  
- 当用户输入“install [技能名称]”、“clawhub install [技能名称]”或“add the [技能名称]”时  
- 当用户请求“scan [技能名称]”、“check [技能名称] 的安全性”或“[技能名称] 安全吗？”时  
- 当用户要求“审计我的技能”或“扫描所有已安装的技能”时  
- 每当您准备从 ClawHub 安装第三方技能时  

## 工作原理  
SkillGuard 会调用一个托管的 Apify 演员（`numerous_hierarchy/skill-guard-actor`，演员 ID：`TMjFBNFqIIUfCBf6K`），该演员执行以下操作：  
1. 从 ClawHub 的公共 API 获取原始的 SKILL.md 文件内容  
2. 将该内容传递给 Lakera Guard 进行提示注入分析  
3. 返回分析结果：`safe`（安全）、`flagged`（被标记为有问题）或 `error`（出现错误），并附上原因说明  

分析结果会通过自定义的 webhook 发送回您的 OpenClaw 代理。  

## 运行该演员  
使用自定义的 webhook 异步触发扫描，并通过 OpenClaw 的钩子端点接收结果：  

### 第一步：构建 webhook 定义  
创建以下 JSON 数组，然后使用 base64 对其进行编码：  
```json
[{
  "eventTypes": ["ACTOR.RUN.SUCCEEDED", "ACTOR.RUN.FAILED"],
  "requestUrl": "$OPENCLAW_WEBHOOK_URL",
  "headersTemplate": "{\"Authorization\": \"Bearer $OPENCLAW_HOOKS_TOKEN\"}",
  "payloadTemplate": "{\"resource\": {{resource}}}"
}]
```  

### 第二步：启动扫描  
使用随附的脚本来完成 webhook 的编码和 API 调用：  
```bash
# Scan by slug
bash {baseDir}/scripts/scan.sh --slug instagram-search

# Scan by search query
bash {baseDir}/scripts/scan.sh --query instagram

# Both (results deduplicated)
bash {baseDir}/scripts/scan.sh --slug instagram-search --query instagram --max 5
```  
该脚本会自动从环境中读取 `APIFY_TOKEN`、`LAKERA_API_KEY`、`OPENCLAW_WEBHOOK_URL` 和 `OPENCLAWHOOKS_TOKEN`。  

**按技能名称扫描：**  
```json
{
  "skillSlugs": ["skill-name-here"],
  "lakeraApiKey": "$LAKERA_API_KEY",
  "maxSkills": 10
}
```  
**按搜索查询扫描：**  
```json
{
  "searchQuery": "instagram",
  "lakeraApiKey": "$LAKERA_API_KEY",
  "maxSkills": 5
}
```  
您可以同时提供 `skillSlugs` 和 `searchQuery`——系统会自动去重处理结果。  

### 第三步：通过 webhook 接收结果  
扫描完成后，OpenClaw 的钩子端点会收到一个 POST 请求，其中包含演员收集的数据集（`resource.defaultDatasetId`）。您可以在以下地址获取这些数据：  
```
GET https://api.apify.com/v2/datasets/{resource.defaultDatasetId}/items
```  

### 结果格式  
数据集中的每个技能都会返回以下信息：  
```json
[
  {
    "slug": "some-skill",
    "name": "Some Skill",
    "author": "username",
    "verdict": "flagged",
    "flagged": true,
    "reasoning": "Flagged by Lakera: prompt_attack, unknown_links",
    "url": "https://clawhub.ai/skills/some-skill",
    "scanned_at": "2026-03-02T19:26:29.666Z"
  }
]
```  

## 如何回应用户：  
### 如果所有技能都通过安全检测（`verdict: "safe"`）：  
告知用户该技能已通过安全扫描，可以继续安装：  
> “✅ [技能名称] 通过了 SkillGuard 的安全检测——未发现提示注入或恶意内容，可以安全安装。”  
然后执行：`clawhub install [技能名称]`  

### 如果有技能被标记为有问题（`verdict: "flagged"`）：  
**不要** 安装该技能，并告知用户：  
> “⚠️ SkillGuard 发现 [技能名称] 存在安全问题。原因：[原因说明]。我不会自动安装该技能。您可以在 [链接] 中手动查看详情并决定是否继续安装。”  
在用户明确确认之前，请不要继续操作。  

### 如果扫描结果为 `error`：  
> “⚠️ SkillGuard 无法扫描 [技能名称]——原因：[错误信息]。请谨慎操作。”  

### 如果同时扫描多个技能：  
首先显示一个汇总表，然后列出所有被标记的技能及其原因。仅安装安全的技能，除非用户明确表示同意继续安装。  

## 示例交互：  
**用户**：“安装 instagram-search 技能。”  
**您**：使用 `skillSlugs: ["instagram-search"]` 启动 SkillGuard 扫描。如果发现有问题，立即停止安装；如果安全，则继续安装。  

**用户**：“扫描所有与 Instagram 相关的技能。”  
**您**：使用 `searchQuery: "instagram"` 启动扫描，并向用户展示每个技能的扫描结果及原因。  

**用户**：“我知道这个技能被标记为有问题，但我还是想安装它。”  
**您**：再次确认用户的决定，然后执行 `clawhub install [技能名称]`，并在回复中注明用户的决定。  

## 所需的环境变量：  
- `APIFY_TOKEN`：您的 Apify API 令牌（在 console.apify.com 获取）  
- `LAKERA_API_KEY`：您的 Lakera Guard API 密钥（在 platform.lakera.ai 获取）  
- `OPENCLAW_WEBHOOK_URL`：您的 OpenClaw 钩子端点地址  
- `OPENCLAWHOOKS_TOKEN`：您的 OpenClaw 钩子认证令牌  

## 首次安装时的处理  
当此技能首次安装并加载时，在回应用户之前，请执行以下操作：  

### 1. 将安装策略写入 TOOLS.md  
将以下内容添加到 `{baseDir}/../../TOOLS.md` 文件中（如果文件尚不存在）：  
```
### ClawHub Install Policy (SkillGuard)
Before running `clawhub install <slug>` for ANY skill, you MUST first run
SkillGuard to scan it. If the scan returns `flagged`, do NOT install and
tell the user why. Only proceed if the user explicitly confirms the override.
```  
使用 bash 命令将内容追加到文件中：  
```bash
cat >> ~/.openclaw/workspace/TOOLS.md << 'EOF'

### ClawHub Install Policy (SkillGuard)
Before running `clawhub install <slug>` for ANY skill, you MUST first run
SkillGuard to scan it. If the scan returns `flagged`, do NOT install and
tell the user why. Only proceed if the user explicitly confirms the override.
EOF
```  

### 2. 通知用户  
在将安装策略写入 TOOLS.md 后，告知用户：  
> “✅ SkillGuard 已成功安装，您的 ClawHub 安装策略已更新至 TOOLS.md。**请立即开始新会话**以激活保护功能——在此之前安装的任何技能将不会被扫描。新会话启动后，所有 `clawhub install` 命令都会自动进行安全检查。”  
在用户确认之前，请勿执行其他操作。  

## 设置与集成  
如果用户需要帮助配置 webhook 端点或 OpenClaw 网关以接收扫描结果，请参考随此技能提供的集成指南：  
`{baseDir}/INTEGRATION.md`  
如果您需要向用户解释任何设置步骤，请自行阅读该指南。