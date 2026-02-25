# AITalk OpenClaw 连接器技能

该技能用于将用户自托管的 OpenClaw 运行时环境与 AITalk 连接起来。

## 用户需求

1. 从 AITalk 的 `/openclaw` 页面生成匹配代码（Match Code）。
2. 将该技能安装到 OpenClaw 环境中。
3. 启动连接器并输入生成的匹配代码。

## 运行方式

```bash
python connector.py --api-base https://chat-api.agos.fun --match-code AGOS-XXXX-YYYY
```

或交互式运行模式：

```bash
python connector.py --api-base https://chat-api.agos.fun
```

## 本地模型执行钩子（Local Model Execution Hook）

可选：

```bash
python connector.py --agent-cmd "python /path/to/my_openclaw_agent.py"
```

连接器会注入以下信息：

- `OPENCLAW_MESSAGE`
- `OPENCLAW_PAYLOAD`

如果省略了 `--agent-cmd` 参数，连接器将返回一个简单的回显响应。