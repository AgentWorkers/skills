---
name: flutter-appstore-doc-ui-kit
description: Generate a launch-ready app package for App Store submission: a complete Markdown feature document plus AI-generated Apple-style UI design images for each page and a square-corner app icon. Use when the user wants a Flutter app concept/spec constrained to FVM Flutter 3.35.1, offline-first (no backend), camera + photo library permissions, anti-saturation positioning, and no TODO/temp placeholders.
---

# Flutter AppStore 文档与 UI 套件

我们将分阶段生成适用于 App Store 的项目包，并在每个阶段要求用户进行审核：

- `docs/app-feature-spec.zh-CN.md` + `docs/app-feature-spec.en-US.md`（应用程序功能规范文档，中英文版本）
- `ui/*.png`（由 AI 生成的 Apple 风格页面设计图片）
- `icon/app_icon_1024.png` + `icon/app_icon_1024.svg`（方形角的 App 图标）

## 工作流程（需用户审核通过）

1. 生成中英文版本的应用程序功能规范文档，并将其输出。
2. 请求用户下载并审核文档；等待用户选择“继续”或“修改文档”。
3. 仅在用户明确批准文档后，才能进入下一阶段。
4. 检查图片生成能力：
   - 如果有 API 或模型访问权限，根据已批准的文档生成页面级别的 UI 图片。
   - 如果没有 API 或模型访问权限，为用户提供统一的样式提示包，以便他们在外部工具中生成图片。
5. 请求用户下载并审核 UI 图片。
6. 仅在用户明确批准 UI 图片后，才能进入下一阶段。
7. 检查图标生成能力：
   - 如果有 API 或模型访问权限，使用模型生成图标。
   - 如果没有 API 或模型访问权限，通过程序化的 SVG 到 PNG 的流程生成图标。
8. 请求用户审核图标。
9. 仅在用户明确批准图标后，才能完成整个流程。

请勿自动跳过任何审核步骤。如果用户要求修改，请仅修改相应阶段的内容，然后重新提交审核。

## 1) 必需输入信息

收集/确认以下信息：
- 应用程序名称
- 目标语言
- 偏好的应用程序方向（如果没有指定，选择饱和度较低的工具类应用方向）
- 可选的颜色风格

必须遵守的硬性要求：
- 技术栈：使用 **FVM Flutter 3.35.1** 构建应用程序
- 应用程序必须包含 **相机** 和 **照片库** 的权限
- 避免使用过于饱和的应用类别，以及可能引发风险的应用描述
- 不需要后端服务器
- 不允许使用 TODO 占位符或临时/虚假数据
- 仅关注第一版本的完整功能（不包括未来的开发计划）
- 可以包含以下通用功能：国际化（i18n）、暗模式、无障碍访问、以用户隐私优先的本地存储
- App 图标必须是 **方形角**（非圆形）

## 2) 第 1 阶段 — 生成并交付功能文档（中英文）

执行一次以下操作：

```bash
python3 scripts/generate_appstore_pack.py \
  --app-name "SnapSort" \
  --out ./out/snapsort \
  --locales "en,zh-Hans" \
  --primary-color "#0A84FF"
```

然后首先准备文档输出，并仅提交文档供审核：
- `docs/app-feature-spec.zh-CN.md`（如果不存在，根据基础规范生成中文版本）
- `docs/app-feature-spec.en-US.md`（如果不存在，根据基础规范生成英文版本）

如果生成工具只生成一个基础规范文件，请在发送给用户之前将其拆分为两个语言版本。

## 3) 第 2 阶段 — 生成并交付 UI 设计图片

在用户审核通过文档后，首先检查相关功能是否可用。

### 选项 A：有 API 或模型访问权限
使用 `scripts/generate_ui_ai.py` 脚本。

所需认证信息：
- 环境变量中的 `OPENAI_API_KEY`（或用户配置的其他图像模型后端）

示例：

```bash
python3 scripts/generate_ui_ai.py \
  --doc ./out/snapsort/docs/app-feature-spec.en-US.md \
  --out ./out/snapsort/ui \
  --primary-color "#0A84FF"
```

输出结果：
- `ui/page-01-*.png` ... `ui/page-08-*.png`（一系列页面设计图片）

### 选项 B：没有 API 或模型访问权限
为用户提供一个统一的样式提示包（包含全局样式和 8 个页面的提示），以便他们在外部工具中手动生成图片。
然后收集用户生成的图片，并进入 UI 审核阶段。

此阶段不交付 App 图标。

## 4) 第 3 阶段 — 生成并交付 App 图标

在用户审核通过 UI 图片后，首先检查相关功能是否可用。

### 选项 A：有 API 或模型访问权限
使用模型生成图标，并导出 PNG 格式的图标。

### 选项 B：没有 API 或模型访问权限
通过程序化的流程（SVG 源文件 + PNG 输出格式）生成图标。

交付的图标文件包括：
- `icon/app_icon_1024.png`
- `icon/app_icon_1024.svg`

## 5) 质量验证

在每个审核步骤之前，验证相关阶段的输出文件是否完整：
- 中英文版本的功能规范文档都已生成，并且在语义上保持一致。
- 功能规范文档中明确指出使用的是 FVM Flutter 3.35.1。
- 功能和隐私相关部分中包含了相机及照片库的权限说明。
- 架构和数据流中不存在对后端服务器的依赖。
- 文档中不包含 TODO、待办事项、临时内容或占位符。

### UI 阶段：
- UI 图片为 PNG 格式（由 AI 生成或用户根据提示包生成）。
- UI 图片涵盖了规范中列出的所有关键页面。
- 图标上的标签和界面布局与文档中的描述一致。

### 图标阶段：
- 图标的形状为正方形（没有圆形边缘）。
- 图标的风格与批准的产品方向一致。

## 6) App Store 安全性指导

请参考 `references/review-safety-checklist.md` 并严格遵守以下指导原则：
- 不得包含任何医疗、财务或法律方面的保证声明。
- 不得使用“立即盈利”或具有误导性的表述。
- 权限的使用必须与用户明确触发的操作相关联。
- 隐私相关的内容必须以用户为中心，并且用户可以自行控制。

## 注意事项

- 本任务仅负责生成设计文档和规范文件，不涉及 Flutter 代码的编写。
- 如果用户还需要应用程序的实现框架，请创建一个单独的 Flutter 开发任务。