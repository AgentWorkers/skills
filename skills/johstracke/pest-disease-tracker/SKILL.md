---
name: pest-disease-tracker
description: **跟踪花园害虫和病害并实施相应的防治措施**  
该工具可用于识别问题、记录防治过程以及监测防治效果，适用于处理花园害虫、植物病害或制定防治计划的情况。  

**安全性说明**：  
文件导出功能仅限于安全目录，确保数据不被未经授权的访问者获取。  

**适用人群**：  
非常适合家庭园艺爱好者及小型农场主，帮助他们有效管理植物的健康状况。
---

# 害虫与疾病追踪器

用于追踪和管理花园中的害虫及疾病，并记录相应的防治措施。

## 快速入门

### 添加害虫或疾病
```bash
pest_tracker.py add --type "pest" --name "aphids" --plants "tomatoes,peppers"
```

### 记录防治措施
```bash
pest_tracker.py treat "<id>" --method "<method>" --product "<product>" --notes "<notes>"
```

### 列出所有问题
```bash
pest_tracker.py list
```

### 查看问题详情
```bash
pest_tracker.py show "<id>"
```

### 搜索问题
```bash
pest_tracker.py search "<query>"
```

### 获取防治建议
```bash
pest_tracker.py recommend "<problem>"
```

### 导出数据
```bash
pest_tracker.py export "<output_file>"
```

## 使用场景

### 害虫识别与追踪
```bash
# Add pest sightings
pest_tracker.py add --type "pest" --name "aphids" --plants "tomatoes" --severity "moderate"
pest_tracker.py add --type "pest" --name "slugs" --plants "lettuce,hostas" --severity "high"

# Get treatment recommendations
pest_tracker.py recommend "aphids"
# Output: Neem oil, insecticidal soap, ladybugs

# Record treatments
pest_tracker.py treat <id> --method "spray" --product "neem oil" --notes "Apply in evening, reapply in 7 days"
pest_tracker.py treat <id> --method "natural" --product "ladybugs" --notes "Released 100 ladybugs"
```

### 疾病管理
```bash
# Add diseases
pest_tracker.py add --type "disease" --name "early blight" --plants "tomatoes" --severity "critical"
pest_tracker.py add --type "disease" --name "powdery mildew" --plants "squash" --severity "moderate"

# Get treatment options
pest_tracker.py recommend "early blight"
# Output: Copper fungicide, remove affected leaves, improve air circulation

# Track treatment effectiveness
pest_tracker.py treat <id> --method "remove" --product "fungicide" --status "effective"
```

### 预防性规划
```bash
# Document common issues in your garden
pest_tracker.py add --type "pest" --name "cucumber beetles" --plants "cucumbers,melons" --severity "low" --notes "Prevent with row covers"

# Set up prevention schedule
pest_tracker.py recommend "cucumber beetles"
# Output: Row covers, beneficial nematodes, crop rotation
```

## 问题类型

### 常见害虫
- **蚜虫**：小型吸汁害虫，会导致新枝条变形
- **蛞蝓**：啃食叶片，并留下黏液痕迹
- **毛虫**：吃掉叶片和果实
- **黄瓜甲虫**：啃食叶片并传播枯萎病
- **日本甲虫**：使叶片变成网状
- **南瓜虫**：刺穿茎部，导致植物枯萎
- **红蜘蛛**：在叶片上结网，并导致叶片出现黄色斑点
- **蓟马**：在叶片上留下疤痕，影响生长
- **白粉虱**：使叶片变黄，并分泌黏性蜜露

### 常见疾病
- **早疫病**：番茄叶片上出现黑色斑点
- **晚疫病**：叶片上出现白色绒毛状物
- **白粉病**：叶片上覆盖白色粉末
- **霜霉病**：叶片上出现黄色斑块和紫色霉斑
- **花端腐烂**：花朵脱落
- **立枯病**：植物枯萎死亡
- **细菌性斑点病**：叶片上出现水渍状斑点
- **炭疽病**：叶片上出现凹陷性病斑

## 防治建议

### 有机/自然防治方法
- **印楝油**：广谱杀虫剂，对有益昆虫安全
- **杀虫皂**：接触性杀虫剂，可杀死软体昆虫
- **硅藻土**：物理性防治方法
- **苏云金杆菌**：针对毛虫的生物防治剂
- **铜基杀菌剂**：用于防治真菌病
- **硫磺杀菌剂**：用于防治白粉病
- **堆肥茶**：增强植物免疫力
- **有益昆虫**：瓢虫、草蛉、寄生蜂
- **物理屏障**：使用防虫罩、防护圈、网罩

### 化学防治方法
- **除虫菊酯**：合成杀虫剂
- **吡虫啉**：内吸性杀虫剂
- **氯噻酮**：广谱杀菌剂
- **代森锰锌**：多效杀菌剂
- **代森锌**：用于种子处理和防治真菌病

**请务必遵循产品标签上的使用说明和安全注意事项。**

## 问题严重程度

| 严重程度 | 描述 | 处理时间表 |
|---------|---------|-----------|
| **轻微** | 仅造成轻微困扰，损害有限 | 7天内处理 |
| **中等** | 损害明显，且正在扩散 | 3-5天内处理 |
| **严重** | 损害严重，影响较大 | 1-2天内处理 |
| **危急** | 植物死亡或作物完全损失 | 立即处理 |

## 示例

### 番茄上的蚜虫爆发
```bash
# Add the problem
pest_tracker.py add --type "pest" --name "aphids" --plants "tomatoes" --severity "high" \
  --notes "Found on new growth, honeydew present"

# Get treatment options
pest_tracker.py recommend "aphids"
# Output: Neem oil, insecticidal soap, ladybugs, strong water spray

# Apply treatment
pest_tracker.py treat <id> --method "spray" --product "neem oil" \
  --notes "Spray every 2-3 days for 2 weeks, apply in evening"
```

### 番茄上的早疫病
```bash
# Add disease
pest_tracker.py add --type "disease" --name "early blight" --plants "tomatoes" --severity "critical" \
  --notes "Found on lower leaves, rainy weather, needs immediate action"

# Get recommendations
pest_tracker.py recommend "early blight"
# Output: Copper fungicide, remove affected leaves, improve air circulation, avoid overhead watering

# Apply treatment
pest_tracker.py treat <id> --method "remove" --product "copper fungicide" \
  --notes "Applied fungicide, removed worst leaves, spaced plants for airflow"
```

### 生菜上的蛞蝓问题
```bash
# Add pest
pest_tracker.py add --type "pest" --name "slugs" --plants "lettuce,hostas" --severity "moderate" \
  --notes "Slime trails visible, holes in leaves"

# Get options
pest_tracker.py recommend "slugs"
# Output: Beer traps, diatomaceous earth, copper tape, beneficial nematodes

# Set up traps
pest_tracker.py treat <id> --method "traps" --product "beer traps" \
  --notes "Set up 5 beer traps around bed, check daily"
```

## 搜索功能

- 按问题名称搜索
- 按类型（害虫/疾病）过滤
- 按受影响植物搜索
- 查看防治历史
- 跟踪防治效果

## 安全性

### 路径验证
`export`函数会验证输出路径，防止恶意写入：
- ✅ 允许的路径：`~/.openclaw/workspace/`、`/tmp/` 和用户主目录
- ❌ 禁止的路径：系统路径（`/etc/`、`/usr/`、`/var/` 等）
- ❌ 禁止的路径：敏感文件（`~/.bashrc`、`~/.ssh` 等）

## 数据存储

- 害虫数据存储在：`~/.openclaw/workspace/pest_tracker_db.json`
- 每个问题记录的信息包括：类型、名称、受影响植物、严重程度、防治措施、状态
- 防治历史包括：方法、产品名称、日期、效果、备注
- 数据采用JSON格式，便于备份或迁移

## 最佳实践

1. **及早识别**：在问题扩散前进行处理
2. **定期监测**：生长季节每天检查植物
3. **采用综合防治方法**：结合多种方法以达到最佳效果
4. **记录防治措施**：记录哪些方法有效，哪些无效
5. **预防为主**：使用物理屏障和有益昆虫减少防治需求
6. **轮换使用防治方法**：防止害虫产生抗药性
7. **严格按照标签说明使用化学药剂**  
8. **改善植物生长环境**：许多害虫在植物生长不良的情况下更容易滋生

## 预防技巧

### 预防害虫
- **轮作**：打破害虫的生命周期
- **使用物理屏障**：防虫罩、网罩、防护圈
- **引入有益昆虫**：如瓢虫、草蛉、螳螂
- **保持花园清洁**：清除可能藏匿害虫的杂物
- **合理种植**：通过伴生种植驱赶害虫

### 预防疾病
- **正确浇水**：避免叶片过湿
- **改善通风**：合理间距种植，定期修剪
- **清洁工具**：在处理不同植物之间对工具进行消毒
- **选择抗病品种**：如果可能的话
- **土壤消毒**：采用太阳能消毒或轮作等方法

## 相关工具

- **植物追踪器**：用于追踪单个植物及其护理计划
- **季节性种植指南**：根据地区推荐种植时间
- **花园布局规划器**：帮助设计合理的种植布局

将这些工具结合使用，实现全面的花园管理！