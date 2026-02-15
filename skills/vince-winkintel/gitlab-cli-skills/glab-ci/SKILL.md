---
name: glab-ci
description: 与 GitLab 的 CI/CD 管道、作业（jobs）以及相关工件（artifacts）进行交互。可用于检查管道状态、查看作业日志、调试 CI 失败问题、触发手动作业、下载工件、验证 `.gitlab-ci.yml` 配置文件，或管理管道的运行过程。触发条件包括：管道状态变化、CI/CD 进程、作业完成、构建完成、部署完成、工件生成、管道失败、以及 CI 日志更新等。
---
# glab ci

本文档介绍了如何使用 GitLab 的持续集成（CI）/持续交付（CD）管道、作业（jobs）以及相关工件（artifacts）。

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

## 管道配置

### 开始使用 `.gitlab-ci.yml`

**使用现成的模板：**
请参阅 [templates/](templates/)，以获取适用于生产环境的管道配置模板：
- `nodejs-basic.yml` - 简单的 Node.js CI/CD 配置
- `nodejs-multistage.yml` - 多环境部署配置
- `docker-build.yml` - 容器构建和部署配置

**使用模板前请进行验证：**
```bash
glab ci lint --path templates/nodejs-basic.yml
```

**最佳实践指南：**
有关详细的配置指南，请参阅 [references/pipeline-best-practices.md](references/pipeline-best-practices.md)：
- 缓存策略
- 多阶段管道模式
- 覆盖率报告集成
- 安全扫描
- 性能优化
- 环境特定配置

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
使用调试脚本可以快速诊断故障：
```bash
scripts/ci-debug.sh 987654
```

该脚本会自动：
- 查找所有失败的作业
- 显示日志
- 提出下一步操作建议

### 使用手动作业

1. **查看包含手动作业的管道：**
   ```bash
   glab ci view
   ```

2. **触发手动作业：**
   ```bash
   glab ci trigger <job-id>
   ```

### 工件管理

**下载构建工件：**
```bash
glab ci artifact main build-job
```

**从特定管道下载工件：**
```bash
glab ci artifact main build-job --pipeline-id 987654
```

### CI 配置

**推送前请进行验证：**
```bash
glab ci lint
```

**验证特定文件：**
```bash
glab ci lint --path .gitlab-ci-custom.yml
```

### 管道操作

**列出最近的管道：**
```bash
glab ci list --per-page 20
```

**运行新的管道：**
```bash
glab ci run
```

**使用变量运行管道：**
```bash
glab ci run --variables KEY1=value1 --variables KEY2=value2
```

**取消正在运行的管道：**
```bash
glab ci cancel <pipeline-id>
```

**删除旧的管道：**
```bash
glab ci delete <pipeline-id>
```

## 故障排除

### 运行时问题

**管道卡住/待处理：**
- 检查运行器的可用性：通过 Web UI 查看管道状态
- 查看作业日志：`glab ci trace <job-id>`
- 取消并重试：`glab ci cancel <id>`，然后 `glab ci run`

**作业失败：**
- 查看日志：`glab ci trace <job-id>`
- 检查工件上传情况：验证作业输出中的文件路径
- 验证配置：`glab ci lint`

### 配置问题

**缓存未生效：**
```bash
# Verify cache key matches lockfile
cache:
  key:
    files:
      - package-lock.json  # Must match actual file name

# Check cache paths are created by jobs
cache:
  paths:
    - node_modules/  # Verify this directory exists after install
```

**作业执行顺序错误：**
```bash
# Add explicit dependencies with 'needs'
build:
  needs: [lint, test]  # Waits for both to complete
  script:
    - npm run build
```

**构建速度慢：**
1. 检查缓存配置（参见 [pipeline-best-practices.md](references/pipeline-best-practices.md#caching-strategies)）
2. 并行执行独立的作业：
   ```yaml
   lint:eslint:
     script: npm run lint:eslint
   lint:prettier:
     script: npm run lint:prettier
   ```
3. 使用更小的 Docker 镜像（例如 `node:20-alpine` 而不是 `node:20`）
4. 优化工件大小（排除不必要的文件）

**后期阶段无法获取工件：**
```yaml
build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour  # Extend if later jobs run after expiry

deploy:
  needs:
    - job: build
      artifacts: true  # Explicitly download artifacts
```

**合并请求（MR）中未显示覆盖率信息：**
```yaml
test:
  script:
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'  # Regex must match output
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

### 性能优化流程

**1. 识别运行缓慢的管道：**
```bash
glab ci list --per-page 20
```

**2. 分析作业耗时：**
```bash
glab ci view --web  # Visual timeline shows bottlenecks
```

**3. 常见优化措施：**
- **并行执行作业：** 同时运行独立的作业
- **积极使用缓存：** 缓存依赖项和构建结果
- **快速检测错误：** 先执行快速检查（如代码格式检查），再执行耗时较长的构建任务
- **优化 Docker 镜像层：** 使用多阶段构建和更小的基础镜像
- **减小工件大小：** 排除源代码映射文件和测试文件

**4. 验证优化效果：**
```bash
# Compare pipeline duration before/after
glab ci list --per-page 5
```

**更多信息：** 有关详细的优化策略，请参阅 [pipeline-best-practices.md](references/pipeline-best-practices.md#performance-optimization)。

## 相关技能

**针对作业的操作：**
- 使用 `glab-job` 命令来执行针对单个作业的操作（列出、查看、重试、取消）
- `glab-ci` 用于管理管道层面，`glab-job` 用于管理作业层面

**管道触发和调度：**
- 使用 `glab-schedule` 实现管道的自动化调度
- 使用 `glab-variable` 管理 CI/CD 变量

**合并请求（MR）集成：**
- 使用 `glab-mr` 执行合并操作
- 通过 `glab mr merge --when-pipeline-succeeds` 实现基于管道状态的合并触发

**自动化：**
- 使用 `scripts/ci-debug.sh` 脚本来快速诊断故障

**配置资源：**
- [templates/](templates/) - 可用的管道模板
- [pipeline-best-practices.md](references/pipeline-best-practices.md) - 完整的配置指南
- [commands.md](references/commands.md) - 完整的命令参考

## 命令参考

有关所有命令的详细说明和参数，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `status` - 查看当前分支的管道状态
- `view` - 查看详细的管道信息
- `list` - 列出最近的管道
- `trace` - 查看作业日志（实时或已完成的状态）
- `run` - 创建/运行新的管道
- `retry` - 重试失败的作业
- `cancel` - 取消正在运行的管道或作业
- `delete` - 删除管道
- `trigger` - 触发手动作业
- `artifact` - 下载作业生成的工件
- `lint` - 验证 `.gitlab-ci.yml` 配置文件
- `config` - 管理 CI/CD 配置
- `get` - 获取管道的 JSON 数据
- `run-trig` - 触发管道执行