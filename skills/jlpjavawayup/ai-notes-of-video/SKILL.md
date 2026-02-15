---
name: ai-notes-of-video
description: 该视频AI笔记工具由百度提供。它根据用户提供的视频下载地址，下载并解析视频内容，最终生成与视频相关的AI笔记（总共可以生成三种类型的笔记：文档笔记、大纲笔记和图文笔记）。
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 人工智能PPT生成功能

该功能允许OpenClaw代理仅根据用户提供的视频地址生成人工智能生成的笔记。

## 设置要求

1. **API密钥：** 确保`BAIDU_API_KEY`环境变量已设置为有效的API密钥。
2. **运行时环境：** API密钥必须在运行时环境中可用。

## API列表

|    名称            |                路径                          |            描述                                      |
|------------|---------------------------------|---------------------------------------|
| AINotesTaskCreate | /v2/tools/ai_note/task_create    | 根据用户提供的视频地址创建人工智能笔记任务            |
| AINotesTaskQuery | /v2/tools/ai_note/query       | 根据任务ID查询人工智能笔记任务的结果                    |

## 工作流程

1. 调用`AINotesTaskCreate` API来执行位于`scripts/ai_notes_task_create.py`的Python脚本。
2. 调用`AINotesTaskQuery` API来执行位于`scripts/ai_notes_task_query.py`的Python脚本。
3. 首先，调用`AINotesTaskCreate` API创建任务并获取任务ID；此时需要提供视频地址。
4. 接着，调用`AINotesTaskQuery` API根据任务ID查询任务结果。
5. 重复步骤2，直到任务状态变为“完成”（状态代码为10002）。状态代码10000表示任务正在进行中；其他状态代码表示任务失败。
6. 笔记列表中的每个条目都包含笔记内容。列表中的每个条目具有以下字段：
   - `tpl_no`：笔记类型（1 - 手稿笔记；2 - 大纲笔记；3 - 图文结合笔记）
   - `detail`：笔记详情；其中`status`字段表示笔记的状态（10002表示成功，10000表示进行中，其他状态代码表示失败）
   - `content`：笔记的具体内容
   - 大纲笔记中的思维导图会用“Mind”标签标出

## 相关API

### AINotesTaskCreate API

#### 参数

- `video_url`：视频的URL（必填）

#### 使用示例
```bash
BAIDU_API_KEY=xxx python3 scripts/ai_notes_task_create.py 'https://xxxxx.bj.bcebos.com/1%E5%88%86%E9%92%9F_%E6%9C%89%E5%AD%97%E5%B9%95.mp4'
```

### PPTOutlineGenerate API

#### 参数

- `task_id`：由`AINotesTaskCreate` API返回的任务ID（必填）

#### 使用示例
```bash
BAIDU_API_KEY=xxx python3 scripts/ai_notes_task_query.py "26943ed4-f5a9-4306-a05b-b087665433a0"
```