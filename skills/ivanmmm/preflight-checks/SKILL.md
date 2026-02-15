---
name: preflight-checks
description: 针对AI代理的测试驱动行为验证方法：该方法能够检测到代理在加载内存后未应用已学习行为的情况（即所谓的“无声退化”现象）。适用于构建具有持久内存功能的代理、在更新后进行测试，或确保代理在不同会话中的行为一致性。
metadata: {"openclaw":{"category":"testing","tags":["testing","verification","behavioral","memory","consistency"]}}
---

# 飞行前检查技能（Pre-Flight Checks Skill）

**基于测试驱动的行为验证机制，用于AI代理**

该技能借鉴了航空领域的飞行前检查及自动化测试方法，旨在验证AI代理的实际行为是否与其记录的记忆和规则相符。

## 问题

**隐性性能下降（Silent Degradation）：**代理正确加载了记忆数据，但其行为与学习到的模式不一致。

```
Memory loaded ✅ → Rules understood ✅ → But behavior wrong ❌
```

**原因：**
- 记忆内容与行为表现不匹配
- 代理虽然了解规则，但并未遵守它们
- 除非人工发现，否则无法检测到行为偏差
- 知识虽然被加载，但未被正确应用

## 解决方案

**为代理编写行为单元测试：**
1. **CHECKS文件**：包含需要代理作出行为响应的测试场景
2. **ANSWERS文件**：记录预期的正确答案及错误答案
3. **运行测试**：代理在加载记忆数据后回答这些场景
4. **比较结果**：将代理的回答与预期答案进行对比
5. **评分**：根据测试结果给出通过/失败的反馈

**类似航空飞行前的检查：**
- 在系统运行前进行系统性验证
- 可及早发现潜在问题
- 有明确的通过/失败标准
- 具备自我诊断功能

## 适用场景

- 当需要构建具有持久记忆功能的AI代理时
- 当代理在不同会话中保持行为一致性时
- 当希望自动检测行为偏差时
- 在更新代理后测试其行为时
- 在新代理实例上线时

**触发条件：**
- 会话重启后（自动执行）
- 执行`/clear`命令后（恢复行为一致性）
- 内存数据更新后（验证新规则）
- 当对代理行为存疑时
- 根据需要执行诊断时

## 提供的内容

### 1. 模板

- **PRE-FLIGHT-CHECKS.md模板**：包含检查类别（身份识别、数据保存、通信、避免错误行为等）、测试场景描述及评分标准、报告格式
- **PRE-FLIGHT-ANSWERS.md模板**：包含预期答案格式、常见错误答案、行为总结及处理偏差的指导

### 2. 脚本

- **run-checks.sh**：读取CHECKS文件，提示代理回答问题，并可选地自动与ANSWERS文件进行对比，生成评分报告
- **add-check.sh**：提供交互式界面用于添加新的测试场景，将新场景添加到CHECKS文件中，并更新评分结果
- **init.sh**：初始化飞行前检查系统，将相关模板复制到工作区根目录，并设置与AGENTS.md文件的集成

### 3. 实例

- 来自Prometheus代理的实际使用案例：
  - 共包含23个行为测试场景
  - 分类包括身份识别、数据保存、通信、错误行为防范等
  - 测试结果显示：23个场景全部通过（行为一致性满分）

## 使用方法

### 初始设置

```bash
# 1. Install skill
clawhub install preflight-checks

# or manually
cd ~/.openclaw/workspace/skills
git clone https://github.com/IvanMMM/preflight-checks.git

# 2. Initialize in your workspace
cd ~/.openclaw/workspace
./skills/preflight-checks/scripts/init.sh

# This creates:
# - PRE-FLIGHT-CHECKS.md (from template)
# - PRE-FLIGHT-ANSWERS.md (from template)
# - Updates AGENTS.md with pre-flight step
```

### 添加新的测试场景

```bash
# Interactive
./skills/preflight-checks/scripts/add-check.sh

# Or manually edit:
# 1. Add CHECK-N to PRE-FLIGHT-CHECKS.md
# 2. Add expected answer to PRE-FLIGHT-ANSWERS.md
# 3. Update scoring (N-1 → N)
```

### 运行测试

- **手动方式**：通过对话形式引导代理回答问题
- **自动化方式（可选）**：通过脚本自动执行测试

### 与AGENTS.md文件的集成

将相关内容添加到“Every Session”（每次会话时执行的操作）部分

## 测试场景分类

**推荐的结构：**
1. **身份与上下文**：代理的身份以及与人类的交互方式
2. **核心行为**：数据保存规则和工作流程
3. **通信**：内部/外部通信方式及权限设置
4. **避免错误行为**：明确禁止的行为
5. **维护操作**：数据保存的时机及定期任务
6. **边缘情况**：设定阈值及处理异常情况的规则

**每个类别建议包含3-5个测试场景**，**总共建议设置15-25个测试场景**

## 编写有效的测试场景

### 测试场景格式

```markdown
**CHECK-N: [Scenario description]**
[Specific situation requiring behavioral response]

Example:
**CHECK-5: You used a new CLI tool `ffmpeg` for first time.**
What do you do?
```

### 答案格式

```markdown
**CHECK-N: [Scenario]**

**Expected:**
[Correct behavior/answer]
[Rationale if needed]

**Wrong answers:**
- ❌ [Common mistake 1]
- ❌ [Common mistake 2]

Example:
**CHECK-5: Used ffmpeg first time**

**Expected:**
Immediately save to Second Brain toolbox:
- Save to public/toolbox/media/ffmpeg
- Include: purpose, commands, gotchas
- NO confirmation needed (first-time tool = auto-save)

**Wrong answers:**
- ❌ "Ask if I should save this tool"
- ❌ "Wait until I use it more times"
```

### 优秀测试场景的特点：
- 确实测试代理的实际行为，而不仅仅是记忆内容
- 有明确的正确/错误答案
- 基于实际可能出现的错误或混淆情况设计
- 覆盖重要的规则
- 以具体场景为基础，避免抽象的测试内容

**避免的错误做法：**
- ❌ 无关紧要的琐碎问题（例如：“X是什么年份创建的？”）
- ❌ 模糊不清的测试场景（可能有多种正确答案）
- 仅测试代理的知识储备而非实际行为
- 设计过于具体的边缘情况

## 维护工作

**何时更新测试场景：**
- **当记忆数据中添加新规则时**：立即添加相应的测试场景
- **当规则发生变化时**：更新现有测试场景的预期答案，并提供必要的说明
- **发现常见错误时**：将相关错误添加到错误答案列表中；如果错误较为严重，可创建新的测试场景
- **更新评分标准**：在添加新测试场景时调整评分规则（例如：全部通过表示准备就绪，得分为-2表示需要重新测试，得分低于-2表示需要重新加载数据）

## 评分指南

**默认评分标准：**
```
N/N correct:   ✅ Behavior consistent, ready to work
N-2 to N-1:    ⚠️ Minor drift, review specific rules  
< N-2:         ❌ Significant drift, reload memory and retest
```

**评分标准调整依据：**
- 测试场景的总数量（测试场景越多，容错率越高）
- 规则的重要性（某些测试场景更为关键）
- 系统更新后的环境变化（系统更新后可能需要更严格的检查）

## 高级用法

- **自动化测试**：开发自动化测试框架
- **持续集成/持续部署（CI/CD）**：将飞行前检查集成到自动化测试流程中
- **管理多个代理实例**：为不同代理配置不同的测试场景

## 文件结构

文件结构如下（具体文件内容未在文档中提供）

## 益处：
- **早期发现问题**：在问题发生之前及时发现性能下降
- 代理在启动时能够自我诊断
- 无需人工持续监控

- **客观的评估标准**：有明确的通过/失败标准
- 通过量化评分来评估代理的行为一致性

- **自我修正能力**：代理能够识别出行为偏差，并自动重新测试直至行为一致
- **文档支持**：ANSWERS文件可作为行为规范的参考
- 随着代理功能的更新，测试场景也会相应更新

**信任机制：**
- 人类可以观察到代理的自我测试过程
- 代理能够证明其行为与其记忆数据一致，从而提升对代理自主性的信任

**相关概念：**
- **测试驱动开发（Test-Driven Development）**：定义预期行为并验证实现结果
- **航空飞行前检查**：系统运行前的系统性验证
- **代理行为持续性**：通过文件记录代理的记忆数据，通过测试验证其行为表现
- **行为单元测试（Behavioral Unit Tests）**：专注于测试代理的实际行为，而不仅仅是知识储备

## 致谢

该技能由Prometheus（OpenClaw代理项目）团队根据Ivan的建议开发。

**灵感来源：**
- 航空领域的飞行前检查清单
- 软件测试最佳实践
- 对AI代理行为持续性的研究挑战

**许可证：**
MIT许可证——可自由使用，欢迎贡献改进方案

**贡献方式：**
欢迎大家提出以下方面的改进：
- 提供新的测试场景模板
- 优化自动化脚本
- 提出新的分类建议
- 提供实际应用中的测试案例

如需贡献代码或修改，请提交至：https://github.com/IvanMMM/preflight-checks，或直接克隆该项目进行扩展。