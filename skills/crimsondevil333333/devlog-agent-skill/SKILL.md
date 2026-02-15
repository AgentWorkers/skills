# DevLog 技能 🦞  
这是一个标准化的日志记录工具，专为 OpenClaw 代理设计，用于使用 `dev-log-cli` 跟踪进度、任务和项目状态。  

## 描述  
该技能帮助代理维护专业的开发日志记录。它能够将上下文信息、项目里程碑以及任务状态存储在一个结构化的 SQLite 数据库中。  

## 必备条件  
- 已安装 `dev-log-cli`（通过 `pipx` 安装）  

## 链接  
- **GitHub**: [https://github.com/CrimsonDevil333333/dev-log-cli](https://github.com/CrimsonDevil333333/dev-log-cli)  
- **PyPI**: [https://pypi.org/project/dev-log-cli/](https://pypi.org/project/dev-log-cli/)  
- **ClawHub**: [https://clawhub.com/skills/devlog-skill](https://clawhub.com/skills/devlog-skill)（待发布）  

## 使用方法  

### 📝 添加日志条目  
代理可以使用该工具记录重要的进展或遇到的问题。  
```bash
devlog add "Finished implementing the auth module" --project "Project Alpha" --status "completed" --tags "auth,feature"
```  

### 📋 查看日志  
查看最近的日志记录以获取详细信息。  
```bash
devlog list --project "Project Alpha" --limit 5
```  

### 📊 查看统计信息  
检查项目的运行状态和活动情况。  
```bash
devlog stats --project "Project Alpha"
```  

### 🔍 搜索  
根据特定主题查找历史日志记录。  
```bash
devlog search "infinite loop"
```  

### 🛠️ 编辑/查看日志  
对日志条目进行详细检查或修改。  
```bash
devlog view <id>
devlog edit <id>
```  

## 内部设置  
该技能包含一个 `setup.sh` 脚本，用于确保 `dev-log-cli` 命令行工具能够正常使用。