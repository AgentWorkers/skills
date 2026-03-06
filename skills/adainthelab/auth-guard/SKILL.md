---
name: auth-guard
description: **标准化API凭证处理和启动时的身份验证检查**，以防止在不同会话之间出现“凭证缺失”的问题。当代理程序频繁丢失身份验证状态、重启后出现间歇性的401/403错误、依赖临时的curl请求，或者需要为HEARTBEAT.md/AGENTS.md文件及辅助脚本实现“身份验证优先”的处理机制时，应采用此方法。
---
# 认证保护（Auth Guard）

确保认证流程的确定性：仅使用一个凭证源、一个辅助命令路径、一个启动时进行的认证检查以及一个备用策略。

## 快速工作流程：

1. 确定目标服务端点及当前出现问题的流程。
2. 定义规范的凭证来源（优先使用环境变量，其次为凭证文件）。
3. 在工作区（`workspace`）中创建或更新一个辅助脚本（文件扩展名为`.pi/`），该脚本会自动执行认证操作。
4. 添加一个启动时执行的认证检查命令，以验证凭证的有效性及对端点的访问权限。
5. 更新`HEARTBEAT.md`或`AGENTS.md`文件，强制使用辅助脚本进行认证（禁止未经认证的直接调用）。
6. 为未经授权的状态明确指定备用处理方式。

## 需遵循的规则：

- 优先使用环境变量`ENV_VAR`进行配置，其次才是`~/.config/<service>/credentials.json`文件。
- 绝不要将敏感信息嵌入日志、内存记录或聊天响应中。
- 如果存在辅助脚本，切勿使用`curl`直接访问受保护的端点。
- 保持备用处理方式的明确性，并尽量减少不必要的错误信息。
- 将辅助脚本保存在工作区的`/.pi/`目录中，以便重复使用。

## 运行时要求：

- 必需安装`bash`、`curl`和`python3`工具。

在使用此功能之前，请先进行以下检查：

```bash
command -v bash curl python3 >/dev/null
```

## 安全限制：

- 默认情况下，仅允许通过`~/.config/<service>/...`路径传递可信的凭证。
- 不要将`--cred-file`参数指向任意工作区文件或无关的秘密存储位置。
- 确保探测请求的URL仅针对目标服务的认证端点。

## 启动时的认证检查流程：

在会话开始时（或在心跳检测循环之前）执行认证检查：

```bash
bash skills/auth-guard/scripts/auth_check.sh \
  --service moltbook \
  --url 'https://www.moltbook.com/api/v1/feed?sort=new&limit=1' \
  --env-var MOLTBOOK_API_KEY \
  --cred-file "$HOME/.config/moltbook/credentials.json"
```

**预期结果：**
- `AUTH_OK` → 继续执行正常的认证流程。
- `AUTH MISSING` 或 `AUTH_FAIL_*` → 使用预先定义的备用路径，并记录简明的错误信息。

## 可复用的代码片段：

可以从`references/snippets.md`文件中获取可复用的认证策略代码片段。

## 参考资料：

- `references/contract.md`：完整的密钥链（Keychain）契约模式。
- `references/snippets.md`：可直接使用的操作代码片段。
- `references/examples.md`：多服务环境下的使用示例（包括Moltbook、GitHub、Slack等场景）。