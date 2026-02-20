---
name: jenkins
description: 通过 REST API 与 Jenkins CI/CD 服务器进行交互。当您需要触发构建、检查构建状态、查看控制台输出、管理作业或监控 Jenkins 节点及队列时，可以使用该功能。支持通过环境变量将应用程序部署到不同的 Jenkins 实例。
---
# Jenkins

通过 REST API 与 Jenkins CI/CD 服务器进行交互。

## 所需的环境变量

- `JENKINS_URL`（示例：`https://jenkins.example.com`）
- `JENKINS_USER`（您的 Jenkins 用户名）
- `JENKINS_API_TOKEN`（从 Jenkins 用户设置中获取的 API 令牌）

## 列出所有作业

```bash
node {baseDir}/scripts/jenkins.mjs jobs
node {baseDir}/scripts/jenkins.mjs jobs --pattern "deploy-*"
```

## 触发构建

```bash
node {baseDir}/scripts/jenkins.mjs build --job "my-job"
node {baseDir}/scripts/jenkins.mjs build --job "my-job" --params '{"BRANCH":"main","ENV":"dev"}'
```

## 检查构建状态

```bash
node {baseDir}/scripts/jenkins.mjs status --job "my-job"
node {baseDir}/scripts/jenkins.mjs status --job "my-job" --build 123
node {baseDir}/scripts/jenkins.mjs status --job "my-job" --last
```

## 查看控制台输出

```bash
node {baseDir}/scripts/jenkins.mjs console --job "my-job" --build 123
node {baseDir}/scripts/jenkins.mjs console --job "my-job" --last --tail 50
```

## 停止构建

```bash
node {baseDir}/scripts/jenkins.mjs stop --job "my-job" --build 123
```

## 查看队列中的作业

```bash
node {baseDir}/scripts/jenkins.mjs queue
```

## 查看节点信息

```bash
node {baseDir}/scripts/jenkins.mjs nodes
```

## 注意事项

- URL 和凭据被设计为可跨环境使用的变量。
- API 响应以 JSON 格式返回。
- 对于需要参数化的构建，请使用 `--params` 参数，并传入 JSON 字符串。