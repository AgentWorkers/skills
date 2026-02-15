# 上下文优化器与任务处理技能包

## 概述
本技能包包含两个强大的 OpenClaw 技能，用于自动化管理对话上下文：

1. **上下文优化器**：自动优化对话上下文，以防止出现“提示信息过长”的错误。
2. **任务处理器**：通过自动将大型任务拆分为较小的子任务来处理这些任务。

## 包含的文件
- `skills/context-optimizer/`：包含所有实现文件的主技能目录
- `commands/optimize-context.js`：用于上下文优化的命令处理程序
- `commands/optimize-context.json`：上下文优化的命令配置文件
- `commands/process-task.js`：用于处理大型任务的命令处理程序
- `commands/process-task.json`：任务处理的命令配置文件
- `systems/context-monitor.js`：用于后台监控上下文的系统
- `systems/context-monitor-config.json`：上下文监控的配置文件
- `task_processing_config.json`：全局任务处理配置文件

## 安装说明
1. 将此包解压到您的 OpenClaw 工作目录中：
   ```bash
   cd ~/.openclaw/workspace
   tar -xzf /path/to/context-optimizer-skill.tar.gz
   ```

2. 安装所需的依赖项（如果有的话）：
   ```bash
   cd ~/.openclaw/workspace/skills/context-optimizer
   npm install
   ```

3. 安装完成后，这些技能将可在您的 OpenClaw 系统中使用：
   - `/optimize-context` 命令：用于手动优化上下文
   - `/process-task` 命令：用于处理需要自动拆分的大型任务

## 功能介绍

### 上下文优化器
- 自动监控对话长度
- 当消息数量超过预设阈值时触发优化
- 在清除旧上下文的同时提取关键信息和事实
- 防止出现“提示信息过长”的错误

### 任务处理器
- 检测超出令牌限制的大型任务
- 自动将大型任务拆分为较小的子任务
- 顺序处理子任务的同时保持上下文的一致性
- 与上下文优化功能集成，以防止上下文溢出

### 自动监控
- 持续监控对话上下文的长度
- 支持配置自动优化的阈值
- 与正常的对话流程无缝集成

## 配置
- 在 `task_processing_config.json` 文件中调整设置
- 修改消息数量和令牌限制的阈值
- 配置自动优化的触发时机

安装完成后，这些技能即可立即投入使用！