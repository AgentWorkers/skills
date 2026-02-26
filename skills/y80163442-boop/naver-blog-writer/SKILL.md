# Naver Blog Writer 技能包（MVP）

此技能包在 OpenClaw/Virtual ACP 环境中标准化了以下工作流程：

- `preflight`（预检查）：执行本地守护进程（local daemon）的操作。
- 如果失败，则返回 `RUNNER_NOT_READY` 并提示用户使用 `setup_url`。
- 执行 `setupRunner` 命令。
- 用户需要登录一次。
- 最后执行 `publish` 操作以发布内容。

## 配置参数

- `OPENCLAW_OFFERING_ID`：默认值为 `naver-blog-writer`。
- `X_LOCAL_TOKEN`：用于本地守护进程身份验证的令牌（`preflight` 和 `publish` 操作必需）。
- **自动生成 `setup_url` 的模式**：需要 `PROOF_TOKEN` 和 `SETUP_ISSUE_URL`。
- **预先生成 `setup_url` 的模式**：如果使用 `SETUP_URL`，则可以跳过验证步骤。
- `LOCAL_DAEMON_PORT`：默认值为 `19090`。
- 如果未指定 `DEVICE_FINGERPRINT`，系统会自动生成 `hostname-platform-arch`。

执行 `publish` 操作时，必须使用以下两种路径之一：

1. **通过 OpenClaw 服务执行的路径**：`OPENCLAW_OFFERING_EXECUTE_URL`（如需要，还需提供 `OPENCLAW_CORE_API_KEY`）。
2. **直接调度的备用路径**：`CONTROL_PLANE_URL` + `ACP_ADMIN_API_KEY`。

## 工具

### 1) preflight（预检查）

```bash
tools/preflight \
  --proof-token "$PROOF_TOKEN" \
  --setup-issue-url "$SETUP_ISSUE_URL" \
  --local-daemon-port 19090 \
  --x-local-token "$X_LOCAL_TOKEN"
```

如果操作成功，将返回用户的本地身份信息（local identity）的 JSON 数据。
如果失败，必须返回以下标准错误信息。

```json
{
  "error": "RUNNER_NOT_READY",
  "setup_url": "https://...",
  "next_action": "RUN_SETUP"
}
```

### 2) setupRunner

```bash
tools/setup_runner \
  --proof-token "$PROOF_TOKEN" \
  --setup-issue-url "$SETUP_ISSUE_URL" \
  --auto-service both
```

执行完成后，用户需要登录一次。

```bash
npx @y80163442/naver-thin-runner login
```

**运行模式**：
- **常驻模式（持续运行）**：使用命令 `npx @y80163442/naver-thin-runner start`。
- **按请求触发模式**：使用命令 `npx @y80163442/naver-thin-runner start --once`。

### 3) publish（发布内容）

```bash
tools/publish --title "제목" --body "본문" --tags "tag1,tag2"
```

操作流程如下：
1. 执行预检查（preflight）。
2. 调用 `/v1/local/identity` 接口。
3. 调用 `/v1/local/seal-job` 接口。
4. 根据需求，通过 OpenClaw 服务执行发布操作（offering execute）或使用直接调度机制（direct dispatch fallback）。

## 注意事项

- **主要支持的操作系统**：macOS。
- 该技能包依赖于可以在本地主机上访问并运行本地守护进程（local daemon）的环境。
- 如果 `start` 命令无法正常终止，说明系统运行正常。
- 如果需要每次请求都触发 OpenClaw/ACP 代理的执行，建议使用 `start --once` 命令。