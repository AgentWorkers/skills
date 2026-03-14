# Vheer Automation Skill

使用 Vheer.com 的浏览器界面实现自动化图像生成。

## 🌟 概述
该技能利用 **Playwright** 来自动化 Vheer.com 上的文本到图像的转换过程。它直接与网页界面进行交互，无需手动管理 Cookie 或进行复杂的 API 反向工程。

## 🛠 功能特点
- **无头模式生成**：可以在后台运行或以可见模式运行。
- **动态提示**：可以通过命令行传递任何提示内容。
- **自动输出**：将生成的图像直接保存到本地机器。
- **持久会话**：支持用户数据目录，以保持登录状态。

## 🚀 使用方法

### 1. 安装
确保已安装所有必要的依赖项：
```bash
python3 -m pip install playwright
playwright install chromium
```

### 2. 生成图像
使用所需的提示内容运行脚本：
```bash
python3 scripts/vheer_automation.py "A majestic phoenix rising from the ashes, cinematic lighting"
```

### 3. 命令行选项
- `-o`, `--output`：指定输出文件名（默认：`vheer_output.png`）。
- `--headful`：以可见模式运行浏览器（便于调试）。
- `--user-data`：浏览器配置文件的路径（用于保持登录状态）。

## 📂 项目结构
- `scripts/vheer_automation.py`：统一的自动化脚本。
- `vheer_output.png`：生成的图像的默认保存位置。

## 💡 工作原理
脚本会启动一个 Chromium 实例，导航到 Vheer 的文本到图像转换页面，填写提示框的内容，然后触发图像生成过程。当“处理中...”状态完成后，脚本会截取最终图像的屏幕截图，从而规避 `blob:` URL 的限制。