---
name: placed-resume-builder
description: 当用户需要“创建简历”、“更新简历”、“将简历导出为PDF格式”、“更改简历模板”、列出自己的所有简历”，或者希望通过placed.exidian.tech上的Placed职业平台来管理简历时，应使用此功能。
version: 1.0.0
metadata: {"openclaw":{"emoji":"📄","homepage":"https://placed.exidian.tech","requires":{"env":["PLACED_API_KEY"]},"primaryEnv":"PLACED_API_KEY"}}
---
# Placed Resume Builder

通过 Placed MCP 服务器，在 AI 的帮助下构建和管理专业简历。

## 前提条件

需要安装 Placed MCP 服务器。安装方法如下：
```json
{
  "mcpServers": {
    "placed": {
      "command": "npx",
      "args": ["-y", "@exidian/placed-mcp"],
      "env": {
        "PLACED_API_KEY": "your-api-key",
        "PLACED_BASE_URL": "https://placed.exidian.tech"
      }
    }
  }
}
```
请在 https://placed.exidian.tech/settings/api 获取您的 API 密钥。

## 可用工具

- `create_resume` — 根据您的个人资料或从零开始创建新的简历
- `get_resume` — 通过 ID 查取简历
- `update.resume` — 更新简历的任何部分（工作经历、教育背景、技能等）
- `list_resumes` — 列出所有简历
- `get_resume_schema` — 查看可用的简历字段
- `list_resume_templates` — 浏览 37 个专业简历模板
- `get_template_preview` — 预览模板
- `change_resume_template` — 更改简历模板
- `get_resume_pdf_url` — 下载简历为 PDF 格式（有效期 15 分钟）
- `get_resume_docx_url` — 下载简历为 Word 文档
- `export_resume_json` — 导出简历为 JSON 格式
- `export Resume_markdown` — 导出简历为 Markdown 格式

## 简历部分

所有部分均为可选，可以独立更新：
- `basics` — 姓名、电子邮件、电话、职位头衔、所在地
- `summary` — 个人职业简介
- `experience` — 工作经历
- `education` — 学历和证书
- `skills` — 技术技能和软技能
- `languages` — 语言能力
- `certifications` — 专业证书
- `awards` — 荣誉和认可
- `projects` — 个人或专业项目
- `publications` — 文章、论文、书籍
- `references` — 专业推荐人
- `volunteer` — 志愿者经历
- `interests` — 兴趣爱好
- `profiles` — LinkedIn、GitHub 等个人资料链接

## 使用方法

**创建简历：**
调用 `create_resume(title="高级工程师简历", target_role="员工工程师")`

**更新简历部分：**
调用 `update_resume(resume_id="...", experience=[...], skills=[...])`

**选择模板：**
1. 调用 `list_resume_templates()` 查看可用模板
2. 调用 `changeresume_template(resume_id="...", template_id="modern")` 应用模板

**导出简历：**
- PDF：调用 `get_resume_pdf_url(resume_id="...)`
- Markdown：调用 `export_resume_markdown(resume_id="...)`
- Word：调用 `get_resume_docx_url(resume_id="...)`

**查看可用字段：**
调用 `get_resume_schema()` 查看所有可用字段及其格式。

## 提示

- 用具体数据（数字、百分比、金额）量化成就
- 在项目列表中的每个条目前使用动词，以提高自动求职系统（ATS）的匹配度
- 使简历内容与职位描述保持一致，以提升匹配效果
- 可使用 `check_ats_compatibility()` 功能测试简历与自动求职系统的兼容性