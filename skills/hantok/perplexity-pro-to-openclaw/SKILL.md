---
name: perplexity-pro-openclaw
description: 将 Perplexity PRO 通过反机器人浏览器自动化工具连接到 OpenClaw，利用 Xvfb 和 VNC 认证绕过 Cloudflare 的保护机制。
homepage: https://github.com/Hantok/Perplexity-PRO-to-OpenClaw
metadata:
  clawdbot:
    emoji: "🔍"
  requires:
    env: ["DISPLAY"]
  files: ["scripts/*"]
version: 1.0.0
---
# OpenClaw的Perplexity PRO技能

该技能允许OpenClaw使用持久的、经过身份验证的会话来搜索Perplexity PRO，通过无法被检测到的浏览器自动化技术绕过Cloudflare的安全防护。

## 该技能的功能

- ✅ 绕过Cloudflare的机器人检测（使用Xvfb和隐身模式的Chrome浏览器）
- ✅ 在重启后保持Perplexity PRO会话的持久性
- ✅ 提供VNC访问功能以进行手动OAuth身份验证
- ✅ 为OpenClaw代理程序提供自动搜索功能

## 先决条件

- Ubuntu Server（无显示器版本或带显示器的版本）
- 已安装并配置好的OpenClaw
- Google Chrome（非Snap版本）
- Xvfb软件包
- x11vnc软件（用于远程访问）

## 交互式设置步骤

在安装过程中，代理程序将指导您完成以下步骤：

### 第1步：安装Chrome浏览器
代理程序会帮助您卸载Snap Chromium并安装正确的Google Chrome浏览器：
```bash
sudo snap remove chromium
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### 第2步：设置浏览器启动器
代理程序会创建`start-stealth-browser.sh`脚本，其中包含以下设置：
- 使用Xvfb虚拟显示器（以绕过无显示器模式的检测）
- 将会话信息保存在`~/.openclaw/browser-profile/`目录中
- 使用隐身模式来隐藏自动化操作的痕迹

### 第3步：配置VNC
代理程序会设置x11vnc以支持远程浏览器访问：
```bash
sudo apt-get install -y x11vnc
x11vnc -storepasswd openclaw /tmp/vncpass
```

**⚠️ 安全提示：** 默认的VNC密码是“openclaw”——在生产环境中请务必更改此密码！

### 第4步：手动身份验证（必选）
**您需要通过VNC进行手动身份验证：**

1. 通过VNC连接（macOS：`open vnc://your-server:5900`；Windows：RealVNC Viewer）
2. 在浏览器中打开Perplexity.ai网站
3. 点击“使用Google登录”
4. 直接输入您的电子邮件地址和密码
5. 如果启用了两步验证，请完成验证流程

**重要提示：** 应用程序密码无法用于Web身份验证，请使用您的真实Google密码。

## 使用方法

设置完成后，您可以使用该技能搜索Perplexity PRO：

```bash
# Via skill script
./scripts/start-stealth-browser.sh

# Search Perplexity
openclaw browser open "https://www.perplexity.ai/search?q=your+query"
```

## 文件结构

```
perplexity-pro-openclaw/
├── SKILL.md          # This file - skill metadata and setup
├── README.md         # Detailed installation guide
├── scripts/
│   └── start-stealth-browser.sh  # Browser launcher
└── CHANGELOG.md      # Version history
```

## 防止机器人攻击的技术（共7层）

1. **浏览器指纹伪装** - 使用`--disable-blink-features=AutomationControlled`选项
2. **会话持久化** - 会话信息保存在`~/.openclaw/browser-profile/`目录中（而非/tmp目录）
3. **使用Xvfb虚拟显示器** - 显示真实的Chrome浏览器窗口，而非无显示器模式
4. **真实的屏幕分辨率** - 1920x1080分辨率
5. **禁用自动化相关功能** - 关闭后台自动化操作
6. **持久化Cookie** - 会话信息在浏览器重启后仍然保留
7. **FlareSolverr**（可选） - 用于极端情况

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| Chrome显示为“HeadlessChrome” | 确保Xvfb正在运行，且未使用`--headless`选项 |
| Cloudflare仍然阻止访问 | 更新Chrome浏览器，并检查所有隐身模式相关设置 |
| VNC连接失败 | 使用`ss -tlnp \| grep 5900`命令检查网络连接；检查防火墙设置 |
| Perplexity要求再次登录 | 检查会话配置文件问题，通过VNC重新进行身份验证 |

## 安全注意事项

- 请将VNC密码从默认的“openclaw”更改为其他安全密码
- 会话配置文件保存在`~/.openclaw/browser-profile/`（用户主目录下，而非/tmp目录）
- OAuth令牌会持续保存在系统中——请确保服务器的安全性
- VNC传输的数据默认是未加密的——建议使用SSH隧道进行远程访问

## 作者

该技能由[rundax.com](https://rundax.com)开发

属于OpenClaw生态系统的一部分——[ClawHub](https://clawhub.com)