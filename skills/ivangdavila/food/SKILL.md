---
name: "Food Tracker"
description: "您的智能食物管理系统：能够吸收、分析并整理您所摄入的所有食物成分。"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
---
## 智能食物吸收功能

该功能能够吸收用户输入的任何食物信息，自动对其进行分类，并整理成有用的数据以供分析。

**规则：**
- 自动检测输入类型：餐食照片、营养标签、食谱、菜单或文本
- 提取并整理信息：包括食物名称、份量、食用环境以及可获取的营养成分
- 为所有数据添加标签：#meal、#recipe、#product、#restaurant、#inventory
- 提供分析选项：“需要营养估算吗？”（用户可自行选择是否使用该功能）
- 建立个人数据数据库：保存扫描的营养标签、经常食用的食物以及保存的食谱
- 分析数据：识别食物种类、摄入频率、进食时间规律以及食物之间的关联
- 永久记录用户的饮食限制，并主动提示可能存在的冲突
- 如需详细记录热量摄入情况，请结合使用 `calories` 功能
- 有关每种输入类型的处理方式，请参阅 `processing.md` 文件。

---

## 记忆存储功能

所有用户数据均保存在文件 `~/food/memory.md` 中。

**格式：**
```markdown
### Preferences
<!-- Their food preferences and restrictions. Format: "item: type" -->
<!-- Examples: nuts: allergy, gluten: intolerance, vegetarian: choice -->

### Products
<!-- Scanned/saved products for quick-log. Format: "product: cal/serving" -->
<!-- Examples: Hacendado yogurt: 120/170g, Oatly oat milk: 45/100ml -->

### Patterns
<!-- Detected eating patterns. Format: "pattern" -->
<!-- Examples: breakfast ~8am, snacks after 10pm, eats out Fridays -->

### Places
<!-- Restaurants and spots. Format: "place: notes" -->
<!-- Examples: Noma: loved fermented plum, Local Thai: go-to takeout -->

### Recipes
<!-- Saved recipes. Format: "dish: key info" -->
<!-- Examples: quick hummus: chickpeas+tahini+lemon 5min, Sunday roast: 2h -->
```

---
*如果某个功能尚未收集到数据，该部分将显示为空。请继续输入食物信息，系统会自动进行处理和分类。*

**提供的分析结果：**  
- 每周食物多样性评分  
- 进食时间规律  
- 经常食用的食物  
- 外出就餐的比例  
- 根据用户需求提供营养估算（非医疗建议）