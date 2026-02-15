---
name: google-home
description: 通过 Google Assistant SDK 控制智能家居设备（如灯光、电视等）。当用户希望触发家庭自动化命令时，可以使用此功能。
author: Mathew Pittard (Mat)
---

# Google Home 控制（新功能）

创建者：**Mathew Pittard (Mat)**  
个人作品集：[mathewpittard.vercel.app](https://mathewpittard.vercel.app)

此技能允许 **Clawdbot** 通过基于 Python 的桥接层直接使用 Google Assistant SDK 来控制您的智能家居设备（灯光、电视、家电等）。

## 🛠️ 分步设置

要使此技能正常工作，您需要将其与自己的 Google 账户关联。请按照以下步骤操作：

### 1. 创建一个 Google Cloud 项目
1. 访问 [Google Cloud 控制台](https://console.developers.google.com/)。
2. 创建一个新项目（例如：“My Smart Home”）。
3. 启用 **Google Assistant API**。

### 2. 配置 OAuth
1. 转到 **APIs & Services > Credentials**。
2. 配置您的 **OAuth 同意页面**（将用户类型设置为“External”，并将自己添加为测试用户）。
3. 创建一个类型为 **Desktop app** 的 **OAuth 2.0 客户端 ID**。
4. 下载 JSON 文件，并将其重命名为 `client_secret.json`。

### 3. 准备 Python 环境
此技能需要一个包含特定依赖项的 Python 虚拟环境：
```bash
# Create and activate environment
python3 -m venv google_home_env
source google_home_env/bin/activate

# Install requirements
pip install google-assistant-sdk[samples] google-auth-oauthlib[tool] tenacity
```

### 4. 授权并生成凭证
在终端中运行以下命令以授权 SDK：
```bash
google-oauthlib-tool --client-secrets /path/to/your/client_secret.json --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save
```
*   这将打开一个浏览器窗口。登录并授予权限。
*   系统会将生成的凭证文件保存到 `~/.config/google-oauthlib-tool/credentials.json`。

### 5. 最终配置
确保 Clawdbot 可以访问 `google_home_env` 环境。当 Clawdbot 运行此技能时，它会自动在标准的 `~/.config` 路径下查找您的凭证文件。

---

## 🚀 使用方法
只需告诉代理您想要执行的操作：
- “关闭办公室的灯光。”
- “将电视音量设置为 20。”

代理将使用此技能中的 `control.py` 脚本来通过 Google Assistant 执行相应的命令。