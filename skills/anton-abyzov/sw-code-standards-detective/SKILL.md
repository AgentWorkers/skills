---
name: code-standards-detective
description: 深入分析代码库，通过统计数据来发现实际的编码规范。适用于分析命名约定、导入模式，或检测现有代码中的不良编码习惯（反模式）。该工具能够基于实际数据检测代码库的运行方式（而非仅依据设计初衷）。
allowed-tools: Read, Grep, Glob, Bash, Write
---

# 代码标准检测工具（Code Standards Detective Skill）

## 概述

该工具用于分析代码库，以发现并记录编码规范。通过统计数据分析代码中的模式、约定以及不良编码习惯。

## 功能分阶段加载

根据需要加载各个功能模块：

| 功能阶段 | 加载时机 | 对应文件 |
|---------|-----------|---------|
| 配置文件分析 | 解析配置文件 | `phases/01-config-analysis.md` |
| 模式检测 | 查找代码模式 | `phases/02-pattern-detection.md` |
| 报告生成 | 创建规范文档 | `phases/03-report.md` |

## 核心原则

1. **基于证据**：使用统计数据和置信度来评估代码质量。
2. **使用真实示例**：引用实际代码库中的代码片段。
3. **提供可操作的指导**：提供明确的规范，而不仅仅是观察结果。

## 快速参考

### 检测类别

1. **命名约定**：
   - 变量命名：驼峰式（camelCase）、帕斯卡式（PascalCase）、大写蛇形（UPPER_SNAKE）
   - 函数命名：使用动词前缀（如 `get`、`set`、`is`、`has`）
   - 文件命名：使用连字符分隔的单词（kebab-case）或帕斯卡式

2. **导入模式**：
   - 绝对路径导入与相对路径导入
   - 导入顺序
   - 显式导入与默认导出

3. **函数特性**：
   - 函数平均长度
   - 参数数量
   - 返回类型模式

4. **类型使用**：
   - 各类型的使用频率
   - 接口与实际类型的匹配情况
   - 类型的严格性

5. **错误处理**：
   - 错误处理机制（try-catch结构）
   - 使用的错误类型
   - 日志记录方式

### 需要解析的配置文件

```
.eslintrc.js / .eslintrc.json
.prettierrc / .prettierrc.json
tsconfig.json
.editorconfig
```

### 输出格式

```markdown
# Coding Standards: [Project Name]

## Naming Conventions

### Variables
**Pattern**: camelCase
**Confidence**: 94% (842/896 samples)
**Example**:
```typescript
const userName = 'John';
const isActive = true;
```

### Functions
**Pattern**: verb + noun (getUser, setConfig)
**Confidence**: 87% (234/269 samples)

## Import Patterns
**Absolute imports**: Enabled (paths in tsconfig)
**Import order**: external → internal → relative
**Example**:
```typescript
import { z } from 'zod';           // 外部库导入
import { logger } from '@/lib';    // 内部库导入
import { helper } from './helper'; // 相对路径导入
```

## Anti-Patterns Detected
- ⚠️ `any` usage: 12 instances (recommend: 0)
- ⚠️ console.log: 8 instances (use logger)
```

## 工作流程

1. **解析配置文件**（每个文件不超过500个代码单元）：使用ESLint、Prettier、TypeScript工具。
2. **检测代码模式**（每个类别不超过600个代码单元）：通过统计分析。
3. **生成报告**（报告内容不超过600个代码单元）：生成规范文档。

## 代码单元限制

**每个分析结果的代码单元数量不得超过2000个！**

## 检测命令

```bash
# Count naming patterns
grep -rE "const [a-z][a-zA-Z]+ =" src/ | wc -l

# Find function patterns
grep -rE "function (get|set|is|has)" src/ | head -20

# Check for any usage
grep -rE ": any" src/ | wc -l
```