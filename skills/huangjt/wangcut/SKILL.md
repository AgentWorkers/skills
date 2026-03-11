---
name: wangcut
description: |
  秦丝智能视频剪辑APP的API集成，用于创建和管理AI视频剪辑任务。
  TRIGGER when: 用户请求创建视频、生成视频剪辑、查看视频任务列表、下载剪辑结果、等待任务完成。
  触发词: "创建视频"、"视频剪辑"、"生成视频"、"查看任务"、"下载视频"、"等待视频"、"wangcut"。
  支持功能: (1) 根据文案创建视频剪辑任务，自动随机选择7个素材 (2) 查看任务列表和详情 (3) 等待任务完成并下载视频到本地
---

# 秦丝智能视频剪辑

通过API操作秦丝智能视频剪辑APP。

## 前置要求

1. 配置文件 `config.ini` 在项目根目录，包含账号密码
2. 脚本依赖: `pip install requests`

## 核心功能

### 创建视频任务

自动从最近100个素材中随机选择7个：

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import create_video_task

task_id = create_video_task("你的视频文案内容")
print(f"任务ID: {task_id}")
```

### 查看任务列表

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import list_recent_tasks

tasks = list_recent_tasks(count=10, with_details=True)
status_map = {0: '待处理', 1: '处理中', 2: '处理中', 3: '处理中', 4: '已完成', 5: '失败'}
for t in tasks:
    print(f"ID:{t['id']} 状态:{status_map.get(t.get('status'),'未知')}")
    print(f"   文案:{(t.get('script_content') or '')[:30]}...")
    print(f"   时长:{t.get('duration')}秒 分辨率:{t.get('resolution')}")
    print(f"   封面:{t.get('cover_title')} 语音:{t.get('voice_name')}")
```

### 等待完成并下载

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import wait_and_download

filepath = wait_and_download(task_id=12575, timeout=600, save_dir="./downloads")
print(f"视频已下载: {filepath}")
```

## 任务状态码

| 码 | 状态 |
|----|------|
| 0 | 待处理 |
| 1-3 | 处理中 |
| 4 | 已完成 |
| 5 | 失败 |

## 高级用法

### 指定素材ID

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import WangcutAPI

api = WangcutAPI()
result = api.create_task(
    script_content="视频文案",
    material_ids=[54131, 54130, 54129],
    voice_speed=1.5,
    subtitle_font_color="white"
)
```

### 查看任务详情

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import WangcutAPI

api = WangcutAPI()
detail = api.get_task_detail(task_id=12575)
info = api.extract_task_info(detail)
print(f"文案: {info['script_content'][:50]}...")
print(f"时长: {info['duration']}秒, 分辨率: {info['resolution']}")
print(f"封面: {info['cover_title']}, 语音: {info['voice_name']}")
if info.get('output_path_auth'):
    print(f"视频地址: {info['output_path_auth']}")
```
