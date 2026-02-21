---
name: wellally-tech
description: 集成数字健康数据源（如 Apple Health、Fitbit、Oura Ring），并与 WellAlly.tech 的知识库进行连接。导入来自外部健康设备的数据，将其转换为本地格式，并根据健康数据推荐相关的 WellAlly.tech 知识库文章。支持 CSV/JSON 格式的导入，提供智能化的文章推荐功能，帮助用户更有效地管理个人健康数据。
allowed-tools: Read, Grep, Glob, Write
---
# WellAlly 数字健康集成

本技能可整合多种数字健康数据源，并连接到 [WellAlly.tech](https://www.wellally.tech/) 知识库，为个人健康管理系统提供数据导入和知识参考服务。

## 核心功能

### 1. 数字健康数据导入
- **Apple Health (HealthKit)**：支持 XML/ZIP 文件导入及解析
- **Fitbit**: 通过 OAuth2 API 进行数据导入（支持 CSV 格式）
- **Oura Ring**: 通过 API v2 同步数据
- **通用数据导入**: 支持 CSV/JSON 文件导入，并支持字段映射

### 2. WellAlly.tech 知识库集成
- **分类文章索引**: 涵盖营养、健身、睡眠、心理健康、慢性病管理等主题
- **智能推荐**: 根据用户健康数据推荐相关文章
- **URL 参考**: 提供直接访问 [WellAlly.tech](https://www.wellally.tech/) 平台的链接

### 3. 数据标准化
- **格式转换**: 将外部数据转换为本地 JSON 格式
- **字段映射**: 智能匹配不同平台的数据字段
- **数据验证**: 确保导入数据的完整性和准确性

### 4. 智能文章推荐
- **健康状况分析**: 基于用户健康数据进行分析
- **相关性匹配**: 推荐与用户健康状况最相关的文章
- **分类导航**: 按健康主题组织知识库文章

## 使用说明

### 触发条件

当用户提及以下场景时，可使用本技能：

**数据导入**：
- ✅ “从 Apple Health 导入我的健康数据”
- ✅ “连接我的 Fitbit 设备”
- ✅ “同步我的 Oura Ring 数据”
- ✅ “导入 CSV 健康数据文件”
- ✅ “如何导入健身追踪器/智能手表的数据”

**知识库查询**：
- ✅ “关于高血压的 WellAlly 平台文章”
- ✅ “推荐一些健康管理阅读材料”
- ✅ “根据我的健康数据推荐文章”
- ✅ “WellAlly 知识库中关于睡眠的文章”
- ✅ “如何改善我的血压（请查阅知识库）”

**数据管理**：
- ✅ “我有哪些健康数据来源”
- ✅ “整合来自不同平台的健康数据”
- ✅ “查看导入的外部数据”

### 执行步骤

#### 第一步：识别用户意图
确定用户的需求：
1. **导入数据**: 从外部健康平台导入数据
2. **查询知识库**: 查找 [WellAlly.tech](https://www.wellally.tech/) 相关文章
3. **获取推荐**: 根据健康数据推荐文章
4. **数据管理**: 查看或管理导入的外部数据

#### 第二步：数据导入流程
如果用户需要导入数据：
**2.1 确定数据来源**
```javascript
const dataSource = identifySource(userInput);
// Possible returns: "apple-health", "fitbit", "oura", "generic-csv", "generic-json"
```

**2.2 读取外部数据**
根据数据来源类型使用相应的导入脚本：
```javascript
// Apple Health
const appleHealthData = readAppleHealthExport(exportPath);

// Fitbit
const fitbitData = fetchFitbitData(dateRange);

// Oura Ring
const ouraData = fetchOuraData(dateRange);

// Generic CSV/JSON
const genericData = readGenericFile(filePath, mappingConfig);
```

**2.3 数据映射与转换**
将外部数据转换为本地格式：
```javascript
// Example: Apple Health steps mapping
function mapAppleHealthSteps(appleRecord) {
  return {
    date: formatDateTime(appleRecord.startDate),
    steps: parseInt(appleRecord.value),
    source: "Apple Health",
    device: appleRecord.sourceName
  };
}

// Save to local file
saveToLocalFile("data/fitness/activities.json", mappedData);
```

**2.4 数据验证**
```javascript
function validateImportedData(data) {
  // Check required fields
  // Validate data types
  // Check data ranges
  // Ensure correct time format

  return {
    valid: true,
    errors: [],
    warnings: []
  };
}
```

**2.5 生成导入报告**
```javascript
const importReport = {
  source: dataSource,
  import_date: new Date().toISOString(),
  records_imported: {
    steps: 1234,
    weight: 30,
    heart_rate: 1200,
    sleep: 90
  },
  date_range: {
    start: "2025-01-01",
    end: "2025-01-22"
  },
  validation: validationResults
};
```

#### 第三步：知识库查询流程
如果用户需要查询知识库：
**3.1 确定查询主题**
```javascript
const topic = identifyTopic(userInput);
// Possible returns: "nutrition", "fitness", "sleep", "mental-health", "chronic-disease", "hypertension", "diabetes", etc.
```

**3.2 查找相关文章**
从知识库索引中查找相关文章：
```javascript
function searchKnowledgeBase(topic) {
  // Read knowledge base index
  const kbIndex = readFile('.claude/skills/wellally-tech/knowledge-base/index.md');

  // Find matching articles
  const articles = kbIndex.categories.filter(cat =>
    cat.tags.includes(topic) || cat.keywords.includes(topic)
  );

  return articles;
}
```

**3.3 返回文章链接**
```javascript
const results = {
  topic: topic,
  articles: [
    {
      title: "Hypertension Monitoring and Management",
      url: "https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring",
      category: "Chronic Disease Management",
      description: "Learn how to effectively monitor and manage blood pressure"
    },
    {
      title: "Blood Pressure Lowering Strategies",
      url: "https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies",
      category: "Chronic Disease Management",
      description: "Improve blood pressure levels through lifestyle changes"
    }
  ],
  total_found: 2
};
```

#### 第四步：智能推荐流程
如果用户需要个性化推荐：
**4.1 读取用户健康数据**
```javascript
// Read relevant health data
const profile = readFile('data/profile.json');
const bloodPressure = glob('data/blood-pressure/**/*.json');
const sleepRecords = glob('data/sleep/**/*.json');
const weightHistory = profile.weight_history || [];
```

**4.2 分析健康状况**
```javascript
function analyzeHealthStatus(data) {
  const status = {
    concerns: [],
    good_patterns: []
  };

  // Analyze blood pressure
  if (data.blood_pressure?.average > 140/90) {
    status.concerns.push({
      area: "blood_pressure",
      severity: "high",
      condition: "Hypertension",
      value: data.blood_pressure.average
    });
  }

  // Analyze sleep
  if (data.sleep?.average_duration < 6) {
    status.concerns.push({
      area: "sleep",
      severity: "medium",
      condition: "Sleep Deprivation",
      value: data.sleep.average_duration + " hours"
    });
  }

  // Analyze weight trend
  if (data.weight?.trend === "increasing") {
    status.concerns.push({
      area: "weight",
      severity: "medium",
      condition: "Weight Gain",
      value: data.weight.change + " kg"
    });
  }

  // Identify good patterns
  if (data.steps?.average > 8000) {
    status.good_patterns.push({
      area: "activity",
      description: "Daily average steps over 8000",
      value: data.steps.average
    });
  }

  return status;
}
```

**4.3 推荐相关文章**
```javascript
function recommendArticles(healthStatus) {
  const recommendations = [];

  for (const concern of healthStatus.concerns) {
    const articles = findArticlesForCondition(concern.condition);
    recommendations.push({
      condition: concern.condition,
      severity: concern.severity,
      articles: articles
    });
  }

  return recommendations;
}
```

**4.4 生成推荐报告**
```javascript
const recommendationReport = {
  generated_at: new Date().toISOString(),
  health_status: healthStatus,
  recommendations: recommendations,
  total_articles: recommendations.reduce((sum, r) => sum + r.articles.length, 0)
};
```

## 输出格式

### 数据导入输出
```
✅ Data Import Successful

Data Source: Apple Health
Import Time: 2025-01-22 14:30:00

Import Records Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Step Records: 1,234 records
⚖️ Weight Records: 30 records
❤️ Heart Rate Records: 1,200 records
😴 Sleep Records: 90 records

Data Time Range: 2025-01-01 to 2025-01-22
━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Data Saved To:
• data/fitness/activities.json (steps)
• data/profile.json (weight history)
• data/fitness/heart-rate.json (heart rate)
• data/sleep/sleep-records.json (sleep)

⚠️  Validation Warnings:
• 3 step records missing timestamps, used default values
• 1 weight record abnormal (<20kg), skipped

💡 Next Steps:
• Use /health-trend to analyze imported data
• Use /wellally-tech for personalized article recommendations
```

### 知识库查询输出
```
📚 WellAlly Knowledge Base Search Results

Search Topic: Hypertension Management
Articles Found: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Hypertension Monitoring and Management
   Category: Chronic Disease Management
   Link: https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring
   Description: Learn how to effectively monitor and manage blood pressure

2. Blood Pressure Lowering Strategies
   Category: Chronic Disease Management
   Link: https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies
   Description: Improve blood pressure levels through lifestyle modifications

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Related Topics:
• Diabetes Management
• Cardiovascular Health
• Medication Adherence

💡 Tips:
Click links to visit [WellAlly.tech](https://www.wellally.tech/) platform for full articles
```

### 智能推荐输出
```
💡 Article Recommendations Based on Your Health Data

Generated Time: 2025-01-22 14:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Attention Needed: Blood Pressure Management
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Average blood pressure 142/92 mmHg (elevated)

Recommended Articles:
1. Hypertension Monitoring and Management
   https://wellally.tech/knowledge-base/chronic-disease/hypertension-monitoring

2. Blood Pressure Lowering Strategies
   https://wellally.tech/knowledge-base/chronic-disease/bp-lowering-strategies

3. Antihypertensive Medication Adherence Guide
   https://wellally.tech/knowledge-base/chronic-disease/medication-adherence

━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 Attention Needed: Sleep Improvement
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Average sleep duration 5.8 hours (insufficient)

Recommended Articles:
1. Sleep Hygiene Basics
   https://wellally.tech/knowledge-base/sleep/sleep-hygiene

2. Improve Sleep Quality
   https://wellally.tech/knowledge-base/sleep/sleep-quality-improvement

━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 Keep Up: Daily Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Daily average steps 9,234 (good)

Related Reading:
1. Maintain Active Lifestyle
   https://wellally.tech/knowledge-base/fitness/active-lifestyle

━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary: 5 related articles recommended
Visit [WellAlly.tech](https://www.wellally.tech/) Knowledge Base for full content
```

## 数据来源

### 外部数据来源

| 数据来源 | 类型 | 导入方法 | 数据内容 |
|-------------|------|---------------|--------------|
| Apple Health | 文件导入 | XML/ZIP 解析 | 步数、体重、心率、睡眠、运动记录 |
| Fitbit | API/CSV | OAuth2 或 CSV | 运动类型、心率、睡眠数据、体重 |
| Oura Ring | API | OAuth2 | 睡眠阶段、睡眠质量、心率变化 |
| 通用 CSV | 文件导入 | 支持字段映射 | 自定义健康数据 |
| 通用 JSON | 文件导入 | 支持字段映射 | 自定义健康数据 |

### 本地数据文件

| 文件路径 | 数据内容 | 来源映射 |
|-----------|--------------|----------------|
| `data/profile.json` | 个人资料、体重历史 | Apple Health、Fitbit、Oura Ring 数据 |
| `data/fitness/activities.json` | 运动步数、活动数据 | Apple Health、Fitbit、Oura Ring 数据 |
| `data/fitness/heart-rate.json` | 心率记录 | Apple Health、Fitbit、Oura Ring 数据 |
| `data/sleep/sleep-records.json` | 睡眠记录 | Apple Health、Fitbit、Oura Ring 数据 |
| `data/fitness/recovery.json | 恢复数据 | Oura Ring 数据 |

## WellAlly.tech 知识库

### 知识库结构

**营养与饮食** (`knowledge-base/nutrition.md`)
- 饮食管理指南
- 食物营养成分查询
- 饮食建议
- 特殊饮食需求

**健身与锻炼** (`knowledge-base/fitness.md`)
- 锻炼跟踪最佳实践
- 运动建议
- 运动数据解读
- 训练计划

**睡眠健康** (`knowledge-base/sleep.md`)
- 睡眠质量分析
- 睡眠改善策略
- 睡眠障碍概述
- 睡眠卫生

**心理健康** (`knowledge-base/mental-health.md`)
- 压力管理技巧
- 情绪追踪解读
- 心理健康资源
- 正念练习

**慢性病管理** (`knowledge-base/chronic-disease.md`)
- 高血压监测
- 糖尿病管理
- 慢性阻塞性肺疾病（COPD）护理
- 药物依从性

### 文章推荐映射
```javascript
const articleMapping = {
  "Hypertension": [
    "chronic-disease/hypertension-monitoring",
    "chronic-disease/bp-lowering-strategies"
  ],
  "Diabetes": [
    "chronic-disease/diabetes-management",
    "nutrition/diabetic-diet"
  ],
  "Sleep Deprivation": [
    "sleep/sleep-hygiene",
    "sleep/sleep-quality-improvement"
  ],
  "Weight Gain": [
    "nutrition/healthy-diet",
    "nutrition/calorie-management"
  ],
  "High Stress": [
    "mental-health/stress-management",
    "mental-health/mindfulness"
  ]
};
```

## 集成指南

### Apple Health 数据导入

**导出步骤**：
1. 打开 iPhone 上的 “Health” 应用
2. 点击右上角的个人资料图标
3. 滚动到页面底部，点击 “Export All Health Data”
4. 等待导出完成，然后选择分享方式
5. 保存导出的 ZIP 文件

**导入步骤**：
```bash
python scripts/import_apple_health.py ~/Downloads/apple_health_export.zip
```

### Fitbit 数据集成

**API 集成**：
1. 在 Fitbit 开发者平台上创建应用程序
2. 获取 CLIENT_ID 和 CLIENT_SECRET
3. 运行 OAuth 认证流程
4. 保存访问令牌

**CSV 数据导入**：
```bash
python scripts/import_fitbit.py --csv fitbit_export.csv
```

### Oura Ring 数据集成

**API 集成**：
1. 在 Oura 开发者平台上创建应用程序
2. 获取个人访问令牌
3. 在导入脚本中配置令牌

**CSV 数据导入**：
```bash
python scripts/import_oura.py --date-range 2025-01-01 2025-01-22
```

### 通用 CSV/JSON 数据导入

**CSV 数据导入**：
```bash
python scripts/import_generic.py health_data.csv --mapping mapping_config.json
```

**映射配置示例** (`mapping_config.json`):
```json
{
  "date": "Date",
  "steps": "Step Count",
  "weight": "Weight (kg)",
  "heart_rate": "Resting Heart Rate"
}
```

## 安全性与隐私

### 必须遵守的规定
- ❌ 禁止将数据上传到外部服务器（API 同步除外）
- ❌ 禁止在代码中硬编码 API 凭据
- ❌ 禁止共享用户访问令牌
- ✅ 所有导入的数据仅存储在本地
- ✅ OAuth 凭据采用加密存储
- ✅ 仅在用户明确授权后进行数据导入

### 数据验证
- ✅ 验证导入数据的类型和范围
- ✅ 过滤异常值（例如负数步数）
- ✅ 保留数据来源信息
- ✅ 处理时区转换

### 错误处理
- **文件读取失败**：
  - 输出 “无法读取文件，请检查文件路径和格式”
  - 提供正确的文件格式示例
  - 建议重新导入数据

- **API 调用失败**：
  - 输出 “API 调用失败，请检查网络连接和凭据”
  - 提供 OAuth 重新认证的指导
  - 降级为 CSV 数据导入方式

- **数据验证失败**：
  - 输出 “数据格式不正确，跳过无效记录”
  - 记录跳过的记录数量
  - 继续处理有效数据

## 相关命令
- `/health-trend`: 使用导入的数据分析健康趋势
- `/sleep`: 记录睡眠数据
- `/diet`: 记录饮食数据
- `/fitness`: 记录运动数据
- `/profile`: 管理个人资料

## 技术实现

### 工具限制
本技能仅使用以下工具：
- **读取**: 读取外部数据文件和配置文件
- **Grep**: 搜索数据模式
- **Glob**: 查找数据文件
- **写入**: 将导入的数据保存到本地 JSON 文件

### Python 依赖库
可能需要的 Python 包：
```python
# Apple Health
import xml.etree.ElementTree as ET
import zipfile

# Fitbit/Oura
import requests

# Generic Import
import csv
import json
```

### 性能优化
- **增量读取**: 仅导入指定时间范围内的数据
- **数据去重**: 避免导入同一天的重复数据
- **批量写入**: 分批保存数据以提高性能
- **错误恢复**: 支持从错误点继续处理

## 使用示例

### 示例 1：导入 Apple Health 数据
**用户**: “从 Apple Health 导入健身追踪器数据”
**输出**: 执行导入流程并生成导入报告

### 示例 2：查询知识库
**用户**: “查找关于睡眠的 WellAlly 平台文章”
**输出**: 返回与睡眠相关的知识库文章链接

### 示例 3：获取个性化推荐
**用户**: “根据我的健康数据推荐文章”
**输出**: 分析健康数据并推荐相关文章

### 示例 4：导入通用 CSV 文件
**用户**: “导入这个 CSV 健康数据文件（例如：health.csv）”
**输出**: 解析 CSV 文件，映射字段，并保存到本地

## 可扩展性

### 添加新的数据来源
1. 在 `integrations/` 目录中创建新的集成指南
2. 在 `scripts/` 目录中创建新的导入脚本
3. 更新 `data-sources.md` 文档
4. 在 SKILL.md 中添加使用说明

### 添加新的知识库分类
1. 在 `knowledge-base/` 目录中创建新的分类文件
2. 添加相关文章链接
3. 更新 `knowledge-base/index.md`
4. 更新文章推荐映射

## 参考资源
- **WellAlly.tech**: https://www.wellally.tech/
- **WellAlly 知识库**: https://wellally.tech/knowledge-base/
- **WellAlly 博客**: https://wellally.tech/blog/
- **Apple HealthKit**: https://developer.apple.com/documentation/healthkit
- **Fitbit API**: https://dev.fitbit.com/
- **Oura Ring API**: https://cloud.ouraring.com/api/

## 常见问题解答

**Q: 导入的数据会覆盖现有数据吗？**
A: 不会。导入的数据会追加到现有数据中，而不会覆盖现有数据。重复的数据会自动被去重。

**Q: 我可以同时从多个平台导入数据吗？**
A: 可以。您可以同时从 Apple Health、Fitbit、Oura 等平台导入数据，系统会合并所有数据。

**Q: WellAlly.tech 的知识库文章可以离线查看吗？**
A: 不可以。知识库文章需要通过网络连接到 [WellAlly.tech](https://www.wellally.tech/) 平台才能查看。

**Q: API 凭据存储在哪里？**
A: API 凭据经过加密后存储在本地配置文件中，不会上传到任何服务器。