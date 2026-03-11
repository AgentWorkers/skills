---
name: lunar-calendar-vietnam
version: v1.0.0
description: >
  **农历查询工具**  
  该工具严格遵循越南历法（GMT+7时区）的标准进行日期转换。  
  **核心功能：**  
  - 将公历转换为农历（包含干支历法及越南生肖）  
  - 将农历转换为公历  
  - 提供基本的黄道日期信息  
  - 支持24节气查询  
  **触发条件：**  
  当用户输入“阴历日期”、“农历”、“黄道时刻”、“农历”、“节气”或“越南历法”等相关关键词时，该工具会自动启动。  
  **输出格式：**  
  以JSON数据形式返回查询结果，并附有自然语言的解释说明。
---
<skill_body>
## 🎯 目的（Purpose）
通过 `amlich.js` 库提供专为越南设计的农历计算功能。这一技能对于确保人工智能不会错误地推断日期（尤其是由于越南农历与中国农历的闰月规则不同而容易产生的误差）至关重要。

## ⏰ 适用场景（When to Use）
- ✅ 当用户询问今年春节是哪一天、今天是农历的哪一天，或者需要查询过去的公历日期以获取对应的农历日期时。
- ✅ 当用户需要查看生肖（例如：甲寅年、乙巳年等）或生肖对应的动物（例如：生肖“鼠”对应的是猫）时。
- ✅ 当用户需要了解黄道时辰、吉日或凶日时。
- ❌ 当用户只是简单地询问“今天是星期几”时（这种情况下，可以由大型语言模型（LLM）自行处理，无需调用该工具）。

## 🧠 必须遵循的步骤（Process）
### 第一步：提取日期信息
- 如果用户提供了公历日期，将其转换为 `YYYY-MM-DD` 格式。
- 如果用户询问农历日期，同样将其转换为 `YYYY-MM-DD` 格式。

### 第二步：运行命令行工具（必选，严禁手动计算）
<critical_rule status="最高优先级">
**严禁** 手动计算农历日期，尤其是在闰年期间。务必通过终端来执行计算。
</critical_rule>

使用 bash 或终端运行 `amlich_calculator.js`（建议使用**相对路径**，以便于分享该技能）：
```bash
# Chạy từ thư mục gốc của skill:
cd lunar-calendar-vietnam
node scripts/amlich_calculator.js --solar "2026-02-13"
node scripts/amlich_calculator.js --lunar "2026-01-01"

# Hoặc chạy từ bất kỳ đâu (tự neo theo vị trí SKILL.md):
node "$(dirname \"/path/to/lunar-calendar-vietnam/SKILL.md\")/scripts/amlich_calculator.js" --solar "2026-02-13"
```


### 第三步：查阅参考资料（如需）
如果用户有更深入的疑问：
- 查阅 `references/fortune_rules.md` 以获取更多关于吉日的信息。
- 查阅 `references/solar_terms.md` 以深入了解节气的相关知识。

### 第四步：回复用户
将终端返回的 JSON 结果转换为自然语言，并以咨询性的方式回复用户。
除非用户有特殊的技术需求，否则无需直接输出原始的 XML 数据。

---

## 📌 快速参考（可选）
如果用户希望使用 iOS 应用程序来快速查询万年历或农历信息（但不能替代工具的计算结果），可以推荐以下应用：
- 越南万年历（iOS）：https://apps.apple.com/vn/app/id6757463234
</skill_body>