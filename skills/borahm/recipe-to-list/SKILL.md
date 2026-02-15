---
name: recipe-to-list
description: 将食谱转换为 Todoist 购物清单：从食谱图片（使用 Gemini Flash 技术）或食谱网页中提取所需食材信息，然后根据预设的相似度/重叠规则将这些食材与现有的购物清单进行比对；跳过厨房中已有的常用食材（如盐、胡椒粉等），并在单位一致的情况下汇总所需食材的数量。同时，将每份制作完成的食谱保存到工作区的食谱目录（recipes/）中。
---

# 创建购物清单（使用 Gemini Flash 和 Todoist）

**操作流程：**
1. 输入内容可以是**图片**或**食谱的网页链接**。
2. 从图片中提取食材信息（使用 Gemini Flash）；对于网页链接，先使用 `web_fetch` 获取文本，再使用 Gemini 进行解析。
3. 从 Todoist 中获取当前的购物清单。
4. 通过比较食材信息以及同义词映射来更新购物清单（仅合并高度匹配的食材，例如：coriander ↔ cilantro, panko ↔ breadcrumbs）。
5. 更新购物清单（默认情况下，仅添加缺失的食材；盐和胡椒等常用食材会被忽略）。

使用提供的脚本来处理从图片到食材信息再到购物清单更新的整个流程。

此外，该脚本还会自动将生成的 Markdown 内容保存到 `recipes/` 目录中（作为你的食谱知识库），并追加到 `recipes/index.md` 文件中。

**对于“食谱名称 → 网页链接”的处理方式：**
首先使用 `web_search` 和 `web_fetch` 功能进行查询确认，然后将获取到的食材信息按照相同的逻辑更新购物清单，并保存相应的食谱信息。

## 先决条件：
- 环境变量：`GEMINI_API_KEY`（或 `GOOGLE_API_KEY`）用于访问 Gemini 服务。
- 环境变量：`TODOIST_API_TOKEN` 用于访问 Todoist 服务。
- 需要安装 `todoist`（todoist-ts-cli）工具。

**输出格式：**
- 购物清单中的食材信息会以“食材名称”开头，后面跟着括号中的数量。
- 购物清单采用扁平化结构（没有 Todoist 的分组或分类）。

**执行方式：**
```bash
python3 skills/recipe-to-list/scripts/recipe_to_list.py \
  --image /path/to/photo.jpg \
  --title "<optional title>" \
  --source "photo:/path/to/photo.jpg"
```

### 可选参数：
- `--model gemini-2.0-flash`（默认值；系统会自动选择兼容的 Gemini 模型）。
- `--dry-run`：仅输出提取的食材信息，不创建任务。
- `--prefix "[Recipe] "`：在每个创建的任务前添加前缀。
- `--no-overlap-check`：跳过对现有购物清单的比对检查。
- `--include-pantry`：在购物清单中包含盐和胡椒等常用食材。
- `--no-save`：跳过将数据保存到 `recipes/` 目录的步骤。

**需要传递给 Gemini 的数据格式：**
脚本要求 Gemini 返回格式为严格 JSON 的数据。

```json
{
  "items": ["2 large globe eggplants", "kosher salt", "..."],
  "notes": "optional"
}
```

**注意事项：**
如果解析数据失败，请尝试重新运行脚本，并提供更清晰的食材列表数据，或者手动输入食材信息。