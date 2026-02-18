---
name: hwpx_my
description: "用于创建、读取、编辑 HWPX 文档（.hwpx 文件）以及进行模板替换的技能。该技能专注于韩文 HWPX 格式，提供了基于模板的替换工作流程。"
---
# hwpx_my

HWPX 文档生成与编辑技能（hwpx_my）

该技能支持通过 ZIP 级别的替换操作来生成基于模板的文档。默认提供的模板为 `assets/report-template.hwpx`。用户上传的模板应放置在 `uploads/` 文件夹中。生成后的文档会保存在 `outputs/` 文件夹中。

命令：
- `analyze-template <path>`：提取模板中的文本占位符。
- `apply-template <template> <mapping.json> <out.hwpx>`：根据提供的 `mapping.json` 文件进行替换，并将结果保存到 `outputs/` 文件夹中。

注意事项：
- 如需使用 ObjectFinder 的全部功能，请安装 `python-hwpx`；如果 `python-hwpx` 无法使用，`lib/hwpx_shim.py` 提供了一个轻量级的替代方案。

许可证：MIT