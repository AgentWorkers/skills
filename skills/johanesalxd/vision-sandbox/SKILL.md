---
name: Vision Sandbox
slug: vision-sandbox
version: 1.1.0
description: 通过 Gemini 的原生代码执行沙箱实现“代理视觉”（Agentic Vision）功能。该功能可用于空间定位（spatial grounding）、视觉计算（visual math）以及用户界面（UI）审计（UI auditing）。
metadata:
  openclaw:
    emoji: "🔭"
    primaryEnv: "GEMINI_API_KEY"
    requires:
      bins: ["uv"]
      env: ["GEMINI_API_KEY"]
---

# Vision Sandbox 🔭

利用 Gemini 的原生代码执行功能，以高精度分析图像。该模型在 Google 托管的沙箱环境中编写和运行 Python 代码，用于验证视觉数据，非常适合进行用户界面（UI）审计、空间定位以及视觉推理。

## 安装

```bash
clawhub install vision-sandbox
```

## 使用方法

```bash
uv run vision-sandbox --image "path/to/image.png" --prompt "Identify all buttons and provide [x, y] coordinates."
```

## 模式库

### 📍 空间定位
要求模型找到特定对象并返回其坐标。
* **提示语：**“在这张截图中找到‘Submit’按钮。使用代码执行功能验证其中心点，并以 [0, 1000] 的比例返回 [x, y] 坐标。”

### 🧮 视觉计算
要求模型根据图像进行计数或计算。
* **提示语：**“计算列表中的项目数量。如果价格信息可见，请使用 Python 对这些价格进行求和。”

### 🖥️ UI 审计
检查布局和可读性。
* **提示语：**“检查标题文本是否与任何图标重叠。使用沙箱功能计算边界框的交集。”

### 🖐️ 计数与逻辑
通过代码验证来解决视觉计数任务。
* **提示语：**“数一数这只手上有多少根手指。使用代码执行功能为每根手指确定边界框，并返回总数。”

## 与 OpenCode 的集成
此技能专为自动化编码工具（如 OpenCode）提供 **视觉定位** 功能：
- **步骤 1：** 使用 `vision-sandbox` 提取 UI 元数据（坐标、大小、颜色）。
- **步骤 2：** 将 JSON 输出结果传递给 OpenCode，以生成或修改 CSS/HTML 代码。

## 配置参数
- **GEMINI_API_KEY**：必需的环境变量。
- **模型**：默认值为 `gemini-3-flash-preview`。