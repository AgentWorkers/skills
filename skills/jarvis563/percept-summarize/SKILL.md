# percept-summarize

这是一个自动对话摘要工具，具备实体提取和关系映射功能。

## 功能概述

当对话结束（持续60秒无语音输入）时，Percept会生成一份由AI生成的摘要，其中包含提取出的实体（人物、公司、主题）、待办事项以及它们之间的关系。这些摘要会被存储在本地，并支持搜索。

## 使用场景

- 用户询问“我们讨论了什么？”或“总结一下那次会议的内容”
- 用户需要获取会议记录或对话中的待办事项
- 代理需要获取最近对话的上下文信息

## 使用要求

- 必须安装并运行 **percept-listen** 工具
- 需要通过CLI访问 **OpenClaw代理**（用于进行大型语言模型（LLM）的摘要生成）

## 工作原理

1. 对话结束（达到60秒的静默时间限制）
2. Percept生成带有发言者标签的文字记录
3. 将文字记录发送给OpenClaw进行AI摘要生成
4. 提取实体（人物、组织、主题）及其之间的关系
5. 将摘要和实体信息存储到SQLite数据库中
6. 实体之间通过关系图进行关联（关联方式包括：works_on、client_of、mentioned_with）

## 实体识别机制

Percept采用五层级联方式来识别实体：
1. **精确匹配**（置信度1.0）
2. **模糊匹配**（置信度0.8）——用于处理拼写错误或昵称
3. **上下文/关系图**（置信度0.7）——利用实体之间的关系进行判断
4. **最近提及**（置信度0.6）——最近被提及的实体优先显示
5. **语义搜索**（置信度0.5）——通过LanceDB进行向量相似度比较

## 摘要查询方式

可以通过Percept的仪表板（端口8960）或直接查询SQLite数据库来检索摘要：

```sql
SELECT * FROM conversations WHERE summary LIKE '%action items%' ORDER BY end_time DESC;
```

**全文搜索**（使用FTS5技术）：
```sql
SELECT * FROM utterances_fts WHERE utterances_fts MATCH 'project deadline';
```

## 数据保留策略

- 语音记录：保留30天
- 摘要：保留90天
- 实体关系：保留180天
- 发言者信息：永久保存

## 链接

- **GitHub仓库**：https://github.com/GetPercept/percept