---
name: glab-job
description: 可以操作单个 CI/CD 作业，包括查看作业状态、重试作业、取消作业、追踪作业日志以及下载作业生成的工件。这些功能适用于调试作业失败、查看作业日志、重试作业或管理作业执行过程。相关触发条件包括作业本身、CI 作业、作业日志以及需要重试的作业等。
---

# glab 工作流程（Working with glab Jobs）

## 操作单个 CI/CD 任务（Working with Individual CI/CD Jobs）

### 快速入门（Quick Start）
```bash
# View job details
glab job view <job-id>

# Download job artifacts
glab job artifact main build-job

# Retry a failed job
glab ci retry <job-id>

# View job logs
glab ci trace <job-id>
```

## 选择使用 `glab ci` 还是 `glab job`？（Decision: Pipeline vs Job Commands?）
```
What level are you working at?
├─ Entire pipeline (all jobs)
│  └─ Use glab-ci commands:
│     ├─ glab ci status     (pipeline status)
│     ├─ glab ci view       (all jobs in pipeline)
│     ├─ glab ci run        (trigger new pipeline)
│     └─ glab ci cancel     (cancel entire pipeline)
│
└─ Individual job
   └─ Use glab-job or glab ci job commands:
      ├─ glab ci trace <job-id>    (job logs)
      ├─ glab ci retry <job-id>    (retry one job)
      ├─ glab job view <job-id>    (job details)
      └─ glab job artifact <ref> <job> (job artifacts)
```

**在以下情况下使用 `glab ci`（pipeline-level）：**
- 检查整个构建过程的进度
- 查看流水线中的所有任务
- 触发新的流水线运行
- 验证 `.gitlab-ci.yml` 文件的配置

**在以下情况下使用 `glab job`（job-level）：**
- 调试特定的失败任务
- 从特定任务中下载生成的工件
- 重试单个任务（而非整个流水线）
- 查看任务的详细信息

## 常见工作流程（Common Workflows）

### 调试失败的任务（Debugging a Failed Job）
1. **找到失败的任务：**
   ```bash
   glab ci view  # Shows all jobs, highlights failures
   ```

2. **查看任务日志：**
   ```bash
   glab ci trace <job-id>
   ```

3. **重试任务：**
   ```bash
   glab ci retry <job-id>
   ```

### 操作生成的工件（Working with Artifacts）
- **从特定任务中下载工件：**
   ```bash
glab job artifact main build-job
```

- **从最近一次成功的构建中下载工件：**
   ```bash
glab job artifact main build-job --artifact-type job
```

### 监控任务进度（Job Monitoring）
- **实时查看任务日志：**
   ```bash
glab ci trace <job-id>  # Follows logs until completion
```

- **检查特定任务的状态：**
   ```bash
glab job view <job-id>
```

## 相关技能（Related Skills）
- **流水线操作（Pipeline Operations）：**
  - 查看 `glab-ci` 中提供的流水线级命令
  - 使用 `glab ci view` 查看流水线中的所有任务
  - 脚本 `scripts/ci-debug.sh` 用于自动化故障诊断

- **CI/CD 配置（CI/CD Configuration）：**
  - 使用 `glab-variable` 管理任务相关的变量
  - 使用 `glab-schedule` 安排任务的定时执行

## 命令参考（Command Reference）
有关所有命令的详细说明和参数，请参阅 [references/commands.md](references/commands.md)。

**可用命令（Available Commands）：**
- `artifact`：下载任务生成的工件
- `view`：查看任务详情
- 大多数任务操作需要使用 `glab ci <command> <job-id>`，例如：
  - `glab ci trace <job-id>`：查看任务日志
  - `glab ci retry <job-id>`：重试任务
  - `glab ci cancel <job-id>`：取消任务