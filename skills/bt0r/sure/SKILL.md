---
name: sure
description: 从Sure个人财务管理平台获取报告
homepage: https://sure.am
metadata: {"clawdbot":{"emoji":"📈","requires":{"bin": ["curl"],"env":["SURE_API_KEY", "SURE_BASE_URL"]}}}
---
# Sure Skill

## 设置
1. 打开您的 Sure 应用程序，例如：https://localhost:3000
2. 进入设置页面并获取 API 密钥，例如：https://localhost:3000/settings/api_key
3. 将 API 密钥和基础 URL 导出为环境变量：
```bash
export SURE_API_KEY="YOUR_API_KEY"
export SURE_BASE_URL="YOUR_BASE_URL"
```

## 获取账户信息
列出所有账户的余额信息
```bash
curl -H "X-Api-Key: $SURE_API_KEY" "$SURE_BASE_URL/api/v1/accounts"
```