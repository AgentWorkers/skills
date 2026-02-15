---
name: courseforge
description: 通过 CourseForge API (caringcourseforge.com) 创建和管理在线课程。当用户需要创建课程、模块、课程内容，生成 AI 内容，导出为 SCORM/xAPI 格式，管理知识库，或与 CourseForge 平台进行交互时，可以使用该 API。该 API 支持课程构建、内容生成、测验功能，以及课程内容的可访问性验证和导出操作。
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: ["node"]
      env: ["COURSEFORGE_API_KEY"]
    install:
      - id: npm
        kind: npm
        package: courseforge-mcp-client
        global: true
        bins: ["courseforge-mcp"]
        label: "Install CourseForge MCP client (npm)"
---

# CourseForge

通过MCP客户端在[Caring CourseForge](https://caringcourseforge.com)上构建和管理课程。

**来源:** [npm — courseforge-mcp-client](https://www.npmjs.com/package/courseforge-mcp-client)  
**发布者:** Caring Consulting Co ([caringcos.com](https://caringcos.com))

## 设置

1. 安装：`npm install -g courseforge-mcp-client`
2. 在环境中设置`COURSEFORGE_API_KEY`：
   - 获取API密钥：登录caringcourseforge.com → 设置 → API密钥
   - **安全存储**：通过网关环境配置或shell配置文件（例如：`export COURSEFORGE_API_KEY=cf_prod_...`）。切勿将API密钥存储在明文的工作区文件中。
3. 验证：`courseforge-mcp`能够无错误地启动。

## 调用工具

使用包装脚本来调用CourseForge提供的89个工具中的任意一个：

```bash
node scripts/courseforge.mjs <tool_name> '<json_args>'
```

该脚本需要环境变量`COURSEFORGE_API_KEY`（通过网关环境或shell配置文件设置）。

```bash
node scripts/courseforge.mjs list_courses '{}'
```

输出为格式整洁的JSON数据（MCP数据包会被自动去除）。

## 可用工具（共89个）

- **课程**（7个）：`list_courses`、`create_course`、`get_course`、`update_course`、`delete_course`、`get_course_settings`、`update_course_settings`
- **模块**（5个）：`create_module`、`update_module`、`delete_module`、`reorder_modules`、`get_module`
- **课程单元**（7个）：`create_lesson`、`get_lesson`、`update_lesson`、`delete_lesson`、`reorderlessons`、`move_lesson`、`duplicate_lesson`
- **内容块**（6个）：`add_content_block`、`get_content_block`、`update_content_block`、`delete_content_block`、`reorder_content_blocks`、`move_content_block`
- **课程管理**（3个）：`validate_course`、`duplicate_module`、`export_course`
- **知识库**（5个）：`list_collections`、`create_collection`、`list_documents`、`delete_document`、`search_knowledge`
- **AI与内容生成**（26个）：`ai_chat_assistant`、`ai_chat_with_research`、`generate_course_outline`、`generate.lesson_content`、`generate_quiz_from_content`、`generate_image`、`generate_job_aid_pdf`、`suggest_improvements`、`auto_fix_quality_issues`、`translate_content`、`summarize_document`、`convert_document_to_pdf`、`analyze_image`、`marketing_support_chat`、`web_search`、`fetch_url_content`、`get_youtube_metadata`、`get_youtube_captions`、`scrape_web_to_knowledge`、`upload_to_knowledge`、`manage_knowledge_files`、`search_user_media`、`list_storage_files`、`delete_storage_file`、`get_storage_usage`、`get_openapi_spec`
- **搜索与媒体**（2个）：`search_stock_media`、`search_youtube`
- **录制内容**（1个）：`list_recordings`
- **API密钥**（3个）：`list_api_keys`、`create_api_key`、`revoke_api_key`
- **技能**（2个）：`list_skills`、`get_skill`
- **交互式用户界面控制**（22个）：`lock_canvas`、`unlock_canvas`、`refresh_canvas`、`notify_user`、`show_progress`、`requestconfirmation`、`request_choice`、`scroll_to_element`、`select_element`、`expand_sidebar_item`、`focus_content_block`、`get_canvas_state`、`open_preview`、`close_preview`、`open_settings`、`toggle_sidebar`、`create_checkpoint`、`rollback_to_checkpoint`、`list_checkpoints`、`add_annotation`、`remove_annotation`、`highlight_issues`

有关任何工具的完整参数详情，请参阅`references/tools.md`。

## 常见工作流程

### 从零开始创建课程

1. `create_course`：设置课程标题、描述和难度级别（初级/中级/高级）
2. 为每个课程模块使用`create_module`命令。
3. 为每个课程单元使用`createLesson`命令，传入`courseId`和`moduleId`。
4. 使用`add_content_block`为课程单元添加文本、图片或测验。
5. 使用`validate_course`检查课程的质量和可访问性。
6. 使用`export_course`将课程导出为SCORM 1.2、SCORM 2004、xAPI或HTML格式。

### 基于AI的课程生成

1. 使用`generate_course_outline`提供主题、目标受众和难度级别，以获取课程结构。
2. 结合`create_course`、`create_module`和`create.lesson`命令构建课程结构。
3. 使用`generate.lesson_content`为每个课程单元自动生成内容。
4. 使用`generate_quiz_from_content`根据课程内容创建评估题。
5. 使用`suggest_improvements`获取AI提供的质量改进建议。
6. 使用`auto_fix_quality_issues`自动修复内容质量问题。

### 使用特定技能生成定制内容

1. 使用`list_skills`查看所有17种可用技能。
2. 使用`get_skill`加载所需技能（例如：“Instructional Designer”或“HR Specialist”）。
3. 在使用`ai_chat_assistant`生成内容时，根据所选技能调整生成内容。

### 导出课程

```bash
node scripts/courseforge.mjs export_course '{"courseId":"xxx","format":"scorm12"}'
```

支持导出格式：`scorm12`、`scorm2004`、`xapi`、`html`。

### 内容块类型

使用`add_content_block`时，`type`字段支持以下类型：
- `text`：富文本/HTML内容
- `image`：带有URL和alt文本的图片
- `video`：嵌入的视频（YouTube、Vimeo或URL）
- `quiz`：交互式测验
- `tabs`：分页的内容区域
- `accordion`：可折叠的内容部分
- `callout`：高亮的提示框
- `divider`：视觉分隔符
- `code`：带有语法高亮的代码块
- `embed`：外部嵌入内容（iframe）
- `hotspot`：交互式图片热点
- `flashcard`：用于复习的闪卡
- `sortable`：支持拖放排序的内容
- `timeline`：时间线可视化
- `process`：逐步指导流程
- `labeled_graphic`：带标签的图表
- `knowledge_check`：快速知识检测
- `scenario`：分支式场景

## 注意事项

- 所有ID均为Firestore文档ID（字母数字字符串）。
- 课程具有层次结构：课程 → 模块 → 课程单元 → 内容块。
- 知识库存储AI工具生成内容所需的参考文档。
- 使用交互式用户界面控制工具时，用户需要在浏览器中打开课程编辑器。
- AI生成工具的使用受到用户订阅级别的限制。