---
name: ganidhuz-foxx
description: 🦊 Ganidhuz-FoxX（Firefox与X的结合体，哈哈）。通过注入cookie，利用已登录的Firefox会话来浏览X/Twitter网站。支持查看用户资料、获取推文、搜索以及滚动浏览信息流——无需API密钥，也不会被机器人程序阻止访问。
license: MIT
---
# Ganidhuz-FoxX 🦊

使用 Firefox 和您的真实会话 cookie 浏览 X/Twitter。这个工具的开发是因为 Chromium 经常被 X 系统识别为机器人并阻止访问。

## 必备条件

- Python 3.7 或更高版本
- Playwright 库：`pip install playwright && playwright install firefox`
- 已安装 Firefox 并且已登录 X/Twitter
- （用于无头服务器）安装了 Xvfb 显示器：`Xvfb :1 &`

## 设置

### 1. 导出您的 X cookie

首先关闭 Firefox，然后执行以下操作：

```bash
bash scripts/export-x-cookies.sh
# Cookies saved to secrets/x-cookies.json by default
# Override: FOXX_COOKIES_OUT=/custom/path.json bash scripts/export-x-cookies.sh
```

自定义 Firefox 配置文件路径：
```bash
FIREFOX_PROFILE_PATH=/path/to/profile bash scripts/export-x-cookies.sh
```

### 2. 健康检查

```bash
bash scripts/check-firefox-env.sh
```

## 使用方法

运行一个计划文件（plan file）：

```bash
DISPLAY=:1 python3 scripts/playwright-firefox-control.py --plan /tmp/foxx-plan.json
```

## 计划示例

### 查看个人资料

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/elonmusk",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 4000},
    {"action": "screenshot", "path": "/tmp/foxx-profile.png"}
  ],
  "close_delay_ms": 3000
}
```

### 实时搜索推文

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/search?q=AI+agents&src=typed_query&f=live",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 4000},
    {"action": "screenshot", "path": "/tmp/foxx-search.png"}
  ],
  "close_delay_ms": 3000
}
```

### 获取推文内容

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/user/status/123456789",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 3000},
    {"action": "content", "selector": "article"},
    {"action": "screenshot", "path": "/tmp/foxx-tweet.png"}
  ],
  "close_delay_ms": 3000
}
```

## 计划选项

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `needs_gui` | 必需 | 必须设置为 `true` 才能启动浏览器 |
| `gui_reason` | 必需 | 可选值：`login`（登录）、`captcha`（验证码）、`mfa`（多因素认证）、`visual_verification`（视觉验证）、`site_only_action`（仅网站操作） |
| `url` | 必需 | 要访问的 URL |
| `cookies_path` | 可选 | 导出后的 cookie JSON 文件路径 |
| `close_delay_ms` | `3000` | 关闭浏览器前的等待时间（毫秒）——先验证结果 |
| `validation_screenshot` | `/tmp/firefox-openclaw-validate.png` | 关闭前自动截取的最终截图 |
| `storage_state_path` | 可选 | 运行后保存会话状态的路径 |

## 支持的步骤操作

- `goto` - 导航到指定 URL
- `click` - 根据选择器点击元素
- `fill` - 根据选择器填写输入框内容
- `type` - 带延迟地输入文本
- `press` - 按下键盘键
- `wait` - 等待指定时间（毫秒）
- `wait_for_selector` - 等待指定元素出现
- `screenshot` - 截取屏幕截图
- `content` - 从元素中提取文本内容

## 行为规则

- 必须等待页面加载完成（建议至少等待 3000 毫秒）
- 关闭浏览器前一定会截取验证截图
- 浏览器会在 `close_delay_ms` 毫秒后关闭——确保结果正确
- 如果 cookie 过期（导致需要重新登录），请重新运行 `export-x-cookies.sh` 命令
- 任务完成后一定会关闭浏览器——避免浏览器处于空闲状态