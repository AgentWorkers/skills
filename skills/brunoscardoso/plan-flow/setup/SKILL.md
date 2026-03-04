---
name: setup
description: 分析项目结构并创建 Plan-Flow 配置
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 设置

分析当前仓库并生成 Plan-Flow 配置文件。

## 功能说明

1. 扫描项目结构以检测使用的语言和框架。
2. 创建 `flow/` 目录结构。
3. 识别代码库中的现有模式。
4. 生成初始配置文件。

## 使用方法

```
/setup [path]
```

**参数：**
- `path`（可选）：要分析的目录。默认为当前目录。

## 输出结果

生成以下目录结构：

```
flow/
├── archive/           # Completed/abandoned plans
├── contracts/         # Integration contracts
├── discovery/         # Discovery documents
├── plans/             # Active implementation plans
├── references/        # Reference materials
├── reviewed-code/     # Code review documents
└── reviewed-pr/       # PR review documents
```

## 示例

```
/setup
```

**输出结果：**
```
Setup Complete!

Analyzed: /path/to/project
Files found: 156
Languages detected: TypeScript, JavaScript
Frameworks detected: Next.js, Jest

Created Directories:
- flow/discovery/
- flow/plans/
- flow/contracts/
- flow/references/
- flow/archive/

Next Steps:
1. Create .plan-flow.yml with your AI API key
2. Run /discovery to gather requirements for a feature
3. Run /create-plan to create an implementation plan
```

## 下一步操作

设置完成后，运行 `/discovery` 命令以开始收集新功能的需求信息。