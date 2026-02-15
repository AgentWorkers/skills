---
name: skill-vettr
version: "2.0.1"
author: britrik
description: 用于第三方 OpenClaw 技能的静态分析安全扫描器。在安装之前，能够检测到评估（eval/spawn）风险、恶意依赖项、域名抢注（typosquatting）以及命令提示符注入（prompt injection）等安全问题。适用于审核来自 ClawHub 或不可信来源的技能。
tags: ["security", "scanner", "vetting", "analysis", "static-analysis"]
emoji: "🛡️"
---

# skill-vettr v2.0.1

这是一个用于检测第三方 OpenClaw 技能的安全扫描工具。在安装之前，它会使用 tree-sitter 的抽象语法树（AST）解析和正则表达式匹配来分析源代码、依赖项以及元数据。

## 命令

- `/skill:vet --path <directory>` — 检查本地技能目录
- `/skill:vet-url --url <https://...>` — 从指定 URL 下载并检查技能
- `/skill:vet-clawhub --skill <slug>` — 从 ClawHub 获取并检查技能

## 检测类别

| 类别 | 方法 | 例子 |
|----------|--------|----------|
| 代码执行 | AST | `eval()`, `new Function()`, `vm.runInThisContext()` |
| Shell 注入 | AST | `exec()`, `execSync()`, `spawn("bash")`, `child_process` 的导入 |
| 动态依赖加载 | AST | `require(variable)`, `require(templateString)` |
| 原型污染 | AST | 使用 `__proto__` 进行赋值 |
| 提示注入 | 正则表达式 | 指令被篡改，控制令牌（存在于字符串字面量中） |
| 同形异义词攻击 | 正则表达式 | 标识符中的西里尔文/希腊文相似字符 |
| 编码后的名称 | 正则表达式 | 使用 Unicode 或十六进制转义的 `eval()`, `exec()` |
| 凭据路径 | 正则表达式 | `.ssh/`, `.aws/`, 密钥链路径引用 |
| 网络调用 | AST | 使用字面 URL 的 `fetch()` 函数（会与允许列表进行比对） |
| 恶意依赖项 | 配置文件 | 已知的恶意包、生命周期脚本、Git/HTTP 依赖项 |
| 拼写错误（Typosquatting） | Levenshtein 算法 | 技能名称与目标名称的编辑距离在 2 以内 |
| 危险权限 | 配置文件 | `shell:exec`, `credentials:read` 等权限设置

## 限制

> ⚠️ **这是一个启发式扫描工具，存在固有的局限性。它无法保证绝对的安全性。**

- **仅进行静态分析** — 无法检测运行时行为（例如，安装后下载恶意代码的行为）
- **可能存在规避手段** — 复杂的混淆技术或多阶段字符串构造可能逃避检测
- **仅支持 JavaScript/TypeScript** — 二进制文件、图像和非文本文件将被忽略
- **网络检测有限** — 仅检测使用字面 URL 的 `fetch()` 函数；无法检测 axios、http 模块或动态生成的 URL
- **不提供沙箱环境** — 不会执行或隔离目标代码
- **不扫描注释** — 提示注入检测仅针对字符串字面量，不包含注释

对于高安全性的环境，建议将此工具与沙箱环境和手动代码审查结合使用。