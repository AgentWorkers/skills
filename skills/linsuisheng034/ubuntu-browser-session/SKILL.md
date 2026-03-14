---
name: ubuntu-browser-session
description: >
  **使用场景：**  
  当需要一个可重复使用的 Ubuntu Server 浏览器会话时，该会话支持可选的辅助登录功能以及主机端的页面检查功能。
---
# Ubuntu 浏览器会话

适用于 Ubuntu Server 主机的可重用浏览器会话工作流程。

## 使用场景

- 从无头（headless）的 Ubuntu Server 主机中打开或查看页面
- 重用已验证的浏览器会话，而无需重新启动
- 当本地重用不足以满足需求时，请求用户进行辅助登录
- 在浏览器会话准备好后，从主机端检查页面的可见状态

## 工作流程

推荐的入口脚本：

```bash
{baseDir}/scripts/open-protected-page.sh --url 'https://target.example' --session-key default
```

仅在需要检查或修复某个具体步骤时，才使用较低级别的辅助脚本：

```bash
{baseDir}/scripts/session-manifest.sh select --origin 'https://target.example'
{baseDir}/scripts/browser-runtime.sh verify --origin 'https://target.example' --session-key default
{baseDir}/scripts/assisted-session.sh start --url 'https://target.example' --origin 'https://target.example' --session-key default
```

## 环境要求

```bash
command -v python3
command -v curl
command -v jq
command -v Xvfb
command -v x11vnc
command -v websockify
command -v google-chrome || command -v chromium || command -v chromium-browser
```

## 关键文件

- `scripts/open-protected-page.sh`：高级会话管理脚本
- `scripts/browser-runtime.sh`：浏览器运行时管理脚本
- `scripts/assisted-session.sh`：辅助浏览器会话管理脚本
- `scripts/session-manifest.sh`：会话记录管理脚本
- `scripts/cdp-eval.py`：主机端页面检查辅助脚本

另请参阅：

- `references/session-manifest.md`
- `references/assisted-session-flow.md`