---
name: medical-triage
description: 根据医疗紧急程度指标，将医疗信息（电子邮件、iMessage）分类为“紧急”、“危急”或“常规”类型。
license: MIT
metadata:
  author: "NAPSTER AI"
  maintainer: "NAPSTER AI"
  openclaw:
    requires:
      bins: []
---
# 医疗分诊

根据紧急程度指标、症状和患者情况，将医疗信息分类为不同的优先级。

## 分类

| 图标 | 分类 | 说明 |
|------|----------|-------------|
| 🔴 | **危急** | 危及生命的症状、紧急关键词、剧烈疼痛 |
| 🟡 | **紧急** | 需要当天处理的症状、症状加重、药物问题 |
| 🟢 | **常规** | 需要跟进的情况、一般性咨询、预约请求 |

## 工作原理

该技能会分析信息内容，包括：
- **紧急关键词**：胸痛、呼吸困难、严重出血等
- **症状的严重程度**：疼痛程度、持续时间、症状的发展情况
- **患者情况**：慢性疾病、正在服用的药物、最近接受的治疗
- **时间紧迫性**：“立即处理”、“症状正在恶化”、“无法等待”

## 输入格式

该技能期望接收一个包含医疗信息的 JSON 数组：

```json
[
  {
    "id": "msg-123",
    "subject": "Chest pain",
    "from": "patient@example.com",
    "date": "2026-02-27T10:30:00Z",
    "body": "I've been having chest pain for the last hour..."
  }
]
```

## 输出格式

返回一个包含分诊结果的 JSON 数组：

```json
[
  {
    "id": "msg-123",
    "category": "critical",
    "reason": "Chest pain mentioned - potential cardiac emergency",
    "confidence": 0.95
  }
]
```

## 使用方式

该技能可通过 OpenClaw 的技能执行 API 以编程方式调用。

## 医疗紧急程度指标

### 危急（🔴）
- 胸痛、压迫感或胸闷
- 呼吸困难或气短
- 严重出血
- 意识丧失
- 中风症状（FAST：面部、手臂、言语、时间）
- 严重过敏反应
- 自杀念头

### 紧急（🟡）
- 高烧（>103°F / 39.4°C）
- 持续性呕吐或腹泻
- 药物副作用
- 慢性疾病恶化
- 中度疼痛（7-8/10）
- 感染迹象（红肿、脓液）
- 心理健康危机

### 常规（🟢）
- 预约请求
- 处方药续药
- 一般性健康咨询
- 稳定状态的病情跟进
- 实验室结果查询
- 轻微症状（<3 天）

## 集成方式

该技能可通过 OpenClaw 命令行界面（CLI）调用：

```bash
openclaw skill run medical-triage --input '[{"id":"msg-1","subject":"...","body":"..."}]' --json
```

或通过编程方式调用：

```typescript
const result = await execFileAsync('openclaw', [
  'skill', 'run', 'medical-triage',
  '--input', JSON.stringify(messages),
  '--json'
]);
```

**推荐模型**：Claude Sonnet 4.5 (`openclaw models set anthropic/claude-sonnet-4-5`)