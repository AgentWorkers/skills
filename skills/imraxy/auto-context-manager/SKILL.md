# 自动上下文管理器

这是一个基于人工智能的自动项目上下文管理工具，能够检测用户当前关注的项目，并保持上下文意识。

## 激活方式

- **自动检测**：在会话开始时或上下文不明确时自动激活。
- **手动调用**：当用户询问项目相关内容或需要切换上下文时手动触发。

## 快速命令

从技能目录中运行以下命令：

```bash
# Detect project from message
python acm.py detect "your message here"

# List all projects
python acm.py list

# Get current active project
python acm.py current

# Switch to different project
python acm.py switch <project_id>
```

## 会话中的使用方式

- 当用户消息中包含项目关键词时：
  1. 运行 `python acm.py detect "<message>"` 以识别当前上下文。
  2. 根据识别出的上下文，优先推荐相关的技能或信息。
  3. 以用户所关注的项目为背景提供相应的回复。

**示例：**
```
User: "Check my portfolio"
-> Detect: financial/trading project
-> Use relevant financial skills
-> Check trading-related memory files
```

## 配置

项目信息存储在 `~/.auto-context/projects.json` 文件中，可以对其进行自定义配置：

```json
{
  "projects": {
    "my-project": {
      "name": "My Project",
      "description": "Project description",
      "keywords": ["keyword1", "keyword2", "keyword3"]
    }
  },
  "current_project": "default"
}
```

## 相关文件

- `auto_context_manager.py`：核心模块
- `acm.py`：命令行接口（CLI）封装层
- `~/.auto-context/projects.json`：项目配置文件（系统自动生成）

## 添加项目

```python
from auto_context_manager import AutoContextManager
acm = AutoContextManager()
acm.create_project('project_id', 'Project Name', ['keyword1', 'keyword2'], 'Description')
```

## 集成说明

- 该工具完全为本地化设计，不依赖任何外部 API。
- 数据存储在 `~/.auto-context/` 目录下。
- 使用置信度评分来表示项目匹配的准确性。
- 该工具总会返回一个处理结果（默认为“default”项目）。