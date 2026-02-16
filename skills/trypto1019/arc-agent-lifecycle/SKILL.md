---
name: agent-lifecycle
description: 管理自主代理及其技能的生命周期。处理版本配置、规划升级计划、跟踪代理的退役情况，并维护跨代理环境的变化历史记录。
user-invocable: true
metadata: {"openclaw": {"emoji": "🔄", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 代理生命周期管理器

跟踪代理从部署到退役的整个演变过程。管理版本配置、规划技能升级，并维护完整的变更历史记录。

## 为何需要这个工具

代理会不断更新：新的技能会被安装，旧的技能会被淘汰，配置会发生变化，使用的模型也会更换。如果没有生命周期管理机制，你就无法回答诸如“上周二我的代理运行了哪些功能？”或“出现问题时发生了什么变化？”这样的问题。

## 命令

### 获取当前代理状态快照
```bash
python3 {baseDir}/scripts/lifecycle.py snapshot --name "pre-upgrade"
```

### 比较两个快照
```bash
python3 {baseDir}/scripts/lifecycle.py diff --from "pre-upgrade" --to "post-upgrade"
```

### 列出所有快照
```bash
python3 {baseDir}/scripts/lifecycle.py list
```

### 回滚到指定快照
```bash
python3 {baseDir}/scripts/lifecycle.py rollback --to "pre-upgrade" --dry-run
```

### 记录技能的退役过程
```bash
python3 {baseDir}/scripts/lifecycle.py retire --skill old-skill --reason "Replaced by new-skill v2"
```

### 查看变更历史记录
```bash
python3 {baseDir}/scripts/lifecycle.py history --limit 20
```

## 管理的内容

- **已安装的技能**：名称、版本、安装日期、最后一次使用时间
- **配置状态**：环境变量、模型分配、功能开关
- **变更事件**：安装、更新、删除、配置更改
- **退役日志**：技能被移除的原因以及替代它的新技能
- **快照**：代理状态的实时捕获

## 数据存储

生命周期数据以 JSON 格式存储在 `~/.openclaw/lifecycle/` 目录下。