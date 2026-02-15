---
name: auto-reply
description: "Instagram私信自动回复系统：用于监控、阅读、回复私信以及进行安全检查（防止恶意代码注入）。适用于检查Instagram私信、阅读未读消息、回复私信、设置私信监控任务，或处理私信自动回复流程。触发事件包括：收到私信、检查私信状态、回复私信以及触发私信自动回复功能。"
author: 무펭이 🐧
---

# Instagram 私信自动回复 🐧

该功能基于 v2.js（内部 API）实现，不使用浏览器快照，而是直接通过 Instagram 的 REST API 进行操作。

## 先决条件

- OpenClaw 浏览器已启动（端口 18800）  
- Instagram 页面已打开并登录  
- `ws` npm 包已安装（通过 `npm i -g ws` 获取，或使用本地版本）  

## 脚本列表

| 脚本 | 功能 |  
|--------|---------|  
| `scripts/v2.js` | 私信管理 CLI（查看收件箱、未读消息、检查、阅读、回复）  
| `scripts/auto-reply.js` | 读取 `dm-alert.json` 文件，进行安全检查，并返回回复元数据  
| `scripts/check-notify.js` | 检查新的私信通知（基于定时任务或状态文件）  
| `scripts/dm-watcher.js` | 实时私信检测守护进程（每 15 秒轮询一次）  

## 核心工作流程

### 1. 检查私信  
```bash
node scripts/v2.js check        # unread count (lightest)
node scripts/v2.js unread       # unread DM list
node scripts/v2.js inbox        # full DM list
```  

### 2. 阅读消息  
```bash
node scripts/v2.js read "<username>" -l 5
```  

### 3. 回复私信  
```bash
node scripts/v2.js reply "<username>" "message content"
```  

如果 API 请求失败，会返回一个 JSON 对象，其中包含 `method: "use_browser"` 和 `threadUrl`，此时系统会回退到浏览器工具进行处理。  

### 4. 通知检查（集成定时任务）  
```bash
node scripts/check-notify.js
```  
- 如果有新私信：输出 `📩 新私信 N 条：...`  
- 如果没有新私信：输出 `no_new`  
- 使用 `dm-state.json` 状态文件来避免重复通知。  

### 5. 自动回复流程  
```bash
node scripts/auto-reply.js
```  
1. 读取由 `dm-watcher` 生成的 `dm-alert.json` 文件  
2. 对每条私信进行安全检查  
3. 根据检查结果返回 `needs_reply`、`security_alert` 或 `skipped`  
4. 对需要回复的私信，使用 AI 生成回复内容，并通过 `v2.js` 发送。  

### 6. 实时检测守护进程  
```bash
node scripts/dm-watcher.js              # detection only
node scripts/dm-watcher.js --auto-reply  # includes Discord notification
```  
每 15 秒轮询一次 `v2.js` 的检查结果。检测到新私信时，会更新 `dm-alert.json` 文件并通过 Discord 发送通知。  

## 安全检查（防止恶意注入）  
`auto-reply.js` 中的 `SECURITY_PATTERNS` 能识别以下恶意行为：  
- **提示注入**：`ignore previous`、`system prompt`、`you are now`、`act as`、`pretend`  
- **越狱尝试**：`override`、`jailbreak`、`DAN mode`、`bypass`  
- **敏感信息请求**：`secret key`、`private key`、`seed phrase`、`wallet address`  
- **代码执行尝试**：`execute command`、`run script`、`eval()`、`rm -rf`、`sudo`  
- **社会工程学攻击**：`simulation mode`、使用零宽度字符  

检测到恶意行为时，系统不会回复私信，而是返回 `security_alert` 并发送单独的通知。  

## 定时任务设置示例  
```yaml
# Check DMs every 5 minutes
- schedule: "*/5 * * * *"
  command: "node /path/to/scripts/check-notify.js"
  systemEvent: true

# Or dm-watcher daemon for continuous monitoring
- schedule: "@reboot"
  command: "node /path/to/scripts/dm-watcher.js --auto-reply"
  background: true
```  

## 令牌使用效率  
- 查看收件箱：约 500 个令牌  
- 回复私信：约 200 个令牌  
- 浏览器快照：不消耗令牌  

---
> 🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统的一部分