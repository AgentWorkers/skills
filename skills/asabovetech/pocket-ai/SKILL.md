# Pocket AI 技能

**语音录制转录、语义搜索以及跨所有对话的会议智能分析。**

Pocket AI 通过可穿戴设备捕捉您的会议、通话和想法内容，随后对这些内容进行转录并建立索引，以便进行语义搜索。

## 快速参考

| 功能 | 说明 |
|------|-------|
| API 基础地址 | `https://public.heypocketai.com/api/v1` |
| API 密钥 | `~/.config/pocket-ai/api_key` |
| 认证方式 | 承载令牌（Bearer token） |
| 文档 | https://docs.heypocketai.com/docs/api |

## 核心功能

### 1. 语义搜索（最强大的功能）
您可以基于内容的含义而非关键词，在所有录音中进行搜索。

**返回结果：**
- `userProfile.dynamicContext[]` — 从所有录音中提取的人工智能生成的洞察
- `relevantMemories[]` — 匹配的转录内容、待办事项、会议片段
- 说话者身份、时间戳、相关性评分

### 2. 待办事项提取
Pocket AI 会自动从会议中提取待办事项。您可以通过以下方式搜索这些待办事项：

### 3. 标签管理
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/tags"
```

### 4. 录音列表
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings"
```

### 5. 获取录音详情
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings/{recording_id}"
```

### 6. 下载音频
```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/pocket-ai/api_key)" \
  "https://public.heypocketai.com/api/v1/public/recordings/{recording_id}/audio"
```

---

## 高价值查询模式

### 联系人信息
*“与 [某人] 讨论了什么内容？”*
```json
{"query": "conversations with Dylan Acquisition.com"}
{"query": "Adrienne intercompany invoices discussion"}
{"query": "meetings with Charlene"}
```

### 业务决策
*“关于 [某个主题] 做出了哪些决策？”*
```json
{"query": "your company manufacturing team restructuring decisions"}
{"query": "entity streamlining strategy"}
{"query": "trading system rules discussed"}
```

### 待办事项与跟进
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
{"query": "your company staff meeting summary"}
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

### 记忆内容类型
- **转录片段：** `[时间戳] 说话者_XX: 实际说出的内容`
- **待办事项：** `待办事项：执行某项任务`
- **会议片段：** `(开始-结束) 片段标题 - 讨论内容的总结`

---

## 集成点

### Athena（家庭助手）
- 查询会议内容以了解您的日程安排
- “我有空吗？” → 检查最近的录音中是否有繁忙的安排
- 将会议洞察纳入日程决策

### 日报
- 从昨天的会议中提取待办事项
- 总结关键决策
- 标记紧急的待办事项

### 任务管理
- 自动将待办事项作为潜在任务显示
- 与现有的待办列表进行关联
- 跟踪已提及但尚未处理的任务

### 运营渠道
- 将重要决策发布到 #operations 频道
- 对关键讨论（团队变动、财务决策）发出警报

---

## 标签（自定义分类）
当前可用标签：`ai`、`business`、`call`、`economy`、`finance`、`game`、`geopolitics`、`hockey`、`outlook`、`personal`、`sales`、`summary`、`test`、`victory`、`weather`、`work`

使用标签来过滤或分类查询结果。

---

## 心跳检测集成
在系统运行期间，可以选择性地检查是否有新的待办事项：

```python
# Check for recent action items (last 24h)
query = "action items from today"
# Parse response for new follow-ups
# Surface anything urgent
```

---

## 隐私与安全
- 所有录音均采用端到端加密
- 数据存储在美国服务器上
- API 密钥应保存在 `~/.config/pocket-ai/api_key` 文件中
- 绝不将完整转录内容发布到公共渠道

---

## 故障排除

**录音列表为空？**
- 可能需要在访问 API 之前同步设备中的录音数据
- 使用搜索接口（适用于已同步的录音）

**认证错误？**
- 检查承载令牌（Bearer token）的格式：`Authorization: Bearer pk_xxx`
- 确认 `~/.config/pocket-ai/api_key` 文件中的密钥是否正确

**搜索结果为空？**
- 尝试使用更宽泛的查询词
- 检查录音数据是否已同步

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