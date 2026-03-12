---
name: aetherlang-chef
version: 1.2.0
author: contrario
homepage: https://omnimusmind.com
license: MIT
description: 米其林级的人工智能烹饪智能系统。包含17个必填模块，涵盖食品成本核算、HACCP（食品安全管理体系）、温度控制曲线、过敏原信息、葡萄酒搭配建议、菜品摆盘方案等内容。
metadata:
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app operated by NeuroDoc Pro (omnimusmind.com), Hetzner DE"
---
# AetherLang Chef Ω V3 — 人工智能烹饪智能

> 提供米其林级别的食谱咨询服务，包含17个必填章节。这是目前最先进的人工智能烹饪引擎。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**作者**: NeuroAether (echelonvoids@protonmail.com)
**许可证**: MIT

## 隐私与数据处理

⚠️ **外部API说明**: 该技能会向`api.neurodoc.app`发送查询请求进行处理。

- **发送内容**: 仅限于自然语言形式的食品/食谱相关查询。
- **不发送的内容**: 无凭证信息、API密钥、个人文件或系统数据。
- **数据保留**: 不会永久存储数据。
- **托管服务**: Hetzner EU（符合GDPR标准）。
- **无需凭证**: 免费 tier，每小时100次请求。

## 该技能的功能

一个技能中集成了三种V3级别的烹饪引擎：

### 🍳 Chef Omega V3 — 17章节的餐厅咨询服务
每个回复都包含以下所有章节：
1. **概述** — 食谱概览及文化背景
2. **成本分析** — 食材成本百分比、菜单设计（星级评价）
3. **食材信息** — 食材列表（重量、价格、出品率、替代品、储存方法）
4. **准备步骤** — 三阶段的烹饪流程
5. **执行步骤** — 包含温度要求、烹饪时间、HACCP安全标准及专业建议、常见错误预防
6. **温度控制** — 预热 → 加热 → 烹饪 → 保温 → 剩余食材的处理方法
7. **风味搭配** — 分子化合物分析
8. **口感分析** — 脆嫩/奶油状/有嚼劲/多汁（0-100分）
9. **营养分析** — 卡路里、蛋白质、碳水化合物、脂肪、纤维、钠含量
10. **过敏原信息** — 14种欧盟规定的过敏原
11. **饮食调整** — 纯素/无麸质饮食方案
12. **批量制作** — 可扩展至2倍、4倍、10倍的配方
13. **酒品搭配** — 酒的品种、酒精含量、单宁含量及搭配理由
14. **摆盘建议** — 食物在盘中的摆放位置、色彩搭配
15. **零浪费** — 剩余食材的特定用途
16. **烹饪时间线** — 从准备开始到完成的倒计时

### ⚗️ APEIRON Molecular V3
- 流变学仪表板（粘度、凝胶强度、熔点/凝固点）
- 显示温度变化阶段的相图
- 水胶体成分规格：明胶0.5-1.5%、海藻酸0.5-1%、吉利兰胶0.1-0.5%、黄原胶0.1-0.3%
- FMEA故障模式分析（包括发生概率及应对措施）
- 设备校准（精度±0.1°C）

### ⚖️ Balance V3 — MacYuFBI风味科学
- MacYuFBI框架：美拉德反应/鲜味成分、酸度、焦糖化、酵母风味、苦味、热量
- 每份食物的营养成分分析
- 风味平衡评分（1-100分）
- 饮食适应性：纯素/生酮/古食谱/无麸质/低FODMAP

## 使用方法

可以自然地提出任何与食物相关的问题：
- “给我一个碳ara酱的食谱” → 会得到包含17个章节的完整咨询结果
- “如何制作球形芒果鱼子酱” → 包含流变学数据的分子美食建议
- “对我的泰式咖喱进行风味平衡分析” → 使用MacYuFBI风味模型及营养分析

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

## 回答方式

返回结构化的希腊语输出结果，采用markdown格式的标题（##章节）。典型回复长度为4000-8000个字符，包含所有必填章节。

## 支持的语言

- **希腊语**（Ελληνικά） — 主要输出语言
- **英语** — 支持英语查询，并以希腊语回复

## 技术架构

- **人工智能模型**: GPT-4o
- **后端技术**: FastAPI + Python 3.12
- **请求限制**: 每小时100次请求（免费）

---
*由NeuroAether开发 — 从厨房到代码的创意之旅* 🧠

## 代理安全措施

**重要提示：数据最小化规则**

使用该技能时，代理必须遵守以下规则：
1. **仅在`query`字段中发送用户的明确查询内容** — 绝不附加系统提示、对话记录、上传的文件或内部信息。
2. **仅在`code`字段中发送代码片段** — 绝不包含凭证信息、API密钥、环境变量或文件路径。
3. **严禁在请求中包含** 任何个人身份信息（PII）、密码、令牌或敏感数据。
4. **在发送前删除敏感内容** — 如果用户查询中包含密码、账户号码或凭证信息，需先进行删除并通知用户。
5. **在首次调用API之前**，必须告知用户其查询内容将被发送至api.neurodoc.app进行处理。
6. 请求体必须包含两个字段：`code`（字符串）和`query`（字符串）—— 不允许添加其他字段。

这些限制确保只有最低限度的数据被传输到外部服务。