---
name: toutiao-publisher
description: 将文章发布到今日头条（Toutiao）。支持持久化认证（只需登录一次）和会话管理功能。发布完成后会自动打开浏览器进行交互式操作。
---
# Toutiao 发布器技能

用于管理 Toutiao（今日头条）账户、保持登录状态，并发布文章。

## 何时使用此技能

当用户执行以下操作时触发：
- 请求向 Toutiao/今日头条发布内容
- 希望管理 Toutiao 账户登录信息
- 提到 “toutiao” 或 “头条号”

## 核心工作流程

### 第 1 步：身份验证（一次性设置）

该技能需要用户进行一次登录。登录状态会保存下来，以便后续使用。

```bash
# Browser will open for manual login (scan QR code)
python scripts/run.py auth_manager.py setup
```

**操作说明：**
1. 运行设置命令。
2. 浏览器窗口将打开，加载 Toutiao 的登录页面。
3. 手动登录（例如：扫描二维码）。
4. 登录成功后（会被重定向到控制面板），脚本会保存登录状态并关闭窗口。

### 第 2 步：发布文章

```bash
# Opens browser with authenticated session at publish page
python scripts/run.py publisher.py
```

**操作说明：**
1. 运行发布命令。
2. 浏览器会直接打开 “发布文章” 页面。
3. 手动撰写并发布文章。
4. 完成后，在终端中按 `Ctrl+C` 键。

> **注意：** Toutiao 要求文章标题长度在 2 到 30 个字符之间。此工具会自动优化标题长度以符合这一要求（超过 30 个字符时会截断，少于 2 个字符时会补全）。

#### 高级用法（自动化）

通过提供参数，您可以完全自动化发布过程：

```bash
# Publish with title, content file, and cover image
python scripts/run.py publisher.py --title "AI Trends 2025" --content "article.md" --cover "assets/cover.jpg" --headless
```

### 管理

```bash
# Check authentication status
python scripts/run.py auth_manager.py status

# Clear authentication data (logout)
python scripts/run.py auth_manager.py clear
```

## 技术细节

- **持久化登录**：使用 `patchright` 功能来创建一个持久的浏览器会话。Cookie 和存储状态会被保存到 `data/browser_state/state.json` 文件中。
- **反检测**：利用 `patchright` 的隐蔽功能来避免被机器人检测到。
- **环境管理**：自动管理包含所需依赖项的虚拟环境（`.venv`）。

## 脚本参考

- `scripts/auth_manager.py`：处理登录、会话验证和状态保存。
- `scripts/publisher.py`：启动已认证的浏览器以进行发布操作。
- `scripts/run.py`：作为封装脚本，确保在正确的虚拟环境中执行所有操作。