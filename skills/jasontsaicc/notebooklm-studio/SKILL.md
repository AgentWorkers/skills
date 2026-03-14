---
name: notebooklm-studio
description: 将来源内容（URL、YouTube视频、文件、文本）导入 Google NotebookLM，并生成用户选择的输出形式：播客、视频、报告、测验、闪卡、思维导图、幻灯片、信息图、数据表。当用户提供内容并请求生成学习材料（如播客、视频或学习包）时，可使用此功能。
version: 2.1.2
metadata:
  openclaw:
    requires:
      bins: [notebooklm, ffmpeg]
    emoji: "🎙️"
---
# NotebookLM Studio

将来源文件导入 NotebookLM，通过 CLI 生成用户选择的输出文件，并将结果下载到本地。

## 输入内容

从用户输入中收集信息（仅询问缺失的字段）：

- **来源文件**：URL、YouTube 链接、文本笔记或文件附件（PDF、Word、音频、图片、Google Drive 链接）
- **输出文件类型**：用户可以从 9 种类型中选择（无默认值——务必询问）：
  - `audio`（播客）、`video`（视频）、`report`（报告）、`quiz`（测验）、`flashcards`（闪卡）、`mind-map`（思维导图）、`slide-deck`（幻灯片）、`infographic`（信息图）、`data-table`（数据表）
- **语言**（可选，默认为 `zh_Hant`）：通过 `notebooklm language set` 设置
  - ⚠️ 这是一个 **全局** 设置——会影响账户中的所有笔记本
- **输出文件选项**（在第 1b 步中讨论）：格式、样式、长度、难度等
  详情请参阅 `references/artifact-options.md`
- **自定义指令**（可选）：作为生成命令的描述传递
- **Telegram 发送目标**（仅限 OpenClaw）：用于发送的聊天 ID

有关来源文件类型检测规则的详细信息，请参阅 `references/source-types.md`。
有关所有 9 种输出文件类型和 CLI 选项的详细信息，请参阅 `references/artifacts.md`。

## 工作流程

**步骤是顺序执行的——请勿跳过或合并步骤。** 每个编号步骤必须在下一个步骤开始之前完成。特别注意：
- 步骤 0（身份验证预检查）必须在执行任何其他 CLI 命令之前运行并通过。
- 步骤 1b（选项讨论）必须在生成之前获得用户的确认。除非用户明确表示“使用默认值”，否则不要假设使用默认值。

0. **身份验证预检查**——在开始任何操作之前验证会话是否有效：
   ```bash
   notebooklm auth check --test --json
   ```
   - 如果 `"status": "ok"` → 继续执行步骤 1。
   - 如果 `"status": "error"` → **立即停止**。告知用户：
     > NotebookLM 登录已过期，请先重新登录（`notebooklm login`），完成后告诉我，我再继续。
   - 如果命令本身失败（网络错误、CLI 未找到等）→ 也停止并报告错误。
   - 必须使用 `--test` 选项——不使用该选项时，仅执行本地检查，即使会话已过期也可能通过。
   - 当用户确认重新登录后，在继续之前重新执行此检查。

1. **解析输入并配置输出文件** —

   **1a. 选择输出文件类型**——从用户输入中检测来源文件类型（URL、文件、文本），确认要生成哪些输出文件类型。

   **1b. 讨论选项**——在生成之前，确认每个选定输出文件类型的键选项。
   请参阅 `references/artifact-options.md` 了解优先级级别：
   - **必须询问**的选项：必须向用户询问
   - **提供默认值**的选项：说明默认值，让用户决定是否更改
   - **使用默认值**的选项：无需询问即可使用默认值
   - 用户已经指定的选项 → 跳过
   - 将所有问题一次性显示给用户（批量显示，而不是逐一显示）

   如果用户表示“使用默认值”→ 跳过所有问题，立即使用默认值。

   例如，代理消息（选择了音频 + 视频 + 报告 + 闪卡 + 幻灯片 + 信息图）：
   > 在生成之前，请确认以下选项：
   > - **播客**：深度剖析 / 简介 / 评论 / 辩论？
   > - **视频**：解释性视频 / 简介视频 / 电影风格？（电影风格视频使用 Veo 3，耗时 30-40 分钟）
   > - **报告**：简报文档 / 学习指南 / 博文文章 / 自定义？
   > - **幻灯片**：详细版 / 演示版？
   > - **测验和闪卡**：难度 `medium`，数量 `standard` —— 需要调整吗？
   > - **信息图**：使用自动样式，还是偏好特定样式（草图笔记、专业风格、日式格子布局...）？
   > - **语言**：`zh_Hant`，可以吗？
   >
   > 或者直接说“使用默认值”以立即开始生成。

2. **生成简短的主题名称**——根据来源文件和用户输入，生成一个简短的名称（2-4 个单词），该名称用于笔记本名称和输出目录。
   - 例如：`react-server-components`、`feynman-technique`、`taiwan-semiconductor-q4`
   - 保持简洁，使用小写字母，仅包含 ASCII 字符（如有需要，可转写非 ASCII 字符）
   - 如果用户提供了主题或标题，优先使用该主题。

3. **创建笔记本** —
   ```bash
   notebooklm create "<slug> <YYYYMMDD>"
   # → {"notebook_id": "xyz789", ...}  ← capture notebook_id
   notebooklm use <notebook_id>
   mkdir -p ./output/<slug>
   ```

4. **设置语言** —
   ```bash
   notebooklm language set <confirmed_language>
   ```
   使用在步骤 1b 中确认的语言。⚠️ 这是一个 **全局** 设置——必须明确设置，以避免之前的设置残留。

5. **添加来源文件** —
   ```bash
   # URL, YouTube, or file path
   notebooklm source add "<url_or_filepath>"

   # Google Drive
   notebooklm source add-drive <file_id> "<title>"
   ```
   对于纯文本文件 → 先保存为 `.txt` 文件，然后执行 `source add "./temp_text.txt"`。

6. **生成输出文件** — 采用两级策略以确保不会重复生成：

   **⚠️ 避免重复生成（仅限第二级）** — 在生成第二级输出文件之前，先调用一次 `artifact list` 并检查所有请求的类型：
   ```bash
   notebooklm artifact list --json
   # → [{"task_id": "abc123", "type": "slide-deck", "status": "processing"}, ...]
   ```
   对于每个即将生成的第二级输出文件，查找 `type` 匹配的条目（例如 `slide-deck`、`audio`、`video`）。如果有多个条目匹配相同类型，则非终止状态（`processing`/`pending`）优先于 `completed` > `failed`：
   - `processing` / `pending` → **不要再次生成**。使用现有的 `task_id`，转到步骤 9（等待 + 发送）。
   - `completed` → **不要再次生成**。直接跳到步骤 9 进行下载和发送。
   - `failed` → 可以重新生成。
   - 如果没有匹配的条目 → 继续生成。

   如果 `artifact list` 自身失败或返回错误，继续生成——避免重复生成是一个安全措施，而不是强制性的步骤。
   重复生成会浪费资源并导致混淆——此步骤用于防止最常见的操作错误。

   **第一级生成——立即执行**（使用 `--wait`，在超时时间内完成）：
   ```bash
   # Sync (instant)
   notebooklm generate mind-map

   # Fast async (1-2 min) — use options confirmed in step 1b
   notebooklm generate report --format <chosen_format> --wait
   notebooklm generate quiz --difficulty <chosen_difficulty> --quantity <chosen_quantity> --wait
   notebooklm generate flashcards --difficulty <chosen_difficulty> --quantity <chosen_quantity> --wait
   notebooklm generate data-table "<description>" --wait

   # Medium async (2-5 min, borderline — if timeout, retry or move to Tier 2)
   notebooklm generate infographic --style <chosen_style> --orientation <chosen_orientation> --wait
   ```

   **第二级生成——延迟执行**（使用 `--json` 且不使用 `--wait`，并保存 `task_id` 以供步骤 9 使用）：
   ```bash
   # Slow async — use options confirmed in step 1b
   # Parse JSON output to extract task_id for polling
   notebooklm generate slide-deck --format <chosen_format> --json
   # → {"task_id": "abc123", "status": "pending"}  ← save task_id

   notebooklm generate video --format <chosen_format> --style <chosen_style> --json
   # → {"task_id": "def456", "status": "pending"}  ← save task_id
   # Note: if cinematic, omit --style (ignored by Veo 3)

   notebooklm generate audio "<description>" --format <chosen_format> --length <chosen_length> --json
   # → {"task_id": "ghi789", "status": "pending"}  ← save task_id
   ```
   在步骤 1b 中接受的默认选项可以省略（CLI 使用其自己的默认值）。
   解析每个 JSON 响应并保存 `task_id`——您将在步骤 9 中需要它。
   仅生成用户请求的输出文件类型。跳过其余的。
   有关第二级生成的详细信息，请参阅 `references/artifacts.md`。

   **写入发送状态** — 在所有第二级输出文件生成完成后，立即写入 `./output/<slug>/delivery-status.json`，以便恢复脚本在代理超时时能够处理：
   ```json
   {
     "slug": "<slug>",
     "notebook_id": "<notebook_id>",
     "created_at": "<ISO 8601>",
     "artifacts": [
       {"type": "slide-deck", "task_id": "<id>", "status": "pending", "output_path": "./output/<slug>/slides.pdf"},
       {"type": "audio", "task_id": "<id>", "status": "pending", "output_path": "./output/<slug>/podcast.mp3"}
     ]
   }
   ```
   随着步骤 9 的进行，将每个输出文件的 `status` 更新为 `completed` 或 `failed`。
   该文件是代理和 `scripts/recover_tier2_delivery.sh` 之间的交接文件。
   Telegram 发送仅由代理执行（需要 OpenClaw 的 `message` 工具）；恢复脚本仅负责下载和状态跟踪。

7. **下载第一级输出文件** — 将每个成功生成的第一级输出文件保存到 `./output/<slug>/`：
   ```bash
   notebooklm download mind-map ./output/<slug>/mindmap.json
   notebooklm download report ./output/<slug>/report.md
   notebooklm download quiz --format json ./output/<slug>/quiz.json
   notebooklm download flashcards --format json ./output/<slug>/flashcards.json
   notebooklm download data-table ./output/<slug>/data.csv
   notebooklm download infographic ./output/<slug>/infographic.png
   ```

8. **报告并发送第一级输出文件** — 向用户展示已完成的第一级输出文件。
   如果第二级输出文件仍在生成中，附上状态提示：
   > “幻灯片/音频/视频仍在生成中，准备好后会发送。”

   **Telegram 发送**（仅限 OpenClaw）——如果 `message` 工具可用：
   1. 先发送包含第二级生成状态的文本摘要
   2. 接着发送报告 → 测验 → 闪卡 → 思维导图 → 信息图 → 数据表

   有关发送协议的详细信息，请参阅 `references/telegram-delivery.md`。
   如果在 OpenClaw 之外运行（例如 Claude Code、Codex），请跳过 Telegram 发送。

9. **按预期速度顺序下载并发送第二级输出文件** — 按照预计完成的速度顺序下载并发送每个延迟生成的输出文件：
   ```bash
   # Wait by expected completion order: slide-deck (fastest) → video → audio (slowest)
   # Uses --interval 5 (not default 2) since Tier 2 artifacts take minutes, not seconds
   notebooklm artifact wait <slide_task_id> --timeout 1800 --interval 5 --json
   # → {"status": "completed", ...}  ← task_id from generate is used as artifact_id here
   notebooklm download slide-deck ./output/<slug>/slides.pdf
   # → deliver to Telegram immediately

   notebooklm artifact wait <video_task_id> --timeout 1800 --interval 5 --json
   # Note: if cinematic, use --timeout 2400 (generation takes 30-40 min)
   notebooklm download video ./output/<slug>/video.mp4
   # → deliver to Telegram immediately

   notebooklm artifact wait <audio_task_id> --timeout 1800 --interval 5 --json
   notebooklm download audio ./output/<slug>/podcast.mp3
   bash scripts/compress_audio.sh ./output/<slug>/podcast.mp3 ./output/<slug>/podcast_compressed.mp3
   # → deliver to Telegram immediately
   ```
   - **顺序很重要**：先等待完成最快的输出文件（幻灯片 → 视频 → 音频），以减少空闲时间
   - 完成后：下载 → 后处理 → 发送到 Telegram → 将 `delivery-status.json` 的状态更新为 `completed`
   - 如果失败：将状态更新为 `failed` 并说明原因，然后继续处理下一个输出文件
   - 如果超时：参见下面的超时恢复机制
   - 每个输出文件的最大等待时间为 30 分钟（针对最慢的音频/视频）
   - 如果代理在仍有输出文件未完成时尝试退出，请告知用户：
     > “第二级生成模式已启动，恢复脚本将每 5 分钟检查并自动发送。”

   **⚠️ 超时恢复** — 如果 `artifact wait` 返回 `status: "timeout"`，则说明输出文件可能仍在生成中。**切勿重新生成**。相反：
   1. 重新检查状态：`notebooklm artifact poll <task_id> --json`
   2. 如果状态为 `processing` → 重新等待：`notebooklm artifact wait <task_id> --timeout 1800 --interval 5 --json`
   3. 如果状态为 `completed` → 下载并发送
   4. 如果失败：向用户通知错误，然后继续处理下一个输出文件
   5. 如果重新等待也超时（总共超时 2 次，大约 60 分钟），则放弃尝试，建议用户直接从 NotebookLM 下载文件
   超时意味着等待时间已到期，并不意味着生成失败。任务仍在服务器端继续进行。重新生成会导致重复生成和浪费资源。

## 错误处理

- **身份验证错误** — 由步骤 0 的预检查捕获。如果后续的任何 CLI 命令返回身份验证/会话错误（HTTP 401、"未登录"、"会话过期"、令牌获取失败），则视为中间流程的身份验证失败——停止操作，要求用户重新登录，然后重新运行步骤 0 后再继续。
- **第一级生成失败**：最多重试 2 次，然后在步骤 8 中包含失败提示。
- **第二级生成失败**：在步骤 9 中逐个通知用户。此时第一级输出文件已经发送完毕，因此第二级生成的失败不会影响文本文件的发送。
- 在发送状态中记录失败原因。

## 发送确认机制

在向用户报告“完成”之前，必须满足以下所有条件：
1. 所有请求的输出文件要么 **成功发送**，要么 **已报告失败并说明原因**
2. 对于 Telegram 发送（使用 OpenClaw）：每个 `message` 工具调用（OpenClaw 的内置消息工具）都必须返回带有 `messageId` 的成功响应
   - 如果发送失败，重试一次。如果仍然失败，向用户报告失败情况——不要默默地跳过
3. 没有任何输出文件仍处于 `processing` 或 `pending` 状态且未被跟踪

**在任何输出文件仍在等待发送时，切勿声称“完成”。** 如果第二级输出文件仍在生成中，必须明确说明并继续等待。直到所有文件都发送完毕或都有明确的处理结果，任务才算完成。

## 质量检查

在发送之前，请验证：
- 来源文件是具体的文章/内容页面（而不是分类页/索引页）。
- 报告包含可操作的要点。
- 测验测试关键概念和机制。
- 闪卡涵盖术语、决策和权衡因素。
- 输出内容符合要求的语言和长度。

有关格式规范的详细信息，请参阅 `references/output-contracts.md`。

## 发送模板

1. 选择理由（不超过 3 个要点）
2. 包含路径和状态的输出文件列表（如果适用，包括所有 9 种类型）
3. 关键要点（3-5 个要点）
4. 失败情况 + 备用说明（如果有）
5. 一个讨论问题

## 更新日志

### v2.1.0

- **身份验证预检查** — 步骤 0 在开始任何操作之前运行 `auth check --test --json`；过期的会话会立即失败，而不会在生成过程中出现问题。
- **避免重复生成** — 步骤 6 在生成第二级输出文件之前检查 `artifact list`，以防止代理重试或恢复时生成重复文件。
- **超时恢复** — `artifact wait` 超时不再触发重新生成；如果连续两次超时（约 60 分钟），则停止尝试并重新等待。
- **发送确认机制** — 代理在所有输出文件发送完毕或明确报告失败之前，不能声称“完成”。
- **发送状态协议** — 步骤 6 在第二级输出文件发送完成后写入 `delivery-status.json`；步骤 9 在输出文件完成后更新该文件。通过 `scripts/recover_tier2_delivery.sh` 可以实现基于 cron 的恢复机制。