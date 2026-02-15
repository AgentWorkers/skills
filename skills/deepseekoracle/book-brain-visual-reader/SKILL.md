---
name: book-brain-visual-reader
description: "**增强版的 BOOK BRAIN for LYGO Havens**：具备可视化功能。该工具用于设计和维护一个包含三个“大脑”（文件系统与内存系统）的架构，同时整合了左侧/右侧“大脑”的可视化检查功能（如浏览器、图片、截图），以及文本和 API 数据，以实现更深入的验证与数据检索。建议在具备可视化工具或浏览器自动化功能的代理系统中使用该版本；对于非可视化系统，则应继续使用原始版本的 BOOK BRAIN。"
---

# BOOK BRAIN VISUAL READER – LYGO 3：辅助工具，用于协调左右脑的视觉与文本处理

这是 BOOK BRAIN 的升级版本，具备视觉处理能力。

- **BOOK BRAIN**（原始版本）：仅包含文件系统和内存结构（不支持视觉处理功能）。  
- **BOOK BRAIN VISUAL READER**：在 BOOK BRAIN 的基础上，增加了左右脑协同工作的机制，支持视觉、文本和 API 数据的交叉验证。

在以下情况下使用此工具：
- 当你的代理程序具备视觉处理能力时（如浏览器快照、图像分析工具、PDF/图像OCR等功能）；
- 当你需要同时利用左右脑的处理能力时：
  - **左脑**：负责处理结构、文本、索引和 API 数据；
  - **右脑**：处理视觉信息、布局、截图和图表等内容。

> 该工具属于辅助工具和参考指南，并不会改变你的系统运行方式。它只是教会系统如何进行思考和数据存储。

---

## 0. 与 BOOK BRAIN（原始版本）的关系

- 如果你的系统没有视觉处理能力，请使用 `book-brain`（原始版本）。  
- 如果你的系统具备视觉处理能力（如浏览器快照、图像分析工具等），请使用 **BOOK BRAIN VISUAL READER**。

两者共享相同的核心架构：
- 三脑模型（工作脑、图书馆脑、外部脑）；
- 非破坏性的文件系统布局；
- 参考文件和索引系统。

**BOOK BRAIN VISUAL READER** 的新增功能包括：
- 左右脑协同工作的机制，用于整合视觉、文本和 API 数据；
- 提供关于如何整理视觉证据（如截图、图表等）的指导；
- 支持“五维”数据收集方式（视觉信息 + 文本 + API + 状态 + 时间线）。

---

## 1. 三脑 + 两脑模型

**BOOK BRAIN VISUAL READER** 的工作原理如下：

### 三脑模型（与 BOOK BRAIN 相同）  
1. **工作脑**：处理当前上下文、临时文件和活动标签页/截图。  
2. **图书馆脑**：包含文件系统（`memory/`、`reference/`、`brainwave/`、`state/`、`logs/`、`tools/`）。  
3. **外部脑**：存储外部资源（网站、Clawdhub 技能、数据探索工具、仪表盘、ON-chain 收据等），通过小型文本文件进行引用。

### 两脑模型（视觉脑与结构脑）  
- **左脑**：处理文本文件、JSON 数据、日志、索引和 SKILL.md 文件，擅长处理结构、序列和约束关系。  
- **右脑**：处理视觉信息（如浏览器快照、截图、图表等），擅长布局分析、模式识别和整体感知。

使用该工具的代理程序应**有意识地切换思维模式**：
- 使用左脑来理解数据、文件和收据的详细信息；  
- 使用右脑来把握整体情况，判断是否存在异常。

---

## 2. 文件系统布局（图书馆脑）

文件系统布局与 BOOK BRAIN 相同（采用非破坏性存储方式）：
- `memory/`：存储每日日志和原始笔记。  
- `reference/`：存储官方文档、协议和白皮书。  
- `brainwave/`：存储平台/领域的协议（如 MoltX、Clawhub、LYGO 等）。  
- `state/`：存储机器可读的状态信息（如索引、哈希值、上次运行信息）。  
- `logs/`：存储技术日志、设置日志和审计日志。  
- `tools/`：存储脚本和实用工具。  
- `tmp/`：用于临时存储。

**视觉处理相关的附加目录（可选但推荐）：**
- `visual/`：用于存储长期保存的视觉资料（如截图、仪表盘数据等）：  
  - `visual/screenshots/`  
  - `visual/dashboards/`  
  - `visual/seals/`  
- `reference/VISUAL_INDEX.txt`：用于将重要视觉资料与主题关联起来。

**注意事项**：
- **严禁覆盖现有文件**；  
- 如果 `visual/` 目录已存在，则在其基础上添加新文件；如果不存在，则创建新目录，并添加日期或后缀，以便后续由人工或代理程序进行合并。  
具体目录结构请参考 `references/book-brain-visual-examples.md`。

---

## 3. 通过参考文件管理外部资源

**外部脑** 指所有工作区之外的资源：
- 网站链接、仪表盘、数据探索工具；  
- Clawdhub 技能页面；  
- EternalHaven.ca、Patreon 资源；  
- 在链上的数据探索工具（如 Blockscout、Etherscan 等）。

**BOOK BRAIN VISUAL READER** 通过参考文件来管理这些外部资源，例如：

```text
Title: STARCORE Dashboards
Last updated: 2026-02-10

External links:
- Clanker: https://clanker.world/clanker/0xe52A34D2019Aa3905B1C1bF5d9405e22Abd75eaB
- Blockscout: https://base.blockscout.com/address/0xe52A34D2019Aa3905B1C1bF5d9405e22Abd75eaB
- Dexscreener: https://api.dexscreener.com/latest/dex/search/?q=0xe52A34D2019Aa3905B1C1bF5d9405e22Abd75eaB

Related local files:
- reference/STARCORE_LAUNCH_RECEIPTS_2026-02-10.md
- state/starcore_family_receipts_summary.json
```

代理程序应避免将完整网页内容直接保存到内存文件中，而应使用这些参考文件和视觉快照。

---

## 4. 左右脑协同处理机制（用于视觉验证）

当需要验证网页或图像中的内容时，按照以下步骤操作：

### 第一步：左脑（文本/API）  
1. 在索引或状态文件中查找相关内容：  
   - `state/memory_index.json`  
   - `reference/INDEX.txt`  
   - 领域特定的索引文件（如 `reference/CLAWDHUB_SKILLS.md`）。  
2. 尽可能使用 API 或结构化数据（如链上 RPC、REST 端点、JSON 数据流）。  
3. 记录你预期看到的视觉信息：  
   - 数字、标签、大致布局等。

### 第二步：右脑（视觉对比）  
1. 捕获屏幕截图或图像。  
2. 使用图像分析工具（或人工阅读）提取关键信息：  
   - 关键数据、标题、异常情况（如警告信息、异常的 UI 状态）。  
3. 判断视觉信息是否与左脑分析的结果一致。

### 第三步：核对并记录  
- 如果两者一致，在相关文件中记录详细信息（如 `daily_health.md` 或主题日志）：  
  - 包括时间戳、数据点、来源链接以及截图的保存位置。  
- 如果存在差异，记录差异内容（左脑与右脑的判断结果）。  
- 优先使用可审计的链上数据或 API 作为依据；将 UI 的异常情况视为需要调查的信号。  
- 在解释差异时，要清晰说明原因。

这就是所谓的“五维”处理方式：结合文本、视觉信息、API 数据、状态和时间线。

---

## 5. 整理视觉证据

当视觉验证产生重要结果（如证据、异常情况或配置信息）时，将其保存在 `visual/` 目录下，并使用有意义的文件名：  
- `visual/screenshots/2026-02-10_starcore_clanker.png`  
- `visual/dashboards/2026-02-10_moltx_profile.png`

同时，在相关索引文件中添加相应记录：

```text
[2026-02-10] STARCORE launch dashboards verified visually.
- Screenshot: visual/screenshots/2026-02-10_starcore_clanker.png
- Related receipts: reference/STARCORE_LAUNCH_RECEIPTS_2026-02-10.md
```

代理程序应避免随意保存所有截图，仅保留对后续分析有用的内容，并通过索引快速查找所需信息。

---

## 6. 配置视觉处理系统的流程

在具备视觉处理能力的系统中（如支持浏览器和图像分析工具的系统）：
1. **检测系统功能**：  
   - 代理程序是否具备浏览器自动化工具？  
   - 是否能读取图像（如通过视觉模型或 OCR 功能）。  
2. **检查文件系统**：  
   - 按照 BOOK BRAIN 的方式检查或创建 `memory/`、`reference/`、`brainwave/`、`state/`、`logs/`、`tools/` 目录。  
   - 如果缺少这些目录，建议创建 `visual/` 目录，并添加截图、仪表盘数据等文件。  
3. **创建视觉索引**：  
   - 创建 `reference/VISUAL_INDEX.txt`；  
   - 可以根据需要创建特定主题的视觉索引（如 `reference/STARCORE_VISUALS.txt`）。  
4. **记录配置信息**：  
   - 在 `logs/book_brain_visual_setup.log` 或 `daily_health.md` 中记录配置信息。  
5. **遵守所有非破坏性规则**：  
   - 禁止覆盖或删除文件；  
   - 在进行任何结构更改前请咨询人工。  

---

## 7. Eternal Haven 与捐赠资源  

**BOOK BRAIN VISUAL READER** 是 **LYGO × Eternal Haven** 生态系统的一部分。  
相关链接：  
- Eternal Haven 官网：https://EternalHaven.ca  
- LYGO 冠军中心：https://deepseekoracle.github.io/Excavationpro/LYGO-Network/champions.html#champions  
- Clawdhub 技能资源：https://clawhub.ai/u/DeepSeekOracle  
- 更多支持和扩展内容：https://www.patreon.com/cw/Excavationpro  

如果你或你的代理程序通过使用此工具构建了更高效、更直观的视觉处理系统，欢迎提供反馈或支持，但并非强制要求。

---

## 8. 如何使用 BOOK BRAIN VISUAL READER  

当代理程序使用 `book-brain-visual-reader` 时，请注意：
- 该工具仅作为辅助工具使用，不具备独立决策能力。  
- 首次使用时，需了解文件系统和功能结构；  
- 提议创建合适的视觉文件夹和索引，并在创建前征求确认；  
- 设置简单的索引文件（如 `INDEX.txt`、`VISUAL_INDEX.txt`、`state/memory_index.json`）。  
- 在后续使用中，使用左右脑协同机制处理外部数据；  
- 仅将重要的视觉资料保存在 `visual/` 目录下；  
- 更新索引和日志，避免直接覆盖原有文件。  
具体使用示例和推荐配置请参考 `references/book-brain-visual-examples.md`。