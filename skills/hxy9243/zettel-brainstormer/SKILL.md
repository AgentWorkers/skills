---
name: zettel-brainstormer
description: 它会从您本地的 Zettelkasten 笔记中读取内容，随机选择一个想法，然后通过链接或标签查找相关参考资料，并利用这些参考资料来进一步扩展这个想法。
---
# Zettel Brainstormer 🧠

该技能旨在将一个初步的想法或草稿通过深入研究、多元化的视角以及结构化的头脑风暴过程进行完善。

配置文件为 `config/models.json`，可以通过手动编辑或使用 `setup.py` 脚本进行配置。

## 新的三阶段工作流程

该技能现在支持一个三阶段的处理流程，以平衡成本与质量：

1) **查找参考资料**（使用 `find_links.py`）：
   - 运行 `scripts/find_links.py` 来识别相关的现有笔记。
   - **包含维基链接的文档**（会追踪 [[wikilinks]] 最多 N 层深度的链接，总共最多 M 个文档）。
   - **具有相似标签的文档**（查找具有重叠标签的笔记）。
   - **与 Obsidian 的原生集成**：如果可用，会使用 `obsidian-cli` 进行高性能的索引和搜索。
   - **语义发现（可选）**：可以利用 `zettel-link` 技能来发现那些没有明确标签或链接的“隐藏”概念关联。
   - **输出**：一个包含相关笔记绝对文件路径的 JSON 列表。

2) **预处理内容**（使用 `preprocess_model`）：
   - 该脚本会遍历第 1 阶段找到的所有文件。
   - 对于每个文件：
     - 读取文件内容。
     - 使用 `templates/preprocess.md` 和提供的种子笔记的关键点以及文件内容作为上下文，应用 `preprocess_model`。
     - 提取：相关性评分、摘要、关键点和引用。
     - **输出**：一个结构化的 Markdown 摘要。

3) **起草并优化内容**（使用 `pro_model`）：
   - 收集第 2 阶段预处理后的所有 Markdown 输出。
   - 使用 `templates/draft.md` 和 `pro_model` 生成最终草稿。
   - 合并各个要点，添加适当的 Obsidian 属性和链接。
   - 如果可用，会使用 `obsidian` 技能来统一格式。

## 文件与脚本

该技能包含以下资源：

- `scripts/find_links.py`  -- 查找相关的笔记路径（包含链接和具有相似标签的笔记）
- `scripts/draft_prompt.py`  -- （已弃用）为脚本生成提示
- `scripts/obsidian_utils.py` -- 用于提取维基链接的通用工具
- `templates/preprocess.md` -- 指示脚本如何从单个笔记中提取信息
- `templates/draft.md` -- 指示如何生成最终草稿
- `config/models.example.json`  -- 示例配置文件

## 配置与设置

**首次运行设置**：
在使用该技能之前，必须运行设置脚本来配置模型和目录。

```bash
python scripts/setup.py
```

这将根据你的偏好创建 `config/models.json` 文件。你可以按回车键接受默认设置。

**配置字段**：
- `pro_model`：用于起草的模型（默认为当前使用的模型）
- `preprocess_model`：用于预处理的简单模型（默认为当前使用的模型）
- `zettel_dir`：你的 Zettelkasten 笔记的路径
- `output_dir`：保存草稿的路径
- `search_skill`：用于网络/X 研究的搜索技能（web_search、brave_search 或无）
- `link_depth`：追踪 [[wikilinks]] 的深度（N 层，默认为 2）
- `max_links`：最多包含的链接数量（M 个链接，默认为 10）
- `discovery_mode`：搜索模式（可选）：`standard`（默认）、`cli`（使用 obsidian-cli）或 `semantic`（使用 zettel-link）。

## 使用方法

- 当用户请求“brainstorm X”、“expand this draft”或“research and add notes to <path>”时触发该技能。
- 示例工作流程（伪代码）：
  1. 选择一个种子笔记。
  2. 查找链接：`python scripts/find_links.py --input <seed_note> --output /tmp/paths.json`
  3. 预处理：
     - 加载 `/tmp/paths.json`。
     - 对于每个路径，读取内容。
     - 使用 `templates/preprocess.md` 和内容调用 `preprocess_model`。
     - 存储结果。
  4. 生成最终草稿：
     - 将种子笔记与所有预处理结果合并。
     - 使用 `templates/draft.md` 和合并后的上下文调用 `pro_model`。
  5. 将结果保存到笔记中。

## 维护者注意事项：

- 保持预处理输出的长度在 200-600 个字符以内，以节省资源。
- 确保所有外部链接都包含在 `References` 部分，并提供完整的标题和 URL。
- 在添加新内容时，务必添加时间戳和简短的来源说明。