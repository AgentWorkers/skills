---
name: universal-skills-manager
description: AI技能的主协调者。负责从多个来源（SkillsMP.com、SkillHub 和 ClawHub）获取技能信息，管理这些技能的安装过程，并确保它们在 Claude Code、Gemini CLI、Google Anti-Gravity、OpenCode 等 AI 工具中的同步。该协调者同时支持用户级（全局）和项目级（本地）的技能管理需求。
homepage: https://github.com/jbendavi/universal-skills_mp-manager
disable-model-invocation: true
metadata:
  clawdbot:
    requires:
      bins: ["python3", "curl"]
    primaryEnv: SKILLSMP_API_KEY
---

## 版本：1.5.1  

### 通用技能管理器  

该技能使代理能够充当AI功能的集中式包管理器。它可以从多个来源发现技能——SkillsMP.com（精选的技能，支持AI语义搜索）、SkillHub（17.3万多个社区技能，无需API密钥）和ClawHub（5,700多个版本化的技能，支持语义搜索，无需API密钥）——并统一管理多个AI工具（Claude Code、Gemini、Anti-Gravity、OpenCode、Cursor等）中的技能，确保一致性和同步性。  

### 何时使用此技能  

在以下情况下激活此技能：  
- 用户希望**查找或搜索**新技能。  
- 用户希望**安装**技能（从搜索结果或本地文件）。  
- 用户希望**在不同AI工具之间同步**技能（例如：“将此Gemini技能复制到OpenCode中”）。  
- 用户请求在**用户范围与项目范围之间移动或复制**技能。  
- 用户在讨论技能/扩展时提到“Google Anti-Gravity”、“OpenCode”或“Gemini”。  
- 用户希望**将此技能打包用于claude.ai或Claude Desktop”（通过ZIP上传）。  

### 支持的生态系统  

该技能管理以下工具和范围。在操作前请务必确认这些路径存在：  

| 工具 | 用户范围（全局） | 项目范围（本地） |  
| :--- | :--- | :--- |  
| **Gemini CLI** | `~/.gemini/skills/` | `./.gemini/skills/` |  
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` | `./.antigravity/extensions/` |  
| **OpenCode** | `~/.config/opencode/skills/` | `./.opencode/skills/` |  
| **OpenClaw** | `~/.openclaw/workspace/skills/` | `./.openclaw/skills/` |  
| **Claude Code** | `~/.claude/skills/` | `./.claude/skills/` |  
| **OpenAI Codex** | `~/.codex/skills/` | `./.codex/skills/` |  
| **block/goose** | `~/.config/goose/skills/` | `./.goose/agents/` |  
| **Roo Code** | `~/.roo/skills/` | `./.roo/skills/` |  
| **Cursor** | `~/.cursor/extensions/` | `./.cursor/extensions/` |  

**claude.ai / Claude Desktop（需要ZIP上传）：**  
| 平台 | 安装方法 |  
| :--- | :--- |  
| **claude.ai** | 通过设置 → 功能 → 上传技能 |  
| **Claude Desktop** | 通过设置 → 功能 → 上传技能 |  

*注意：claude.ai和Claude Desktop无法访问本地环境变量。请使用“打包用于claude.ai/Desktop”功能（第5节）将API密钥嵌入ZIP文件中。*  

### 通用技能管理器的平台限制  

该技能需要网络访问权限来调用SkillsMP API、SkillHub API、ClawHub API和GitHub。请处理以下情况：  
- **如果用户请求将通用技能管理器本身打包/上传到claude.ai：**  
  告诉用户：“通用技能管理器无法在claude.ai上使用，因为它需要网络访问权限来调用SkillsMP API、SkillHub API和ClawHub API。claude.ai的代码执行环境不允许外部网络请求。但是，我可以为您打包其他技能以上传到claude.ai——只要这些技能不需要网络访问权限即可。”  
- **如果用户希望在Claude Desktop上使用通用技能管理器：**  
  告诉用户：“Claude Desktop具有网络访问权限。要在Claude Desktop上使用通用技能管理器，您可能需要在Cowork设置中扩展对这些域的访问权限：  
  - `skillsmp.com`（用于SkillsMP技能搜索）  
  - `skills.palebluedot.live`（用于SkillHub技能搜索）  
  - `clawhub.ai`（用于ClawHub技能搜索和直接文件下载）  
  - `api.github.com`和`raw.githubusercontent.com`（用于从GitHub下载技能）  
  这是一个实验性功能——Cowork的默认网络访问权限是受限的。请检查您的Cowork网络出站设置。”  

### 核心功能  

#### 1. 智能安装与同步  
**触发条件：**用户请求安装技能（例如：“安装调试技能”或“安装技能ID xyz”）。  
**流程：**  
1. **确定来源：**  
    - 如果来自SkillsMP搜索结果：使用API响应中的`githubUrl`。  
    - 如果来自SkillHub搜索结果：通过`/api/skills/{id}`获取`skillPath`和`branch`，然后构建GitHub树URL。  
    - 如果来自ClawHub搜索结果：使用`slug`通过ClawHub的 `/file`端点获取内容（见下文C节）。  
    - 如果通过技能名称/ID查找：搜索可用的来源（SkillsMP、SkillHub和/或ClawHub）。  
    - 如果是本地技能：确定来源路径。  
2. **验证仓库结构（关键步骤）：**  
    - 下载前，浏览GitHub仓库以确认技能文件夹的位置。  
    - 使用GitHub API列出目录内容：`GET /repos/{owner}/{repo}/contents?ref={branch}`。  
    - 查找包含`SKILL.md`的文件夹——这是实际的技能目录。  
    - 常见路径模式：`skill/`、`skills/{name}/`、根目录或自定义文件夹名称。  
    - 在生成下载URL之前确认正确的路径。  
3. **使用辅助脚本下载：**  
    - 使用位于该技能`scripts/`文件夹中的`install_skill.py`脚本：  
    （此处为代码块）  
    *脚本处理：原子安装、验证、子目录、安全检查。  
    ***安全特性：**如果目标目录是根技能目录，脚本将中止（退出代码4）。  
    ***更新检测：**如果技能存在，显示差异并提示用户确认。  
    ***安全扫描：**安装脚本会自动扫描下载的技能是否存在安全威胁（不可见字符、数据泄露、命令注入等）。在继续之前请查看任何发现的结果。  
4. **确定主要目标：**  
    - 询问：“这是要全局安装（用户范围）还是本地安装（项目范围）？”  
    * 确定主要使用的工具（例如，如果用户使用的是Claude Code，则Claude是主要工具）。  
5. **“同步检查”（关键步骤）：**  
    * **扫描：**检查系统中是否已安装其他支持的工具（查找它们的配置文件夹）。  
    * **建议：**“我看到您还安装了OpenCode和Cursor。是否也想将这些技能同步到它们？”  
6. **执行：**  
    * 为每个目标位置运行安装脚本。  
    * 确保保持标准结构。  
7. **报告成功：**  
    * 显示已安装的技能名称、作者和位置。  
    * 显示GitHub URL和星星数量以供参考。  

#### 2. “更新与一致性”检查  
**触发条件：**用户修改了技能或请求“同步”技能。  
**流程：**  
1. **比较：**检查所有已安装位置上的技能的修改时间或内容。  
2. **报告：**“Gemini中的‘code-review’技能比OpenCode中的版本更新。”  
3. **操作：**建议用新版本覆盖旧版本以确保一致性。  

#### 3. 多源技能发现  
**触发条件：**用户搜索技能（例如：“查找调试技能”或“搜索React技能”）。  
**流程：**  
1. **获取API密钥并选择来源：**  
    - **步骤1 - 环境变量：**检查 `$SKILLSMP_API_KEY`  
        （此处为代码块）  
        如果设置且不为空，使用SkillsMP作为主要搜索来源。  
        **注意：**使用`printenv`（而不是`echo $VAR`）——它直接查询进程环境，在不同shell环境中更可靠。  
    - **步骤2 - 配置文件：**检查该技能目录中的`config.json`文件：  
        （此处为代码块）  
        如果`skillsmp_api_key`字段有非空值，使用SkillsMP作为主要来源。  
    - **步骤3 - 选择来源：**如果没有找到API密钥，向用户提供选择：  
        > “我没有看到配置的SkillsMP API密钥。您有三个选项：  
        > A）提供您的SkillsMP API密钥（在skillsmp.com获取）——提供带有AI语义搜索的精选技能  
        > B）搜索SkillHub的开放目录——17.3万多个社区技能，无需API密钥  
        > C）搜索ClawHub——5,700多个版本化的技能，支持语义搜索，无需API密钥  
        > 您选择哪个？”  
        - 如果用户选择**A**：收集密钥，将其存储在会话内存中，然后继续使用SkillsMP。  
        - 如果用户选择**B**：继续使用SkillHub搜索（无需密钥）。  
        - 如果用户选择**C**：继续使用ClawHub搜索（无需密钥）。  
    * **安全注意事项：**切勿记录、显示或回显完整的API密钥值。  
    **对于claude.ai/Desktop用户：**环境变量不可用。请使用“打包用于claude.ai/Desktop”功能（第5节）创建包含API密钥的ZIP文件，或在提示时提供密钥。**  
2. **根据所选来源执行搜索：**  
    - **如果使用SkillsMP（主要来源，精选技能）：**  
        - **选择方法：**  
            - **关键词搜索**（`/api/v1/skills/search`）：用于特定术语的精确匹配。  
            - **AI语义搜索**（`/api/v1/skills/ai-search`）：用于自然语言查询（例如：“帮我调试代码”）。  
        - **重要提示：**始终先将API密钥捕获到本地变量中，然后使用它。在某些shell环境中直接使用 `$SKILLSMP_API_KEY` 可能会失败：  
        （此处为代码块）  
    - **解析：**从`data.skills[]`（关键词搜索）或`data.data[]`（AI搜索）中提取信息。  
    - 可用字段：`id`、`name`、`author`、`description`、`githubUrl`、`skillUrl`、`stars`、`updatedAt`。  
    - **注意：**SkillsMP需要`q`参数——没有浏览/列表端点。对于“顶级技能”或无特定查询的浏览，请使用SkillHub或ClawHub。**  
    - **如果使用SkillHub（开放目录，无需认证）：**  
        - **执行：**  
        （此处为代码块）  
    - **解析：**从`skills[]`数组中提取信息。  
    - 可用字段：`id`、`name`、`description`、`githubOwner`、`githubRepo`、`githubStars`、`downloadCount`、`securityScore`。  
    - **注意：**SkillHub不支持AI语义搜索——仅支持关键词搜索。**  
    - **如果使用ClawHub（版本化技能，支持语义搜索，无需认证）：**  
        - **选择方法：**  
            - **语义搜索**（`/api/v1/search`）：用于自然语言查询——按相似度`score`排序结果。  
            - **浏览/列表**（`/api/v1/skills`）：按人气、星星数量或最新更新时间浏览。  
        - **执行：**  
        （此处为代码块）  
    - **解析：**  
        - 语义搜索：从`results[]`数组中提取信息——每个结果包含`score`、`slug`、`displayName`、`summary`、`version`。  
        - **浏览：**从`items[]`数组中提取信息——每个结果包含`slug`、`displayName`、`summary`、`version`、`stats.stars`、`stats.downloads`。  
    - **显示结果（统一格式）：**  
        无论来源如何，都以一致的表格格式显示结果。包括**来源**列以指示来源：  
        （此处为代码块）  
        - 对于SkillsMP的AI搜索：同时显示相关性分数。  
        - 对于SkillHub：显示`securityScore`（如果可用）。  
        - 对于ClawHub的语义搜索：显示相似度`score`（如果可用）。  
        - 限制显示结果数量为10-15个以便于阅读。  
3. **搜索更多来源：**  
    在显示任何来源的结果后，提供搜索剩余未搜索来源的选项：  
        - **如果还有2个来源：**“还想搜索{source1}或{source2}吗？或者两个都搜索？”  
        - **如果只剩下1个来源：**“还想搜索{source}吗？”  
        可用的来源：SkillsMP（需要API密钥）、SkillHub（无需密钥）、ClawHub（无需密钥）。  
        如果用户同意：  
        - 使用相同的搜索词查询选定的来源。  
        - **去重：**比较不同来源的结果：  
            - SkillsMP ↔ SkillHub：通过完整的技能ID（`{owner}/{repo}/{path}`）。  
            - ClawHub ↔ 其他来源：通过技能名称（ClawHub使用slug，而不是GitHub路径）。  
        - 将唯一的结果添加到显示结果中，并标注来源标签。  
4. **提供安装选项：**  
    - 显示结果后，询问：“您想安装哪个技能？”  
    - 对于SkillsMP的结果：注意技能的`githubUrl`以获取内容。  
    - 对于SkillHub的结果：注意技能的`id`以获取详细信息（需要`skillPath`和`branch`）。  
    - 对于ClawHub的结果：注意技能的`slug`以通过ClawHub的 `/file`端点直接获取文件。  

#### 4. 技能矩阵报告  
**触发条件：**用户请求技能报告/概览（例如：“显示我的技能”、“我有哪些技能？”、“技能报告”、“比较我的工具”）。  
**流程：**  
1. **检测已安装的工具：**通过检查用户级别的技能目录是否存在来检测已安装的AI工具：  
    （此处为代码块）  
2. **收集所有技能：**  
    为每个检测到的工具列出技能文件夹：  
    （此处为代码块）  
3. **生成矩阵表格：**  
    创建一个markdown表格，其中：  
        - **行** = 技能名称（在所有工具中去除重复）。  
        - **列** = 仅显示系统中已安装的工具。  
        - **单元格** = ✅（已安装）或❌（未安装）。  
    示例输出：  
    （此处为代码块）  
4. **显示摘要：**  
    - 所有工具中的总技能数量。  
    - 仅在一个工具中独有的技能。  
    - 在所有工具中都安装的技能。  

#### 5. 为claude.ai / Claude Desktop打包技能  

**触发条件：**用户希望在该技能在claude.ai或Claude Desktop中使用（例如：“将此技能打包用于claude.ai”、“为Claude Desktop创建ZIP文件”、“我想将此技能上传到claude.ai”、“准备技能以供网络上传”）。  
**流程：**  
1. **解释流程：**  
    “我将创建一个ZIP文件，以便将其上传到claude.ai或Claude Desktop。由于云环境无法访问您的本地环境变量，我将在包中嵌入您的API密钥。”  
2. **收集API密钥：**  
    - **询问：**“请提供您的SkillsMP API密钥。您可以在https://skillsmp.com获取。”  
    - 等待用户提供密钥。  
    * **安全注意事项：**不要将密钥显示或返回给用户。**  
    * **注意：**API密钥会存储在ZIP包内的`config.json`文件中。此技能在搜索技能时仅在运行时使用API密钥与SkillsMP进行身份验证。**  
3. **创建包内容：**  
    - **创建临时目录结构：**  
    （此处为代码块）  
    - 生成包含用户API密钥的`config.json`文件：  
    （此处为代码块）  
4. **创建ZIP文件：**  
    - 使用Python创建ZIP文件：  
    （此处为代码块）  
    - 或者，提供可下载的ZIP文件。  
5. **提供上传说明：**  
    - “您的技能包已准备好！使用方法如下：”  
    - “1. 下载ZIP文件：`universal-skills-manager.zip`。”  
    - “2. 转到claude.ai → 设置 → 功能。”  
    - “3. 滚动到技能部分并点击‘上传技能’。”  
    - “4. 选择ZIP文件并上传。”  
    - “5. 启用技能并开始使用！”  
6. **安全提醒：**  
    - **注意：**此ZIP文件包含您的API密钥。请不要公开分享或将其提交到版本控制系统中。”  

### 操作规则  
1. **结构完整性：**安装时，确保技能有自己的文件夹（例如：`.../skills/my-skill/`）。不要将文件直接放入根技能目录。  
2. **冲突处理：**如果目标位置已经存在技能，请**始终**询问用户是否要覆盖它，除非用户明确请求“强制同步”。  
3. **关于OpenClaw的注意事项：**如果`openclaw.json`中未启用`skills.load.watch`，OpenClaw可能需要重启才能加载新技能。安装后请提醒用户这一点。  
4. **跨平台适配：**  
    - Gemini使用`SKILL.md`文件格式。  
    - 如果OpenCode或Anti-Gravity需要特定的清单文件（例如`manifest.json`），则在安装期间根据`SKILL.md`的前言文件生成一个基本的清单文件。  

### 可用的工具  
- `bash`（curl）：用于调用SkillsMP.com、SkillHub（skills.palebluedot.live）和ClawHub（clawhub.ai）的API；从GitHub或ClawHub直接获取技能内容。  
- `web_fetch`：从GitHub raw URLs、SkillHub API或ClawHub API获取技能内容（作为curl的替代方案）。  
- `read_file` / `write_file`：管理本地技能文件。  
- `glob`：在本地目录中查找现有技能。  

### 实现细节  

### 技能结构  
技能通常包含：  
- **SKILL.md**（必需）：包含前言的主要说明文件。  
- **参考文档**：额外的文档文件。  
- **脚本**：辅助脚本（Python、shell等）。  
- **配置文件**：JSON、YAML配置文件。  

### 安装逻辑  

#### A. 从SkillsMP API安装  
1. **获取技能内容：**  
    - 将`githubUrl`转换为原始内容URL：  
        （此处为代码块）  
    - 使用curl或`web_fetch`获取SKILL.md内容。  
2. **创建目录：**  
    - 使用API响应中的技能`name`创建目录：`.../skills/{skill-name}/`  
    - 例如：`.../skills/code-debugging/`  
3. **保存SKILL.md：**  
    - 将获取的内容写入新目录中的`SKILL.md`文件。  
    - 保留原始的YAML前言和内容。  
4. **处理其他文件（可选）：**  
    - 检查GitHub仓库是否有其他文件（参考文档、脚本等）。  
    - （可选）获取并保存它们以维护完整的技能包。  
5. **确认：**  
    - 报告：“已安装‘{name}’，作者为{author}，路径为{path}。”  
    - 显示GitHub URL和星星数量。  
    - 提供与其他AI工具同步的选项。  

#### B. 从SkillHub安装  
1. **获取技能详细信息：**  
    - 使用搜索结果中的技能`id`获取完整详细信息：  
        （此处为代码块）  
    - **重要提示：**`id`字段（例如`wshobson/agents/debugging-strategies`）并不对应仓库中的文件路径。必须使用详细信息端点来获取实际的`skillPath`和`branch`。  
    - 从响应中提取`githubOwner`、`githubRepo`、`branch`、`skillPath`。  
2. **构建GitHub URL：**  
    - 根据详细信息响应构建GitHub树URL：  
        （此处为代码块）  
    - 例如：`https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`  
3. **使用辅助脚本下载：**  
    - 从这一步开始，安装流程与SkillsMP相同：  
        （此处为代码块）  
4. **确认：**  
    - 报告：“已从SkillHub安装‘{name}’，路径为{path}。”  
    - 显示GitHub URL和星星数量。  
    - 提供与其他AI工具同步的选项。  

#### C. 从ClawHub安装  
ClawHub直接托管技能文件（不在GitHub上），因此安装流程会绕过`install_skill.py`，并通过ClawHub的API获取内容：  
1. **获取SKILL.md内容：**  
    - 使用ClawHub的文件端点获取原始SKILL.md内容：  
        （此处为代码块）  
    - **重要提示：**此端点返回的是原始`text/plain`内容，而不是JSON。将响应体直接保存为文件。  
    - 可以使用`x-content-sha256`响应头来验证文件完整性。  
2. **处理多文件技能（如果适用）：**  
    - 如果技能有额外的文件（脚本、配置文件），使用ClawHub的下载端点：  
        （此处为代码块）  
    - 要检查技能是否有多个文件，请检查`GET /api/v1/skills/{slug}`的详细响应——`latestVersion`字段可能指示文件数量。  
3. **运行安全扫描：**  
    - 由于绕过了`install_skill.py`，因此需要手动运行安全扫描：  
        （此处为代码块）  
    - 在继续之前请查看任何发现的结果。ClawHub集成了VirusTotal扫描工具；我们的扫描提供了额外的安全保障。  
4. **验证YAML前言：**  
    - 验证SKILL.md是否具有有效的YAML前言（名称、描述字段）。  
    - 如果无效，警告用户并询问是否继续。  
5. **创建目录并安装：**  
    - 创建目标目录：`.../skills/{slug}/`  
    - 将所有文件从临时目录复制到目标位置：  
        （此处为代码块）  
6. **确认：**  
    - 报告：“已从ClawHub安装‘{displayName}’（版本{version}），路径为{path}。”  
    - 显示版本信息和星星数量。  
    - 提供与其他AI工具同步的选项。  

#### D. 从本地来源安装（同步/复制）  
1. **检索：**从源目录读取所有文件。  
2. **创建目录：**创建目标目录`.../skills/{slug}/`。  
3. **保存文件：**将所有文件复制到新位置。  

### SkillsMP API配置  
**基础URL：**`https://skillsmp.com/api/v1`  

**认证：**  
（此处为代码块）  

**可用端点：**  
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}`  
- `GET /api/v1/skills/ai-search?q={query}`  

**响应格式（关键词搜索）：**  
（此处为代码块）  

**响应格式（AI搜索）：**  
（此处为代码块）  

**错误处理：**  
- `401`：API密钥无效或缺失。  
- `400`：缺少必需的查询参数。  
- `500`：内部服务器错误。  

### SkillHub API配置  
**基础URL：**`https://skills.palebluedot.live/api`  

**认证：**无需认证（开放API）  

**可用端点：**  
- `GET /api/skills?q={query}&limit={20}` — 按关键词搜索技能。  
- `GET /api/skills/{id}` — 获取技能的完整详细信息（包括`skillPath`、`branch`、`rawContent`）。  
- `GET /api/categories` — 列出技能类别。  
- `GET /api/health` — 健康检查。  

**搜索响应格式：**  
（此处为代码块）  

**详细响应格式（GET /api/skills/{id}）：**  
（此处为代码块）  

**安装所需的字段：**  
- `skillPath`：GitHub仓库中的实际目录路径（关键字段——`id`与文件路径不匹配）。  
- `branch`：分支名称（例如`main`）。  
- `githubOwner` + `githubRepo`：用于构建GitHub URL。  
- `rawContent`：SKILL.md的完整内容（如果GitHub无法访问时可用）。  

**错误处理：**  
- `404`：技能未找到。  
- `500`：内部服务器错误。  

### ClawHub API配置  
**基础URL：**`https://clawhub.ai/api/v1`  

**认证：**无需认证（开放API）  

**速率限制：**每IP每分钟120次读取（在`x-ratelimit-remaining`和`x-ratelimit-reset`响应头中显示）。  

**可用端点：**  
- `GET /api/v1/search?q={query}&limit={20}` — 按相似度排名进行语义搜索。  
- `GET /api/v1/skills?limit={20}&sort={stars|downloads|updated|trending}&cursor={cursor}` — 带有分页功能的浏览/列表。  
- `GET /api/v1/skills/{slug}` — 获取技能的完整详细信息（所有者、版本）。  
- `GET /api/v1/skills/{slug}/file?path={filepath}&version={ver}` — 下载技能的原始文件（文本格式，不是JSON）。  
- `GET /api/v1/download?slug={slug}&version={ver}` — 下载技能的ZIP文件。  

**浏览响应格式（GET /api/v1/skills）：**  
（此处为代码块）  

**详细响应格式（GET /api/v1/skills）：**  
（此处为代码块）  

**文件端点（GET /api/v1/skills/{slug}/file?path=SKILL.md）：**  
- 返回原始`text/plain`内容（不是JSON）。  
- 响应头包含`x-content-sha256`（完整性哈希）和`x-content-size`（文件大小）。  
- 使用`version`查询参数获取特定版本（默认为最新版本）。  

**与SkillsMP/SkillHub的关键区别：**  
- **直接托管：**ClawHub直接托管技能文件——无需构建GitHub URL。  
- **版本化技能：**每个技能都有明确的版本号；使用`version`参数来指定版本。  
- **基于slug的ID：**技能通过`slug`标识（例如`self-improving-agent`），而不是GitHub路径。  
- **内置语义搜索：**`/search`端点使用向量相似度进行搜索。  
- **VirusTotal集成：**ClawHub通过VirusTotal进行扫描；`moderation`字段表示状态。  

**错误处理：**  
- `404`：技能或文件未找到。  
- `429`：超出速率限制（每分钟120次读取）。  
- `500`：内部服务器错误。  

### 指南：**  
- **多源搜索：**当有API密钥时，优先使用SkillsMP作为主要来源。提供SkillHub和ClawHub作为备用或额外来源。  
- **优先使用AI/语义搜索：**对于自然语言查询，使用SkillsMP的 `/ai-search`或ClawHub的 `/search`（两者都支持语义匹配）。  
- **来源标记：**始终在结果中标明来源（`[SkillsMP]`、`[SkillHub]`或`[ClawHub]`），以便用户区分来源。  
- **从SkillHub安装技能时：**始终先获取详细信息端点以获取正确的`skillPath`和`branch`。切勿尝试将`id`字段解析为文件路径。  
- **ClawHub直接托管：**ClawHub直接托管技能文件——使用`/file`端点获取内容。无需构建GitHub URL。使用`slug`字段作为技能标识符。  
- **ClawHub版本控制：**ClawHub技能有明确的版本号。在安装时显示版本号。如果需要，使用`version`参数指定特定版本。  
- **去重：**在显示来自多个来源的结果时，通过完整的技能ID（`{owner}/{repo}/{path}`）去重；ClawHub与其他来源通过技能名称去重（因为ClawHub使用slug）。  
- **验证内容：**从任何来源获取内容后，验证SKILL.md是否具有有效的YAML前言。  
- **结构完整性：**保持`.../skills/{skill-name}/SKILL.md`的结构。  
- **同步：**安装技能后，提供将其同步（复制）到其他检测到的AI工具的选项。  
- **GitHub URL：**对于SkillsMP/SkillHub的安装，始终将树URL转换为raw.githubusercontent.com URL以获取内容。  
- **安全性：**无论来源如何，都对所有安装进行安全扫描（SkillsMP、SkillHub或ClawHub）。SkillHub的`securityScore`和ClawHub的`moderation`状态仅用于提供信息。我们在安装时使用`scan_skill.py`进行额外扫描。