---
name: hsk-learning
description: "HSK中文学习系统具备间隔重复练习功能、词汇分析能力以及自适应测验生成功能。适用场景包括：  
(1) 跟踪HSK词汇的学习进度；  
(2) 生成个性化的自适应测验；  
(3) 分析日常对话中中文语言的使用情况；  
(4) 管理间隔重复复习计划。  
不适用于：  
- 非HSK范围内的中文语言学习；  
- 发音练习；  
- 书写练习。"
metadata:
  openclaw:
    emoji: "📚"
    requires:
      node: true
    install:
      - id: "init"
        kind: "node"
        script: "scripts/init-mastery-db.js"
        label: "Initialize mastery database (first-time setup)"
---
# OpenClaw的HSK学习技能

**用途**：提供一个全面的HSK中文学习系统，具备间隔重复学习机制、掌握情况跟踪、词汇分析以及自适应测验生成功能。

**版本**：1.1.0  
**作者**：Claw  
**日期**：2026-02-18

## 主要功能

- **间隔重复学习机制**：使用受SM-2算法跟踪所有2,211个HSK 3.0单词的掌握状态（未知/学习中/已掌握）。
- **词汇暴露分析**：扫描对话记录，按HSK级别对汉字/词进行分类，并生成进度报告。
- **测验日志解析**：自动从测验表现日志中提取词汇和正确答案。
- **自适应测验生成**：根据单词的掌握情况，优先生成需要复习的测验。
- **综合工具集**：包含六个工具，用于更新、查询和管理HSK学习系统。

## 工具

### 1. `hsk_update_vocab_tracker`
扫描`memory/*.md`文件中的汉字/词，按HSK级别进行分类，并更新`memory/hsk-word-report.md`文件。

**参数**：
- `force`（布尔值）：即使最近已经扫描过，也强制更新（默认值：false）

### 2. `hsk_update_mastery_from_quiz`
处理测验表现日志并更新掌握情况数据库。

**参数**：
- `date`（字符串）：特定日期（YYYY-MM-DD）或“all”（所有日志）（默认值：“all”）

### 3. `hsk_get_mastery_stats`
返回掌握情况统计信息：未知/学习中/已掌握的单词数量，按HSK级别划分。

**参数**：
- `format`（字符串）：输出格式：“text”、“json”或“markdown”（默认值：“text”）

### 4. `hsk_get_due_words`
列出根据间隔重复学习计划需要复习的单词。

**参数**：
- `limit`（数字）：返回的最大单词数量（默认值：20）
- `level`（数字）：按HSK级别筛选（1-6），0表示全部级别（默认值：0）

### 5. `hsk_generate_quiz`
根据掌握情况生成自适应测验。

**参数**：
- `difficulty`（字符串）：“review”（复习）、“learning”（学习中）、“new”（新单词）或“mixed”（混合）（默认值：“mixed”）
- `format`（字符串）：“simple”（简单）、“listening”（听力）、“reading”（阅读）、“writing”（写作）或“full”（综合）（默认值：“simple”）

### 6. `hsk_parse_quiz_log`
解析测验表现日志文件并提取词汇。

**参数**：
- `filePath`（字符串）：测验日志文件的路径（必需）

## 数据文件

该技能将数据文件保存在`data/`目录中：

| 文件 | 用途 |
|------|---------|
| `hsk-word-to-level.json` | HSK 3.0单词与级别的映射表（2,211个单词） |
| `hsk-database.json` | 完整的HSK数据库及元数据 |
| `hsk-mastery-db.json` | 所有HSK单词的掌握情况（用户专属） |

## 设置与安装

### 新用户（首次设置）

1. 通过ClawHub安装该技能：
   ```bash
   clawhub install hsk-learning
   ```

2. 初始化您的个人掌握情况数据库（每位用户都需要执行此操作）：
   ```bash
   cd skills/hsk-learning
   node scripts/init-mastery-db.js
   ```
   此操作会创建一个包含所有2,211个HSK单词的`hsk-mastery-db.json`文件，初始状态均为“未知”。

3. **可选：配置用户设置**：
   ```bash
   cp data/user-config.template.json data/user-config.json
   # Edit user-config.json with your preferences
   ```

4. 重新启动OpenClaw门户以加载该技能：
   ```bash
   openclaw gateway restart
   ```

## 数据文件结构

| 文件 | 用途 | 是否为用户专属？ | 是否被Git忽略？ |
|------|---------|----------------|--------------|
| `hsk-database.json` | HSK单词数据库（共享） | ❌ 否 | ❌ 否 |
| `hsk-word-to-level.json` | 单词与级别的映射表（共享） | ❌ 否 | ❌ 否 |
| `hsk-mastery-db.json` | 个人掌握情况跟踪数据 | ✅ 是 | ✅ 是 |
| `user-config.json` | 用户偏好设置（可选） | ✅ 是 | ✅ 是 |
| `user-config.template.json` | 配置模板 | ❌ 否 | ❌ 否 |

## Git仓库设置

在发布或贡献此技能时：

1. **用户专属文件会通过`.gitignore`自动被忽略**。
2. **共享数据文件（HSK数据库）会被包含在仓库中**。
3. **初始化脚本会在首次运行时创建用户数据**。
4. **任何个人数据都不会被提交到仓库中**。

## 技能测试

重启后，测试基本功能：

```javascript
// In an OpenClaw session
hsk_get_mastery_stats({ format: 'text' });
hsk_update_mastery_from_quiz({ date: 'all' });
hsk_get_due_words({ limit: 5 });
```

## 维护

- 测验日志处理完成后，掌握情况数据库会自动更新。
- 词汇报告可通过cron作业或手动触发进行更新。
- 建议添加每周一次的系统健康检查任务。

## 下一步计划

1. 更新所有与HSK相关的cron作业，以使用该技能的工具。
2. 通过基于GPT的文本生成功能改进测验内容。
3. 添加带有音频的听力练习。
4. 实现HSK模拟考试（全面测试模拟）。

## 参考资料

- **HSK 3.0单词列表**：mandarinbean.com
- **间隔重复学习算法**：SM-2（SuperMemo）
- **OpenClaw技能文档**：https://docs.openclaw.ai

---
*该技能是William个性化HSK学习系统的一部分，与OpenClaw的cron调度器集成，实现自动化运行。*