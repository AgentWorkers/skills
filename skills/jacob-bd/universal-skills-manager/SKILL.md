---
name: universal-skills-manager
description: "AI技能的主协调者。负责从多个来源（SkillsMP.com、SkillHub 和 ClawHub）收集技能信息，管理这些技能的安装过程，并确保它们在 Claude Code、Gemini CLI、Google Anti-Gravity、OpenCode 等 AI 工具中的同步。支持用户级（全局）和项目级（本地）的技能管理需求。"
compatibility: "Requires python3, curl, and network access to skillsmp.com, skills.palebluedot.live, clawhub.ai, and github.com"
metadata:
  homepage: https://github.com/jacob-bd/universal-skills-manager
  disable-model-invocation: "true"
  requires-bins: "python3, curl"
  primaryEnv: SKILLSMP_API_KEY
---
## 版本：1.6.0  

### 通用技能管理器  

该技能使代理能够充当AI功能的集中式技能管理器。它可以从多个来源发现技能：  
- **SkillsMP.com**（精选的技能，支持AI语义搜索）；  
- **SkillHub**（社区技能，无需API密钥）；  
- **ClawHub**（版本化的技能，支持语义搜索，无需API密钥）。  
该技能能够统一管理多个AI工具（如Claude Code、Gemini、Anti-Gravity、OpenCode、Cline、Cursor等）中的技能，确保技能的一致性和同步性。  

### 何时使用此技能  

当用户需要：  
- **查找或搜索**新技能；  
- **安装**技能（从搜索结果或本地文件）；  
- **在不同AI工具之间同步**技能；  
- **在技能/扩展的上下文中提及**“Google Anti-Gravity”、“OpenCode”或“Gemini”；  
- **将技能打包用于claude.ai或Claude Desktop”（通过ZIP上传）时，可激活此技能。  

### 支持的生态系统  

该技能管理以下工具和范围：  
| 工具        | 用户范围（全局） | 项目范围（本地） |  
|------------|------------|------------|  
| **Gemini CLI**    | `~/.gemini/skills/`   | `./.gemini/skills/`   |  
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` | `./.antigravity/extensions/` |  
| **OpenCode**    | `~/.config/opencode/skills/` | `./.opencode/skills/` |  
| **OpenClaw**    | `~/.openclaw/workspace/skills/` | `./.openclaw/skills/` |  
| **Claude Code** | `~/.claude/skills/`   | `./.claude/skills/`   |  
| **OpenAI Codex** | `~/.codex/skills/`   | `./.codex/skills/`   |  
| **block/goose**    | `~/.config/goose/skills/`   | `./.goose/agents/`   |  
| **Roo Code**    | `~/.roo/skills/`   | `./.roo/skills/`   |  
| **Cursor**    | `~/.cursor/skills/`   | `./.cursor/skills/`   |  

**注意（针对claude.ai / Claude Desktop）：**  
需要通过“Settings → Capabilities → Upload Skill”上传ZIP文件。  

**重要提示：**  
- **通用技能管理器平台限制**：  
  该技能需要网络访问权限来调用SkillsMP API、SkillHub API、ClawHub API和GitHub。  
  - 如果用户希望将通用技能管理器本身打包用于claude.ai，请告知用户：  
    “通用技能管理器无法在claude.ai上使用，因为它需要网络访问权限来调用相关API。但我可以打包其他技能用于claude.ai。”  
  - **关于Claude Desktop**：  
    - Claude Desktop具有网络访问权限，但存在一个已知问题：添加到“Additional allowed domains”设置中的自定义域名不会包含在网络请求的JWT令牌中，这可能导致技能无法访问所需API。  
    - **所需域名**：`skillsmp.com`（用于SkillsMP技能搜索）；`skills.palebluedot.live`（用于SkillHub技能搜索）；`clawhub.ai`（用于ClawHub技能搜索和直接文件下载）；`api.github.com`和`raw.githubusercontent.com`（用于从GitHub下载技能）。  

### 核心功能  

#### 1. 智能安装与同步  
**触发条件**：用户请求安装技能（例如：“安装调试技能”或“安装技能ID xyz”）。  
**流程**：  
1. **确定来源**：  
   - 如果来自SkillsMP搜索结果：使用API响应中的`githubUrl`；  
   - 如果来自SkillHub搜索结果：通过`/api/skills/{id}`获取`skillPath`和`branch`，然后构建GitHub路径；  
   - 如果来自ClawHub搜索结果：使用`slug`通过ClawHub的 `/file`端点获取内容；  
   - 如果通过技能名称/ID查找：在SkillsMP、SkillHub和/或ClawHub中搜索技能；  
   - 如果是本地技能：确定来源路径。  
2. **验证仓库结构**：  
   - 下载前浏览GitHub仓库以确认技能文件夹的位置；  
   - 使用GitHub API列出目录内容：`GET /repos/{owner}/{repo}/contents?ref={branch}`；  
   - 查找包含`SKILL.md`的文件夹；  
   - 常见路径模式：`skill/`、`skills/{name}/`、根目录或自定义文件夹名称；  
   - 生成下载URL前确认路径正确性。  
3. **使用辅助脚本下载**：  
   - 使用`install_skill.py`（位于技能的`scripts/`文件夹中）；  
   - 脚本负责原子安装、验证、处理子目录和安全检查；  
   - **安全特性**：如果目标目录是根目录，脚本将中止（退出代码4）；  
   - **更新检测**：如果技能已存在，显示差异并请求确认；  
   - **安全扫描**：安装脚本会自动扫描下载的技能是否存在安全威胁（如不可见字符、数据泄露、命令注入等）。  
4. **确定主要目标**：  
   - 询问用户是全局安装（用户范围）还是本地安装（项目范围）；  
   - 确定主要使用的工具（例如，如果用户使用的是Claude Code，则Claude为主要工具）；  
   - 如果用户指定目标为claude.ai或Claude Desktop，跳至步骤4a。  

#### 4a. Claude Desktop / claude.ai目标流程：**  
   - 如果用户希望将技能安装到claude.ai或Claude Desktop：  
     1. 通过`validate_frontmatter.py`验证下载的SKILL.md文件；  
     2. 如果技能通过验证，将其打包为ZIP并提供上传说明；  
     3. 如果技能未通过验证，先告知用户具体问题；  
     4. 如果用户同意，进行修复并重新验证；  
     5. 将修复后的技能打包为ZIP。  
   - **6a. 打包并交付ZIP**：  
     - 创建包含技能文件夹的ZIP文件（如果适用，修复后的SKILL.md文件也会包含在内）；  
     - 提供上传说明：  
       > “您的技能已打包完毕。要在Claude Desktop上安装：  
       > 1. 进入Settings → Capabilities；  
       > 2. 在Skills部分点击‘Upload skill’；  
       > 3. 选择ZIP文件并上传；  
     - 继续步骤5，将技能同步到其他本地工具。  

#### 5. “同步检查”（关键步骤）：  
   - 检查系统中是否安装了其他支持的工具；  
   - 提议：“我看到您还安装了OpenCode和Cursor，是否也想将这些技能同步到它们？”  

#### 6. 执行安装：**  
   - 为每个目标位置运行安装脚本；  
   - 确保保持标准结构。  
   - **报告安装结果**：显示安装的技能名称、作者和位置；  
   - 显示GitHub URL和星级数量。  

#### 7. “更新与一致性检查”  
**触发条件**：用户修改技能或请求同步技能。  
**流程**：  
   - 比较所有安装位置上的技能修改时间和内容；  
   - 报告：“Gemini中的‘code-review’技能比OpenCode中的版本更新。”  
   - **操作**：建议用新版本覆盖旧版本以确保一致性。  

#### 8. 多源技能发现  
**触发条件**：用户搜索技能（例如：“查找调试技能”）。  
**流程**：  
1. **获取API密钥并选择来源**：  
   - **步骤1 - 环境变量**：检查 `$SKILLSMP_API_KEY`；  
     如果设置且非空，使用SkillsMP作为主要搜索来源；  
     注意：使用`printenv`（而非`echo $VAR`），因为它直接查询进程环境，适用于各种shell环境。  
   - **步骤2 - 配置文件**：检查技能目录中的`config.json`文件；  
     如果`skillsmp_api_key`字段有值，使用SkillsMP作为主要来源；  
   - **步骤3 - 选择来源**：如果没有找到API密钥，向用户提供选择：  
     > “未配置SkillsMP API密钥。您有三个选项：  
       > A) 提供您的SkillsMP API密钥（可在skillsmp.com获取）——提供精选技能和AI语义搜索；  
       > B) 在SkillHub的开放目录中搜索——无需API密钥；  
       > C) 在ClawHub中搜索——版本化技能，无需API密钥；  
     根据用户选择继续操作。  
   - **密钥验证**：SkillsMP API密钥始终以`sk_live_skillsmp_`开头。如果提供的密钥不符合此前缀，立即拒绝；  
     **安全提示**：切勿记录、显示或回显完整的API密钥。  

#### 9. 报告技能矩阵**  
**触发条件**：用户请求技能报告/概览。  
**流程**：  
1. **检测安装的AI工具**：通过检查用户级别的技能目录来确认；  
2. **收集所有技能**：列出每个工具的技能文件夹；  
3. **生成矩阵表**：创建一个Markdown表格，显示：  
   - **行**：技能名称（跨所有工具去重）；  
   - **列**：仅在系统中安装的工具；  
   - **单元格**：✅（已安装）或❌（未安装）。  

#### 10. 为claude.ai / Claude Desktop打包技能**  
**触发条件**：用户希望将技能用于claude.ai或Claude Desktop。  
**流程**：  
1. **解释流程**：  
   “我将创建一个ZIP文件，以便上传到claude.ai或Claude Desktop。由于云环境无法访问您的本地环境变量，我可以选择将API密钥嵌入包中。注意：API密钥是可选的——SkillHub和ClawHub无需密钥即可使用。”  
2. **验证前端内容**：  
   运行`validate_frontmatter.py`检查SKILL.md文件是否符合Agent Skills规范；  
   如果通过验证，将其打包为ZIP并提供上传说明。  

#### 操作规则  
1. **结构完整性**：安装时确保技能有独立的文件夹（例如`.../skills/my-skill/`）。不要将文件直接放入根目录。  
2. **冲突处理**：如果目标位置已存在相同技能，请在覆盖前询问用户是否允许覆盖。  
3. **OpenClaw注意事项**：如果`openclaw.json`中未启用`skills.load.watch`，安装新技能可能需要重启OpenClaw。安装后提醒用户这一点。  
4. **跨平台适配**：  
   - Gemini使用`SKILL.md`格式；  
   - Cline使用相同的`SKILL.md`格式（包含`name`和`description`字段）。`name`字段必须与文件夹名称匹配。Cline还会读取`.claude/skills/`文件夹中的技能。  
   - 如果OpenCode或Anti-Gravity需要特定清单（如`manifest.json`），在安装期间根据SKILL.md生成基本清单。  
5. **claude.ai / Claude Desktop前端内容验证**：  
   在将技能上传或打包到claude.ai或Claude Desktop时，验证SKILL.md文件是否符合[Agent Skills规范](https://agentskills.io/specification)。Claude Desktop使用`strictyaml`（非标准PyYAML），会拒绝不符合规范的文件。  

#### 可用工具  
- `bash`（curl）：用于调用SkillsMP.com、SkillHub（skills.palebluedot.live）和ClawHub（clawhub.ai）的API；从GitHub或ClawHub直接获取技能内容。  
- `web_fetch`：从GitHub原始URL、SkillHub API或ClawHub API获取技能内容。  
- `read_file` / `write_file`：管理本地技能文件。  
- `glob`：在本地目录中查找现有技能。  

### 实现细节  
- **技能结构**：  
  技能通常包含：  
    - **SKILL.md**（必需）：包含主要说明和前端内容；  
    - **参考文档**：额外的文档文件；  
    - **脚本**：辅助脚本（Python、shell等）；  
    - **配置文件**：JSON或YAML配置文件。  

#### 安装逻辑  
#### A. 从SkillsMP API安装  
1. **获取技能内容**：  
   - 将`githubUrl`转换为原始内容URL；  
   - 使用curl或`web_fetch`获取SKILL.md内容；  
2. **创建目录**：  
   - 使用API响应中的技能`name`创建目录（例如`.../skills/code-debugging/`）；  
3. **保存SKILL.md**：  
   - 将获取的内容保存到新的SKILL.md文件中；  
   - 保留原始的YAML前端内容；  
4. **处理其他文件（可选）**：  
   - 检查GitHub仓库是否有其他文件（参考文档、脚本等）；  
   - （可选）获取并保存这些文件以保持技能包的完整性；  
5. **确认**：  
   - 报告：“已安装‘{name}’，作者为{author}，路径为{path}”；  
   - 显示GitHub URL和星级数量；  
   - 提供与其他AI工具同步的选项。  

#### B. 从SkillHub安装  
1. **获取技能详情**：  
   - 使用搜索结果中的技能`id`获取完整详情；  
   - **重要提示**：`id`字段（例如`wshobson/agents/debugging-strategies`）不对应仓库中的文件路径。必须使用详细信息端点获取`skillPath`和`branch`；  
   - 从响应中提取`githubOwner`、`githubRepo`、`branch`、`skillPath`；  
2. **构建GitHub路径**：  
   - 根据详细信息响应构建GitHub路径；  
   - 例如：`https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`；  
3. **使用辅助脚本下载**：  
   - 此后的流程与从SkillsMP安装相同；  
4. **确认**：  
   - 报告：“已从SkillHub安装‘{name}’，路径为{path}”；  
   - 显示GitHub URL和星级数量；  
   - 提供与其他AI工具同步的选项。  

#### C. 从ClawHub安装  
   ClawHub直接托管技能文件（不在GitHub上），因此安装流程跳过`install_skill.py`，通过ClawHub的API获取内容：  
1. **获取SKILL.md内容**：  
   - 使用ClawHub的文件端点获取SKILL.md的原始内容；  
   - **重要提示**：此端点返回原始`text/plain`内容；  
   - 使用`x-content-sha256`响应头验证文件完整性；  
2. **处理多文件技能（如果适用）**：  
   - 如果技能有多个文件（脚本、配置文件），使用ClawHub的下载端点；  
   - 检查`GET /api/v1/skills/{slug}`的详细信息响应以获取文件数量；  
3. **运行安全扫描**：  
   - 由于跳过了`install_skill.py`，需要手动运行安全扫描；  
   - 在继续之前查看扫描结果。ClawHub集成了VirusTotal安全扫描工具；  
4. **验证YAML前端内容**：  
   - 确认SKILL.md具有有效的YAML前端内容；  
   - 如果无效，警告用户是否继续；  
5. **创建目录并安装**：  
   - 创建目标目录（例如`.../skills/{slug}/`）；  
   - 将所有文件复制到目标目录；  
6. **确认**：  
   - 报告：“已从ClawHub安装‘{displayName}（版本{version}’”；  
   - 显示版本信息和星级数量；  
   - 提供与其他AI工具同步的选项。  
7. **清理**：  
   - 删除临时目录。  

#### D. 从本地源安装（同步/复制）  
1. **检索**：从源目录读取所有文件；  
2. **创建目录**：创建目标目录`.../skills/{slug}/`；  
3. **保存文件**：将所有文件复制到新位置。  

#### SkillsMP API配置  
**基础URL**：`https://skillsmp.com/api/v1`  

**认证**：  
（省略具体细节……）  

**可用端点**：  
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}`  
- `GET /api/v1/skills/ai-search?q={query}`  

**响应格式**：  
（省略具体细节……）  

**错误处理**：  
- `401`：API密钥无效或缺失；  
- `400`：缺少必需的查询参数；  
- `500`：内部服务器错误。  

#### SkillHub API配置  
**基础URL**：`https://skills.palebluedot.live/api`  

**认证**：无需认证（开放API）  

**可用端点**：  
- `GET /api/skills?q={query}&limit={20}`——按关键词搜索技能；  
- `GET /api/skills/{id}`——获取完整技能详情（包括`skillPath`、`branch`、`rawContent`）；  
- `GET /api/categories`——列出技能类别；  
- `GET /api/health`——健康检查。  

**搜索响应格式**：  
（省略具体细节……）  

**ClawHub API配置**  
**基础URL**：`https://clawhub.ai/api/v1`  

**认证**：无需认证（开放API）  

**速率限制**：每IP每分钟120次请求（在`x-ratelimit-remaining`和`x-ratelimit-reset`响应头中显示）  

**可用端点**：  
- `GET /api/v1/search?q={query}&limit={20}`——按相似度排名搜索；  
- `GET /api/v1/skills?limit={20}&sort={stars|downloads|updated|trending}&cursor={cursor}`——按流行度/星级/更新时间排序浏览；  
- `GET /api/v1/skills/{slug}`——获取完整技能详情；  
- `GET /api/v1/skills/{slug}/file?path={path}&version={ver}`——下载完整技能文件（文本格式）；  
- `GET /api/v1/download?slug={slug}&version={ver}`——下载完整技能文件（ZIP格式）。  

**注意事项**：  
- **多源搜索**：当有API密钥时，优先使用SkillsMP。如果无法使用API密钥，提供SkillHub和ClawHub作为替代或额外来源。  
- **推荐使用AI/语义搜索**：对于自然语言查询，使用SkillsMP的 `/ai-search`或ClawHub的 `/search`（两者都支持语义匹配）。SkillHub仅支持关键词搜索。  
- **来源标注**：始终在结果中标明来源（`[SkillsMP]`、`[SkillHub]`或`[ClawHub]`），以便用户区分来源。  
- **从SkillHub安装技能时**：务必先获取详细信息端点以获取正确的`skillPath`和`branch`。  
- **ClawHub直接托管**：使用`/file`端点获取技能文件；无需构建GitHub路径。使用`slug`字段作为技能标识符。  
- **ClawHub版本控制**：ClawHub技能有明确的版本号；安装时显示版本号。如果需要，使用`version`参数指定版本。  
- **去重**：在显示结果时，根据完整技能ID（`{owner}/{repo}/{path}`）区分SkillsMP和SkillHub的结果；根据技能名称（ClawHub使用`slug`）区分其他来源的结果。  
- **验证内容**：从任何来源获取技能后，验证SKILL.md具有有效的YAML前端内容。  
- **结构完整性**：保持`.../skills/{skill-name}/SKILL.md`结构。  
- **同步**：安装技能后，提供将其同步到其他检测到的AI工具的选项。  
- **GitHub URL**：对于SkillsMP/SkillHub的安装，始终将树路径转换为raw.githubusercontent.com路径以获取内容。  
- **安全**：无论来源如何，都会对所有安装进行安全扫描。SkillHub的`securityScore`和ClawHub的`moderation`状态仅供参考；安装时会运行`scan_skill.py`进行额外安全检查。