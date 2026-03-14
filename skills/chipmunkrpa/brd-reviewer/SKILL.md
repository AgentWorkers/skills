---
name: brd-reviewer
description: >
  **任务描述：**  
  审查以 `.docx` 格式保存的业务需求文档（Business Requirements Documents, BRD）。具体步骤如下：  
  1. 阅读现有的 BRD 文件，提取其中段落级别的关键信息。  
  2. 对表述不明确的部分提出澄清问题。  
  3. 编写一份最终的 Word 文档，将所有评论和修改建议整合其中。  
  **适用场景：**  
  当用户希望他人对 BRD 进行审查、指出其中的模糊之处，或提出改进建议时，可以使用此方法。同时，该方法能够充分利用 Word 文档本身的审阅功能（如标记高亮、添加注释等）。
---
# BRD 审核器

## 概述
逐段审核 BRD（Business Requirements Document），记录对模糊或不完整需求的澄清问题，并生成一个包含 Word 评论和修订记录的 `.docx` 文件。

建议使用集成化的流程，以便最终交付物是一个基于 Word 的审核文档，而不仅仅是聊天记录。

## 工作流程
1. 确认源 BRD 的 `.docx` 文件路径。
2. 初始化段落审核 JSON 数据结构：
   ```bash
   python scripts/brd_review_pipeline.py init-review \
     --input <brd.docx> \
     --output <brd.review.json>
   ```
3. 阅读 BRD 并填写审核 JSON 数据：
   - 对于每个 `paragraphs[]` 条目，保持 `paragraph_index`、`style_id`、`heading_path` 和 `source_text` 不变。
   - 如果段落内容不明确、不完整、内部逻辑不一致，或缺少验收标准、数据定义、负责人、依赖关系、假设或边界情况，请将 `needs_comment` 设置为 `true`。
   - 将 `comment_question` 编写为适合在 Word 评论中使用的简洁问题。
   - 如果段落需要重新编写以提高准确性、完整性或可测试性，请将 `needsrevision` 设置为 `true`。
   - 将 `proposed_replacement` 编写为完整的替换内容，而不仅仅是片段。
   - 使用 `issue_tags` 来明确说明修改原因。推荐的标签包括：`ambiguity`（模糊性）、`scope`（范围）、`actor`（参与者）、`data`（数据）、`workflow`（工作流程）、`exception`（异常情况）、`dependency`（依赖关系）、`acceptance-criteria`（验收标准）、`nonfunctional`（非功能性）、`term-definition`（术语定义）或 `conflict`（冲突）。
4. 将审核后的 `.docx` 文件保存在与源 BRD 相同的文件夹中：
   ```bash
   python scripts/brd_review_pipeline.py materialize \
     --input <brd.docx> \
     --review-json <brd.review.json> \
     --output <brd.reviewed.docx> \
     --author "Codex BRD Reviewer"
   ```
5. 验证输出质量：
   - 确认审核后的文件存在于源 BRD 旁边。
   - 确认带有 `needs_comment=true` 的段落上显示了 Word 评论。
   - 确认带有 `needsrevision=true` 的段落上的更改记录可见。
   - 如果 BRD 需要大量使用表格或特殊布局，在交付前使用 `$doc` 工具来渲染和查看结果。

## 审核标准
- 对于任何未解决实现细节的段落都要提出问题。
- 对于缺失的信息，使用评论进行说明；对于需要修改的表述，使用修订记录。
- 将需求重写为具体且可测试的陈述。
- 标记未定义的参与者、系统、接口、计算方法、时间安排、权限和异常处理机制。
- 不要自行臆造业务规则。如果 BRD 缺少关键细节，应在评论中提出，而不是猜测。
- 保持评论简短且具体，以便在评论框中直接执行操作。
- 保持提出的替换内容专业且可以直接用于文档中。

## 输出要求
- 必须生成以下两个文件：
  - `<name>.review.json`
  - `<name>.reviewed.docx`
- 将这两个文件放在与源 BRD 相同的文件夹中，除非用户另有要求。
- 将聊天分析视为补充内容。`.docx` 文件是主要的交付物。

## 资源
- 段落审核规范：`references/review-json-schema.md`
- 主要工具：`scripts/brd_review_pipeline.py`

## 依赖关系
如果缺少，请安装以下依赖项：
```bash
python -m pip install python-docx lxml
```