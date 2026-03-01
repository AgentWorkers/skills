---
name: zentable
description: "ZenTable工作流程的文档/适配器包。运行时代码通过GitHub上的固定版本（ pinned release）提供。"
homepage: https://github.com/con2000us/zenTable
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3", "google-chrome"]
allowed-tools: ["exec", "read", "write"]
---
# ZenTable 技能（ClawHub 仅文本格式的包）

## 包类型

为了与当前的 ClawHub 验证器保持兼容性，此包被设计为 **仅文本格式**。它提供了工作流程说明和政策，而可运行的源代码则通过 GitHub 上的固定版本进行分发。

## 简而言之

ZenTable 帮助代理将杂乱无章的表格内容转换为清晰、适合决策使用的表格格式（支持移动/桌面设备）。

**支持的输入类型：**
- 基于文本的内容（原始文本表格、长篇回复）
- 结构化的 JSON 数据
- 通过 OCR 技术处理的截图/真实照片

**核心输出功能：**
- 使用 CSS 和 PIL 进行渲染
- 支持排序、过滤和分页功能
- 可选的高亮显示功能以及 PNG/TXT 格式的辅助输出

## 运行时与安全注意事项：**
- 运行时代码 **不包含在该仅文本格式的包中**。请仅使用 `INSTALL.md` 文件中指定的固定版本。
- 在首次执行前，请务必检查代码及其依赖项。
- 对于首次设置或执行，需要用户的明确确认。

## 已知的局限性：**
- ASCII 格式的输出目前仍处于测试/实验阶段，可能在不同平台上表现有所不同。
- 目前的验证主要针对 Discord 平台；其他渠道可能需要调整格式设置。

## 联系方式：**
- GitHub 问题报告：https://github.com/con2000us/zenTable/issues
- 维护者：@con2000us（Discord）