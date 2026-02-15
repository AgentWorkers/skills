---
name: calibre-metadata-apply
description: 通过 Content 服务器，使用 `calibredb` 对现有的 Calibre 书籍应用元数据更新。在通过只读查询确认目标 ID 后，使用该方法进行受控的元数据编辑。
metadata: {"openclaw":{"requires":{"bins":["node","calibredb"],"env":["CALIBRE_PASSWORD"]},"optionalBins":["pdffonts"],"optionalEnv":["CALIBRE_USERNAME"],"primaryEnv":"CALIBRE_PASSWORD","dependsOnSkills":["subagent-spawn-command-builder"],"localWrites":["skills/calibre-metadata-apply/state/runs.json","~/.config/calibre-metadata-apply/auth.json","~/.config/calibre-metadata-apply/config.json"],"modifiesRemoteData":["calibre:metadata"]}}
---

# calibre-metadata-apply

这是一个用于更新现有Calibre书籍元数据的技能。

## 要求

- 在运行时环境中，`calibredb`必须可以在PATH路径下找到。
- 必须安装了`subagent-spawn-command-builder`（用于生成生成payload的数据）。
- `pdffonts`是可选的/推荐的，用于PDF证据的检查。
- 可以访问的Calibre内容服务器URL：
  - `http://HOST:PORT/#LIBRARY_ID`
- 如果启用了身份验证，请使用`/home/altair/.openclaw/.env`文件中的配置：
  - `CALIBRE_USERNAME=<user>`
  - `CALIBRE_PASSWORD=<password>`
- 可以通过`--password-env CALIBRE_PASSWORD`参数传递密码（用户名会自动从环境变量中加载）。
- 也可以通过`--username <user>`显式覆盖用户名。
- 可选的身份验证缓存：`--save-auth`（默认文件：`~/.config/calibre-metadata-apply/auth.json`）

## 支持的字段

### 直接字段（`set_metadata --field`）
- `title`（书名）
- `title_sort`（书名排序）
- `authors`（作者列表，可以用`&`分隔或作为数组）
- `author_sort`（作者排序）
- `series`（系列名称）
- `series_index`（系列索引）
- `tags`（标签列表）
- `publisher`（出版商）
- `pubdate`（出版日期，格式为`YYYY-MM-DD`）
- `languages`（语言）
- `comments`（评论）

### 辅助字段
- `comments_html`（用于插入评论的HTML标记）
- `analysis`（自动生成评论的分析HTML）
- `analysis_tags`（添加标签）
- `tags_merge`（默认值为`true`，表示合并标签）
- `tags_remove`（在合并后删除特定标签）

## 必须执行的流程

### A. 目标确认（强制要求）
1. 运行只读查询以缩小候选范围。
2. 显示`id`, `title`, `authors`, `series`, `series_index`等信息。
3. 获取用户的确认，以确定最终的目标ID。
4. 仅使用已确认的ID来构建JSONL数据。

### B. 提案生成（当元数据缺失时）
1. 从文件提取和网络来源收集证据。
2. 显示一个合并后的提案表格，其中包含：
   - `candidate`（候选项）、`source`（来源）、`confidence`（置信度：高|中|低）
   - `title_sort_candidate`、`author_sort_candidate`（候选书名的排序和作者排序）
3. 获取用户的决策：
   - `approve all`（全部批准）
   - `approve only: <fields>`（仅批准某些字段）
   - `reject: <fields>`（拒绝某些字段）
   - `edit: <field>=<value>`（修改某个字段的值）
4. 仅应用已批准/最终确定的字段。
5. 如果置信度低或来源存在冲突，则保留字段为空。

### C. 应用元数据
1. 首先进行模拟运行（强制要求）。
2. 仅在用户明确批准后运行`--apply`命令。
3. 重新读取并报告最终结果。

## 分析工作流程策略

- 使用`subagent-spawn-command-builder`生成用于处理大量候选项的`sessions_spawn` payload：
  - 必须指定`task`参数。
  - 配置文件应包含此工作流程的模型、思考时间、超时设置和清理步骤。
- 使用轻量级的子代理模型进行分析（避免使用主模型）。
- 将最终决策以及模拟运行和实际应用的结果保存在主进程中。

## 数据流处理方式

- 本地执行：
  - 从JSONL数据构建`calibredb set_metadata`命令。
  - 读写本地状态文件`state/runs.json`以及`~/.config/calibre-metadata-apply/`目录下的可选身份验证/配置文件。
- 子代理执行（用于处理大量候选项）：
  - 通过`subagent-spawn-command-builder`使用`sessions_spawn`。
  - 发送的文本和元数据会到达运行时配置的模型端点。
- 远程写入：
  - `calibredb set_metadata`命令会将元数据更新到目标Calibre内容服务器上。

### 安全规则：
- 除非用户明确要求，否则不要使用`--save-plain-password`参数。
- 建议使用基于环境变量的密码设置（`--password-env CALIBRE_PASSWORD`），而不是直接在命令行中输入密码。
- 如果用户不希望使用外部模型或子代理进行处理，可以将流程限制在本地，并跳过子代理的调用。

## 长期运行的分阶段执行策略（适用于整个图书馆）

对于整个图书馆的批量处理任务，始终使用分阶段执行的方式。

## 未知文档的处理流程（M3）

### 批量处理规则：
- 确保每个未知文档的批次大小足够小，以便在聊天界面中显示每一行的详细结果（避免抽样）。
- 如果仍有未解决的文档，停止处理并等待用户的下一步指示。

### 用户干预的检查点

1. **简单处理（仅更新元数据）**
   - 默认情况下始终执行此步骤（无需额外用户指令）。
   - 仅分析现有的元数据（不读取文件内容）。
   - 向用户展示以下信息：
     - 当前文件/书名
     - 推荐的书名/元数据
     - 置信度/证据摘要
   - 在进行更深入的处理之前，停止并等待用户指令。

2. **根据用户请求：仅处理第1页**
   - 仅读取第1页的内容并优化提案。
   - 报告与简单处理相比的差异。

3. **如果仍然不确定：进行深入处理**
   - 读取前5页和最后5页的内容。
   - 添加网络证据进行搜索。
   - 提出包含置信度和理由的最终提案。

4. **审批流程**
   - 在应用元数据之前，向用户展示详细的分析结果并请求明确批准。

### 待处理和不受支持的文档的处理方式

- 对于未解决或待处理的文档，使用`pending-review`标签进行标记。
- 如果文档在当前处理流程中仍未解决，不要强制更新其元数据。
  - 用`pending-review`标签标记这些文档，并留待后续处理。

### 差异报告格式（针对未知文档的批量处理）

返回完整的处理结果（而非样本）：
- 处理总结（包括处理的目标文档、已更改的文档、待处理的文档、跳过的文档以及出现错误的文档）
- 包含`id`和修改前后的字段的完整列表
- 包含`id`和错误原因的完整待处理文档列表
- 置信度必须表示为`high|medium|low`。

### 运行时的临时文件管理策略

- 仅在处理过程中保留运行状态和临时生成的文件。
- 成功完成处理后，删除每次运行的状态文件和临时文件。
- 如果处理失败，仅保留最小范围的临时文件以供重试或调试使用，然后在问题解决后清理这些文件。

### 内部协调策略（推荐）

- 对所有分析阶段使用轻量级的子代理。
- 将应用决策保存在主进程中。
- 将每个阶段的运行状态保存在`state/runs.json`文件中。

### 分阶段执行流程

- 第1阶段：主进程定义处理范围。
- 主进程通过`subagent-spawn-command-builder`生成生成payload的数据（配置示例：`calibre-meta`），然后调用`sessions_spawn`。
- 通过`scripts/run_state.mjs upsert`保存`run_id`, `session_key`, `task`等信息。
- 立即告知用户这是一个子代理任务，并说明使用的分析模型。
- 回复用户“分析已经开始”，并保持聊天界面的正常响应。

### 第2阶段：完成处理
- 收到子代理的处理完成通知。
- 保存处理结果JSON。
- 通过`scripts/handle_completion.mjs --run-id ... --result-json ...`完成状态处理。
- 根据需要返回处理后的提案。

### PDF提取策略

- 首先尝试使用`ebook-convert`命令进行转换。
- 如果转换失败或没有结果，使用`pdftotext`命令。
- 如果这两种方法都失败，则切换到优先使用网络证据的模式。

### 文本排序策略

- 使用用户配置的`reading_script`来处理日文/非拉丁文字段的排序：
  - `katakana` / `hiragana` / `latin`
- 首次使用时询问用户一次排序方式，之后保持设置并重复使用。
- 默认策略是读取全部内容（不进行截断）。
- 配置文件路径：`~/.config/calibre-metadata-apply/config.json`
  - 关键字段：`reading_script`

## 使用方法

### 模拟运行：
```bash
cat changes.jsonl | node skills/calibre-metadata-apply/scripts/calibredb_apply.mjs \
  --with-library "http://127.0.0.1:8080/#MyLibrary" \
  --password-env CALIBRE_PASSWORD \
  --lang ja
```

### 应用元数据：
```bash
cat changes.jsonl | node skills/calibre-metadata-apply/scripts/calibredb_apply.mjs \
  --with-library "http://127.0.0.1:8080/#MyLibrary" \
  --password-env CALIBRE_PASSWORD \
  --apply
```

### 注意事项：
- 不要仅基于模糊的标题匹配就直接运行`--apply`命令。
- 不要在应用元数据的payload中包含未经确认的文档ID。
- 未经用户明确确认，不要自动填充置信度较低的候选项。