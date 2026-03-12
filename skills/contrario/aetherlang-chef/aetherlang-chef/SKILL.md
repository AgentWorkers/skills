---
name: aetherlang-chef
description: 米其林级别的烹饪配方与美食分析，内容涵盖从食材选择到菜肴摆盘，以及分子美食学的17个方面（共17个章节）。
version: 1.0.1
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

> 提供米其林级别的食谱咨询服务，包含17个必填部分。这是目前最先进的AI烹饪引擎。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**作者**: NeuroAether (echelonvoids@protonmail.com)
**许可证**: MIT

## 隐私与数据管理

⚠️ **外部API说明**: 该技能会向`api.neurodoc.app`发送请求进行处理。

- **发送内容**: 仅限与食物/食谱相关的自然语言查询。
- **不发送的内容**: 无需发送任何凭证、API密钥、个人文件或系统数据。
- **数据保留**: 数据不会被永久存储。
- **托管服务**: Hetzner EU（符合GDPR标准）。
- **无需凭证**: 免费 tier，每小时100次请求。

> **需要确认**: 在向API发送任何请求之前，需通知用户：
> “此请求将发送到api.neurodoc.app（NeuroDoc Pro，Hetzner DE）。继续吗？(y/n)”
> 仅在使用者明确确认后才能继续。
> 请勿在请求中包含密码、个人数据或机密信息。

## 该技能的功能

一个技能中集成了三种V3级别的烹饪引擎：

### 🍳 Chef Omega V3 — 17个部分的餐厅咨询服务
每个回复都包含以下所有部分：
1. **概述** — 食谱概览及文化背景
2. **成本分析** — 食物成本百分比、菜单设计（星级评估）
3. **食材信息** — 食材列表（重量、价格、出品率、替代品、储存方法）
4. **准备步骤** — 三阶段烹饪流程
5. **执行细节** — 包含温度要求、烹饪时间、HACCP安全规范及常见错误提示
6. **温度控制** — 预热、烹饪、保温等步骤
7. **风味搭配** — 分子化合物分析
8. **口感分析** — 脆嫩度、奶油感、多汁度等（0-100分）
9. **营养分析** — 卡路里、蛋白质、碳水化合物、脂肪、纤维、钠含量
10. **过敏原信息** — 14种欧盟常见过敏原
11. **饮食调整** — 素食/无麸质版本
12. **扩展功能** — 可将食谱量放大2倍、4倍或10倍
13. **酒品搭配** — 指定酒款、酒精浓度、单宁含量及搭配理由
14. **摆盘建议** — 食物摆放位置、色彩搭配
15. **零浪费** — 剩余食材的特定用途
16. **烹饪倒计时** — 从准备开始到完成的倒计时

### ⚗️ APEIRON Molecular V3
- 流变学仪表盘（粘度、凝胶强度、熔点/凝固点）
- 显示温度变化的相图
- 水胶体成分规格：琼脂0.5-1.5%、海藻酸0.5-1%、吉利兰胶0.1-0.5%、黄原胶0.1-0.3%
- FMEA故障模式分析（包括概率和应对措施）
- 设备校准（精度±0.1°C）

### ⚖️ Balance V3 — MacYuFBI风味科学
- MacYuFBI框架：美拉德反应、鲜味成分、酸度、焦糖化、酵母作用等
- 每份食物的营养成分分析
- 风味平衡评分（1-100分）
- 饮食适应性：素食/生酮/古食谱/无麸质

## 使用方法

可以自然地询问任何与食物相关的问题：
- “给我一个碳ara酱的食谱” → 会提供完整的17部分咨询服务
- “如何制作球形芒果鱼子酱” → 包含流变学数据的分子美食建议
- “对我的泰式咖喱进行风味平衡分析” → 结合MacYuFBI风味模型和营养分析

## API详情
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```

### Chef流程
```json
{
  "code": "flow Chef {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Chef: chef cuisine=\"auto\", difficulty=\"medium\", servings=4;\n  output text recipe from Chef;\n}",
  "query": "Your food question here"
}
```

### Molecular流程
```json
{
  "code": "flow Molecular {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Lab: molecular technique=\"auto\";\n  output text result from Lab;\n}",
  "query": "Your molecular gastronomy question here"
}
```

## 回答方式

返回结构化的希腊语输出，使用markdown格式的标题（##部分）。典型回复长度为4000-8000个字符，包含所有必填内容。

## 支持的语言

- **希腊语** (Ελληνικά) — 主要输出语言
- **英语** — 支持英语查询，并以希腊语回复

## 技术架构

- **AI模型**: GPT-4o
- **后端技术**: FastAPI + Python 3.12
- **请求限制**: 每小时100次请求（免费）

---
*由NeuroAether开发 — 从厨房到代码的智慧结晶* 🧠