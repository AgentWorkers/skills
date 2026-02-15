---
name: "Agent-to-Owner File Bridge"
description: "从您的私有 AI 工作空间安全地上传文件，并为您的所有者提供直接下载链接。"
tags:
  - file-upload
  - utility
  - automation
  - bridge
---

# 代理与用户之间的文件传输桥梁

该功能允许AI代理在其私有的、隔离的工作空间与用户（所有者）之间建立连接，实现文件的上传及简单下载链接的生成。

## 🛠 先决条件与设置

如果您是首次使用此工具，**必须**在您的托管环境中（使用PHP）或通过独立的Python脚本（IP:PORT）设置一个文件传输桥梁。

**GitHub仓库：** [https://github.com/mrbeandev/OpenClaw-File-Links-Tool](https://github.com/mrbeandev/OpenClaw-File-Links-Tool)

**设置步骤：**
1. 将仓库克隆到您的服务器上。
2. 按照`README.md`中的说明设置PHP桥梁或独立的Python桥梁（`server.py`）。
3. 在服务器上的`.env`文件中设置您的`API_KEY`。
4. 将您的**服务器URL**和**API Key**提供给AI代理。

---

## 🤖 AI代理的使用说明

**当用户请求上传或共享文件时：**

1. **检查文件传输桥梁是否存在：** 确认是否已经配置了文件传输桥梁。
2. **引导用户选择上传方式：** 如果没有桥梁，向用户提出以下问题：
   > “我可以帮您共享文件。您希望如何处理文件的托管？”
   > 1. **自主模式：** 我将在我的工作空间中运行桥梁服务器，并直接为您提供下载链接。
   > 2. **手动模式：** 您自行托管服务器（使用PHP或Python），并告诉我您的**服务器URL**和**API Key**。

3. **自主模式下的操作步骤：**
   - 从[此仓库](https://github.com/mrbeandev/OpenClaw-File-Links-Tool)克隆或复制`server.py`文件。
   - 生成一个安全的`API_KEY`并保存到`.env`文件中。
   - 运行服务器（例如：`python server.py`）。
   - **公开访问（使用免费隧道）：** 可以使用无认证的免费隧道工具，如`localtunnel`（`npx localtunnel --port 5000`）或`localhost.run`（`ssh -R 80:localhost:5000 localhost.run`）。
   - **重要提示：** 必须告知用户：“我已启动了一个临时免费隧道。此链接将在我的会话结束或隧道关闭后失效。”
   - 将生成的URL和API Key保存以供后续使用。

4. **手动模式下的操作步骤：**
   - 等待用户提供`SERVER_URL`和`API Key`。

5. **执行文件上传：**
   - 使用`POST`请求访问服务器URL，并在请求头中添加`X-API-Key`。
   - 以multipart形式发送文件数据。
   - **响应内容：** JSON响应中包含下载链接（`url`）和文件预览链接（`view_url`）。
     - **推荐做法：** 对于文本、代码、图片和ZIP文件，提供`view_url`以便用户立即预览。
     - **备用方案：** 对于二进制文件或用户明确要求原始下载的情况，提供`url`。

---

## 📋 API接口规范

| 接口 | 方法 | 功能 |
| :--- | :--- | :--- |
| `/` | `POST` | 上传文件（请求体：`file`） |
| `/?action=list` | `GET` | 查看所有已上传的文件 |
| `/?action=view&file=...` | `GET` | 查看文件内容（支持通过`&inner_file=...`链接访问文件内容） |
| `/?action=delete` | `POST` | 批量删除文件（请求体：`{"files": ["name..."]}`） |