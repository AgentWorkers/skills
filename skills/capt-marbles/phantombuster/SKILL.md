---
name: phantombuster
description: 通过 API 控制 PhantomBuster 自动化代理。可以列出代理、启动自动化任务、获取输出结果、检查代理状态以及中止正在运行的代理。适用于用户需要执行 LinkedIn 数据抓取、Twitter 自动化操作、潜在客户生成任务或任何 PhantomBuster 工作流程的场景。
version: 1.0.0
author: captmarbles
---

# PhantomBuster 技能

您可以通过命令行来控制您的 [PhantomBuster](https://phantombuster.com) 自动化代理。

## 设置

1. 从 [工作区设置](https://phantombuster.com/workspace-settings) 获取您的 API 密钥。
2. 设置环境变量：
   ```bash
   export PHANTOMBUSTER_API_KEY=your-api-key-here
   ```

## 使用方法

所有命令都使用该技能目录中提供的 `pb.py` 脚本。

### 列出代理

查看所有已配置的 PhantomBuster 代理。

```bash
python3 pb.py list
python3 pb.py list --json  # JSON output
```

### 启动代理

根据代理的 ID 或名称来启动一个代理。

```bash
python3 pb.py launch <agent-id>
python3 pb.py launch <agent-id> --argument '{"search": "CEO fintech"}'
```

### 获取代理输出

获取最近一次运行代理的结果。

```bash
python3 pb.py output <agent-id>
python3 pb.py output <agent-id> --json  # Raw JSON
```

### 检查代理状态

查看代理是正在运行、已完成还是出现了错误。

```bash
python3 pb.py status <agent-id>
```

### 中止正在运行的代理

停止当前正在运行的代理。

```bash
python3 pb.py abort <agent-id>
```

### 获取代理详细信息

获取特定代理的完整详细信息。

```bash
python3 pb.py get <agent-id>
```

### 下载结果数据

从代理的最新运行中下载实际的结果数据（CSV 格式）。

```bash
python3 pb.py fetch-result <agent-id>
python3 pb.py fetch-result <agent-id> > output.csv
```

该命令会从代理的 S3 存储中下载 `result.csv` 文件，非常适合将 PhantomBuster 的数据集成到您的工作流程中。

## 示例命令

- *"列出我的 PhantomBuster 代理"
- *"启动我的 LinkedIn Sales Navigator 抓取器"
- *"获取代理 12345 的输出"
- *"检查我的 Twitter 关注者抓取器是否仍在运行"
- *"中止当前正在运行的代理"

## 常见自动化任务

PhantomBuster 提供了许多预先构建的自动化任务：
- **LinkedIn Sales Navigator 搜索** — 从搜索结果中提取潜在客户信息
- **LinkedIn 个人资料抓取器** — 获取个人资料数据
- **Twitter 关注者收集器** — 抓取 Twitter 关注者信息
- **Instagram 个人资料抓取器** — 获取 Instagram 个人资料数据
- **Google 地图搜索导出** — 提取商家信息

## 访问限制

PhantomBuster 的执行时间受到您所选计划的限制。API 本身没有严格的访问限制，但代理的执行会消耗您计划中的时间。