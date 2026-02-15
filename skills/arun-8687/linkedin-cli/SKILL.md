---
name: linkedin-cli
description: 一个类似LinkedIn的命令行工具（CLI），支持通过会话cookie搜索用户资料、查看消息以及汇总用户信息流（feed）。
homepage: https://github.com/clawdbot/linkedin-cli
metadata: {"clawdbot":{"emoji":"💼","requires":{"bins":["python3"],"env":["LINKEDIN_LI_AT","LINKEDIN_JSESSIONID"]}}}
---

# LinkedIn CLI (lk)

这是一个简洁、实用的LinkedIn命令行工具（CLI），其设计灵感来源于`bird` CLI。该工具使用会话cookie进行身份验证，支持自动化地浏览个人资料、查看动态摘要以及检查消息，而无需使用浏览器。

## 设置

1. **提取Cookie**：在Chrome或Firefox中打开LinkedIn。
2. 转到**开发者工具（F12）** -> **应用程序** -> **Cookie** -> `www.linkedin.com`。
3. 复制`li_at`和`JSESSIONID`的值。
4. 将这些值设置到你的环境变量中：
    ```bash
    export LINKEDIN_LI_AT="your_li_at_value"
    export LINKEDIN_JSESSIONID="your_jsessionid_value"
    ```

## 使用方法

- `lk whoami`：显示你当前的个人资料信息。
- `lk search "query"`：根据关键词搜索用户。
- `lk profile <public_id>`：获取特定用户的详细个人资料信息。
- `lk feed -n 10`：汇总你时间线上的前N条动态。
- `lk messages`：快速查看你最近的聊天记录。
- `lk check`：同时显示你的个人资料信息和聊天记录。

## 依赖项

需要`linkedin-api` Python包：
```bash
pip install linkedin-api
```

## 开发者

- 由Fido 🐶开发