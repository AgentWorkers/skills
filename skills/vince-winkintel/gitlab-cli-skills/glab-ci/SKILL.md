---
name: glab-ci
description: 与 GitLab 的 CI/CD 管道、作业（jobs）以及相关工件（artifacts）进行交互。可用于查看管道状态、查看作业日志、调试 CI 失败问题、触发手动作业、下载工件、验证 `.gitlab-ci.yml` 文件，或管理管道运行。触发条件包括：管道状态变化、CI/CD 进程、作业完成、构建完成、部署完成、工件生成、管道状态变化、构建失败以及 CI 日志更新等。
---

# glab ci  
与 GitLab 的持续集成（CI/CD）管道、作业以及相关工件进行交互。  

## 快速入门  
```bash
# View current pipeline status
glab ci status

# View detailed pipeline info
glab ci view

# Watch job logs in real-time
glab ci trace <job-id>

# Download artifacts
glab ci artifact main build-job

# Validate CI config
glab ci lint
```  

## 常见工作流程  

### 调试管道故障  
1. **检查管道状态：**  
   ```bash
   glab ci status
   ```  
2. **查看失败的作业：**  
   ```bash
   glab ci view --web  # Opens in browser for visual review
   ```  
3. **获取失败作业的日志：**  
   ```bash
   # Find job ID from ci view output
   glab ci trace 12345678
   ```  
4. **重试失败的作业：**  
   ```bash
   glab ci retry 12345678
   ```  

**自动化调试：**  
使用调试脚本可快速诊断故障：  
```bash
scripts/ci-debug.sh 987654
```  
该脚本会自动：  
- 查找所有失败的作业  
- 显示日志  
- 提出下一步操作建议。  

### 操作手动作业  
1. **查看包含手动作业的管道：**  
   ```bash
   glab ci view
   ```  
2. **触发手动作业：**  
   ```bash
   glab ci trigger <job-id>
   ```  

### 工件管理  
- **下载构建工件：**  
   ```bash
glab ci artifact main build-job
```  
- **从特定管道下载工件：**  
   ```bash
glab ci artifact main build-job --pipeline-id 987654
```  

### CI 配置  
- **推送前进行验证：**  
   ```bash
glab ci lint
```  
- **验证特定文件：**  
   ```bash
glab ci lint --path .gitlab-ci-custom.yml
```  

### 管道操作  
- **列出最近的管道：**  
   ```bash
glab ci list --per-page 20
```  
- **运行新的管道：**  
   ```bash
glab ci run
```  
- **使用变量运行管道：**  
   ```bash
glab ci run --variables KEY1=value1 --variables KEY2=value2
```  
- **取消正在运行的管道：**  
   ```bash
glab ci cancel <pipeline-id>
```  
- **删除旧的管道：**  
   ```bash
glab ci delete <pipeline-id>
```  

## 故障排除  
- **管道卡住/处于待处理状态：**  
  - 检查运行器的可用性：通过 Web 界面查看管道状态  
  - 查看作业日志：`glab ci trace <job-id>`  
  - 取消并重试：`glab ci cancel <id>`，然后 `glab ci run`  

- **作业失败：**  
  - 查看日志：`glab ci trace <job-id>`  
  - 检查工件上传情况：验证作业输出中的文件路径  
  - 验证配置：`glab ci lint`  

## 相关技能  
- **针对作业的操作：**  
  - 查看 `glab-job` 以获取单个作业的命令（列出、查看、重试、取消）  
  - 使用 `glab-ci` 进行管道级操作，`glab-job` 进行作业级操作  

- **管道触发器和调度：**  
  - 查看 `glab-schedule` 以设置管道自动化任务  
  - 查看 `glab-variable` 以管理 CI/CD 变量  

- **与 MR（Merge Request）的集成：**  
  - 查看 `glab-mr` 以执行合并操作  
  - 使用 `glab mr merge --when-pipeline-succeeds` 实现基于管道状态的合并  

- **自动化：**  
  - 脚本：`scripts/ci-debug.sh` 用于快速故障诊断  

## 命令参考  
有关所有命令的详细文档和参数，请参阅 [references/commands.md](references/commands.md)。  

**可用命令：**  
- `status` - 查看当前分支的管道状态  
- `view` - 查看详细的管道信息  
- `list` - 列出最近的管道  
- `trace` - 查看作业日志（实时或已完成状态）  
- `run` - 创建/运行新的管道  
- `retry` - 重试失败的作业  
- `cancel` - 取消正在运行的管道/作业  
- `delete` - 删除管道  
- `trigger` - 触发手动作业  
- `artifact` - 下载作业工件  
- `lint` - 验证 `.gitlab-ci.yml` 配置文件  
- `config` - 管理 CI/CD 配置  
- `get` - 获取管道的 JSON 数据  
- `run-trig` - 触发管道执行