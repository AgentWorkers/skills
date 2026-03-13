---
name: note
description: 知识捕获与连接系统，具备自动组织和检索功能。适用于用户需要做笔记、记录想法、保存见解或查找以往笔记的场景。该系统能够从任何来源捕获信息，根据主题和项目自动对内容进行分类整理，并在需要时呈现相关笔记；同时还能跨不同领域关联相关的内容。所有数据均存储在本地设备上。
---
# 注意

这是一个知识捕获系统，帮助您记住所有事情并快速找到所需的信息。

## 关键的隐私与安全措施

### 数据存储（至关重要）
- **所有笔记仅存储在本地**：`memory/notes/`
- **不使用任何云笔记服务**  
- **不进行外部同步**——完全采用本地存储  
- **不共享任何笔记或想法**  
- 用户可以完全控制数据的保留和删除

### 数据结构
笔记存储在您的本地工作空间中：
- `memory/notes/notes.json` – 所有捕获的笔记  
- `memory/notes/topics.json` – 自动分类的笔记主题  
- `memory/notes/projects.json` – 按项目组织的笔记  
- `memory/notes/connections.json` – 笔记之间的关联关系  
- `memory/notes/search_index.json` – 用于优化搜索的索引  

## 核心工作流程

### 捕获笔记  
```
User: "Note: The insight from the book about feedback loops applies to our onboarding problem"
→ Use scripts/capture_note.py --content "Feedback loops from book apply to onboarding" --context "reading"
→ Extract note, identify topics, store automatically
```

### 查找相关笔记  
```
User: "What have I written about onboarding?"
→ Use scripts/find_notes.py --query "onboarding" --context current
→ Surface all notes related to onboarding, including unexpected connections
```

### 会议准备  
```
User: "I'm meeting with Sarah tomorrow"
→ Use scripts/prep_meeting.py --person "Sarah"
→ Pull all previous notes about Sarah, her projects, commitments made
```

### 连接相关想法  
```
User: "This reminds me of something I read last month"
→ Use scripts/connect_notes.py --current-note "NOTE-123" --search "last month"
→ Find and surface related notes, create explicit connection
```

### 将笔记转化为知识  
```
User: "Synthesize my notes on product strategy"
→ Use scripts/synthesize.py --topic "product-strategy"
→ Transform scattered notes into coherent framework
```

## 模块参考  
- **捕获系统**：请参阅 [references/capture.md](references/capture.md)  
- **自动组织**：请参阅 [references/organization.md](references/organization.md)  
- **检索与搜索**：请参阅 [references/retrieval.md](references/retrieval.md)  
- **建立关联**：请参阅 [references/connections.md](references/connections.md)  
- **知识合成**：请参阅 [references/synthesis.md](references/synthesis.md)  
- **会议准备**：请参阅 [references/meeting-prep.md](references/meeting-prep.md)  

## 脚本参考  
| 脚本 | 用途 |  
|--------|---------|  
| `capture_note.py` | 从任何上下文中捕获笔记  
| `find_notes.py` | 搜索并检索相关笔记  
| `prep_meeting.py` | 为会议准备笔记  
| `connect_notes.py` | 显式地连接相关的笔记  
| `synthesize.py` | 将笔记转化为知识  
| `review_recent.py` | 查看最近的捕获内容  
| `organize_project.py` | 按项目组织笔记  
| `build_map.py` | 构建跨领域的知识地图