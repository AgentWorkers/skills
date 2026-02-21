---
name: solo-you2idea-extract
description: >
  **通过 solograph MCP 从 YouTube 视频中提取创业灵感——实现索引、搜索并导出到 you2idea 网站**  
  该系统采用多 MCP 协调模式（从 YouTube 获取视频 → 分析内容 → 将结果存储到知识库中）。适用于用户执行以下操作的场景：  
  - “从 YouTube 中提取创业灵感”  
  - “对 YouTube 视频进行索引处理”  
  - “更新 you2idea 系统”  
  - “在视频中寻找创业灵感”  
  - “将视频内容同步到网站”  
  **注意：**  
  - 本系统专用于从 YouTube 视频中提取与创业相关的信息，不适用于普通观看视频（无需任何技能）或内容创作（请使用 /content-gen 功能）。
license: MIT
metadata:
  author: fortunto2
  version: "1.0.0"
  openclaw:
    emoji: "💡"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__source_search, mcp__solograph__source_list, mcp__solograph__source_tags, mcp__solograph__source_related, mcp__solograph__kb_search, mcp__solograph__web_search, mcp__solograph__codegraph_query
argument-hint: "[video-url or channel-name or 'deploy']"
---
# /you2idea-extract

## 多MCP协调技能：YouTube MCP工具 → 想法分析 → 知识库/网站导出

该工具支持三种模式：

- **索引**：通过`solograph CLI`将视频添加到FalkorDB源图中。
- **分析**：在索引后的视频库中搜索创业想法，并提取有价值的见解。
- **部署**：将FalkorDB的数据导出到you2idea网站（数据文件 → R2 → Cloudflare Pages）。

### MCP工具

- `source_search(query, source="youtube")`：对索引后的视频进行语义搜索。
- `source_list()`：查看已索引视频的数量。
- `source_tags()`：自动检测带有置信度分数的主题。
- `source_related(video_url)`：根据共享标签查找相关视频。
- `kb_search(query)`：与solopreneur知识库进行交叉查询。
- `web_search(query, engines="youtube")`：发现新的视频以进行索引。
- `codegraph_query(cypher)`：对YouTube图谱进行原始查询。

### 操作步骤

#### 模式1：索引（如果提供了URL，则默认使用此模式）

1. **解析输入**：
   - URL（例如：`https://youtube.com/watch?v=...`）：单个视频的索引。
   - 频道名称（例如：`GregIsenberg`）：批量索引多个视频。
   - 如果输入为空，提示：“请输入视频URL、频道名称或‘deploy’？”

2. **通过`solograph CLI`索引视频**：
   ```bash
   # Single video (no SearXNG needed — direct yt-dlp)
   cd ~/startups/shared/solograph && uv run solograph-cli index-youtube -u "$URL"

   # Channel batch (needs SearXNG for discovery)
   cd ~/startups/shared/solograph && TAVILY_API_URL=http://localhost:8013 uv run solograph-cli index-youtube -c "$CHANNEL" -n 5
   ```

3. **验证索引结果**：使用`source_list()`确认新视频的数量。

4. **查看索引数据**：使用`source_tags()`查看主题分布情况。

#### 模式2：分析（如果输入包含查询内容）

1. **在视频库中搜索**：`source_search(query="$ARGUMENTS", source="youtube")`。

2. **与知识库进行交叉查询**：`kb_search(query="$ARGUMENTS")`以查找相关的创业机会。

3. **提取见解**：
   - 识别每个相关视频中提到的创业想法。
   - 记录时间戳和演讲者的背景信息。
   - 根据具体性、市场证据和可行性评估想法的潜力。

4. **将见解写入`3-inbox/`文件夹**（使用指定的格式），或打印摘要。

#### 模式3：部署（如果`$ARGUMENTS`包含“deploy”、“sync”或“update site”）

1. **检查前提条件**：
   ```bash
   # FalkorDB source graph exists?
   test -f ~/.solo/sources/youtube/graph.db && echo "graph_ok" || echo "no_graph"
   # you2idea project accessible?
   test -d ~/startups/active/you2idea && echo "project_ok" || echo "no_project"
   ```

2. **在you2idea项目中运行导出流程**：
   ```bash
   cd ~/startups/active/you2idea
   make export              # FalkorDB → all-videos.json + videos.json
   make export-vectors      # FalkorDB → vectors.bin + chunks-meta.json + graph.json
   ```

3. **获取新视频的转录文件（VTT格式）**：
   ```bash
   cd ~/startups/active/you2idea
   make fetch-transcripts   # yt-dlp → public/data/vtt/
   ```

4. **上传到R2 CDN**：
   ```bash
   cd ~/startups/active/you2idea
   make upload              # Incremental → R2 (you2idea-data bucket)
   ```

5. **构建并部署网站**：
   ```bash
   cd ~/startups/active/you2idea
   make build && make deploy  # Astro → Cloudflare Pages
   ```

6. **报告结果**：显示视频数量、文件大小以及部署后的网站URL。

**快捷命令**：`make update-all`可一次性执行整个流程。

### 流程架构（多MCP模式）

MCP工具为整个流程提供了查询层：
- 索引之前：`web_search(engines="youtube")`用于发现新的视频。
- 索引之后：`source_search`用于查找相关的内容。
- 跨项目关联：`kb_search`将创业想法与现有的机会进行匹配。

### 常见问题及解决方法

- **solograph CLI未找到**：
  **原因**：未安装`solograph`包或未将其添加到PATH环境变量中。
  **解决方法**：进入`~/startups/shared/solograph`目录，然后运行`uv sync`。`solograph-cli`的完整命令是`uv run solograph-cli`。

- **使用频道模式时SearXNG不可用**：
  **原因**：SSH隧道未启用。频道模式需要SearXNG来发现视频。
  **解决方法**：在`solopreneur`目录中运行`make search-tunnel`命令。或者使用URL模式（`-u`选项）来绕过SearXNG。

- **导出失败，提示“no graph”**：
  **原因**：`~/.solo/sources/youtube/graph.db`文件不存在。
  **解决方法**：首先至少索引一个视频：`solograph-cli index-youtube -u "VIDEO_URL"`。

- **R2上传失败**：
  **原因**：`rclone`未配置或`wrangler`未登录。
  **解决方法**：运行`~/startups/active/you2idea/scripts/setup-rclone-r2.sh`命令，或登录`wrangler`账户。