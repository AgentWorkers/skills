---
name: phoenixclaw
description: |
  Passive journaling skill that scans daily conversations via cron to generate
  markdown journals using semantic understanding.

  Use when:
  - User requests journaling ("Show me my journal", "What did I do today?")
  - User asks for pattern analysis ("Analyze my patterns", "How am I doing?")
  - User requests summaries ("Generate weekly/monthly summary")
metadata:
  version: 0.0.12
---

# PhoenixClaw：零标记被动式日志记录系统

PhoenixClaw 利用语义智能自动将日常对话提炼成有意义的反思内容，自动识别值得记录的时刻、模式以及个人成长的机会。

## 🛠️ 核心工作流程

> [!重要] **必须完成整个工作流程**  
> 无论通过何种方式调用，都必须完整执行以下 9 个步骤：  
> - **定时任务执行**（每晚 10 点）  
> - **手动调用**（例如：“显示我的日志”、“生成今天的日志”等）  
> - **重新生成日志请求**（例如：“重新生成我的日志”、“更新今天的记录”）  

> **切勿跳过任何步骤**。部分执行会导致以下问题：  
> - 图片缺失（会话日志未被扫描）  
> - 财务数据缺失（账本插件未触发）  
> - 日志不完整（插件未执行）  

PhoenixClaw 遵循结构化的流程以确保日志的一致性和深度：  

1. **用户配置**：检查 `~/.phoenixclaw/config.yaml` 文件。如果文件缺失，请按照 `references/user-config.md` 中的定义进行初始化。  
2. **上下文获取**：  
   - **扫描内存文件**：读取 `memory/YYYY-MM-DD.md` 和 `memory/YYYY-MM-DD-*.md` 文件，这些文件包含用户通过命令（如 “记一下”）手动记录的每日反思内容。**重要提示**：不要跳过这些文件，因为它们包含了会话日志可能遗漏的用户的真实想法。  
   - **扫描会话日志**：调用 `memory_get` 获取当天的内存数据，然后 **重要提示**：扫描所有原始会话日志并按消息时间戳进行筛选。会话日志通常分散在多个文件中。**注意**：不要根据文件的时间戳（`mtime`）来分类图片：  
      ```bash
      # Read all session logs from both OpenClaw locations, then filter by per-message timestamp
      # Use timezone-aware epoch range to avoid UTC/local-day mismatches.
      TARGET_DAY="$(date +%Y-%m-%d)"
      TARGET_TZ="${TARGET_TZ:-Asia/Shanghai}"
      read START_EPOCH END_EPOCH < <(
        python3 - <<'PY' "$TARGET_DAY" "$TARGET_TZ"
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import sys

day, tz = sys.argv[1], sys.argv[2]
start = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=ZoneInfo(tz))
end = start + timedelta(days=1)
print(int(start.timestamp()), int(end.timestamp()))
PY
      )

      for dir in "$HOME/.openclaw/sessions" "$HOME/.agent/sessions"; do
        [ -d "$dir" ] || continue
        find "$dir" -name "*.jsonl" -print0
      done |
        xargs -0 jq -cr --argjson start "$START_EPOCH" --argjson end "$END_EPOCH" '
          (.timestamp // .created_at // empty) as $ts
          | ($ts | fromdateiso8601?) as $epoch
          | select($epoch != null and $epoch >= $start and $epoch < $end)
        '
      ```  
      读取**所有匹配的文件**，无论文件名如何（例如，file_22 或 file_23 可能名称较早，但仍然包含当天的内容）。  
   - **从会话日志中提取图片**：会话日志中包含类型为 “image” 的条目，你需要：  
      1. 找到所有图片条目  
      2. 仅保留消息时间戳在目标日期范围内的条目  
      3. 提取 `file_path` 或 `url` 字段  
      4. 将文件复制到 `assets/YYYY-MM-DD/` 目录  
      5. 尽可能给文件起描述性名称  
   - **为什么需要会话日志**：`memory_get` 仅返回文本数据。图片元数据、照片引用和媒体附件仅存在于会话日志中。跳过会话日志会导致所有图片丢失。  
   - **活动信号质量**：不要将心跳信号或定时任务系统的噪音视为用户活动。首先提取用户/助手的对话内容和媒体事件，然后再进行分类。  
   - **特殊情况 - 午夜边界**：对于跨越午夜的夜间活动，扩展时间戳范围以包含之前的时间（例如，前一天 23:00-24:00），但仍需按消息时间戳进行筛选。  
   - **合并来源**：结合内存文件和会话日志的内容。内存文件记录用户的明确反思；会话日志记录对话流程和媒体内容。两者结合以构建完整的上下文。  
   - **备用方案**：如果内存数据较少，从会话日志中重建上下文，然后更新内存，以便后续运行使用更完整的数据。可以通过 `memory_search`（如果嵌入数据不可用则跳过）来整合历史上下文。  

3. **事件识别**：识别值得记录的内容：关键决策、情绪变化、重要时刻或共享的媒体文件。具体操作方法请参见 `references/media-handling.md`。此步骤会生成插件依赖的 `moments` 数据结构。  
   **图片处理（重要）**：  
      - 对每张提取的图片生成描述性替代文本  
      - 对图片进行分类（食物、自拍、截图、文档等）  
      - 将图片与相关事件关联起来（例如，早餐照片 → 早餐时刻）  
      - 将图片元数据与事件一起存储，用于日志嵌入  

4. **模式识别**：检测重复出现的主题、情绪波动和能量水平，并根据 `references/skill-recommendations.md` 将这些模式映射为个人成长的机会。  

5. **插件执行**：在预定的钩点执行所有已注册的插件。完整的插件生命周期请参见 `references/plugin-protocol.md`：  
   - `pre-analysis`：对话分析之前  
   - `post-moment-analysis`：账本和其他主要插件在此阶段执行  
   - `post-pattern-analysis`：模式检测之后  
   - `journal-generation`：插件在此阶段插入自定义内容  
   - `post-journal`：日志生成完成后  

6. **日志生成**：使用 `assets/daily-template.md` 将当天的事件合成漂亮的 Markdown 文件。遵循 `references/visual-design.md` 中的视觉设计指南。**仅嵌入精选的图片**，而非所有图片。优先展示重要内容和时刻。  
   - 将财务相关的截图路由到账本（收据、发票、交易证明）部分。  
   - 使用 `references/media-handling.md` 中规定的 Obsidian 格式，并添加描述性标题。  
   - 从文件系统中生成图片链接：计算图片路径相对于当前日志文件的路径。切勿输出绝对路径。  
   - **不要硬编码路径深度**（如 `../` 或 `../../`）：根据 `daily_file_path` 和 `image_path` 动态计算路径。  
   - **使用文件名作为唯一来源**：如果资产文件名为 `image_124917_2.jpg`，链接必须指向该文件名。  

7. **时间线整合**：如果发生了重要事件，使用 `assets/timeline-template.md` 和 `references/obsidian-format.md` 中的格式将其添加到主时间线文件 `timeline.md` 中。  

8. **成长映射**：如果检测到新的行为模式或技能兴趣，更新 `growth-map.md`（基于 `assets/growth-map-template.md`）。  

9. **个人资料更新**：更新长期用户资料（`profile.md`），以反映用户价值观、目标和性格特征的最新变化。具体方法请参见 `references/profile-evolution.md` 和 `assets/profile-template.md`。  

## ⏰ 定时任务与被动运行  
PhoenixClaw 设计为无需用户干预即可自动运行。它利用 OpenClaw 的内置定时系统，每天在当地时间 10:00（0 22 * * *）触发分析。  
- 设置详情请参见 `references/cron-setup.md`。  
- **运行模式**：主要为被动模式。AI 会主动总结当天的活动，无需用户请求。  

## 💬 显式触发命令  

虽然系统默认为被动模式，但用户可以使用以下命令直接与 PhoenixClaw 交互：  
- “显示我今天的日志/昨天的日志。”  
- “我今天完成了什么？”  
- “分析我上周的情绪模式。”  
- “生成我的每周/每月总结。”  
- “我在个人目标方面进展如何？”  
- “重新生成我的日志。”  

> [!警告] **手动调用 = 完整执行整个工作流程**  
> 当用户请求生成或重新生成日志时，必须执行上述完整的 9 个步骤。这可以确保：  
> - 包含所有图片（通过扫描会话日志）  
- 账本插件被执行（在 `post-moment-analysis` 钩点）  
- 所有插件按预定顺序执行  

> **常见错误**：  
> ❌ 仅调用 `memory_get`（会错过图片）  
> ❌ 跳过事件识别（插件无法触发）  
> ❌ 直接生成日志而忽略插件生成的定制内容  

## 📚 文档参考  
### 参考资料（`references/`）  
- `user-config.md`：初始设置和数据持久化配置。  
- `cron-setup.md`：夜间自动化的配置文件。  
- `plugin-protocol.md`：插件架构、钩点和集成协议。  
- `media-handling.md：从图片和多媒体中提取信息的策略。  
- `session-day-audit.js`：用于验证会话日志中目标日期消息覆盖情况的诊断工具。  
- `visual-design.md`：可读性和美观性的布局原则。  
- `obsidian-format.md`：确保与 Obsidian 和其他知识管理工具的兼容性。  
- `profile-evolution.md：系统如何维护用户的长期身份信息。  
- `skill-recommendations.md：根据日志内容推荐新技能的逻辑。  

### 资源文件（`assets/`）  
- `daily-template.md`：每日日志条目的模板。  
- `weekly-template.md`：高级每周总结的模板。  
- `profile-template.md`：个人资料文件的架构。  
- `timeline-template.md`：时间线文件的架构。  
- `growth-map-template.md`：成长地图的架构。