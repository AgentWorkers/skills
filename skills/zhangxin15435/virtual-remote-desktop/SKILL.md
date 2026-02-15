---
name: virtual-remote-desktop
description: 在无头 Linux 系统上，使用 Xvfb、x11vnc 以及基于令牌认证的 noVNC Web 代理来启动和管理一个安全的虚拟桌面。该虚拟桌面可用于远程图形登录、验证码处理，以及执行虚拟桌面的启动、停止、状态检查与健康监控等操作。
read_when:
  - User asks for noVNC remote login on headless Linux
  - User needs visual captcha handling on server
  - User asks to start, stop, inspect, or health-check virtual desktop
metadata:
  {"clawdbot":{"emoji":"🖥️","requires":{"bins":["Xvfb","fluxbox","x11vnc","node","python3"],"paths":["/root/.openclaw/workspace/novnc-web"],"optionalBins":["google-chrome","chromium","/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"]},"safety":{"persists":["WORKDIR/logs","WORKDIR/chrome-profile","WORKDIR/pids.env","WORKDIR/vncpass","WORKDIR/access.token"],"network":["api.ipify.org","ifconfig.me","checkip.amazonaws.com"],"disclosure":"Stores browser profile data (cookies/session) for persistence. Run only on trusted hosts."}}}
---

# 虚拟远程桌面（noVNC）

## 使用方法（最少步骤）

1) 启动：

```bash
bash /root/.openclaw/workspace/skills/virtual-remote-desktop/scripts/start_vrd.sh
```

2) 打开输出中的“一键访问链接”，然后输入“VNC密码”。

3) 登录后，检查状态和运行情况：

```bash
bash /root/.openclaw/workspace/skills/virtual-remote-desktop/scripts/status_vrd.sh
bash /root/.openclaw/workspace/skills/virtual-remote-desktop/scripts/health_vrd.sh
```

4) 停止：

```bash
bash /root/.openclaw/workspace/skills/virtual-remote-desktop/scripts/stop_vrd.sh
```

## 常见配置选项

- `CHROME_PROFILE_DIR`：Chrome 配置文件的持久化存储目录（默认为 `${WORKDIR}/chrome-profile`）
- `AUTO_LAUNCH_URL`：启动后自动打开的 URL
- `AUTO_STOP Idle_SECS`：空闲时的自动停止超时时间（以秒为单位，默认为 900 秒）
- `NOVNC_BIND`：监听地址（默认为 `0.0.0.0`）
- `ACCESS_TOKEN_TTL_SECS`：访问令牌的有效期（以秒为单位，默认为 86400 秒）

## 安全性与数据持久化说明

- 默认使用随机生成的 `VNC_PASSWORD` 并通过令牌进行访问控制。
- 访问令牌存储在 `WORKDIR/access.token` 文件中，文件权限设置为 `600`（而非以明文形式保存在 `pids.env` 文件中）。
- 登录信息会尽可能地保存在 `CHROME_PROFILE_DIR` 中，但会话的持续时间仍取决于目标网站的认证/会话策略。