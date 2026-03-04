# 可靠性证据包（Reliability Evidence Pack, REP）

这是一个全面的运行时系统，用于通过结构化的工件记录、验证和合规性报告来记录和验证代理的操作可靠性。

## 包含内容

### 核心脚本（`/scripts`）
- `rep.mjs` - 主要的命令行界面（CLI），用于初始化、验证和包管理
- `rep-validate.mjs` - 用于验证REP工件的模式验证引擎
- `rep-heartbeat-cron.mjs` - 按计划记录代理的心跳信息
- `rep-near-miss-cron.mjs` - 跟踪接近失败的可靠性事件
- `rep-performance-baseline.mjs` - 收集性能指标
- `rep-generate-bundle.mjs` - 从工件生成REP包

### CLI包（`/cli`）
- 可安装的npm包，方便通过命令行进行操作
- 请参阅`cli/README.md`以获取安装和使用说明

### GitHub Action（`/github-action`）
- 用于自动化验证的CI/CD集成
- 请参阅`github-action/README.md`以了解设置方法

### 模式（`/schemas`）
- 所有REP工件类型的JSON模式定义：
  - `decision_rejection_log.json`
  - `handoff_acceptance_packet.json`
  - `memory_reconstruction_audit.json`
  - `near_miss_reliability_trailer.json`
  - `signed_divergence_violation_record.json`

### 示例（`/examples`）
- 样本工件和工作流程
- 不同用例的集成模式

## 所需的二进制文件

- **Node.js**（v16或更高版本 - 运行时脚本所需）
- **npm**（用于安装CLI包）

无需其他系统二进制文件。

## 安装

### 选项1：直接使用脚本
```bash
# Clone or copy this bundle to your project
cp -r rep-bundle-v2 /path/to/your/project/rep
cd rep

# Make scripts executable
chmod +x scripts/*.mjs

# Test
node scripts/rep.mjs --help
```

### 选项2：使用CLI包
```bash
cd cli
npm install -g
rep --help
```

### 选项3：使用GitHub Action
```yaml
- uses: ./github-action
  with:
    bundle-path: ./rep
```

## 配置

通过设置环境变量来配置系统行为：
```bash
# Path to artifacts directory (default: ./artifacts)
REP_ARTIFACTS_PATH=./artifacts

# Path to schemas directory (default: ./schemas)  
REP_SCHEMAS_PATH=./schemas

# Log file path (optional)
REP_LOG_FILE=/var/log/rep.log
```

## 使用方法

### 初始化一个新的REP
```bash
node scripts/rep.mjs init --name "my-agent"
```

### 验证工件
```bash
node scripts/rep-validate.mjs ./artifacts --strict
```

### 运行心跳记录（定时任务）
```bash
REP_ARTIFACTS_PATH=./artifacts node scripts/rep-heartbeat-cron.mjs
```

### 设置定时任务（crontab示例）
```bash
# Add to crontab - run heartbeat every 5 minutes
*/5 * * * * cd /path/to/rep && REP_ARTIFACTS_PATH=./artifacts node scripts/rep-heartbeat-cron.mjs >> /var/log/rep-heartbeat.log 2>&1
```

## 工件类型

| 工件类型 | 用途 |
|---------|---------|
| `agent_heartbeat_record` | 代理生命周期事件 |
| `decision_rejection_log` | 决策及其结果 |
| `context_snapshot` | 内存/上下文状态 |
| `handoff_acceptance_packet` | 代理间交接验证 |
| `near_miss_reliability_trailer` | 接近失败事件 |
| `memory_reconstruction_audit` | 内存完整性检查 |
| `signed_divergence_violation_record` | 政策违规记录 |

## 安全考虑

- **凭证**：此工具不需要处理凭证
- **文件访问**：仅写入配置好的工件目录
- **定时任务**：不会修改系统的crontab设置 - 需由操作员配置
- **日志**：日志可记录到可配置的路径

## 许可证

MIT许可证

## 支持

- 文档：`SPEC.md`, `QUICKSTART.md`, `INTEGRATION.md`
- 示例：`examples/`
- 验证工具：`node scripts/rep-validate.mjs --help`

## 安全注意事项

### 敏感数据
REP会捕获可能包含敏感信息的上下文快照、决策日志和内存相关数据。
- 将`REP_ARTIFACTS_PATH`设置为受控的、隔离的目录
- 在外部共享之前，请审查或删除工件内容
- 考虑在容器中运行或使用非特权账户

### 签名密钥
规范中包含了用于验证工件完整性的签名字段，但密钥管理由操作员负责：
- **不要将私钥放在工件目录中**
- 对于生产环境，请使用外部KMS或安全保管库进行签名
- 在测试环境中，可以外部生成密钥并通过环境变量传递（未来功能）

### CI使用
GitHub Action是在您的仓库中运行的：
- 在公共CI环境中使用之前，请查看`github-action/entrypoint.sh`
- 确保没有工件泄露到外部端点
- 在CI环境中使用隔离的工件路径

### 网络行为

- 所有脚本都在本地运行
- 不会发送遥测数据或调用外部API
- 不会自动更新
- 所有文件I/O操作仅针对配置好的工件路径

### 最佳实践
1. 将工件目录与源代码分开存放
2. 将工件路径添加到`.gitignore`文件中
3. 定期轮换日志文件
4. 在外部共享之前对工件进行审计