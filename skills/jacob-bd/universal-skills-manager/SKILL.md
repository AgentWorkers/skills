---
name: universal-skills-manager
description: AI技能的中央协调器。负责从多个来源（SkillsMP.com、SkillHub 和 ClawHub）获取技能信息，管理这些技能的安装过程，并确保它们在 Claude Code、Gemini CLI、Google Anti-Gravity、OpenCode 等 AI 工具中的同步。该协调器支持用户级（全局）和项目级（本地）的权限管理。
homepage: https://github.com/jbendavi/universal-skills_mp-manager
disable-model-invocation: true
metadata:
  clawdbot:
    requires:
      bins: ["python3", "curl"]
    primaryEnv: SKILLSMP_API_KEY
---

## 版本：1.5.5

### 通用技能管理器

该技能使代理能够作为人工智能功能的集中式技能管理器。它可以从多个来源发现技能——包括 SkillsMP.com（精选的技能，支持人工智能语义搜索）、SkillHub（社区技能，无需 API 密钥）和 ClawHub（带版本号的技能，支持语义搜索，也无需 API 密钥），并在多个人工智能工具（如 Claude Code、Gemini、Anti-Gravity、OpenCode、Cline、Cursor 等）之间统一技能管理，确保一致性和同步性。

## 何时使用此技能

在以下情况下激活此技能：
- 用户想要**查找或搜索**新技能。
- 用户想要**安装**某个技能（从搜索结果或本地文件中）。
- 用户想要在不同的人工智能工具之间**同步**技能（例如，“将这个 Gemini 技能复制到 OpenCode”）。
- 用户请求在**用户范围与项目范围**之间**移动或复制**技能。
- 用户在讨论技能/扩展时提到“Google Anti-Gravity”、“OpenCode”或“Gemini”。
- 用户想要**将此技能打包用于 claude.ai 或 Claude Desktop**（通过 ZIP 文件上传）。

## 支持的生态系统

此技能管理以下工具和范围。在操作前，请务必确认这些路径存在：

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

**claude.ai / Claude Desktop（需要 ZIP 文件上传）：**

| 平台 | 安装方法 |
| :--- | :--- |
| **claude.ai** | 通过设置 → 功能 → 上传技能来上传 ZIP 文件 |
| **Claude Desktop** | 通过设置 → 功能 → 上传技能来上传 ZIP 文件 |

*注意：claude.ai 和 Claude Desktop 无法访问本地环境变量。请使用“打包用于 claude.ai/Desktop”功能（第 5 节）来创建 ZIP 文件。嵌入 API 密钥是可选的——SkillHub 和 ClawHub 的搜索功能不需要密钥。如果包含密钥，请**不要**公开分享 ZIP 文件（请参阅第 5 节中的凭证安全指南）。*

### 通用技能管理器的平台限制

此技能需要网络访问权限来调用 SkillsMP API、SkillHub API、ClawHub API 和 GitHub。请处理以下情况：
- **如果用户请求将通用技能管理器本身打包/ZIP 用于 claude.ai：**
  告诉用户：“通用技能管理器无法在 claude.ai 上使用，因为它需要网络访问权限来调用 SkillsMP API、SkillHub API、ClawHub API 和 GitHub API。claude.ai 的代码执行环境不允许外部网络请求。但是，我可以为您打包其他技能以供 claude.ai 上传——只要这些技能不需要网络访问权限即可。”

- **如果用户想在带有 Coworker 的 Claude Desktop 上使用通用技能管理器：**
  告诉用户：“Claude Desktop with Coworker 具有网络访问权限。要在那里使用通用技能管理器，您可能需要在 Cowork 设置中扩展网络访问权限：
  - `skillsmp.com`（用于 SkillsMP 技能搜索）
  - `skills.palebluedot.live`（用于 SkillHub 技能搜索）
  - `clawhub.ai`（用于 ClawHub 技能搜索和直接文件下载）
  - `api.github.com` 和 `raw.githubusercontent.com`（用于从 GitHub 下载技能）”

*注意：如果某个工具使用不同的目录结构，请询问用户确认路径，以便将来参考。*

### 核心功能

#### 1. 智能安装与同步
**触发条件：**用户请求安装某个技能（例如，“安装调试技能”或“安装技能 ID xyz”）。

**操作步骤：**
1. **确定来源：**
    - 如果来自 SkillsMP 搜索结果：使用 API 响应中的 `githubUrl`。
    - 如果来自 SkillHub 搜索结果：通过 `/api/skills/{id}` 获取 `skillPath` 和 `branch`，然后构建 GitHub 树形 URL。
    - 如果来自 ClawHub 搜索结果：使用 `slug` 通过 ClawHub 的 `/file` 端点获取内容（详见第 C 节）。
    - 如果通过技能名称/ID 获取：在可用来源（SkillsMP、SkillHub 和/或 ClawHub）中搜索该技能。
    - 如果是本地技能：确定来源路径。
2. **验证仓库结构（至关重要）：**
    - 下载前，浏览 GitHub 仓库以确认技能文件夹的位置。
    - 使用 GitHub API 列出目录内容：`GET /repos/{owner}/{repo}/contents?ref={branch}`。
    - 查找包含 `SKILL.md` 的文件夹——这是实际的技能目录。
    - 常见模式：`skill/`、`skills/{name}/`、根目录或自定义文件夹名称。
    - 在生成下载 URL 之前确认正确的路径。
3. **使用辅助脚本下载：**
    - 使用位于该技能的 `scripts/` 文件夹中的 `install_skill.py` 脚本：
    ```bash
    python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
      --url "https://github.com/{owner}/{repo}/tree/{branch}/{skill-folder}" \
      --dest "{target-path}" \
      --dry-run  # Preview first, then remove flag to install
    ```
    - 该脚本负责：原子安装、验证、子目录处理、安全检查。
    - **安全特性**：如果目标目录是根技能目录，脚本将中止（退出代码 4）。
    - **更新检测**：如果技能已存在，显示差异并提示确认。
    - **安全扫描**：安装脚本会自动扫描下载的技能以检测安全威胁（不可见字符、数据泄露、提示注入）。在继续之前请查看任何发现的结果。
4. **确定主要目标：**
    - 询问：“这是应该全局安装（用户范围）还是本地安装（项目范围）？”
    - 确定主要使用的工具（例如，如果用户使用的是 Claude Code，则 Claude 是主要目标）。
5. **“同步检查”（至关重要）：**
    - **扫描：**检查系统中是否已安装其他支持的工具（查找它们的配置文件夹）。
    - **建议：**“我看到您还安装了 OpenCode 和 Cursor。您是否也想将这些技能同步到它们？”
6. **执行：**
    - 为每个目标位置运行安装脚本。
    - 确保保持标准结构。
7. **报告成功：**
    - 显示安装的技能名称、作者和位置。
    - 显示 GitHub URL 和星星数量以供参考。

#### 2. “更新与一致性”检查
**触发条件：**用户修改了某个技能或请求“同步”技能。

**操作步骤：**
1. **比较：**检查所有安装位置上的技能的修改时间或内容。
2. **报告：**“Gemini 中的‘code-review’技能比 OpenCode 中的版本更新。”
3. **操作：**建议用新版本覆盖旧版本以确保一致性。

#### 3. 多源技能发现
**触发条件：**用户搜索技能（例如，“查找调试技能”或“搜索 React 技能”）。

**操作步骤：**
1. **获取 API 密钥并选择来源：**
    - **步骤 1 - 环境变量：**检查 `$SKILLSMP_API_KEY`
        ```bash
        printenv SKILLSMP_API_KEY
        ```
        如果已设置且不为空，则使用 SkillsMP 作为主要搜索来源。
        **注意：**使用 `printenv`（而不是 `echo $VAR`）——它直接查询进程环境，在不同的 shell 环境中更可靠。
    - **步骤 2 - 配置文件：**检查该技能目录中的 `config.json`
        ```bash
        # Look for config.json in skill directory (path varies by tool)
        cat ~/.claude/skills/universal-skills-manager/config.json 2>/dev/null
        ```
        如果 `skillsmp_api_key` 字段有非空值，则使用 SkillsMP 作为主要来源。
    - **步骤 3 - 选择来源：**如果没有找到 API 密钥，向用户提供选择：
        > “我没有看到配置 SkillsMP API 密钥。您有三个选项：
        >
        > A) 提供您的 SkillsMP API 密钥（在 skillsmp.com 获取）——提供带有人工智能语义搜索的精选技能
        >
        > B) 在 SkillHub 的开放目录中搜索——社区技能，无需 API 密钥
        >
        > C) 在 ClawHub 中搜索——带版本号的技能，也无需 API 密钥
        >
        > 您选择哪个？”
        -
        - 如果用户选择 **A**：收集密钥，**验证它**（详见下文），将其存储在内存中以供本次会话使用，然后继续使用 SkillsMP。
        - 如果用户选择 **B**：继续使用 SkillHub 搜索（无需密钥）。
        - 如果用户选择 **C**：继续使用 ClawHub 搜索（无需密钥）。
    - **密钥验证：**SkillsMP API 密钥始终以 `sk_live_skillsmp_` 开头。如果用户提供的密钥不符合此前缀，请立即拒绝：
        > “这看起来不是一个有效的 SkillsMP API 密钥。密钥应以 `sk_live_skillsmp_` 开头。您可以在 https://skillsmp.com 获取密钥——或者选择使用 SkillHub/ClawHub 搜索（无需密钥）。”
    - **安全注意事项：**永远不要记录、显示或回显完整的 API 密钥值。
    **对于 claude.ai/Desktop 用户的注意：**环境变量不可用。请使用“打包用于 claude.ai/Desktop”功能（第 5 节）来创建包含 API 密钥的 ZIP 文件，或者在提示时提供密钥。**

2. **根据选定的来源执行搜索：**

    - **如果使用 SkillsMP（主要来源，精选技能）：**
        - **选择方法：**
            - **关键词搜索**（`/api/v1/skills/search`）：用于特定术语，精确匹配。
            - **人工智能语义搜索**（`/api/v1/skills/ai-search`）：用于自然语言查询（例如，“帮助我调试代码”）。
    - **重要提示：**始终首先将 API 密钥捕获到本地变量中，然后使用它。在某些 shell 环境中，直接使用 `$SKILLSMP_API_KEY` 可能会失败：
        ```bash
        # Step 1: Capture key (do this once per session)
        API_KEY=$(printenv SKILLSMP_API_KEY)

        # Step 2: Use ${API_KEY} in curl commands
        # Keyword Search
        curl -X GET "https://skillsmp.com/api/v1/skills/search?q={query}&limit=20&sortBy=recent" \
          -H "Authorization: Bearer ${API_KEY}"

        # AI Semantic Search (for natural language queries)
        curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q={query}" \
          -H "Authorization: Bearer ${API_KEY}"
        ```
    - **解析：**从 `data.skills[]`（关键词）或 `data.data[]`（人工智能搜索）中提取信息。
    - 可用的字段：`id`、`name`、`author`、`description`、`githubUrl`、`skillUrl`、`stars`、`updatedAt`。
    - **注意：**SkillsMP 需要 `q` 参数——没有浏览/列表端点。对于“热门技能”或无特定查询的浏览，请使用 SkillHub 或 ClawHub。

    - **如果使用 SkillHub（开放目录，无需认证）：**
        - **执行：**
        ```bash
        # SkillHub Search (no authentication required)
        curl -X GET "https://skills.palebluedot.live/api/skills?q={query}&limit=20"
        ```
    - **解析：**从 `skills[]` 数组中提取信息。
    - 可用的字段：`id`、`name`、`description`、`githubOwner`、`githubRepo`、`githubStars`、`downloadCount`、`securityScore`。
    - **注意：**SkillHub 不支持人工智能语义搜索——仅支持关键词搜索。

    - **如果使用 ClawHub（带版本号的技能，无需认证）：**
        - **选择方法：**
            - **语义搜索**（`/api/v1/search`）：用于自然语言查询——按相似度 `score` 对结果进行排序。
            - **浏览/列表**（`/api/v1/skills`）：按受欢迎程度、星星数量或最新更新时间进行浏览。
    - **执行：**
        ```bash
        # Semantic Search (vector/similarity search)
        curl -X GET "https://clawhub.ai/api/v1/search?q={query}&limit=20"

        # Browse by stars or downloads
        curl -X GET "https://clawhub.ai/api/v1/skills?limit=20&sort=stars"
        ```
    - **解析：**
        - **语义搜索：**从 `results[]` 数组中提取信息——每个条目包含 `score`、`slug`、`displayName`、`summary`、`version`。
        - **浏览：**从 `items[]` 数组中提取信息——每个条目包含 `slug`、`displayName`、`summary`、`version`、`stats.stars`、`stats.downloads`。
    - **注意：**ClawHub 直接托管技能文件（不在 GitHub 上）。安装时使用 `slug` 字段——详见第 C 节。

3. **以统一格式显示结果：**
    无论来源如何，都以一致的表格格式显示结果。包括 **来源** 列以指示来源：

    ```
    | # | Skill | Author | Stars | Source | Description |
    |---|-------|--------|-------|--------|-------------|
    | 1 | debugging-strategies | wshobson | 27,021 | SkillHub | Master systematic debugging... |
    | 2 | code-debugging | AuthorX | 15 | SkillsMP | Systematic debugging methodology... |
    | 3 | self-improving-agent | clawhub-user | 42 | ClawHub | Agent that improves itself... |
    ```

    - 对于 SkillsMP 人工智能搜索：同时显示相关性分数。
    - 对于 SkillHub：如果可用，显示 `securityScore`。
    - 对于 ClawHub 语义搜索：如果可用，显示相似度 `score`。
    - 限制显示结果数量为前 10-15 个以便于阅读。

4. **搜索更多来源：**
    在显示了任何来源的结果后，提供搜索剩余未搜索来源的选项：

    - **如果还有 2 个来源：**“您还想搜索 {source1} 或 {source2} 吗？或者两个都搜索？”
    - **如果只剩下 1 个来源：**“您还想搜索 {source} 吗？”
    可用的来源：SkillsMP（需要 API 密钥）、SkillHub（无需密钥）、ClawHub（无需密钥）。

    如果用户同意：
    - 使用相同的搜索词查询选定的来源。
    - **去重：**比较来自不同来源的结果：
        - SkillsMP ↔ SkillHub：通过完整的技能 ID (`{owner}/{repo}/{path}`）。
        - ClawHub ↔ 其他来源：通过技能名称（ClawHub 使用 slug，而不是 GitHub 路径）。
    - 将唯一的结果添加到显示结果中，并标注其来源标签。

5. **提供安装选项：**
    - 显示结果后，询问：“您想安装哪个技能？”
    - 对于 SkillsMP 的结果：注意技能的 `githubUrl` 以获取内容。
    - 对于 SkillHub 的结果：注意技能的 `id` 以获取详细信息（需要 `skillPath` 和 `branch`）。
    - 对于 ClawHub 的结果：注意技能的 `slug` 以便通过 ClawHub 的 `/file` 端点直接获取文件。

#### 4. 技能矩阵报告
**触发条件：**用户请求技能报告/概览（例如，“显示我的技能”、“我有哪些技能？”、“技能报告”、“比较我的工具”）。

**操作步骤：**
1. **检测已安装的工具：**
    通过检查用户级别的技能目录是否存在来检测已安装的人工智能工具：
    ```bash
    # Check each tool's skills directory
    ls -d ~/.claude/skills 2>/dev/null && echo "Claude: ✓"
    ls -d ~/.codex/skills 2>/dev/null && echo "Codex: ✓"
    ls -d ~/.gemini/skills 2>/dev/null && echo "Gemini: ✓"
    ls -d ~/.gemini/antigravity/skills 2>/dev/null && echo "Antigravity: ✓"
    ls -d ~/.openclaw/workspace/skills 2>/dev/null && echo "OpenClaw: ✓"
    ls -d ~/.cursor/skills 2>/dev/null && echo "Cursor: ✓"
    ls -d ~/.config/opencode/skills 2>/dev/null && echo "OpenCode: ✓"
    ls -d ~/.roo/skills 2>/dev/null && echo "Roo: ✓"
    ls -d ~/.config/goose/skills 2>/dev/null && echo "Goose: ✓"
    ls -d ~/.cline/skills 2>/dev/null && echo "Cline: ✓"
    ```

2. **收集所有技能：**
    为每个检测到的工具列出技能文件夹：
    ```bash
    find ~/.{claude,codex,gemini,gemini/antigravity,openclaw/workspace,cursor,config/opencode,config/goose,roo,cline}/skills -maxdepth 1 -type d 2>/dev/null | \
      xargs -I{} basename {} | sort -u
    ```

3. **生成矩阵表格：**
    创建一个 markdown 表格，其中：
    - **行** = 技能名称（在所有工具中去除重复）。
    - **列** = 仅在系统中安装的工具。
    - **单元格** = ✅（已安装）或 ❌（未安装）。

    示例输出：
    ```
    | Skill | Claude | Codex | Gemini |
    |-------|--------|-------|--------|
    | humanizer | ✅ | ❌ | ✅ |
    | skill-creator | ❌ | ✅ | ❌ |
    | using-superpowers | ✅ | ✅ | ✅ |
    ```

4. **显示摘要：**
    - 所有工具中的总技能数量。
    - 仅在一个工具中独有的技能。
    - 在所有工具中都安装的技能。

#### 5. 为 claude.ai / Claude Desktop 打包

**触发条件：**用户希望在该工具中使用此技能（例如，“将此技能打包用于 claude.ai”、“为 Claude Desktop 创建一个 ZIP 文件”、“我想将此技能上传到 claude.ai”、“准备技能以供网络上传”）。

**操作步骤：**
1. **解释流程：**
    “我将创建一个 ZIP 文件，以便将其上传到 claude.ai 或 Claude Desktop。由于云环境无法访问您的本地环境变量，我可以选择将您的 API 密钥嵌入到包中。注意：API 密钥是可选的——SkillHub 和 ClawHub 的搜索功能不需要密钥。”
2. **收集 API 密钥（可选）：**
    - **询问：**“您是否希望包含您的 SkillsMP API 密钥以进行精选搜索？这是可选的——SkillHub 和 ClawHub 的搜索功能不需要密钥。如果您跳过此步骤，打包的技能仍然可以在 SkillHub 和 ClawHub 上使用。”
    - **如果用户希望包含密钥：**
        - **询问：**“请提供您的 SkillsMP API 密钥。您可以在 https://skillsmp.com 获取它。”
        - **等待用户提供密钥。**
        - **验证：**密钥必须以 `sk_live_skillsmp_` 开头。如果无效，请拒绝并重新提示或选择跳过。**
        - **安全提示：****请注意：此 ZIP 文件将包含您的 API 密钥（以明文形式）。请遵循以下预防措施：
        > **不要**公开分享此 ZIP 文件，不要将其发布到网上，也不要将其提交到版本控制系统中。
        > **不要**将此 ZIP 文件分发给其他人——每个用户都应该自己打包他们的密钥。
        > **如果您的提供商支持，请使用有限权限的密钥。**
        > **如果怀疑 ZIP 文件被泄露，请轮换密钥。**
        > **密钥存储在 ZIP 文件内的 `config.json` 中，并且仅在运行时用于与 SkillsMP API 验证。**

3. **创建包内容：**
    - **创建临时目录结构：**
    ```
        universal-skills-manager/
        ├── SKILL.md          # Copy from current skill
        ├── config.json       # Create with embedded API key
        └── scripts/
            └── install_skill.py  # Copy from current skill
        ```
    - **使用用户的 API 密钥生成 `config.json`：**
    ```json
        {
          "skillsmp_api_key": "USER_PROVIDED_KEY_HERE"
        }
        ```

4. **创建 ZIP 文件：**
    - **使用 Python 创建 ZIP 文件：**
    ```python
        import zipfile
        import json
        import tempfile
        from pathlib import Path
        
        # Create ZIP in user's Downloads or current directory
        zip_path = Path.home() / "Downloads" / "universal-skills-manager.zip"
        skill_dir = Path("~/.claude/skills/universal-skills-manager").expanduser()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy skill files
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file() and file_path.name != 'config.json':
                    rel_path = file_path.relative_to(skill_dir)
                    dest = temp_path / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(file_path.read_bytes())
            
            # Create config.json with API key
            config = {"skillsmp_api_key": "USER_API_KEY"}
            (temp_path / "config.json").write_text(json.dumps(config, indent=2))
            
            # Create ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = f"universal-skills-manager/{file_path.relative_to(temp_path)}"
                        zf.write(file_path, arcname)
        ```
    - **或者，提供可下载的 ZIP 文件。**

5. **提供上传说明：**
    - “您的技能包已准备好！使用方法如下：**
    - **1. 下载 ZIP 文件：`universal-skills-manager.zip`**
    - **2. 转到 claude.ai → 设置 → 功能**
    - **3. 滚动到技能部分并点击‘上传技能’**
    - **4. 选择 ZIP 文件并上传**
    - **5. 启用技能并开始使用！**

6. **安全提示：**
    - **如果嵌入了密钥：**“此 ZIP 文件包含您的 API 密钥。请不要公开分享它，不要将其分发给其他人，也不要将其提交到版本控制系统中。如果您需要共享技能，请创建一个不包含密钥的版本（不包含 `config.json`），并让每个用户自己添加他们的密钥。”
    - **如果未嵌入密钥：**“此 ZIP 文件是安全的，可以共享——它不包含任何凭据。接收者可以之后添加自己的密钥，或者使用 SkillHub/ClawHub 搜索（不需要密钥）。**

## 操作规则

1. **结构完整性：**安装时，始终确保技能有自己的文件夹（例如，`.../skills/my-skill/`）。不要将文件直接放入根技能目录。
2. **冲突安全：**如果目标位置已经存在某个技能，请**始终**在覆盖之前询问用户，除非用户明确请求“强制同步”。
3. **关于 OpenClaw 的注意：**如果 `openclaw.json` 中未启用 `skills.load.watch`，OpenClaw 可能需要重启才能加载新技能。安装后请提醒用户这一点。
4. **跨平台适应性：**
    - Gemini 使用 `SKILL.md` 格式。
    - Cline 使用相同的 `SKILL.md` 格式，`name` 和 `description` 作为前置内容。`name` 字段必须与目录名称匹配。不需要生成清单文件。注意：Cline 也在项目级别读取 `.claude/skills/`，因此 Claude Code 项目中的技能可以在 Cline 中自动使用。
    - 如果 OpenCode 或 Anti-Gravity 需要特定的清单文件（例如 `manifest.json`），则在安装期间根据 `SKILL.md` 前置内容生成一个基本的清单文件。

## 可用的工具
- `bash`（curl）：用于调用 SkillsMP.com、SkillHub（skills.palebluedot.live）和 ClawHub（clawhub.ai）的 API；从 GitHub 或 ClawHub 直接获取技能内容。
- `web_fetch`：从 GitHub 原始 URL、SkillHub API 或 ClawHub API 获取技能内容（作为 curl 的替代方案）。
- `read_file` / `write_file`：管理本地技能文件。
- `glob`：在本地目录中查找现有的技能。

## 实现细节

### 技能结构
技能通常包含：
- **SKILL.md**（必需）：包含前置内容的主要指令。
- **参考文档**：额外的文档文件。
- **脚本**：辅助脚本（Python、shell 等）。
- **配置文件**：JSON、YAML 配置文件。

### 安装逻辑

#### A. 从 SkillsMP API 安装
1. **获取技能内容：**
    - 将 `githubUrl` 转换为原始内容 URL：
        ```
        Input:  https://github.com/{user}/{repo}/tree/{branch}/{path}
        Output: https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}/SKILL.md
        ```
    - 使用 curl 或 web_fetch 获取 SKILL.md 内容。
2. **创建目录：**
    - 使用 API 响应中的技能 `name` 创建目录：`.../skills/{skill-name}/`
    - 例如：`.../skills/code-debugging/`
3. **保存 SKILL.md：**
    - 将获取的内容写入新的目录中的 SKILL.md 文件。
    - 保留原始的 YAML 前置内容和内容。
4. **处理其他文件（可选）：**
    - 检查 GitHub 仓库是否有额外的文件（参考文档、脚本）。
    - 可选地获取并保存它们以维护完整的技能包。
5. **确认：**
    - 报告：“已安装 '{name}'，作者为 {author}，路径为 {path}”
    - 显示 GitHub URL 和星星数量。
    - 提供与其他人工智能工具同步的选项。

#### B. 从 SkillHub 安装
1. **获取技能详细信息：**
    - 使用搜索结果中的技能 `id` 获取完整详细信息：
        ```bash
        curl -X GET "https://skills.palebluedot.live/api/skills/{id}"
        ```
    - **重要提示：**`id` 字段（例如，`wshobson/agents/debugging-strategies`）并不对应于仓库内的文件路径。您必须使用详细信息端点来获取实际的 `skillPath` 和 `branch`。
    - 从响应中提取：`githubOwner`、`githubRepo`、`branch`、`skillPath`。
2. **构建 GitHub URL：**
    - 根据详细信息响应构建 GitHub 树形 URL：
        ```
        https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}
        ```
    - 例如：`https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`
3. **使用辅助脚本下载：**
    - 从这一点开始，安装流程与 SkillsMP 安装相同：
        ```bash
        python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
          --url "https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}" \
          --dest "{target-path}"
        ```

4. **确认：**
    - 报告：“已从 SkillHub 安装 '{name}'，路径为 {path}”
    - 显示 GitHub URL 和星星数量。
    - 提供与其他人工智能工具同步的选项。

#### C. 从 ClawHub 安装
ClawHub 直接托管技能文件（不在 GitHub 上），因此安装流程会绕过 `install_skill.py` 并通过 ClawHub 的 API 获取内容。

1. **获取 SKILL.md 内容：**
    - 使用 ClawHub 的文件端点获取原始的 SKILL.md 内容：
        ```bash
        curl -s "https://clawhub.ai/api/v1/skills/{slug}/file?path=SKILL.md" \
          -o /tmp/clawhub-{slug}/SKILL.md
        ```
    - **重要提示：**此端点返回原始的 `text/plain` 内容，而不是 JSON。将响应体直接保存为文件。
    - 可以使用 `x-content-sha256` 响应头来验证文件完整性。
2. **处理多文件技能（如果适用）：**
    - 如果技能有额外的文件（脚本、配置文件），使用 ClawHub 的下载端点：
        ```bash
        curl -s "https://clawhub.ai/api/v1/download?slug={slug}" \
          -o /tmp/clawhub-{slug}.zip
        unzip -o /tmp/clawhub-{slug}.zip -d /tmp/clawhub-{slug}/
        ```
    - 要检查技能是否有多个文件，请检查 `GET /api/v1/skills/{slug}` 的详细响应——`latestVersion` 对象可能表示文件数量。
3. **运行安全扫描：**
    - 由于绕过了 `install_skill.py`，因此需要手动运行安全扫描：
        ```bash
        python3 ~/.claude/skills/universal-skills-manager/scripts/scan_skill.py /tmp/clawhub-{slug}/
        ```
    - 在继续之前请查看任何发现的结果。ClawHub 集成了 VirusTotal 功能，但我们的扫描提供了额外的安全检查。
4. **验证 YAML 前置内容：**
    - 验证 SKILL.md 是否具有有效的 YAML 前置内容（名称、描述字段）。
    - 如果无效，警告用户并询问是否继续。
5. **创建目录并安装：**
    - 创建目标目录：`.../skills/{slug}/`
    - 将所有文件从临时目录复制到目标位置：
        ```bash
        mkdir -p {target-path}/{slug}
        cp -r /tmp/clawhub-{slug}/* {target-path}/{slug}/
        ```

6. **确认：**
    - 报告：“已从 ClawHub 安装 '{displayName}'（版本 {version}），路径为 {path}”
    - 显示版本信息和星星数量。
    - 提供与其他人工智能工具同步的选项。

7. **清理：**
    - 删除临时目录：
        ```bash
        rm -rf /tmp/clawhub-{slug}/ /tmp/clawhub-{slug}.zip
        ```

#### D. 从本地来源安装（同步/复制）
1. **检索：**从源目录中读取所有文件。
2. **创建目录：**创建目标目录 `.../skills/{slug}/`。
3. **保存文件：**将所有文件复制到新位置，保留文件名。

### SkillsMP API 配置

**基础 URL：**`https://skillsmp.com/api/v1`

**认证：**
```bash
Authorization: Bearer $SKILLSMP_API_KEY
```

**可用端点：**
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}``
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

**响应格式（人工智能搜索）：**
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
- `401`：API 密钥无效或缺失。
- `400`：缺少必需的查询参数。
- `500`：内部服务器错误。

### SkillHub API 配置

**基础 URL：**`https://skills.palebluedot.live/api`

**认证：**无需认证（开放 API）

**可用端点：**
- `GET /api/skills?q={query}&limit={20}` — 按关键词搜索技能
- `GET /api/skills/{id}` — 获取完整技能详细信息（包括 `skillPath`、`branch`、`rawContent`）
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

**详细响应格式（GET /api/skills/{id}）：**
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
- `skillPath`：GitHub 仓库内的实际目录路径（至关重要——`id` 并不对应文件路径）。
- `branch`：分支名称（例如，`main`）。
- `githubOwner` + `githubRepo`：用于构建 GitHub URL。
- `rawContent`：完整的 SKILL.md 内容（如果 GitHub 不可用，可以使用此内容作为备用）。

**错误处理：**
- `404`：未找到技能。
- `500`：内部服务器错误。

### ClawHub API 配置

**基础 URL：**`https://clawhub.ai/api/v1`

**认证：**无需认证（开放 API）

**速率限制：**每 IP 每分钟 120 次读取（在 `x-ratelimit-remaining` 和 `x-ratelimit-reset` 响应头中显示）

**可用端点：**
- `GET /api/v1/search?q={query}&limit={20}` — 按相似度分数进行语义/向量搜索
- `GET /api/v1/skills?limit={20}&sort={stars|downloads|updated|trending}&cursor={cursor}` — 带有分页的浏览/列表
- `GET /api/v1/skills/{slug}` — 获取完整技能详细信息（所有者、版本）
- `GET /api/v1/skills/{slug}/file?path={path}&version={ver}` — 下载完整技能文件（文本格式，不是 JSON）
- `GET /api/v1/download?slug={slug}&version={ver}` — 下载完整技能文件（ZIP 格式）

**搜索响应格式（GET /api/v1/search）：**
```json
{
  "results": [
    {
      "score": 0.82,
      "slug": "self-improving-agent",
      "displayName": "Self-Improving Agent",
      "summary": "An agent that iteratively improves itself...",
      "version": "1.0.0",
      "updatedAt": "2026-01-15T10:30:00Z"
    }
  ]
}
```

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

**详细响应格式（GET /api/v1/skills/{slug}）：**
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
- 返回原始的 `text/plain` 内容（不是 JSON）。
- 响应头包含 `x-content-sha256`（完整性哈希）和 `x-content-size`（文件大小）。
- 使用 `version` 查询参数来获取特定版本（默认为最新版本）。

**与 SkillsMP/SkillHub 的主要区别：**
- **直接托管：**ClawHub 直接托管技能文件——无需构建 GitHub URL。
- **带版本号的技能：**每个技能都有明确的版本号；使用 `version` 参数来指定版本。
- **基于 slug 的 ID：**技能通过 `slug` 进行标识（例如，`self-improving-agent`），而不是 GitHub 路径。
- **内置的语义搜索：**`/search` 端点使用向量相似度进行搜索，而不是关键词匹配。
- **VirusTotal 集成：**ClawHub 通过 VirusTotal 进行扫描；`moderation` 字段表示状态。

**错误处理：**
- `404`：未找到技能或文件。
- `429`：超出速率限制（每分钟 120 次读取）。
- `500`：内部服务器错误。

**指南：**
- **多源搜索：**当有 API 密钥时，优先使用 SkillsMP 作为主要来源。提供 SkillHub 和 ClawHub 作为备用或额外来源。
- **优先使用人工智能/语义搜索：**对于自然语言查询，使用 SkillsMP 的 `/ai-search` 或 ClawHub 的 `/search`（两者都支持语义匹配）。SkillHub 仅支持关键词搜索。
- **来源标注：**始终在结果中标明来源（`[SkillsMP]`、`[SkillHub]` 或 `[ClawHub]`），以便用户区分来源。
- **从 SkillHub 安装技能时：**始终首先获取详细信息端点以获取正确的 `skillPath` 和 `branch`。切勿尝试将 `id` 字段解析为文件路径。
- **ClawHub 直接托管：**ClawHub 直接托管技能文件——使用 `/file` 端点获取内容。无需构建 GitHub URL。使用 `slug` 字段作为技能标识符。
- **ClawHub 版本控制：**ClawHub 技能有明确的版本号。在安装确认时显示版本号。如果需要，可以使用 `version` 查询参数来指定特定版本。
- **去重：**在显示来自多个来源的结果时，进行去重：SkillsMP ↔ SkillHub 通过完整的技能 ID (`{owner}/{repo}/{path}`）；ClawHub ↔ 其他来源通过技能名称（因为 ClawHub 使用 slug，而不是 GitHub 路径）。
- **验证内容：**从任何来源获取内容后，验证 SKILL.md 是否具有有效的 YAML 前置内容。
- **结构完整性：**保持 `.../skills/{skill-name}/SKILL.md` 的结构。
- **同步：**安装技能后，提供将其同步（复制）到其他检测到的人工智能工具。
- **GitHub URL：**对于 SkillsMP/SkillHub 的安装，始终将树形 URL 转换为 raw.githubusercontent.com URL 以获取内容。
- **安全性：**无论来源如何，都对所有安装进行安全扫描（SkillsMP、SkillHub 或 ClawHub）。SkillHub 的 `securityScore` 和 ClawHub 的 `moderation` 状态仅用于提供信息——我们在安装时使用自己的 `scan_skill.py` 进行扫描。