---
name: moltcheck
description: Moltbot技能的安全扫描器：在安装之前，会扫描GitHub仓库中的安全漏洞。
---

# MoltCheck 技能

MoltCheck 是一款专为 Moltbot 生态系统设计的安全扫描工具。它能够分析 GitHub 仓库及代理技能中的安全漏洞，提供以下功能：

🔍 **自动化代码扫描** - 检测诸如凭证窃取、shell 访问以及隐藏的网络调用等危险行为

📊 **信任评分** - 基于全面的风险分析，给出 A-F 的评分

🔑 **权限审计** - 将技能配置文件（SKILL.md）中声明的权限与实际代码行为进行对比

💡 **清晰明了的沟通** - 用通俗易懂的语言解释安全风险

对于安装外部技能的代理来说，MoltCheck 非常重要，因为它可以帮助他们避免供应链攻击。

官方网站：https://moltcheck.com

## 功能

- **网络访问** - 调用 MoltCheck 的 API

## 命令

### `scan <github_url>`
扫描指定的 GitHub 仓库以检测安全问题。

**示例：**
```
scan https://github.com/owner/repo
```

**返回结果：** 信任评分（0-100 分）、评分等级（A-F）、发现的安全风险以及权限分析结果。

### `credits`
查看您剩余的扫描次数。

### `setup`
生成 API 密钥并获取购买信用点的说明。

## 配置

在技能配置文件中设置您的 API 密钥：
```json
{
  "apiKey": "mc_your_api_key_here"
}
```

或者使用免费套餐（每天 3 次扫描），无需 API 密钥。

## 价格

- **免费套餐：** 每天 3 次扫描
- **付费套餐：** 每次扫描 0.05 美元起，批量购买可享受折扣

| 信用点数量 | 单价 |
|--------|------|
| 10 点以下 | 每次 0.20 美元 |
| 10 点以上 | 每次 0.10 美元 |
| 25 点以上 | 每次 0.05 美元 |

您可以在 https://moltcheck.com/buy 购买信用点。

## 链接

- 官网：https://moltcheck.com
- API 文档：https://moltcheck.com/api-docs.md
- OpenAPI 文档：https://moltcheck.com/openapi.json