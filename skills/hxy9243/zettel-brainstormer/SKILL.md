---
name: zettel-brainstormer
description: 它会从您本地的 Zettelkasten 笔记中读取内容，随机选择一个想法，然后通过链接或标签找到相关的参考资料，并利用这些参考资料来进一步扩展这个想法。
---
# Zettel Brainstormer 🧠

该技能旨在将一个初步的想法或草稿通过深入研究、多元化的视角以及结构化的头脑风暴过程进行完善。

配置文件为 `config/models.json`，用户可以手动编辑该文件，也可以使用 `setup.py` 脚本进行配置。

## 新的三阶段工作流程

该技能现在支持一个三阶段的处理流程，以平衡成本与质量：

1) **查找参考资料**（使用 `find_links.py`）：
   - 运行 `scripts/find_links.py` 来识别相关的现有笔记。
   - **包含维基链接的文档**（会追踪 [[wikilinks]] 中的链接，最多追溯到 M 个文档）。
   - **具有相似标签的文档**（查找具有重叠标签的笔记）。
   - 输出：一个包含相关笔记绝对文件路径的 JSON 列表。

2) **子代理：预处理内容**（使用 `preprocess_model`）：
   - 该子代理会遍历第 1 阶段找到的所有文件。
   - 对于每个文件：
     - 读取文件内容。
     - 使用 `preprocess_model` 和种子笔记的关键点以及文件内容作为上下文，应用 `templates/preprocess.md` 模板。
     - 提取：相关性评分、摘要、关键点和引用。
     - 输出：该笔记的结构化 Markdown 摘要。

3) **起草并优化内容**（使用 `pro_model`）：
   - 收集第 2 阶段预处理后的所有 Markdown 结果。
   - 使用 `templates/draft.md` 模板，应用 `pro_model` 来生成最终草稿。
   - 合并各个要点，添加适当的 Obsidian 属性和链接。
   - 如果可用，会使用 `obsidian` 技能来统一文档格式。

## 文件与脚本

该技能包含以下资源（位于技能文件夹内）：

- `scripts/find_links.py`  -- 查找相关笔记的路径（包含维基链接和具有相似标签的笔记）
- `scripts/draft_prompt.py`  -- （已弃用）为子代理生成提示信息
- `scripts/obsidian_utils.py` -- 用于提取维基链接的通用工具函数
- `templates/preprocess.md` -- 指示子代理如何从单个笔记中提取信息的模板
- `templates/draft.md` -- 用于生成最终草稿的模板
- `config/models.example.json` -- 配置文件示例

## 配置与设置

**首次运行设置**：
在使用该技能之前，必须运行设置脚本来配置模型和目录。

```bash
python scripts/setup.py
```

这将根据你的偏好创建 `config/models.json` 文件。你可以按 Enter 键接受默认设置。

**配置字段**：
- `pro_model`：用于起草的模型（默认为当前使用的模型）
- `preprocess_model`：用于预处理的模型（默认为当前使用的模型）
- `zettel_dir`：Zettelkasten 笔记的存储路径
- `output_dir`：草稿文件的保存路径
- `search_skill`：用于网络搜索的技能（web_search、brave_search 或无）
- `link_depth`：追踪 [[wikilinks]] 的深度（最多 N 层，默认为 2）
- `max_links`：允许包含的最大链接数量（最多 M 个链接，默认为 10）

## 使用方法

- 当用户请求“brainstorm X”、“expand this draft”或“research and add notes to <path>”时，可以触发该技能。
- 示例工作流程（伪代码）：
  1. 选择一个种子笔记。
  2. 查找参考资料：`python scripts/find_links.py --input <seed_note> --output /tmp/paths.json`
  3. 子代理预处理流程：
     - 加载 `/tmp/paths.json`。
     - 对于每个路径，读取文件内容。
     - 使用 `templates/preprocess.md` 和文件内容作为输入，调用 `preprocess_model`。
     - 保存处理结果。
  4. 生成最终草稿：
     - 将种子笔记与所有预处理结果合并。
     - 使用 `templates/draft.md` 和合并后的内容作为输入，调用 `pro_model`。
  5. 将结果保存到 Zettelkasten 笔记中。

## 维护说明：
- 保持预处理后的输出内容简短（200–600 个字符），以节省资源。
- 确保所有外部链接都包含在 `References` 部分，并提供完整的标题和网址。
- 在添加新内容时，务必添加时间戳和来源信息。