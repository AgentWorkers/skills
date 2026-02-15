## 描述  
本技能专为 Fabric AI 框架（https://github.com/danielmiessler/Fabric）设计，用于文本处理。它通过直接读取本地的模式文件来执行文本处理任务，并利用 Fabric CLI 来完成特定的网页内容抓取、YouTube 视频下载以及搜索功能。  

## 规则  

### 1. 模式应用（文本处理）  
**限制：** 禁止使用 `fabric -p "pattern"` 来处理文本。必须手动应用相应的模式，具体步骤如下：  
1. **确定模式名称：** 查明正确的模式名称。如果不确定，请阅读 `~/.config/fabric/patterns/pattern_explanations.md` 以找到合适的模式。  
2. **读取说明文件：** 打开位于 `~/.config/fabric/patterns/"pattern_name"/system.md` 的文件，其中包含处理文本的详细指令。  
3. **执行处理：** 根据 `system.md` 文件中的指令来处理用户提供的文本。  

### 2. Fabric CLI 使用（数据检索与工具）  
仅使用 `fabric` 命令行工具来完成以下特定任务：  

- **YouTube/视频下载：** 使用 `fabric -y "URL"`  
  * **默认行为：** 下载视频的文字记录（transcript）。  
  * **支持的参数：**  
    * `--playlist`（优先选择播放列表中的视频）  
    * `--transcript`（默认选项）  
    * `--transcript-with-timestamps`（包含时间戳的文字记录）  
    * `--comments`（获取视频评论）  
    * `--metadata`（获取视频元数据）  
    * `--yt-dlp-args="..."`（例如：`--cookies-from-browser brave`）  
    * `--spotify="..."`（用于获取 Spotify 播客/剧集的元数据）  
- **网页内容抓取：** 使用 `fabric -u "URL"` 将网页内容以 Markdown 格式下载。  
- **Jina AI 搜索：** 使用 `fabric -q "问题内容"` 进行搜索。  
- **模式更新：** 使用 `fabric -U` 更新本地的模式文件。  

### 3. 与其他工具的集成  
- **Obsidian：** 如果用户需要将处理后的内容保存到 Obsidian 文档库中（例如：“将这个摘要保存到我的 Obsidian 文档库中”），请使用 `obsidian-cli` 技能。  

## 示例  

**用户：** “使用 `extract_wisdom` 模式对这个网站的内容进行总结：https://example.com”  
**操作步骤：**  
1. 运行 `fabric -u "https://example.com"` 以获取网页的原始文本。  
2. 读取 `~/.config/fabric/patterns/extract_wisdom/system.md` 文件中的处理指令。  
3. 根据 `system.md` 中的说明处理原始文本。  

**用户：** “使用 `fabric` 下载这个视频的文字记录（包含时间戳）。”  
**操作步骤：**  
   运行 `fabric -y "VIDEO_URL" --transcript-with-timestamps`。  

**用户：** “我需要使用 `fabric` 分析这段文本，但不知道该使用哪个模式。”  
**操作步骤：**  
1. 阅读 `~/.config/fabric/patterns/pattern_explanations.md` 以选择合适的模式。  
2. 选择最合适的模式，并根据其 `system.md` 文件中的说明来处理文本。