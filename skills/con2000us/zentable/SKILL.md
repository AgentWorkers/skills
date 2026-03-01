---
name: zentable
description: "使用无头版Chrome（Headless Chrome）将结构化表格数据渲染为高质量的PNG图像。适用场景：需要为聊天界面、报告或社交媒体可视化表格数据的情况。不适用场景：不需要可视化的简单文本表格。"
homepage: ~/.openclaw/custom-skills/zentable/SKILL.md
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3", "google-chrome"]
allowed-tools: ["exec", "read", "write"]
---
# ZenTable 技能

该技能可将结构化表格数据渲染为高质量的 PNG 图像。

## 命名规范

- 标准代码名称：`zentable`（小写）
- 用户界面/品牌名称：`ZenTable`
- `zeble*` / `zenble*` 是旧的兼容性别名
- 详细说明请参考：`/var/www/html/zenTable/NAMING_MIGRATION.md`

## 适用场景

✅ 当您需要表格的可视化图像而非纯文本时；
✅ 当您需要用于聊天、报告或社交分享的精美输出时；
✅ 当数据集量较大，纯文本难以阅读时；
✅ 当您需要特定的视觉样式（如 iOS 风格、深色主题、紧凑布局等）时。

❌ 以下情况请勿使用该技能：
- 表格内容非常简短，纯文本即可满足需求；
- 用户明确要求不生成图像输出；
- 用户需要可编辑的电子表格格式（如 CSV/Excel）。

## 功能矩阵（SkillHub 版本）

| 功能          | 状态    | 备注                |
|---------------|--------|-------------------|
| CSS 格式输出       | ✅      | 主要输出格式；默认设置为 `minimal_ios_mobile` 且宽度为 450 像素 |
| PIL 格式输出       | ✅      | 当 Chrome 浏览器不可用时的安全备用方案 |
| ASCII 格式输出     | ⚠️  测试中/实验性 | 可正常工作，但不同平台间的对齐效果可能因字体和空白处理方式而有所不同 |

## 已知限制

- ASCII 格式输出受平台字体设置和空白处理方式的影响较大；
- 需为每个平台创建单独的校准配置文件，切勿盲目共享；
- 选项 `--both` 会在没有指定文本主题时自动使用默认主题；
- 在 Discord 中，连续的空格会被合并；为保持间距可能需要使用 Unicode 空格字符；
- 该功能主要在 Discord 上经过验证，其他聊天平台可能需要客户端端的格式调整。

## Zx 缩写规则（项目规定）

当用户输入 `Zx` 时，视为强烈的渲染请求：

1. 默认情况下直接执行渲染操作（无需预先询问用户）；
2. 默认输出格式为 CSS 格式，宽度设置为 450 像素；
3. 仅在以下情况下才进一步询问用户：
   - 当当前或之前的输入数据无法用于渲染；
   - 用户的请求不符合表格渲染的常规需求；
   - 关键信息缺失，可能导致输出错误；
4. 如果目标平台支持图像显示，直接返回图像（而非仅提供链接）。

**Zx 的数据来源优先级：**
1. 当前消息的图像（通过 OCR 技术解析）；
2. 当前消息的文本（转换为表格格式）；
3. 之前消息的图像（通过 OCR 技术解析）；
4. 之前消息的文本（转换为表格格式）。

## 语法简化与标准映射

| 简化形式       | 标准形式            | 处理方式                | 最终渲染参数            |
|--------------|------------------|------------------|-------------------|
| `--width N`     | `width`             | 正整数                | `--width N`             |
| `--transpose`    | `transpose`            | 布尔值                | `--transpose`            |
| `--tt`        | `keep_theme_alpha`         | 布尔值                | `--tt`                |
| `--per-page N`    | `per_page`             | 正整数                | `--per-page N`             |
| `--page ...`     | `page_spec`            | `N` / `A-B` / `A-` / `all`     | 由 `tableRenderer.py` 扩展处理   |
| `--all`       | `page_spec`            | 等同于 `all`              | 由 `tableRenderer.py` 扩展处理   |
| `--text-scale V`    | `text_scale`           | 枚举值/比例             | `--text-scale V`             |
| `--sort SPEC`     | `sort_spec`            | 单个/多个排序键             | `--sort SPEC`             |
| `--asc`        | `sort_default_dir`         | 默认排序方向             | `--asc`                |
| `--f SPEC`     | `filters`             | 可重复使用的过滤条件         | `--f SPEC`             |
| `--smart-wrap`    | `smart_wrap`            | 布尔值                | `--smart-wrap`            |
| `--no-smart-wrap`   | `--nosw`            | 布尔值                | `--no-smart-wrap`            |
| `--theme NAME`    | `theme`             | 主题 ID                | `--theme NAME`             |
| `--both`      | `output_both`           | 布尔值                | `--both`               |
| `--pin KEYS`     | `pin_keys`             | 保持默认设置             | `--pin`                |
| `--pin-reset`    | `pin_reset`            | 重置已固定的默认设置         | `--pin-reset`            |

**固定的默认设置：**
- 主题：`minimal_ios_mobile`
- 宽度：450 像素
- 自动换行：`true`

## `page_spec` 的含义：

- `N`：仅显示第 N 页
- `A-B`：显示从 A 到 B 的所有页面
- `A-`：显示从 A 到最后一页的所有页面
- 如果省略：显示默认的预览页面（第 1-3 页）

## 标准参数示例

```json
{
  "theme": "minimal_ios_mobile",
  "width": 900,
  "transpose": false,
  "keep_theme_alpha": false,
  "per_page": 15,
  "page_spec": "2-",
  "sort_spec": "score:desc,name:asc",
  "sort_default_dir": "asc",
  "filters": ["col:!note,attachment", "row:status!=disabled;score>=60"],
  "text_scale": "auto",
  "smart_wrap": true,
  "output_both": false
}
```

## 命令示例

```bash
# basic CSS output
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.png --theme minimal_ios_mobile --width 900 --text-scale large --page 1

# transpose + disable smart wrap
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.png --theme compact_clean --transpose --no-smart-wrap --page 1

# page range expansion (2-4)
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.p2.png --per-page 12 --page 2
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.p3.png --per-page 12 --page 3
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.p4.png --per-page 12 --page 4

# PNG + ASCII side output
python3 ~/.openclaw/custom-skills/zentable/table_renderer.py - /tmp/out.png --theme mobile_chat --both
```

## 验证流程（最低要求）

- 使用 `python3 -m py_compile scripts/zentable_render.py` 运行脚本；
- 确保 CSS 格式的输出正确；
- 确保 PIL 格式的输出正确；
- 验证 `--pin`、`--pin-reset` 和 `--both` 选项的功能；
- 在相关测试中通过所有黄金测试。

## 发布状态

当前版本为 **测试版**。
ASCII 格式的输出在 SkillHub 中仍处于 **测试/实验性** 阶段。

## 技术支持与联系方式

- GitHub 问题报告：[https://github.com/con2000us/zenTable/issues](https://github.com/con2000us/zenTable/issues)
- 维护者：@con2000us（Discord）
- 错误报告需包含以下信息：
  - 输入类型（文本、截图、照片或 JSON 数据）
  - 预期输出与实际输出之间的差异
  - 使用的平台（Discord、移动设备或桌面端）
  - 使用的命令或选项