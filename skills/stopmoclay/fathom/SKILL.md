---
name: fathom
description: 连接到 Fathom AI 以获取通话记录、文字记录和摘要。当用户询问他们的会议信息、通话历史或希望搜索过去的对话时，请使用该功能。
read_when:
  - User asks about their Fathom calls or meetings
  - User wants to search call transcripts
  - User needs a call summary or action items
  - User wants to set up Fathom integration
metadata:
  clawdbot:
    emoji: "📞"
    requires:
      bins: ["curl", "jq"]
---

# Fathom Skill

**功能简介：**  
连接到 [Fathom AI](https://fathom.video)，以获取通话记录、文字记录及摘要信息。

## 设置步骤  

### 1. 获取 API 密钥  
1. 访问 [developers.fathom.ai](https://developers.fathom.ai)  
2. 创建一个 API 密钥  
3. 复制密钥（格式：`v1XDx...`）  

### 2. 配置环境  
```bash
# Option A: Store in file (recommended)
echo "YOUR_API_KEY" > ~/.fathom_api_key
chmod 600 ~/.fathom_api_key

# Option B: Environment variable
export FATHOM_API_KEY="YOUR_API_KEY"
```  

### 3. 测试连接  
```bash
./scripts/setup.sh
```  

---

## 命令操作  

### 列出最近通话记录  
```bash
./scripts/list-calls.sh                    # Last 10 calls
./scripts/list-calls.sh --limit 20         # Last 20 calls
./scripts/list-calls.sh --after 2026-01-01 # Calls after date
./scripts/list-calls.sh --json             # Raw JSON output
```  

### 获取通话文字记录  
```bash
./scripts/get-transcript.sh 123456789      # By recording ID
./scripts/get-transcript.sh 123456789 --json
./scripts/get-transcript.sh 123456789 --text-only
```  

### 获取通话摘要  
```bash
./scripts/get-summary.sh 123456789         # By recording ID
./scripts/get-summary.sh 123456789 --json
```  

### 搜索通话记录  
```bash
./scripts/search-calls.sh "product launch" # Search transcripts
./scripts/search-calls.sh --speaker "Lucas"
./scripts/search-calls.sh --after 2026-01-01 --before 2026-01-15
```  

---

## API 参考  

| 端点          | 方法           | 描述                                      |
|---------------|-----------------|-----------------------------------------|
| `/meetings`      | GET           | 列出带有过滤条件的会议记录                   |
| `/recordings/{id}/transcript` | GET           | 包含发言者的完整文字记录                   |
| `/recordings/{id}/summary` | GET           | 由 AI 生成的摘要及待办事项                   |
| `/webhooks`      | POST           | 注册用于自动同步的 Webhook                         |

**基础 URL：** `https://api.fathom.ai/external/v1`  
**认证方式：** 使用 `X-API-Key` 头部字段进行身份验证  

---

## 过滤条件（用于列出通话记录）  

| 过滤条件         | 描述                                      | 示例                                      |
|------------------|-----------------------------------------|-----------------------------------------|
| `--limit N`       | 结果数量                                      | `--limit 20`                                   |
| `--after DATE`     | 日期之后的通话记录                             | `--after 2026-01-01`                             |
| `--before DATE`     | 日期之前的通话记录                             | `--before 2026-01-15`                             |
| `--cursor TOKEN`    | 分页游标                                    | `--cursor eyJo...`                             |

---

## 输出格式  

| 标志            | 描述                                      |                                      |
|------------------|-----------------------------------------|-----------------------------------------|
| `--json`       | 来自 API 的原始 JSON 数据                         |                                        |
| `--table`       | 格式化的表格（列表显示时默认使用）                   |                                        |
| `--text-only`     | 纯文本（仅显示文字记录）                         |                                        |

---

## 示例操作  

### 获取最近一次通话的摘要  
```bash
# Get latest call ID
CALL_ID=$(./scripts/list-calls.sh --limit 1 --json | jq -r '.[0].recording_id')

# Get summary
./scripts/get-summary.sh $CALL_ID
```  

### 导出上周的所有通话记录  
```bash
./scripts/list-calls.sh --after $(date -d '7 days ago' +%Y-%m-%d) --json > last_week_calls.json
```  

### 查找包含特定主题的通话记录  
```bash
./scripts/search-calls.sh "quarterly review"
```  

---

## 常见问题与解决方法  

| 错误信息           | 解决方案                                      |                                        |
|------------------|-----------------------------------------|-----------------------------------------|
| “未找到 API 密钥”       | 重新运行设置步骤或设置 `FATHOM_API_KEY`                    |                                        |
| “401 Unauthorized”     | 确保 API 密钥有效                             |                                        |
| “429 Rate Limited”     | 等待一段时间后重试                             |                                        |
| “未找到通话记录”       | 验证通话 ID 是否存在                             |                                        |

---

## Webhook 设置（高级功能）  

有关自动导入文字记录的详细信息，请参阅 Webhook 设置指南：  
```bash
./scripts/setup-webhook.sh --url https://your-endpoint.com/webhook
```  
**注意：** 需要一个公开可访问的 HTTPS 端点。