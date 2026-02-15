---
name: youtube-transcript
description: YouTube 长视频（超过 1 小时）的完整转录与翻译工作流程：适用于用户需要执行以下操作的情况：  
1. 从 YouTube 视频中提取字幕；  
2. 将英文字幕翻译成中文；  
3. 处理超出平台会话时间限制的长视频；  
4. 处理来自 DownSub API 的响应并生成格式化的文档。
---

# YouTube 长视频的字幕提取与翻译

针对时长超过1小时的YouTube视频，提供完整的字幕提取和翻译工作流程。

## 先决条件

- DownSub API密钥（以`AIza...`开头的Bearer令牌）
- `zhiyan`工具（可选，用于在线文档生成）
- 子代理（sub-agent）的启动能力（用于处理长视频）

## DownSub API配置

**端点**：`https://api.downsub.com/download`
**方法**：`POST`
**请求头**：
```
Authorization: Bearer AIzaM9ifctIOxusNAldvGeajHqq4rH6e7MJNfN
Content-Type: application/json
```
**请求体**：
```json
{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}
```

**⚠️ 重要提示**：务必检查响应中的`lang`字段。**仅使用`en`或`en-auto`**。**切勿使用其他语言（例如`lt`表示立陶宛语）。**

## 预处理（必须先执行）

1. **检查DownSub API访问权限**
   - 确认`Authorization`请求头已正确配置
   - 常见错误：“401 Unauthorized”表示API密钥缺失或无效

2. **检查输出功能**
   - 是否安装了`zhiyan`工具？ → 可以生成在线文档
   - 未安装`zhiyan`？ → 生成本地`.md`文件

3. **检查会话资源限制**
   - 确保系统具有启动子代理的能力，以便处理长视频内容

## 工作流程

### 第1步：准备工作（主会话）

1. **环境检查**：确认已获取DownSub API密钥
2. **获取视频链接**
3. **验证语言设置**：使用DownSub API查询视频的语言设置
   - 如果`lang="en"`或`"en-auto"` → 继续处理
   - 如果`lang="lt"`或其他语言 → 停止处理，不进行翻译
4. **检查字幕长度**：如果字幕超过1000行，**不要在主会话中处理**该视频

5. **启动子代理**：
   ```
   Task: Translate transcript.txt to Chinese verbatim.
   Process in 500-line chunks to separate files (part1.md, etc.).
   Merge to full_transcript.md.
   Add Executive Summary and Key Metrics Table (Chinese) at top.
   Do NOT use zhiyan.
   Budget: 30 minutes or $2 cost limit.
   ```

### 第2步：执行（子代理）

1. **分块读取视频内容**：每次读取500行数据（限制每次读取量）
2. **翻译并格式化**：将字幕内容逐行翻译成中文，并添加适当的标题（如`## 开场`等）
3. **写入文件**：将翻译后的内容分别写入不同的文件中，或使用`cat >>`命令将所有内容合并到一个文件中
4. **补充信息**：
   - 读取前500行以提取关键数据（如收入、增长情况等）
   - 生成执行摘要（3-5条要点，中文格式）
   - 创建关键数据表格（Markdown格式）
   - 将这些内容添加到最终文件中
5. **返回结果**：返回包含完整字幕内容的文件路径（`full_transcript.md`）

### 第3步：结果交付（主会话）

1. 从子代理获取文件路径
2. **上传结果**：如果可用，请使用`zhiyan`工具的MCP功能（`parse_markdown`）处理文件
3. 将生成的文档链接或文件发送给用户

## 常见问题及解决方法

**问：“什么是DownSub API密钥？”**
→ API密钥未配置。请提供Bearer令牌或将其添加到配置文件中。

**问：“`zhiyan`工具找不到”**
→ 未安装`zhiyan`工具。**解决方法**：跳过上传步骤，直接发送`.md`文件。

**问：翻译结果混乱或包含随机内容**
→ 下载的字幕语言设置错误（例如选择了立陶宛语）。**解决方法**：检查`lang`字段，确保使用`en`语言。

**问：任务超时或停止响应**
→ 视频长度过长，无法在单次会话中完成处理。**解决方法**：启动子代理在后台继续处理视频内容。