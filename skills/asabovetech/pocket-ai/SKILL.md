# Pocket AI 技能

**语音记录转录、语义搜索以及全面覆盖所有对话的会议智能分析。**

Pocket AI 通过可穿戴设备捕获 Marc 的会议内容、通话记录以及他的思考内容，随后对这些数据进行处理并建立索引，以便进行语义搜索。

## 快速参考

| 功能 | 说明 |
|------|-------|
| API 基础地址 | `https://public.heypocketai.com/api/v1` |
| API 密钥 | `~/.config/pocket-ai/api_key` |
| 认证方式 | 承载令牌（Bearer token） |
| 文档 | https://docs.heypocketai.com/docs/api |

## 核心功能

### 1. 语义搜索（最强大的功能）
可以基于内容含义而非关键词，在所有记录中进行搜索。

**返回结果：**
- `userProfile.dynamicContext[]` — 从所有记录中提取的人工智能生成的洞察信息
- `relevantMemories[]` — 匹配的转录内容、待办事项以及会议片段
- 说话者识别信息、时间戳、内容相关性评分

### 2. 待办事项提取
Pocket AI 会自动从会议记录中提取待办事项。您可以通过以下方式查询这些待办事项：

### 3. 标签管理
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/tags"
```

### 4. 记录列表
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings"
```

### 5. 获取记录详情
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings/{recording_id}"
```

### 6. 下载音频文件
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings/{recording_id}/audio"
```

---

## 高价值查询模式

### 联系人相关内容
*“与 [某人] 讨论了什么？”*
```json
{"query": "conversations with Dylan Acquisition.com"}
{"query": "Adrienne intercompany invoices discussion"}
{"query": "meetings with Charlene"}
```

### 商业决策
*“关于 [某个主题] 做出了哪些决策？”*
```json
{"query": "Red Run manufacturing team restructuring decisions"}
{"query": "entity streamlining strategy"}
{"query": "trading system rules discussed"}
```

### 待办事项及后续行动
*“需要完成什么任务？”*
```json
{"query": "action items tasks todo follow up"}
{"query": "scheduled meetings upcoming"}
{"query": "things to review or approve"}
```

### 个人见解
*“我关于 [某个主题] 说了什么？”*
```json
{"query": "trading psychology patience discipline"}
{"query": "family financial planning kids college"}
{"query": "team performance frustrations"}
```

### 会议总结
*“[会议类型] 中发生了什么？”*
```json
{"query": "Red Run staff meeting summary"}
{"query": "financial review discussion"}
{"query": "geopolitical analysis conversation"}
```

---

## 响应结构

### 搜索结果
```json
{
  "success": true,
  "data": {
    "userProfile": {
      "dynamicContext": [
        "AI-built insight from recordings...",
        "Another pattern detected..."
      ],
      "staticFacts": []
    },
    "relevantMemories": [
      {
        "content": "Transcript segment or action item...",
        "metadata": {"source": "turbopuffer", "sources": ["transcript_segment", "action_item"]},
        "recordingDate": "2026-01-28 01:16:14",
        "recordingId": "uuid",
        "recordingTitle": "Untitled Recording",
        "relevanceScore": 8.19,
        "speakers": "SPEAKER_00, SPEAKER_01",
        "transcriptionId": "uuid"
      }
    ],
    "total": 8,
    "timing": 490
  }
}
```

### 记录内容类型
- **转录片段：** `[时间戳] 说话者_XX: 实际说出的内容`
- **待办事项：** `待办事项：执行某项任务`
- **会议片段：** `(开始时间-结束时间) 片段标题 - 讨论内容的总结`

---

## 集成点

### Athena（家庭助手）
- 查询会议内容以了解 Marc 的工作负担
- “Marc 有空吗？” → 检查最近的记录中是否包含繁忙的安排
- 将会议洞察信息用于日程安排决策

### 日报功能
- 提取昨天会议中的待办事项
- 总结关键决策
- 标记紧急的后续行动事项

### 任务管理
- 自动将待办事项作为潜在任务显示
- 与现有待办列表进行关联
- 跟踪已提及但尚未处理的任务

### 操作通道
- 将重要决策发布到 #operations 频道
- 对于关键讨论（如团队变动、财务决策）发出警报

---

## 标签（Marc 使用的标签分类）
当前使用的标签：`ai`、`business`、`call`、`economy`、`finance`、`game`、`geopolitics`、`hockey`、`outlook`、`personal`、`sales`、`summary`、`test`、`victory`、`weather`、`work`

您可以使用标签来过滤或分类查询结果。

---

## 心跳功能集成
在心跳检测过程中，可以选择性地检查是否有新的待办事项：

```python
# Check for recent action items (last 24h)
query = "action items from today"
# Parse response for new follow-ups
# Surface anything urgent
```

---

## 隐私与安全
- 所有记录均采用端到端加密方式存储
- 数据存储在美国的服务器上
- API 密钥应保存在 `~/.config/pocket-ai/api_key` 文件中
- 禁止将完整转录内容发布到公共渠道

---

## 故障排除

**记录列表为空？**
- 可能需要在访问 API 之前先同步设备中的记录
- 可以使用搜索接口（适用于已同步的记录）

**认证错误？**
- 检查承载令牌（Bearer token）的格式：`Authorization: Bearer pk_xxx`
- 确认 `~/.config/pocket-ai/api_key` 文件中的密钥是否正确

**搜索结果为空？**
- 尝试使用更宽泛的查询关键词
- 检查记录是否最近已同步

---

## 辅助脚本

### search.sh
```bash
#!/bin/bash
# Usage: ./search.sh "your query"
API_KEY=$(cat ~/.config/pocket-ai/api_key)
curl -s -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$1\"}" \
  "https://public.heypocketai.com/api/v1/public/search"
```

### Python 辅助工具
有关完整的 Python 集成方案，请参阅 `pocket_api.py` 文件。