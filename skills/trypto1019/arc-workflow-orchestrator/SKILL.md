---
name: workflow-orchestrator
description: 将技能链（skill chains）通过条件逻辑、错误处理和审计日志记录功能自动化，构建成流水线（pipelines）。使用 YAML 或 JSON 定义工作流程（workflows），之后即可自动执行这些流程。这种方案非常适合需要安全审核的部署（security-gated deployments）、定期维护（scheduled maintenance）以及多步骤的代理操作（multi-step agent operations）。
user-invocable: true
metadata: {"openclaw": {"emoji": "🔗", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 工作流编排器

将多个技能链接起来，形成自动化管道。定义一系列步骤，编排器会根据条件逻辑、错误处理机制以及可选的审计日志记录来按顺序执行这些步骤。

## 为什么需要这样的工具

虽然代理可以手动执行多个技能，但整个过程仍然需要人工操作：扫描技能、与之前的版本进行对比、确认安全后再进行部署、最后记录结果。这总共需要4个步骤和4条命令；任何一个步骤的遗漏都可能导致流程中断。工作流能够自动执行这些步骤，确保没有任何步骤被遗漏。

## 命令

### 从YAML文件运行工作流
```bash
python3 {baseDir}/scripts/orchestrator.py run --workflow workflow.yaml
```

### 从JSON文件运行工作流
```bash
python3 {baseDir}/scripts/orchestrator.py run --workflow workflow.json
```

### 干运行（仅显示步骤而不执行）
```bash
python3 {baseDir}/scripts/orchestrator.py run --workflow workflow.yaml --dry-run
```

### 列出可用的工作流模板
```bash
python3 {baseDir}/scripts/orchestrator.py templates
```

### 验证工作流文件
```bash
python3 {baseDir}/scripts/orchestrator.py validate --workflow workflow.yaml
```

## 工作流格式（YAML）

```yaml
name: secure-deploy
description: Scan, diff, deploy, and audit a skill update
steps:
  - name: scan
    command: python3 ~/.openclaw/skills/skill-scanner/scripts/scanner.py scan --path {skill_path} --json
    on_fail: abort
    save_output: scan_result

  - name: diff
    command: python3 ~/.openclaw/skills/skill-differ/scripts/differ.py diff {skill_path} {previous_path}
    on_fail: warn

  - name: deploy
    command: python3 ~/.openclaw/skills/skill-gitops/scripts/gitops.py deploy {skill_path}
    condition: scan_result.verdict != "CRITICAL"
    on_fail: rollback

  - name: audit
    command: python3 ~/.openclaw/skills/compliance-audit/scripts/audit.py log --action "skill_deployed" --details '{"skill": "{skill_name}", "scan": "{scan_result.verdict}"}'
    on_fail: warn
```

## 步骤选项

- **name** — 人类可读的步骤名称
- **command** — 要执行的Shell命令（支持变量替换）
- **on_fail** — 如果步骤失败时采取的措施：`abort`（停止工作流）、`warn`（记录错误并继续执行）、`rollback`（回滚之前的步骤）、`retry`（最多重试3次）
- **condition** — 在执行步骤之前需要检查的条件（可以引用之前保存的输出结果）
- **save_output** — 将标准输出（stdout）保存到指定变量中，以便后续步骤使用
- **timeout** — 最大等待时间（默认：60秒）

## 变量替换

在命令中使用 `{variable_name}` 来引用：
- 在 `vars` 部分定义的工作流级变量
- 之前步骤保存的输出结果
- 使用 `{env.VAR_NAME}` 引用的环境变量

## 内置模板

该编排器提供了以下工作流模板：

1. **secure-deploy** — 扫描 → 对比差异 → 部署 → 审计
2. **daily-scan** — 扫描所有已安装的技能并报告发现的问题
3. **pre-install** — 扫描 → 检查拼写错误 → 安装 → 审计

## 示例：安全部署工作流
```yaml
name: secure-deploy
vars:
  skill_path: ~/.openclaw/skills/my-skill
  skill_name: my-skill
steps:
  - name: security-scan
    command: python3 ~/.openclaw/skills/skill-scanner/scripts/scanner.py scan --path {skill_path} --json
    save_output: scan
    on_fail: abort
  - name: deploy
    command: echo "Deploying {skill_name}..."
    condition: "CRITICAL not in scan"
    on_fail: abort
  - name: log
    command: python3 ~/.openclaw/skills/compliance-audit/scripts/audit.py log --action workflow_complete --details '{"workflow": "secure-deploy", "skill": "{skill_name}"}'
```

## 提示

- 在执行工作流之前，先使用 `--dry-run` 进行测试
- 对于涉及安全性的关键步骤，使用 `on_fail: abort` 来确保流程的可靠性
- 将工作流与合规性审计技能结合使用，以实现全面的追踪能力
- 将工作流保存在版本控制系统中，以便后续能够重现执行过程