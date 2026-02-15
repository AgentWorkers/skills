---
name: brave-api-setup
description: 为 OpenClaw 的 web_search 功能配置 Brave Search API。当用户需要配置 Brave API、获取 Brave API 密钥、启用网络搜索功能，或解决 “missing_brave_api_key” 错误时，请使用此方法。
metadata:
  openclaw:
    requires:
      bins: ["node"]
    triggers:
      - Brave Search
      - brave api
      - web_search
      - missing_brave_api_key
      - search API
---

# Brave API 设置

本脚本用于自动提取 Brave Search 的 API 密钥，并配置 OpenClaw。

## 包含的文件

| 文件 | 说明 |
|------|-------------|
| `SKILL.md` | 本文档 |
| `scripts/apply-api-key.js` | 将 API 密钥应用到 OpenClaw 配置中（Node.js） |

## 依赖项
- Node.js（用于 `apply-api-key.js`）
- OpenClaw 浏览器功能（`browser` 工具）

## 使用场景
- 用户希望在 OpenClaw 中启用 `web_search` 功能
- 出现错误：“missing_brave_api_key”
- 用户请求设置 Brave Search API

## 先决条件
- 用户必须拥有 Brave Search API 账户
- 用户必须已登录（使用 OpenClaw 浏览器）
- API 密钥必须存在于控制面板中

## 工作流程

### 第一步：导航到 API 密钥页面

```
browser(action="navigate", profile="openclaw", 
        targetUrl="https://api-dashboard.search.brave.com/app/keys")
```

### 第二步：点击“显示”按钮（眼睛图标）

拍摄屏幕截图，找到“显示”按钮并点击它：
```
browser(action="act", kind="click", ref="<eye-button-ref>")
```

### 第三步：通过 JavaScript 提取密钥（避免大型语言模型（LLM）的转录错误）

```
browser(action="act", kind="evaluate", 
        fn="(() => { const cells = document.querySelectorAll('td'); for (const cell of cells) { const text = cell.textContent?.trim(); if (text && text.startsWith('BSA') && !text.includes('•') && text.length > 20) return text; } return null; })()")
```

结果字段中包含完整的 API 密钥。

### 第四步：将密钥应用到配置文件中（直接写入文件，不涉及大型语言模型）

相对于技能目录的路径：
```bash
node <skill_dir>/scripts/apply-api-key.js "<extracted-key>"
```

或者使用 `gateway config.patch` 并传入提取的密钥。

## 采用此方法的原因

**问题**：大型语言模型在转录时可能会混淆相似的字符（例如：O 和 0、l 和 1）。

**解决方案**：
1. `evaluate` 通过 JavaScript 提取密钥，返回精确的字符串。
2. `apply-api-key.js` 直接将密钥写入配置文件，确保数据完全准确无误。
密钥在整个过程中都不会经过大型语言模型的文本生成环节。

## 手动账户设置

如果用户没有账户：
1. 访问 https://api-dashboard.search.brave.com
2. 使用电子邮件注册
3. 订阅免费计划（需要信用卡）
4. 在控制面板中创建 API 密钥
5. 然后运行此脚本

## 问题咨询 / 反馈

如有关于错误的报告、功能请求或反馈，请发送至以下邮箱：
- 邮箱：contact@garibong.dev
- 开发者：Garibong Labs（가리봉랩스）