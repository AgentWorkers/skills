---
name: ai-ppt-generate
description: 这款智能PPT生成工具由百度提供。它可以根据用户提供的主题或问题，智能地生成PPT文件。用户可以选择PPT的主题、模板，甚至可以自定义自己的模板。该工具还支持导入图片或资源文件（如PDF、Word、TXT等格式）。最终生成的PPT文件的下载地址也会被提供给用户。
metadata: { "openclaw": { "emoji": "📑", "requires": { "bins": ["python"] } } }
---

# AI PPT 生成

该功能允许 OpenClaw 代理仅根据用户提供的主题来生成 PPT 文件。如果可能的话，用户还可以提供图片或资源文件，该工具可以帮助生成完美的 PPT 文件。

## 设置

1. **API 密钥：** 确保 `BAIDU_API_KEY` 环境变量已设置为您的有效 API 密钥。
2. **运行时环境：** API 密钥必须在运行时环境中可用。

## API 表格
|    名称          |                路径                |            描述                                      |
|------------|---------------------------------|---------------------------------------|
| PPTThemeQuery | /v2/tools/ai_ppt/get_ppt_theme    | 查询内置的 PPT 主题和模板列表                   |
| PPTOutlineGenerate | /v2/tools/ai_ppt/generate_outline   | 根据提供的主题、模板 ID、样式 ID 等生成 PPT 大纲           |
| PPTGenerate    | /v2/tools/ai_ppt/generate_ppt_by_outline | 根据提供的 PPT 大纲生成 PPT 文件                         |

## 工作流程

1. `PPTThemeQuery` API 会执行位于 `scripts/ppt_theme_list.py` 的 Python 脚本。
2. `PPTOutlineGenerate` API 会执行位于 `scripts/ppt_outline_generate.py` 的 Python 脚本。
3. `PPTGenerate` API 会执行位于 `scripts/ppt_generate.py` 的 Python 脚本。
4. 首先，用户需要通过 `PPTThemeQuery` 接口查询 PPT 的样式 ID 和模板 ID。
5. 然后，使用第一步查询到的样式 ID 和模板 ID 作为参数，调用 `PPTOutlineGenerate` API 生成 PPT 大纲（该接口返回 SSE 流式数据）。此步骤依赖于第一步的结果；如果第一步失败，请求可以终止。
6. 最后，根据第二步生成的 PPT 大纲，调用 `PPTGenerate` API 生成最终的 PPT 文件（请求参数 `outline` 来自大纲生成接口的返回结果）。用户可以对大纲进行编辑和修改，但修改后的大纲必须为 Markdown 格式；否则可能会导致失败。此步骤严格依赖于第二步的结果；如果第二步失败，请求也可以终止。

## API

### PPTThemeQuery API

#### 参数
无参数

#### 使用示例
```bash
BAIDU_API_KEY=xxx python3 scripts/ppt_theme_list.py
```

### PPTOutlineGenerate API

#### 参数
- `query`：PPT 的标题或用户查询内容（必填）
- `resource_url`：资源文件的 URL（例如 PDF、Word、TXT 等）
- `page_range`：PPT 文件的页码范围（格式为 1-10、11-20 等）
- `layout`：PPT 文件的布局（可选值：1（极简模式）、2（专业模式）
- `language_option`：PPT 文件的语言选项（可选值：zh、en）
- `gen_mode`：PPT 的生成模式（可选值：1（智能优化）、2（创意模式）

#### 使用示例
```bash
BAIDU_API_KEY=xxx python3 scripts/ppt_outline_generate.py --query "generate a ppt about the future of AI" 
```

### PPTGenerate API

#### 参数
- `query_id`：来自 `PPTOutlineGenerate` API 的查询 ID（必填）
- `chat_id`：来自 `PPTOutlineGenerate` API 的聊天 ID（必填）
- `outline`：来自 `PPTOutlineGenerate` API 的 PPT 大纲（必须为 Markdown 格式，用户可对其进行修改）
- `query`：用户最初的查询内容（必填）
- `title`：来自 `PPTOutlineGenerate` API 的 PPT 标题（必填）
- `style_id`：来自 `PPTThemeQuery` API 的 PPT 样式 ID（必填）
- `tpl_id`：来自 `PPTThemeQuery` API 的 PPT 模板 ID（必填）
- `resource_url`：资源文件的 URL（例如 PDF、Word、TXT 等）
- `custom_tpl_url`：用户自定义的 PPT 模板的下载路径（可选）
- `gen_mode`：PPT 的生成模式（可选值：1（智能优化）、2（创意模式）
- `ai_info`：是否在生成的 PPT 最后一页使用 AI 生成的内容（可选）

#### 使用示例
```bash
BAIDU_API_KEY=xxx python3 scripts/ppt_generate.py --query_id "xxx" --chat_id "xxx" ...
```