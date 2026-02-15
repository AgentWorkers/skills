---
name: camoufox
version: 1.0.0
description: 使用 Camoufox（基于 Firefox 的工具）来规避浏览器自动化检测。在需要应对大量机器人检测的网站（如 X/Twitter、Naver 等受保护的网站）上，建议使用 Camoufox 代替 Chrome 或 Playwright。Camoufox 提供了隐秘浏览功能，包括伪造操作系统和浏览器的特征信息、模拟自然的人类鼠标操作方式以及保持会话的持续性。
---

# Camoufox

**用于替代 OpenClaw 内置的浏览器工具，以检测机器人访问的网站。**

## 设置（一次性操作）
```bash
bash scripts/setup.sh
```

## 使用方法
```bash
source ~/.openclaw/workspace/camoufox-env/bin/activate
xvfb-run -a --server-args="-screen 0 1920x1080x24" python3 your_script.py
```

## 必需的设置
```python
from camoufox.sync_api import Camoufox

with Camoufox(
    headless=False,      # MUST be False (True gets detected)
    os='linux',          # MUST match server OS (stack traces leak real OS)
    humanize=True,
    persistent_context=True,
    user_data_dir='~/.openclaw/camoufox-profile'
) as browser:
    page = browser.new_page()
    # Use standard Playwright API from here
```

## 路径配置
- 环境变量：`~/.openclaw/workspace/camoufox-env/`
- 配置文件：`~/.openclaw/camoufox-profile/`

## 图形验证码处理
首次访问受保护的网站时可能需要手动输入图形验证码：
```bash
DISPLAY=:1 python3 scripts/login_session.py https://site.com/login
```
可以通过 VNC 进行操作，会话信息会保存在配置文件中，以便后续自动化使用。

## 脚本
- `scripts/setup.sh` - 安装依赖项
- `scripts/browse.py <url> --screenshot out.png` - 快速浏览网站并生成截图
- `scripts/login_session.py <url>` - 通过 VNC 手动登录网站