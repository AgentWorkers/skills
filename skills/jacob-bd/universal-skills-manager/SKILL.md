---
name: universal-skills-manager
description: AI技能的主协调者。负责从多个来源（SkillsMP.com、SkillHub 和 ClawHub）发现技能，管理这些技能的安装过程，并确保它们在 Claude Code、Gemini CLI、Google Anti-Gravity、OpenCode 等 AI 工具之间的同步。该协调者同时处理用户级（全局）和项目级（本地）的技能管理需求。
homepage: https://github.com/jbendavi/universal-skills_mp-manager
disable-model-invocation: true
metadata:
  clawdbot:
    requires:
      bins: ["python3", "curl"]
    primaryEnv: SKILLSMP_API_KEY
---

## 版本：1.5.3  

### 通用技能管理器  

该技能使代理能够充当AI功能的集中式包管理器。它可以从多个来源发现技能——SkillsMP.com（精选的技能，支持AI语义搜索）、SkillHub（17.3万多个社区技能，无需API密钥）和ClawHub（5,700多个版本化的技能，支持语义搜索，无需API密钥）——并统一管理多个AI工具（Claude Code、Gemini、Anti-Gravity、OpenCode、Cline、Cursor等）中的技能，确保一致性和同步性。  

### 何时使用该技能  

在以下情况下激活该技能：  
- 用户希望**查找或搜索**新技能。  
- 用户希望**安装**技能（从搜索结果或本地文件）。  
- 用户希望**在不同AI工具之间同步**技能（例如：“将此Gemini技能复制到OpenCode”）。  
- 用户请求在**用户范围与项目范围之间移动或复制**技能。  
- 用户在讨论技能/扩展时提到“Google Anti-Gravity”、“OpenCode”或“Gemini”。  
- 用户希望**将该技能打包以便上传到claude.ai或Claude Desktop”（需要ZIP格式）。  

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
| **Cursor** | `~/.cursor/skills/` | `./.cursor/skills/` |  
| **Cline** | `~/.cline/skills/` | `./.cline/skills/` |  

**claude.ai / Claude Desktop（需要ZIP上传）：**  
| 平台 | 安装方法 |  
| :--- | :--- |  
| **claude.ai** | 通过设置 → 功能 → 上传技能 |  
| **Claude Desktop** | 通过设置 → 功能 → 上传技能 |  

*注意：claude.ai和Claude Desktop无法访问本地环境变量。请使用“Package for claude.ai/Desktop”功能（第5节）将API密钥嵌入ZIP文件中。*  

### 通用技能管理器的平台限制  

该技能需要网络访问权限来调用SkillsMP API、SkillHub API、ClawHub API和GitHub。请处理以下情况：  
- **如果用户请求将通用技能管理器本身打包/上传到claude.ai：**  
  告诉用户：“通用技能管理器无法在claude.ai上使用，因为它需要网络访问权限来调用SkillsMP API、SkillHub API、ClawHub API和GitHub API。claude.ai的代码执行环境不允许外部网络请求。但是，我可以为您打包其他技能以上传到claude.ai——只要这些技能不需要网络访问权限即可。”  
- **如果用户希望在Claude Desktop上使用通用技能管理器：**  
  告诉用户：“Claude Desktop具有网络访问权限。要在Claude Desktop上使用通用技能管理器，您可能需要在Cowork设置中扩展网络访问权限：  
  - `skillsmp.com`（用于SkillsMP技能搜索）  
  - `skills.palebluedot.live`（用于SkillHub技能搜索）  
  - `clawhub.ai`（用于ClawHub技能搜索和直接文件下载）  
  - `api.github.com`和`raw.githubusercontent.com`（用于从GitHub下载技能）”  
  *注意：这仅适用于实验性环境。请检查Cowork的网络出站设置。*  

### 核心功能  

#### 1. 智能安装与同步  
**触发条件：** 用户请求安装技能（例如：“安装调试技能”或“安装技能ID xyz”）。  
**操作步骤：**  
1. **确定来源：**  
   - 如果来自SkillsMP搜索结果：使用API响应中的`githubUrl`。  
   - 如果来自SkillHub搜索结果：通过`/api/skills/{id}`获取`skillPath`和`branch`，然后构建GitHub树URL。  
   - 如果来自ClawHub搜索结果：使用`slug`通过ClawHub的 `/file`端点获取内容（详见第C节）。  
   - 如果通过技能名称/ID查找：在SkillsMP、SkillHub和/或ClawHub中搜索该技能。  
   - 如果是本地技能：确定来源路径。  
2. **验证仓库结构（关键步骤）：**  
   - 下载前，浏览GitHub仓库以确认技能文件夹的位置。  
   - 使用GitHub API列出目录内容：`GET /repos/{owner}/{repo}/contents?ref={branch}`。  
   - 查找包含`SKILL.md`的文件夹——这是实际的技能目录。  
   - 常见路径模式：`skill/`、`skills/{name}/`、根目录或自定义文件夹名称。  
   - 在生成下载URL之前确认路径正确。  
3. **使用辅助脚本下载：**  
   - 使用位于该技能`scripts/`文件夹中的`install_skill.py`脚本：  
   **安全特性：** 如果目标目录是根技能目录，脚本将中止（退出代码4）。  
   - **更新检测：** 如果技能已存在，显示差异并提示用户确认。  
   - **安全扫描：** 安装脚本会自动扫描下载的技能是否存在安全威胁（如不可见字符、数据泄露、命令注入等）。在继续之前请查看任何发现的结果。  
4. **确定主要目标：**  
   - 询问：“应该全局安装（用户范围）还是本地安装（项目范围）？”  
   - 确定主要使用的工具（例如，如果用户使用的是Claude Code，则Claude是主要目标）。  
5. **“同步检查”（关键步骤）：**  
   - **扫描：** 检查系统中是否已安装其他支持的工具（查找它们的配置文件夹）。  
   - **建议：** “我看到您还安装了OpenCode和Cursor。是否也想将这些技能同步到它们？”  
6. **执行：**  
   - 为每个目标位置运行安装脚本。  
   - 确保保持标准结构。  
7. **报告成功：**  
   - 显示已安装的技能名称、作者和位置。  
   - 显示GitHub URL和星数以供参考。  

#### 2. “更新与一致性”检查  
**触发条件：** 用户修改了技能或请求“同步”技能。  
**操作步骤：**  
1. **比较：** 检查所有安装位置上的技能的修改时间或内容。  
2. **报告：** “Gemini中的‘code-review’技能比OpenCode中的版本更新。”  
3. **操作：** 提供用新版本覆盖旧版本的选项，以确保一致性。  

#### 3. 多源技能发现  
**触发条件：** 用户搜索技能（例如：“查找调试技能”或“搜索React技能”）。  
**操作步骤：**  
1. **获取API密钥并选择来源：**  
   - **步骤1 - 环境变量：** 检查 `$SKILLSMP_API_KEY`  
     如果已设置且非空，使用SkillsMP作为主要搜索来源。  
     **注意：** 使用`printenv`（而不是`echo $VAR`）——它直接查询进程环境，在不同shell环境中更可靠。  
   - **步骤2 - 配置文件：** 检查该技能目录中的`config.json`文件  
     如果`skillsmp_api_key`字段有非空值，使用SkillsMP作为主要来源。  
   - **步骤3 - 选择来源：** 如果未找到API密钥，向用户提供选择：  
     > “我没有看到配置的SkillsMP API密钥。您有三个选项：  
     > A) 提供您的SkillsMP API密钥（可在skillsmp.com获取）——提供带有AI语义搜索的精选技能  
     > B) 在SkillHub的开放目录中搜索——17.3万多个社区技能，无需API密钥  
     > C) 在ClawHub中搜索——5,700多个版本化的技能，支持语义搜索，无需API密钥  
     > 您选择哪个？”  
     - 如果用户选择**A**：收集密钥，并将其存储在会话内存中，然后继续使用SkillsMP。  
     - 如果用户选择**B**：继续使用SkillHub搜索（无需密钥）。  
     - 如果用户选择**C**：继续使用ClawHub搜索（无需密钥）。  
   - **安全注意事项：** 请勿记录、显示或回显完整的API密钥值。  
   *对于claude.ai/Desktop用户：** 环境变量不可用。请使用“Package for claude.ai/Desktop”功能（第5节）创建包含API密钥的ZIP文件，或在提示时提供密钥。**  
2. **根据选定的来源执行搜索：**  
   - **如果使用SkillsMP（主要来源，精选内容）：**  
     - **选择方法：**  
       - **关键词搜索**（`/api/v1/skills/search`）：用于特定术语的精确匹配。  
       - **AI语义搜索**（`/api/v1/skills/ai-search`）：用于自然语言查询（例如：“帮我调试代码”）。  
     - **重要提示：** 请务必首先将API密钥捕获到本地变量中，然后使用它。在某些shell环境中直接使用`$SKILLSMP_API_KEY`可能会导致问题。  
     - **解析：** 从`data.skills[]`（关键词搜索）或`data.data[]`（AI搜索）中提取信息。  
     - 可用字段：`id`、`name`、`author`、`description`、`githubUrl`、`skillUrl`、`stars`、`updatedAt`。  
     - **注意：** SkillsMP需要`q`参数——没有浏览/列表端点。对于“热门技能”或无特定查询的浏览，请使用SkillHub或ClawHub。**  
   - **如果使用SkillHub（开放目录，无需认证）：**  
     - **执行：**  
     - **解析：** 从`skills[]`数组中提取信息。  
     - 可用字段：`id`、`name`、`description`、`githubOwner`、`githubRepo`、`githubStars`、`downloadCount`、`securityScore`。  
     - **注意：** SkillHub不支持AI语义搜索——仅支持关键词搜索。  
   - **如果使用ClawHub（版本化技能，支持语义搜索，无需认证）：**  
     - **选择方法：**  
       - **语义搜索**（`/api/v1/search`）：用于自然语言查询——结果按相似度`score`排序。  
       - **浏览/列表**（`/api/v1/skills`）：按流行度、星数或最新更新时间浏览。  
     - **执行：**  
     - **解析：**  
       - 从`results[]`数组中提取信息：每个结果包含`score`、`slug`、`displayName`、`summary`、`version`。  
       - **浏览：** 从`items[]`数组中提取信息：每个结果包含`slug`、`displayName`、`summary`、`version`、`stats.stars`、`stats.downloads`。  
     - **显示结果（统一格式）：** 无论来源如何，都以一致的表格格式显示结果。包括**来源**列以指示来源：  
       - 对于SkillsMP的AI搜索结果：同时显示相关性分数。  
       - 对于SkillHub的结果：显示`securityScore`（如果可用）。  
       - 对于ClawHub的语义搜索结果：显示相似度`score`（如果可用）。  
       - 限制显示结果数量为10-15个以提高可读性。  
4. **搜索更多来源：**  
   - 在显示任何来源的结果后，提供搜索剩余未搜索来源的选项：  
     - **如果剩余2个来源：** “还想搜索{source1}或{source2}吗？或者两个都搜索？”  
     - **如果剩余1个来源：** “还想搜索{source}吗？”  
     - 可用的来源：SkillsMP（需要API密钥）、SkillHub（无需密钥）、ClawHub（无需密钥）。  
     - 如果用户同意：  
       - 使用相同的搜索词查询选定的来源。  
       - **去重：** 比较不同来源的结果：  
         - SkillsMP ↔ SkillHub：通过完整的技能ID（`{owner}/{repo}/{path}`）。  
         - ClawHub ↔ 其他来源：通过技能名称（ClawHub使用slug，而非GitHub路径）。  
       - 将唯一结果添加到显示结果中，并标注来源标签。  
5. **提供安装选项：**  
   - 显示结果后，询问：“您想安装哪个技能？”  
   - 对于SkillsMP的结果：记下技能的`githubUrl`以获取内容。  
   - 对于SkillHub的结果：记下技能的`id`以获取详细信息（需要`skillPath`和`branch`）。  
   - 对于ClawHub的结果：记下技能的`slug`以便通过ClawHub的 `/file`端点直接下载文件。  

#### 4. 技能矩阵报告  
**触发条件：** 用户请求技能报告/概览（例如：“显示我的技能”、“我有哪些技能？”、“技能报告”、“比较我的工具”）。  
**操作步骤：**  
1. **检测已安装的工具：** 通过检查用户级别的技能目录是否存在来确认已安装的AI工具。  
2. **收集所有技能：** 为每个检测到的工具列出技能文件夹。  
3. **生成矩阵表：** 创建一个markdown表格，其中：  
   - **行** = 技能名称（在所有工具中去除重复）。  
   - **列** = 仅在系统中安装的工具。  
   - **单元格** = ✅（已安装）或❌（未安装）。  
   **示例输出：**  
5. **显示摘要：**  
   - 所有工具中的总技能数量。  
   - 仅在一个工具中独有的技能。  
   - 在所有工具中都安装的技能。  

#### 5. 为claude.ai / Claude Desktop打包技能  

**触发条件：** 用户希望在claude.ai或Claude Desktop中使用该技能（例如：“将该技能打包到claude.ai”、“为Claude Desktop创建ZIP文件”、“我想将此技能上传到claude.ai”、“准备技能以供网络上传”）。  
**操作步骤：**  
1. **解释流程：** “我将创建一个ZIP文件，以便将其上传到claude.ai或Claude Desktop。由于云环境无法访问您的本地环境变量，我会在包中嵌入您的API密钥。”  
2. **收集API密钥：**  
   - **询问：** “请提供您的SkillsMP API密钥。您可以在https://skillsmp.com获取。”  
   - 等待用户提供密钥。  
   **安全注意事项：** 请勿将密钥显示或回显给用户。  
   **注意：** API密钥会存储在ZIP包内的`config.json`文件中。该密钥在运行时仅用于通过SkillsMP API搜索技能时进行身份验证。**  
3. **创建包内容：**  
   - 创建临时目录结构。  
   - 生成包含用户API密钥的`config.json`文件。  
4. **创建ZIP文件：**  
   - 使用Python创建ZIP文件。  
5. **提供上传说明：**  
   - “您的技能包已准备好！使用方法如下：”  
   - “1. 下载ZIP文件：`universal-skills-manager.zip`。”  
   - “2. 转到claude.ai → 设置 → 功能。”  
   - “3. 浏览到技能部分并点击‘上传技能’。”  
   - “4. 选择ZIP文件并上传。”  
   - “5. 启用技能并开始使用！”  
6. **安全提醒：**  
   - **注意：** 该ZIP文件包含您的API密钥。请勿公开分享或提交到版本控制系统中。”  

### 操作规则  
1. **结构完整性：** 安装技能时，确保技能有自己的文件夹（例如：`.../skills/my-skill/`）。不要将文件直接放入根技能目录。  
2. **冲突处理：** 如果目标位置已存在技能，请在覆盖之前始终询问用户，除非用户明确请求“强制同步”。  
3. **OpenClaw注意事项：** 如果`openclaw.json`中未启用`skills.load.watch`，OpenClaw可能需要重启才能识别新技能。安装后请提醒用户这一点。  
4. **跨平台适配：**  
   - Gemini使用`SKILL.md`格式。  
   - Cline使用相同的`SKILL.md`格式，其中`name`和`description`作为前置内容。`name`字段必须与目录名称匹配。Cline还读取`.claude/skills/`目录中的技能，因此Claude Code项目中的技能可以在Cline中自动使用。  
   - 如果OpenCode或Anti-Gravity需要特定的清单文件（例如`manifest.json`），则在安装期间根据`SKILL.md`前置内容生成一个基本清单文件。  

### 可用的工具  
- `bash`（curl）：用于调用SkillsMP.com、SkillHub（skills.palebluedot.live）和ClawHub（clawhub.ai）的API；从GitHub或ClawHub直接获取技能内容。  
- `web_fetch`：从GitHub原始URL、SkillHub API或ClawHub API获取技能内容（作为curl的替代方案）。  
- `read_file` / `write_file`：管理本地技能文件。  
- `glob`：在本地目录中查找现有技能。  

### 实现细节  

#### 技能结构  
技能通常包含：  
- **SKILL.md**（必需）：包含前置内容的主要指令文件。  
- **参考文档**：额外的文档文件。  
- **脚本**：辅助脚本（Python、shell等）。  
- **配置文件**：JSON、YAML格式的配置文件。  

#### 安装逻辑  

#### A. 从SkillsMP API安装  
1. **获取技能内容：**  
   - 将`githubUrl`转换为原始内容URL。  
   - 使用curl或`web_fetch`获取SKILL.md内容。  
2. **创建目录：**  
   - 使用API响应中的技能`name`创建目录：`.../skills/{skill-name}/`  
   - 例如：`.../skills/code-debugging/`  
3. **保存SKILL.md：**  
   - 将获取的内容写入新目录中的`SKILL.md`文件。  
   - 保留原始的YAML前置内容和内容。  
4. **处理其他文件（可选）：**  
   - 检查GitHub仓库是否有其他文件（参考文档、脚本等）。  
   - （可选）获取并保存这些文件以维护完整的技能包。  
5. **确认：**  
   - 报告：“已安装‘{name}’，作者为{author}，路径为{path}。”  
   - 显示GitHub URL和星数。  
   - 提供与其他AI工具同步的选项。  

#### B. 从SkillHub安装  
1. **获取技能详细信息：**  
   - 使用搜索结果中的技能`id`获取完整详细信息：  
     **重要提示：** `id`字段（例如`wshobson/agents/debugging-strategies`）不对应于仓库中的文件路径。必须使用详细信息端点来获取实际的`skillPath`和`branch`。  
     - 从响应中提取`githubOwner`、`githubRepo`、`branch`、`skillPath`。  
2. **构建GitHub URL：**  
   - 根据详细信息响应构建GitHub树URL：  
     **示例：** `https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`  
3. **使用辅助脚本下载：**  
   - 从这一步开始，安装流程与SkillsMP相同。  
4. **确认：**  
   - 报告：“已从SkillHub安装‘{name}’，路径为{path}。”  
   - 显示GitHub URL和星数。  
   - 提供与其他AI工具同步的选项。  

#### C. 从ClawHub安装  
ClawHub直接托管技能文件（不在GitHub上），因此安装流程绕过`install_skill.py`，并通过ClawHub的API获取内容：  
1. **获取SKILL.md内容：**  
   - 使用ClawHub的文件端点获取SKILL.md的原始内容：  
     **重要提示：** 此端点返回的是原始`text/plain`内容，而非JSON。将响应体直接保存为文件。  
     - 可使用`x-content-sha256`响应头验证文件完整性。  
2. **处理多文件技能（如果适用）：**  
   - 如果技能有额外的文件（脚本、配置文件），使用ClawHub的下载端点：  
     **注意：** 如果技能有多个文件，检查`GET /api/v1/skills/{slug}`的详细响应——`latestVersion`字段可能指示文件数量。  
3. **运行安全扫描：**  
   - 由于绕过了`install_skill.py`，因此需要手动运行安全扫描脚本：  
     **注意：** 在继续之前请查看任何发现的结果。ClawHub集成了VirusTotal扫描工具；我们的扫描提供了额外的安全保障。  
4. **验证YAML前置内容：**  
   - 验证SKILL.md是否具有有效的YAML前置内容（`name`、`description`字段）。  
   - 如果无效，警告用户并询问是否继续。  
5. **创建目录并安装：**  
   - 创建目标目录：`.../skills/{slug}/`  
   - 将所有文件从临时目录复制到目标位置：  
6. **确认：**  
   - 报告：“已从ClawHub安装‘{displayName}’（版本{version}），路径为{path}。”  
   - 显示版本信息和星数。  
   - 提供与其他AI工具同步的选项。  

#### D. 从本地源安装（同步/复制）  
1. **检索：** 从源目录中读取所有文件。  
2. **创建目录：** 创建目标目录`.../skills/{slug}/`。  
3. **保存文件：** 将所有文件复制到新位置。  

#### SkillsMP API配置  
**基础URL：** `https://skillsmp.com/api/v1`  

**认证：**  
```bash
Authorization: Bearer $SKILLSMP_API_KEY
```  

**可用端点：**  
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}`  
- `GET /api/v1/skills/ai-search?q={query}`  

**响应格式（关键词搜索）：**  
```json
{
  "success": true,
  "data": {
    "skills": [
      {
        "id": "...",
        "name": "skill-name",
        "author": "AuthorName",
        "description": "...",
        "githubUrl": "https://github.com/user/repo/tree/main/path",
        "skillUrl": "https://skillsmp.com/skills/...",
        "stars": 10,
        "updatedAt": 1768838561
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 3601,
      "totalPages": 1801,
      "hasNext": true
    }
  }
}
```  

**响应格式（AI搜索）：**  
```json
{
  "success": true,
  "data": {
    "search_query": "...",
    "data": [
      {
        "file_id": "...",
        "filename": "...",
        "score": 0.656,
        "skill": {
          "id": "...",
          "name": "...",
          "author": "...",
          "description": "...",
          "githubUrl": "...",
          "skillUrl": "...",
          "stars": 0,
          "updatedAt": 1769542668
        }
      }
    ]
  }
}
```  

**错误处理：**  
- `401`：API密钥无效或缺失。  
- `400`：缺少必要的查询参数。  
- `500`：内部服务器错误。  

#### SkillHub API配置  
**基础URL：** `https://skills.palebluedot.live/api`  

**认证：** 不需要（开放API）  

**可用端点：**  
- `GET /api/skills?q={query}&limit={20}` — 按关键词搜索技能  
- `GET /api/skills/{id}` — 获取技能的完整详细信息（包括`skillPath`、`branch`、`rawContent`）  
- `GET /api/categories` — 列出技能类别  
- `GET /api/health` — 健康检查  

**搜索响应格式：**  
```json
{
  "skills": [
    {
      "id": "wshobson/agents/debugging-strategies",
      "name": "debugging-strategies",
      "description": "Master systematic debugging...",
      "githubOwner": "wshobson",
      "githubRepo": "agents",
      "githubStars": 27021,
      "downloadCount": 0,
      "securityScore": 100,
      "securityStatus": null,
      "rating": 0,
      "isVerified": false,
      "compatibility": { "platforms": [] }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000,
    "totalPages": 50
  },
  "searchEngine": "meilisearch",
  "processingTimeMs": 10
}
```  

**详细信息响应格式（GET /api/skills/{id}）：**  
```json
{
  "id": "wshobson/agents/debugging-strategies",
  "name": "debugging-strategies",
  "description": "...",
  "githubOwner": "wshobson",
  "githubRepo": "agents",
  "skillPath": "plugins/developer-essentials/skills/debugging-strategies",
  "branch": "main",
  "githubStars": 27021,
  "rawContent": "---\nname: debugging-strategies\n..."
}
```  

**安装所需的字段：**  
- `skillPath`：GitHub仓库中的实际目录路径（关键字段——`id`与文件路径不匹配）。  
- `branch`：分支名称（例如`main`）。  
- `githubOwner` + `githubRepo`：用于构建GitHub URL。  
- `rawContent`：SKILL.md的完整内容（如果GitHub不可用时可用）。  

**错误处理：**  
- `404`：技能未找到。  
- `500`：内部服务器错误。  

#### ClawHub API配置  
**基础URL：** `https://clawhub.ai/api/v1`  

**认证：** 不需要（开放API）  

**速率限制：** 每IP每分钟120次读取（在`x-ratelimit-remaining`和`x-ratelimit-reset`响应头中显示）  

**可用端点：**  
- `GET /api/v1/search?q={query}&limit={20}` — 按相似度排名进行语义搜索  
- `GET /api/v1/skills?limit={20}&sort={stars|downloads|updated|trending}&cursor={cursor}` — 带有分页功能的浏览/列表  
- `GET /api/v1/skills/{slug}` — 获取技能的完整详细信息（包括所有者、版本）  
- `GET /api/v1/skills/{slug}/file?path={path}&version={ver}` — 下载技能的原始文件（格式为text/plain）  
- `GET /api/v1/download?slug={slug}&version={ver}` — 下载技能的ZIP文件  

**浏览响应格式（GET /api/v1/skills）：**  
```json
{
  "items": [
    {
      "slug": "self-improving-agent",
      "displayName": "Self-Improving Agent",
      "summary": "...",
      "version": "1.0.0",
      "stats": {
        "stars": 42,
        "downloads": 150
      }
    }
  ],
  "nextCursor": "eyJ..."
}
```  

**详细信息响应格式（GET /api/v1/skills/{slug}）：**  
```json
{
  "skill": {
    "slug": "self-improving-agent",
    "displayName": "Self-Improving Agent",
    "summary": "...",
    "version": "1.0.0"
  },
  "owner": {
    "handle": "username",
    "displayName": "User Name"
  },
  "latestVersion": "1.0.0",
  "moderation": "approved"
}
```  

**文件端点（GET /api/v1/skills/{slug}/file?path=SKILL.md）：**  
- 返回原始`text/plain`内容（格式为JSON）。  
- 响应头包含`x-content-sha256`（完整性哈希）和`x-content-size`（文件大小）。  
- 使用`version`查询参数获取特定版本（默认为最新版本）。  

**与SkillsMP/SkillHub的主要区别：**  
- **直接托管：** ClawHub直接托管技能文件——无需构建GitHub URL。  
- **版本化技能：** 每个技能都有明确的版本号；使用`version`参数进行指定。  
- **基于slug的ID：** 技能通过`slug`标识（例如`self-improving-agent`），而非GitHub路径。  
- **内置语义搜索：** `/search`端点支持语义搜索。  
- **VirusTotal集成：** ClawHub通过VirusTotal进行扫描；`moderation`字段表示状态。  

**错误处理：**  
- `404`：技能或文件未找到。  
- `429`：超出速率限制（每分钟120次读取）。  
- `500`：内部服务器错误。  

**指南：**  
- **多源搜索：** 当有API密钥时，优先使用SkillsMP作为主要来源。提供SkillHub和ClawHub作为备用或额外来源。  
- **优先使用AI/语义搜索：** 对于自然语言查询，使用SkillsMP的 `/ai-search`或ClawHub的 `/search`（两者都支持语义匹配）。  
- **来源标注：** 始终在结果中标明来源（`[SkillsMP]`、`[SkillHub]`或`[ClawHub]`），以便用户区分来源。  
- **从SkillHub安装技能时：** 在安装前务必先获取详细信息端点以获取正确的`skillPath`和`branch`。切勿尝试将`id`字段解析为文件路径。  
- **ClawHub直接托管：** ClawHub直接托管技能文件——使用`/file`端点获取内容。无需构建GitHub URL。使用`slug`字段作为技能标识符。  
- **ClawHub版本控制：** ClawHub技能有明确的版本号。在安装时显示版本号。如果需要，使用`version`参数指定特定版本。  
- **去重：** 在显示来自多个来源的结果时，通过完整的技能ID（`{owner}/{repo}/{path}`）去重；ClawHub与其他来源通过技能名称去重（因为ClawHub使用slug）。  
- **验证内容：** 在从任何来源获取内容后，验证SKILL.md是否具有有效的YAML前置内容。  
- **结构完整性：** 保持`.../skills/{skill-name}/SKILL.md`的结构。  
- **同步：** 安装技能后，提供将其同步（复制）到其他检测到的AI工具的选项。  
- **GitHub URL：** 对于SkillsMP/SkillHub的安装，始终将树URL转换为raw.githubusercontent.com URL以获取内容。  
- **安全：** 无论来源如何，都对所有安装进行安全扫描（SkillsMP、SkillHub或ClawHub）。SkillHub的`securityScore`和ClawHub的`moderation`状态仅用于提供信息。