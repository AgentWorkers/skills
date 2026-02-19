# AetherLang Chef Ω V3 — 人工智能烹饪智能

> 提供米其林级别的食谱咨询服务，包含17个必填板块。这是目前最先进的AI烹饪引擎。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT

## 隐私与数据处理

⚠️ **外部API说明**: 该功能会向`api.neurodoc.app`发送查询以进行处理。

- **发送内容**: 仅限与食物/食谱相关的自然语言查询
- **不发送内容**: 无需发送任何凭证、API密钥、个人文件或系统数据
- **数据存储**: 数据不会被永久保存
- **托管服务**: Hetzner EU（符合GDPR标准）
- **无需凭证**: 免费 tier，每小时100次请求

## 该功能的功能

一个功能中集成了三种V3版本的烹饪引擎：

### 🍳 Chef Omega V3 — 17个板块的餐厅咨询服务
每个回复都包含以下所有板块：
1. **ΕΠΙΣΚΟΠΗΣΗ** — 食谱概述及文化背景
2. **ΟΙΚΟΝΟΜΙΚΑ** — 食材成本百分比、菜单设计（星级评价）
3. **ΥΛΙΚΑ** — 食材清单（克数、成本、产量百分比、替代品、储存方法）
4. **MISE EN PLACE** — 三阶段烹饪步骤
5. **ΒΗΜΑΤΑ ΕΚΤΕΛΕΣΕΣ** — 烹饪步骤（包含温度、时间、HACCP要求及实用技巧、常见错误）
6. **THERMAL CURVE** — 预热 → 加热 → 烹饪过程 → 保温 → 最后处理
7. **FLAVOR PAIRING MATRIX** — 分子化合物分析
8. **TEXTURE ARCHITECTURE** — 食物口感（酥脆/奶油状/有嚼劲/多汁）
9. **MacYuFBI 分析** — 8个风味维度（0-100分）
10. **ΔΙΑΤΡΟΣΗΑ ΑΝΑΛΥΣΗ** — 热量、蛋白质、碳水化合物、脂肪、纤维、钠含量
11. **ΑΛΛΕΡΓΙΟΓΟΝΑ** — 14种欧盟过敏原信息
12. **DIETARY TRANSFORMER** — 素食/无麸质食谱调整
13. **SCALING ENGINE** — 食材用量放大/缩小公式
14. **WINE & BEVERAGE PAIRING** — 葡萄酒与饮品的搭配建议（具体品种、酒精含量、单宁水平）
15. **PLATING BLUEPRINT** — 菜品摆盘方案（中心位置、色彩搭配）
16. **零浪费** — 剩余食材的再利用建议
17. **KITCHEN TIMELINE** — 厨房操作时间倒计时（60分钟至0分钟）

### ⚗️ APEIRON Molecular V3
- 流变学仪表盘（粘度、凝胶强度、熔点/凝固点）
- 显示温度变化的相图
- 水胶体成分规格：琼脂0.5-1.5%、海藻酸0.5-1%、吉兰胶0.1-0.5%、黄原胶0.1-0.3%
- FMEA故障模式分析（包括发生概率及应对措施）
- 设备校准（精度±0.1°C）

### ⚖️ Balance V3 — MacYuFBI 风味科学
- MacYuFBI框架：美拉德反应/鲜味成分、酸度、焦糖化、酵母作用、苦味、热量
- 每份食物的营养成分分析
- 风味平衡评分（1-100分）
- 饮食适应性：素食/生酮/古食谱/无麸质/低FODMAP

## 使用方法

可以自然地提出任何与食物相关的问题：
- “给我一个碳ara酱的食谱” → 会收到包含17个板块的完整咨询结果
- “如何制作球形芒果鱼子酱” → 包含流变学数据的分子美食建议
- “为我的泰式咖喱进行风味平衡分析” → 结合MacYuFBI风味模型和营养成分分析

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

回复内容采用结构化的希腊语格式，并使用markdown标记（## 板块）。典型回复长度为4000-8000个字符，包含所有必填板块。

## 支持的语言

- **希腊语**（Ελληνικά） — 主要输出语言
- **英语** — 支持英语查询，并以希腊语回复

## 技术架构

- **AI模型**: GPT-4o
- **后端技术**: FastAPI + Python 3.12
- **请求限制**: 每小时100次请求（免费）

---
*由NeuroAether开发 — 从厨房到代码的创意之旅* 🧠