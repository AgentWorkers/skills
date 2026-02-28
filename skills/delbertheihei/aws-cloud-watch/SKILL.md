---
name: aws-cloud-watch
description: 查询 AWS CloudWatch 中与 ECS/EC2/RDS 相关的指标，并生成相应的图表。
---
# AWS CloudWatch 技能

使用此技能可以获取 ECS（Elastic Container Service）、EC2（Elastic Compute Cloud）和 RDS（Relational Database Service）的 CloudWatch 指标，并返回文本摘要。

## 输入参数

推荐的输入脚本：

```
node {baseDir}/src/skill.mjs --service ecs --metric cpu --resource <cluster-name> --hours 1
```

## 环境变量

必需的环境变量（AK/AK_Secret）：
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

可选的环境变量：
- `AWS_REGION`（默认值：`us-west-2`）

## 使用方法（内部使用）

在 `{baseDir}` 目录下运行 CLI 脚本：

```
node {baseDir}/src/cli.js --service ecs --metric CPUUtilization --resource <cluster-name-or-arn> --hours 1
node {baseDir}/src/cli.js --service ecs --metric cpu --resource <cluster-name>
```

您可以在 `{baseDir}/config.json` 文件中定义指标别名（请参考 `config.example.json` 文件）。

### 支持的服务
- `ecs`（集群级别的指标）
- `ec2`
- `rds`

### 默认值
- 区域：`us-west-2`
- 时间周期：300 秒（5 分钟）
- 时间窗口：1 小时

## 注意事项
- 除非启用了 Container Insights，否则 ECS 指标为集群级别的指标。
- 如果某个指标无法获取，请返回一条明确的提示信息。
- 仅输出文本格式的结果（不生成图表）。
- 该技能使用原生的加密技术进行 SigV4 签名（不依赖 AWS SDK 或任何外部包）。