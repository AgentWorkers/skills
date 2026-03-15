---
name: trello_planner
author: tomas-mikula
web: FrontendAccelerator.com
description: >
  这是一个使用 Trello 官方 Boards API 的只读型 Trello 规划工具。
  🧠 人工智能规划功能：任务优先级排序、冲刺容量评估、看板优化
  📊 分析功能：从 /boards/{id}/* 端点获取列表/卡片/成员信息
  🔍 搜索功能：查询逾期任务、任务分配者以及跨看板的标签信息
  所需权限：TRELLO_API_KEY + TRELLO_TOKEN（读权限）
  可用端点：/1/boards/{id}/lists, /cards, /members（官方规范）
user-invocable: true
install: []
env:
  - TRELLO_API_KEY
  - TRELLO_TOKEN
primary-credential: TRELLO_TOKEN
gating:
  - env: TRELLO_API_KEY
    message: "TRELLO_API_KEY: https://trello.com/app-key"
  - env: TRELLO_TOKEN
    message: "TRELLO_TOKEN: https://trello.com/1/authorize?key=[KEY]&scope=read&expiration=never"
  - binary: node
slash-commands: ["/trello-plan", "/trello-optimize"]
tags: [trello, planner, boards-api]
categories: [productivity, pms]
metadata: {"openclaw":{"emoji":"🗓️","requires":{"env":["TRELLO_API_KEY", "TRELLO_TOKEN"]},"primaryEnv":"TRELLO_TOKEN","homepage":"https://developer.atlassian.com/cloud/trello/rest/api-group-actions/"}}
---
# Trello Planner - 官方看板 API  
[https://developer.atlassian.com/cloud/trello/rest/api-group-boards/](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)  

## 🛠 设置（仅读取权限的令牌）  
```
1. https://trello.com/app-key → API Key
2. https://trello.com/1/authorize?key=[YOUR_KEY]&name=TrelloPlanner&scope=read&expiration=never → Token  
3. Test: https://api.trello.com/1/members/me/boards?key=[KEY]&token=[TOKEN]
```  

## 已验证的 API 端点（看板组）  

| 端点 | 功能 | 参数 | 文档链接 |  
|----------|---------|--------|------|  
| `GET /1/members/me/boards` | 查看用户拥有的看板 | `fields=name,id` | [用户→看板] |  
| `GET /1/boards/{id}/lists` | 查看看板上的列表 | `fields=name,id,closed` | [看板 API] |  
| `GET /1/boards/{id}/cards` | 查看所有卡片 | `fields=name,due,idList,closed` | [看板 API] |  
| `GET /1/boards/{id}/members` | 查看团队成员 | `fields=username,fullName` | [看板 API] |  
| `GET /1/search` | 查找逾期未完成的卡片 | `query="due:<now"` | [搜索 API] |  

## 🚀 使用示例及输出  

**查询示例**: `/trello-plan Engineering`  
```json
{
  "status": "success",
  "data": {
    "board_name": "Engineering Sprint 42",
    "cards_open": 18,
    "overdue_count": 2,
    "planner_insights": ["🚨 PRIORITY: Fix login (overdue 2d)", "⚖️ Review overloaded (8 cards)"],
    "health_score": "🟡 Needs attention"
  }
}
```  

## 注意事项  

**✅ 可以做的事情：**  
- 同时调用 `/boards/{id}/lists`、`cards` 和 `members`  
- 使用 `fields=` 参数进行筛选  
- 结果缓存 30 分钟（看板数据相对稳定）  

**❌ 不应该做的事情：**  
- 写入数据（POST/PUT/DELETE 操作）  
- 请求全部卡片字段（会导致附件加载缓慢）  
- 记录令牌信息（影响安全性）  

## 🧪 测试用例（已验证）  

| 测试内容 | 预期结果 |  
|------|----------|  
| 未提供令牌 | `error_type: "auth"` + 显示设置所需的 URL |  
| 已关闭的卡片 | 被正确地从结果中排除 |  
| 大型看板 | 使用 `limit=100` 可以避免数据量过大 |  
| 超过请求频率限制 | `error_type: "rate_limit"` |  

## 📈 指标说明  
- **健康状况**：逾期/未完成卡片占比 < 15% = 🟢  
- **计划工具洞察**：显示最逾期的卡片及相应的处理建议  
- **容量指标**：显示团队成员数量与未完成卡片的数量比例  

## 🔒 安全性（ClawHub 审批通过）  
```
✅ read scope ONLY
✅ api.trello.com exclusively  
✅ No persistence/file I/O
✅ No token logging/output
✅ 12s timeout
✅ package.json registry aligned
```  

---  
**ClawHub v1.0.8** | tomas-mikula | FrontendAccelerator.com  
---