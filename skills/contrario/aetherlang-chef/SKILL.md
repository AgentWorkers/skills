---
name: aetherlang-chef
description: 米其林级别的烹饪食谱与美食分析，内容涵盖从食材选择到菜肴摆盘，以及分子美食学等17个方面，全部以希腊语呈现。
version: 1.1.0
author: contrario
homepage: https://masterswarm.net
requirements:
  binaries: []
  env: []
metadata:
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app operated by NeuroDoc Pro (same as masterswarm.net), Hetzner DE"
  privacy_policy: https://masterswarm.net
license: MIT
---
# AetherLang Chef Ω V3 — 人工智能烹饪智能

> 提供米其林级别的食谱咨询服务，包含17个必填章节。这是目前最先进的AI烹饪引擎。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT

## 隐私与数据管理

⚠️ **外部API说明**: 该技能会向`api.neurodoc.app`发送查询请求进行处理。

- **发送内容**: 仅限与食物/食谱相关的自然语言查询。
- **不发送的内容**: 无需发送任何凭证、API密钥、个人文件或系统数据。
- **数据存储**: 数据不会被永久保存。
- **托管服务**: Hetzner EU（符合GDPR标准）。
- **免费 tier**: 每小时100次请求。

> **确认要求**: 在向API发送任何请求之前，需通知用户：
> “此操作会将您的查询发送到api.neurodoc.app（NeuroDoc Pro，托管在Hetzner DE）。是否继续？(y/n)”
> 只有在用户明确确认后才能继续执行请求。
> 请勿在查询中包含密码、个人数据或机密信息。

## 该技能的功能

一个技能中集成了三种V3级别的烹饪引擎：

### 🍳 Chef Omega V3 — 17个章节的餐厅咨询服务
每个回复都包含以下所有章节：
1. **ΕΠΙΣΚΟΠΗΣΗ** — 食谱概述及文化背景
2. **ΟΙΚΟΝΟΜΙΚΑ** — 食物成本百分比、菜单设计（星级评价）
3. **ΥΛΙΚΑ** — 食材列表（克数、价格、出品率、替代品、储存方法）
4. **MISE EN PLACE** — 三阶段准备流程
5. **ΒΗΜΑΤΑ ΕΚΤΕΛΕΣΕΣ** — 操作步骤（包含温度、时间、HACCP要求及专业提示）
6. **THERMAL CURVE** — 预热 → 加热 → 烹饪 → 保温 → 最后处理
7. **FLAVOR PAIRING MATRIX** — 风味搭配分析
8. **TEXTURE ARCHITECTURE** — 食物质地（酥脆/奶油状/有嚼劲/多汁）
9. **MacYuFBI 分析** — 8个风味维度（0-100分）
10. **ΔΙΑΤΡΟΠΗΑΝΑ ΑΝΑΛΥΣΗ** — 营养成分（卡路里、蛋白质、碳水化合物、脂肪、纤维、钠）
11. **ΑΛΛΕΡΓΙΟΓΟΝΑ** — 14种欧盟过敏原信息
12. **DIETARY TRANSFORMER** — 素食/无麸质配方调整
13. **SCALING ENGINE** — 食物量放大/缩小公式（×2、×4、×10）
14. **WINE & BEVERAGE PAIRING** — 葡萄酒与饮料的搭配建议（品种、酒精含量、单宁水平）
15. **PLATING BLUEPRINT** — 上菜布局（中心位置、色彩搭配）
16. **零浪费** — 剩余食材的特定用途
17. **KITCHEN TIMELINE** — 前60分钟至烹饪结束的倒计时

### ⚗️ APEIRON Molecular V3
- 流变学仪表盘（粘度、凝胶强度、熔点/凝固点）
- 显示温度变化的相图
- 水胶体成分规格（琼脂0.5-1.5%、海藻酸0.5-1%、吉兰胶0.1-0.5%、黄原胶0.1-0.3%）
- FMEA故障模式分析（包含概率及应对措施）
- 设备校准（精度±0.1°C）

### ⚖️ Balance V3 — MacYuFBI 风味科学
- MacYuFBI框架：美拉德反应/鲜味成分、酸度、焦糖化、酵母、苦味、热量等因素
- 每份食物的营养成分分析
- 风味平衡评分（1-100分）
- 饮食适应性：素食/生酮/古食谱/无麸质

## 使用方法

可以自然地提出任何与食物相关的问题：
- “给我一个碳ara酱的食谱” → 会得到包含17个章节的完整咨询结果
- “如何制作球形芒果鱼子酱” → 包含流变学数据的分子美食建议
- “为我的泰式咖喱进行风味平衡分析” → 结合MacYuFBI风味模型和营养分析

## API详情
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```

### Chef Flow
```json
{
  "code": "flow Chef {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Chef: chef cuisine=\"auto\", difficulty=\"medium\", servings=4;\n  output text recipe from Chef;\n}",
  "query": "Your food question here"
}
```

### Molecular Flow
```json
{
  "code": "flow Molecular {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Lab: molecular technique=\"auto\";\n  output text result from Lab;\n}",
  "query": "Your molecular gastronomy question here"
}
```

## 回复内容

返回结构化的希腊语输出结果，采用markdown格式的标题（##章节）。典型回复长度为4000-8000个字符，包含所有必填章节。

## 支持的语言

- **希腊语** (Ελληνικά) — 主要输出语言
- **英语** — 支持英语查询，并以希腊语回复

## 技术架构

- **AI模型**: GPT-4o
- **后端**: FastAPI + Python 3.12
- **请求限制**: 每小时100次请求（免费）

---
*由NeuroAether开发 — 从厨房到代码的智慧结晶* 🧠