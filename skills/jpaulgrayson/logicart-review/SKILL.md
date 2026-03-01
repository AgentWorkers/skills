---
name: code-review
description: 通过LogicArt实现的基于人工智能的代码分析工具——可以发现代码中的错误、安全问题，并提供逻辑流程的可视化展示。适用于代码审查、代码质量分析、漏洞检测、安全检查以及逻辑分析等场景。该工具会在用户执行“审查代码”、“分析代码”、“查找错误”、“代码质量检查”或“逻辑分析”等操作时自动触发。
---
# 代码审查

代码分析由 LogicArt 提供支持，网址为：https://logic.art。

## 分析代码

```bash
node {baseDir}/scripts/analyze.mjs --code "function add(a,b) { return a - b; }"
```

或者分析一个文件：

```bash
node {baseDir}/scripts/analyze.mjs --file path/to/code.js
```

## API

**端点：** `POST https://logic.art/api/agent/analyze`

```bash
curl -s -X POST "https://logic.art/api/agent/analyze" \
  -H "Content-Type: application/json" \
  -d '{"code": "your code here", "language": "javascript"}'
```

响应通常包含：错误信息、安全问题、代码复杂度评分、改进建议以及代码逻辑流程。

## 全仓库扫描

如需扫描整个仓库，请使用 Validate Repo：https://validate-repo.replit.app

## 展示结果

向用户展示结果时，请按照以下顺序进行：
1. 首先列出关键的错误或安全问题；
2. 显示代码复杂度评分；
3. 按优先级列出改进建议；
4. 如果提供了代码逻辑流程，请一并展示。

## 适用场景

- **workflow-engine** — 将代码审查流程集成到持续集成/持续部署（CI/CD）管道中；
- **quack-coordinator** — 雇佣专业的代码审查人员。

由 Quack Network 提供支持 🦆