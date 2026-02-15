---
description: 诊断 `.env` 文件的问题：缺失的变量、格式错误、安全风险以及配置错误。
---

# Env Doctor

用于诊断和修复 `.env` 文件中的问题。

## 使用说明

1. **读取文件**：解析 `.env` 文件（如果存在 `.env.example`，也会一并解析）。
2. **检测问题**：

   | 严重程度 | 问题描述 | 例子 |
   |----------|-------|---------|
   | 🔴 严重 | 密钥被提交到 Git 仓库 | `.env` 文件未被包含在 `.gitignore` 中 |
   | 🔴 严重 | 缺少必要的变量 | 变量存在于 `.env.example` 中，但不存在于 `.env` 文件中 |
   | 🟡 警告 | 键重复 | `DB_HOST` 被定义了两次 |
   | 🟡 警告 | 值为空 | `API_KEY=` |
   | 🟡 警告 | 等号周围有空格 | `DB_HOST = localhost`（会导致解析错误） |
   | 🔵 提示 | 存在多余的键 | 变量存在于 `.env` 文件中，但不存在于 `.env.example` 中 |
   | 🔵 提示 | 布尔值使用了引号 | `DEBUG="true"`（应写为 `DEBUG=true`） |

3. **验证检查**：
   - URL 缺少协议（例如：`example.com` 应改为 `https://example.com`）
   - 端口号超出范围（0-65535）
   - 值中包含空格（未使用引号）
   - 文件开头有换行符（BOM 字符）
4. **交叉引用**：如果存在 `.env.example` 文件，会报告缺失或多余的键。

5. **Git 安全性检查**：
   ```bash
   # Is .env in .gitignore?
   grep -q "^\.env$" .gitignore 2>/dev/null && echo "✅ Protected" || echo "🔴 NOT in .gitignore!"
   # Was .env ever committed?
   git log --all --diff-filter=A -- .env 2>/dev/null
   ```

6. **报告格式**：
   ```
   🩺 Env Doctor — .env

   Found 3 issues:

   🔴 CRITICAL: .env not in .gitignore
      Fix: echo ".env" >> .gitignore

   🟡 WARNING: Duplicate key DB_HOST (lines 4, 12)
      Fix: Remove duplicate on line 12

   🔵 INFO: ANALYTICS_KEY in .env but not .env.example
      Fix: Add to .env.example (with empty value)
   ```

## 安全性注意事项

- **切勿输出实际的密钥值** — 应将密钥值替换为 `sk-****...abc` 的格式
- 检查 `.env` 文件是否被 Git 跟踪 — 这是最大的安全风险
- 如果发现生产环境所需的凭据出现在开发环境的 `.env` 文件中，应立即标记出来。

## 特殊情况处理

- **没有 `.env` 文件**：检查当前工作目录（cwd），建议使用 `cp .env.example .env` 命令创建 `.env` 文件。
- **多行值**：处理跨多行的值（使用 `\n` 进行换行）。
- **变量插值**：检查 `${VAR}` 这样的引用是否指向有效的变量。

## 系统要求

- 无需任何依赖库 — 仅依赖文本文件解析功能。
- 不需要任何 API 密钥。