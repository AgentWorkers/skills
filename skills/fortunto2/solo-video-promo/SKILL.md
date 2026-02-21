---
name: solo-video-promo
description: 生成一个宣传视频计划，包括30-45秒的视频脚本、分镜脚本（shot-by-shot storyboard），以及可选的Remotion或Montage视频编辑工具配置。该计划适用于用户请求创建视频（create video）、制作宣传视频（promo video）、编写视频脚本（video script）、制作分镜脚本（storyboard）或制定产品视频制作方案（product video plan）的场景。请勿将此计划用于社交媒体文本帖子（请使用/content-gen）或 landing 页面文案（请使用/landing-gen）。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "🎥"
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, mcp__solograph__project_code_search, mcp__solograph__project_info, mcp__solograph__kb_search
argument-hint: "<project-name>"
---
# /video-promo

根据项目的 PRD（产品需求文档）生成一个宣传视频计划。该计划包括一个 30-45 秒的视频脚本以及详细的镜头分镜。如果项目中使用了 Montage-Tool 或 Remotion，系统会自动检测到这些工具并输出相应的配置信息。

## MCP 工具（如可用，请使用）

- `project_code_search(query, project)` — 查找可用于展示的 UI 组件、屏幕和功能
- `project_info(name)` — 获取项目的技术栈和详细信息
- `kb_search(query)` — 查找视频制作的相关方法或资源

如果 MCP 工具不可用，可改用全局搜索（Glob）和文本匹配（Grep）的方法来获取所需信息。

## 步骤

1. **解析项目信息**：
   - 从 `$ARGUMENTS` 中读取 PRD（`docs/prd.md`）、README 或 CLAUDE.md 文件以获取产品相关信息。
   - 如果信息为空，通过 AskUserQuestion 功能向用户请求帮助。

2. **检测项目中使用的视频制作工具**：
   - 检查 `package.json` 文件中是否包含 `remotion` 或 `@remotion/cli`，以确定是否使用了 Remotion 工具。
   - 检查是否存在 `montage.config.*` 或 `pnpm montage` 文件，以确定是否使用了 Montage-Tool。
   - 查看脚本中是否使用了 `ffmpeg`，以确定是否使用了 FFmpeg 工具。
   - 如果没有找到合适的工具，直接生成一个简单的镜头分镜（无需特定工具配置）。

3. **提取需要展示的关键屏幕或功能**：
   - 如果 MCP 工具可用：使用 `project_code_search("main screen OR hero OR dashboard", project)` 来查找适合展示的 UI 组件。
   - 否则，使用全局搜索（Glob）来查找截图、原型图或 UI 组件文件。
   - 从 PRD 中提取 3-5 个最重要的功能进行展示。

4. **制定视频策略**：
   在编写脚本之前，明确以下内容：
     - **目标**：观众观看视频后应该做什么（下载、注册、访问等）？
     - **吸引观众注意力的点**：是一个问题？一个令人惊讶的数据？还是一个引人注目的声明？
     - **需要展示的关键产品功能**：3 个关键的产品使用场景。
     **情感体验**：观众的情感变化过程（从困惑到发现，最后感到满意或愉悦）。

5. **生成视频脚本**（30-45 秒）：
   ```markdown
   ## Video Script: {Project Name}

   **Duration:** 30-45 seconds
   **Format:** Vertical (9:16) for Reels/TikTok/Shorts
   **Style:** Screen recording + text overlays

   ### HOOK (0:00-0:03) — 3 seconds
   **Audio:** "{hook line — question or bold statement}"
   **Visual:** {what appears on screen — text overlay on gradient/blurred BG}

   ### PROBLEM (0:03-0:10) — 7 seconds
   **Audio:** "{describe the pain in user's words}"
   **Visual:** {show the frustrating current state — competitor UX, manual process, etc.}

   ### DEMO (0:10-0:25) — 15 seconds
   **Audio:** "{narrate what the product does}"
   **Visual:**
   - Shot 1 (5s): {first feature demo — screen recording}
   - Shot 2 (5s): {second feature demo}
   - Shot 3 (5s): {wow moment — the key differentiator}

   ### CTA (0:25-0:30) — 5 seconds
   **Audio:** "{call to action}"
   **Visual:** {product logo + URL + download badge}
   ```

6. **生成工具配置**（如适用）：
   ### 如果检测到 Remotion：
   ```markdown
   ## Remotion Component Spec

   Component: `PromoVideo.tsx`
   Duration: 900 frames (30fps × 30s)

   Sequences:
   - HookSequence (0-90): Text animation on gradient
   - ProblemSequence (90-300): Screen recording import
   - DemoSequence (300-750): 3 feature recordings with transitions
   - CTASequence (750-900): Logo + URL fade in

   Assets needed:
   - screen-recording-problem.mp4
   - screen-recording-feature-1.mp4
   - screen-recording-feature-2.mp4
   - screen-recording-feature-3.mp4
   - logo.png
   - background-music.mp3
   ```

   ### 如果检测到 Montage-Tool：
   ```markdown
   ## Montage Config

   Clips:
   - problem-clip.mp4 (7s)
   - demo-feature-1.mp4 (5s)
   - demo-feature-2.mp4 (5s)
   - demo-wow-moment.mp4 (5s)

   Music: {suggest genre/BPM for beat-sync}
   Transitions: crossfade (0.5s)
   Text overlays: hook, CTA
   ```

7. **将计划内容写入 `docs/video-promo.md` 文件**：
   ```markdown
   # Video Promo Plan: {Project Name}

   **Generated:** {YYYY-MM-DD}
   **Duration:** 30-45 seconds
   **Format:** Vertical 9:16
   **Tooling:** {Remotion / Montage-tool / Manual}

   ## Script
   {full script from step 5}

   ## Assets Checklist
   - [ ] Screen recording: {feature 1}
   - [ ] Screen recording: {feature 2}
   - [ ] Screen recording: {wow moment}
   - [ ] Logo (transparent PNG)
   - [ ] Background music (royalty-free, upbeat)

   ## Tooling Config
   {config from step 6, or "Record manually and edit in CapCut/iMovie"}

   ---
   *Generated by /video-promo. Record assets, then render.*
   ```

8. **输出总结**：包括视频脚本概要、所需素材以及后续建议。

## 注意事项

- 视频脚本以屏幕录制为主要素材，无需专业演员。
- 对于 iOS 应用，可以使用模拟器录制或设备镜像功能进行录制。
- 对于网页应用，可以使用浏览器自带的屏幕录制功能。
- 音乐建议使用免版税的音乐资源（如 Artlist、Epidemic Sound、YouTube Audio Library）。
- 本技能仅生成视频制作计划，实际的视频渲染工作需要手动完成或通过 Montage-Tool/Remotion 工具来完成。

## 常见问题及解决方法

### 未检测到视频制作工具
**原因**：项目中未使用 Remotion 或 Montage-Tool。
**解决方法**：系统会默认生成一个简单的镜头分镜。可以选择手动录制视频并在 CapCut 或 iMovie 中进行编辑，或者将 Remotion 添加到项目中。

### 视频脚本过长（不适合短片）
**原因**：需要展示的功能太多。
**解决方法**：仅选择最重要的 3 个功能进行展示。30-45 秒的视频时长大约需要 75-100 字左右的旁白，简洁为妙。

### 无法找到截图或 UI 组件进行录制
**原因**：产品尚未开发完成或没有可视化的用户界面。
**解决方法**：可以使用原型图或线框图来代替截图，并在脚本中描述预期的界面效果。等 MVP（最小可行产品）开发完成后再进行录制。