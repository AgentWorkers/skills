---
name: xiaohongshu-extract
description: 从小红书（XHS）的分享或发现页面的 URL 中提取元数据，方法是通过解析 `window.__INITIAL_STATE__` 来获取笔记详情。当需要从公开的 XHS 链接中获取页面内容、笔记元数据、视频信息或互动数据时，可以使用此方法。
---

# Xiaohongshu 提取工具

## 概述

该工具使用内置脚本从 Xiaohongshu 的分享链接或发现链接中提取笔记元数据（标题、描述、类型、时间、用户信息、互动次数、标签以及视频流信息）。

## 快速入门

1. 运行提取工具，并将输出结果以 JSON 格式打印到标准输出（stdout）：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --pretty
```
   ```

2. 将 JSON 数据写入文件：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --output /tmp/xhs_note.json
```
   ```

3. 仅输出扁平化后的数据记录：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --flat-only --pretty
```
   ```

4. 仅将扁平化后的数据记录写入文件：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --flat-only --output /tmp/xhs_flat.json
```
   ```

5. 以 JSON 格式输出错误信息：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --error-json
```
   ```

6. 将错误信息（包括 `final_url` 和 `status_code`（如可用）以 JSON 格式输出到文件：
   ```bash
   ```bash
python scripts/xiaohongshu_extract.py "<xhs_url>" --error-json --output /tmp/xhs_error.json
```
   ```

## 工作流程

1. 使用用户提供的链接运行 `scripts/xiaohongshu_extract.py`。
2. 如果脚本无法找到 `window.__INITIAL_STATE__`，则请求用户提供直接的发现链接。
3. 使用 JSON 输出结果来汇总笔记元数据，或将其用于后续分析。

## 输出说明

脚本返回一个 JSON 对象，其中包含以下字段：

- `note_id`：笔记的唯一标识符
- `title`：笔记的标题
- `desc`：笔记的描述
- `type`：笔记的类型
- `time`：笔记创建的时间
- `ip_location`：用户访问笔记的 IP 地址
- `user`：用户的昵称、用户 ID 和头像信息
- `interact`：用户的互动记录（点赞、收藏、评论、分享次数）
- `tags`：笔记的标签
- `video`：视频的详细信息（视频 ID、时长、宽度、高度、帧率、视频大小以及流媒体链接）
- `field_mapping`：字段名称的映射关系（将嵌套结构转换为扁平化结构）
- `flat`：包含标准化计数和 ISO 时间戳的扁平化数据记录

如果视频流列表为空，`video` 字段可能为空或为 `null`。

- 如果使用 `--flat-only` 参数，仅输出扁平化后的数据。
- 如果使用 `--error-json` 参数，错误信息将以 JSON 格式输出，其中可能包含 `final_url` 和 `status_code`（如果存在）。

## 资源

### scripts/

- `scripts/xiaohongshu_extract.py`：用于从 Xiaohongshu 的分享链接或发现链接中提取笔记元数据的脚本。