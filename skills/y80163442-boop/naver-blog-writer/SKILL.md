---
name: naver-blog-writer
description: 通过 ACP 市场流程发布 Naver 博文（包括买家端的 thin-runner、加密后的数据传输以及相应的执行逻辑）。适用于以下场景：用户请求撰写或发布 Naver 博文时；在用户初次使用 ACP 时遇到 RUNNER_NOTREADY 错误时；需要一次性设置 thin-runner 并完成登录操作时；或者需要提交一篇应通过您的 ACP 服务（naver-blog-writer）进行处理的博文以执行付费服务时。
---
# Naver Blog Writer（与ACP市场平台集成）

使用此技能来实现**真正的ACP商业功能**：

1. **预检查（Preflight）**：确保本地守护进程（daemon）正常运行。
2. **异常处理**：当运行器（runner）尚未准备好时，使用`setup_url`进行恢复。
3. **一次性设置/登录**：完成运行器的初始配置。
4. **发布内容**：通过ACP提供的执行服务（付费路径）进行发布。

## 所需的运行环境配置

- **买家机器**：macOS系统，且已安装`@y80163442/naver-thin-runner`软件。
- **本地守护进程**：运行在`127.0.0.1:${LOCAL_DAEMON_PORT:-19090}`地址上。
- **付费模式**：必须配置`OPENCLAW_OFFERING_EXECUTE_URL`。

## 核心命令

### 1) 预检查（Preflight）

如果运行器尚未准备好，系统会返回相应的错误信息。

### 2) 设置运行器（One-time setup）

执行一次性的运行器配置操作。

### 3) 发布内容（Publish）

发布内容的流程如下：
- 首先执行预检查。
- 发送请求到`/v1/local/identity`以获取用户身份信息。
- 然后发送请求到`/v1/local/seal-job`以完成内容签名/验证流程。
- 最后将处理结果发送到`OPENCLAW_OFFERING_EXECUTE_URL`（推荐使用，属于付费服务路径）。
- **备用方案**：如果上述路径不可用，可直接发送请求到`/v2/jobs/dispatch-and-wait`（仅限管理员/内部使用）。

## 环境变量

请参考`references/setup.md`文件中的相关配置变量：
- `X_LOCAL_TOKEN`：用于身份验证的令牌。
- `LOCAL_DAEMON_PORT`：本地守护进程的端口号（默认为19090）。
- `OPENCLAW_OFFERING_ID`：Naver Blog Writer服务的唯一标识符。
- `OPENCLAW_OFFERING_EXECUTE_URL`：用于执行发布操作的URL（付费路径必需）。
- `PROOF_TOKEN`、`SETUP_ISSUE_URL`：用于处理自动配置相关的问题。

## 安全注意事项

- **切勿泄露真实令牌或密钥**。
- 仅将`ACP_ADMIN_API_KEY`用于内部调试目的。
- 对于正式的商业交易和计费操作，请务必使用官方的发布服务路径（而非备用方案）。

## 参考文档

- `references/setup.md`：配置指南。
- `references/ops-checklist.md`：操作检查清单。