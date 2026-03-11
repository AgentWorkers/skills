# ssh-lab — 远程服务器SSH工作台

> 用于管理远程GPU服务器的结构化SSH操作工具。
> 标准化通用功能（如GPU、磁盘、进程管理），并将数据解析任务委托给大型语言模型（LLM）处理。

## 使用场景

- 用户查询GPU状态、服务器健康状况或远程进程信息
- 需要检查训练是否正在运行、磁盘是否已满、GPU是否处于空闲状态
- 在远程服务器上执行命令
- 查看远程日志文件、列出检查点
- 在本地与远程之间进行文件传输（使用rsync命令）
- 并行比较多台服务器的GPU、磁盘和进程信息
- 设置针对GPU空闲、磁盘满或进程异常的警报
- 与`ssh-lab`、`gpu status`、`server status`、`nvidia-smi`等术语相关的操作

## 安装与配置

```bash
cd /path/to/ssh-lab && npm run build
```

安装完成后，可以通过以下命令使用命令行界面（CLI）：
```bash
ssh-lab status all          # if npm link'd or installed globally
npx ssh-lab status all      # via npx
node dist/cli.js status all # direct invocation
```

该CLI会自动读取`~/.ssh/config`配置文件；对于已存在的SSH主机，无需额外配置。

## 命令列表

### 列出所有主机
```bash
ssh-lab hosts [--json]
```

### 检查服务器状态（GPU、磁盘、进程）
```bash
ssh-lab status [host|all] [--json] [--timeout ms] [--heartbeat] [--quiet]
```
返回结构化的数据：GPU利用率/显存温度、磁盘使用情况、活跃进程信息。
支持自动警报功能：当GPU空闲、磁盘使用率达到90%以上或温度超过85°C时触发警报。
`--heartbeat`选项可生成简洁的文本输出，便于集成到自动化系统中；`--quiet`选项可抑制所有警报信息（适用于定时任务）。

### 在远程服务器上执行命令
```bash
ssh-lab run <host|all> <command...> [--json] [--timeout ms]
```
支持对所有主机并行执行命令。

### 查看远程日志文件
```bash
ssh-lab tail <host> <path> [-n lines] [--json]
```
默认显示最后50行日志；当日志文件超过50KB时会自动截断。

### 列出远程目录
```bash
ssh-lab ls <host> <path> [--sort time|size|name] [--json]
```
显示目录中的文件及其大小、创建日期和权限信息，适用于查看检查点文件。

### 显示磁盘使用情况
```bash
ssh-lab df <host|all> [path] [--json]
```
显示所有文件系统的磁盘使用情况；可选地，可以通过`du -sh`命令指定特定目录进行查看。

### 文件同步（rsync）
```bash
ssh-lab sync <host> <src> <dst> [--direction up|down] [--dry-run] [--exclude pat1,pat2]
```
支持数据传输方向：`down`（从远程到本地，默认）或`up`（从本地到远程）。执行同步前请务必使用`--dry-run`选项进行测试。

### 监控文件状态（用于实时检查）
```bash
ssh-lab watch <host> <path> [-n lines] [--prev-hash hash] [--json]
```
捕获文件的当前状态和元数据；当提供`--prev-hash`参数时，会返回文件是否发生变化的提示（`changed: true/false`）。
该工具通过定时任务或心跳机制持续监控文件状态。

### 并行比较多台服务器的配置信息
```bash
ssh-lab compare <host1> <host2> [--probes gpu,disk,process] [--json]
ssh-lab compare all [--probes gpu]
ssh-lab compare GMI4 GMI5 GMI6 --probes gpu,disk
```
可以并行比较多台服务器的GPU、磁盘和进程信息。
支持设置并发任务的数量以优化数据收集效率。

### 进行故障诊断
```bash
ssh-lab doctor <host> [--json] [--timeout ms]
```
对指定主机进行连接性、系统健康状况的诊断，包括SSH可达性、认证过程和基本系统功能的检查。

### 警报管理
```bash
# List configured rules
ssh-lab alert list [--json]

# Add a rule
ssh-lab alert add <kind> <host> [--threshold N] [--process-pattern regex]

# Remove a rule
ssh-lab alert remove <rule-id>

# Evaluate alerts against live status
ssh-lab alert check [host|all] [--json] [--quiet]
```

**支持的警报类型**：`gpu_idle`（GPU空闲）、`disk_full`（磁盘满）、`process_died`（进程异常）、`ssh_unreachable`（SSH连接失败）、`oom_detected`（内存不足）、`high_temp`（温度过高）。

**使用示例**：
```bash
ssh-lab alert add disk_full all --threshold 90
ssh-lab alert add process_died GMI4 --process-pattern "torchrun|deepspeed"
ssh-lab alert check all --json
```

### 添加新的远程主机
```bash
ssh-lab add <name> <user@host> [--port N] [--tags a,b] [--notes "desc"]
```

## 输出格式

所有命令支持三种输出格式：
- **summary**（默认）：格式化后的文本，便于人类阅读
- **json**（`--json`或`-j`）：结构化的JSON格式，适用于程序化处理
- **raw**（`--raw`或`-r`）：仅输出原始命令结果

## 超时设置

各命令使用默认的超时时间；用户可以通过`--timeout`参数自定义超时时间：
- **quick**（5秒）：适用于`hosts`、`add`、`doctor`等连接性检查命令
- **standard**（15秒）：适用于`status`、`run`、`ls`、`df`、`alert`、`compare`等常规操作
- **stream**（30秒）：适用于`tail`、`watch`等实时监控命令
- **transfer**（60秒）：适用于`sync`等文件同步操作

## 架构特点

- **数据采集模块**：支持插件化设计（如GPU、磁盘、进程监控模块），可灵活收集结构化数据
- **通过子进程实现SSH连接**：利用系统自带的`ssh`命令，继承用户的SSH配置和代理设置（ProxyJump）
- **连接管理**：通过`/tmp/ssh-lab-%r@%h:%p` socket维护持久连接；自动清理无效的连接（使用`ssh -O check`命令），并在重试前删除无效文件
- **错误处理机制**：对于临时性故障，采用指数级重试策略；错误类型（如AUTH_FAILED、TIMEOUT等）会得到相应的提示
- **分层超时设置**：根据命令类型设置不同的超时时间
- **并行执行**：支持通过`withPool`函数并行处理多个主机
- **警报系统**：内置6种警报规则，支持自定义阈值
- **依赖库**：仅依赖开发依赖项（typescript、@types/node）
- **配置文件别名**：对于`~/.ssh/config`中的主机，会自动使用别名，确保代理规则（ProxyJump/Match/Include）得到正确应用

## 心跳机制集成

详细配置请参考`HEARTBEAT.md`文件：
```
- [ ] Run: ssh-lab status all --heartbeat
  Check for: GPU idle, disk >90%, processes died
- [ ] Run: ssh-lab alert check all --json
  Act on any critical firings
```

## 配置文件

自定义主机信息保存在`~/.config/ssh-lab/config.json`文件中（系统自动生成，符合XDG规范）；
系统会自动识别`~/.ssh/config`中的SSH主机。
可以通过`SSH_LAB_CONFIG`环境变量修改配置文件的路径。