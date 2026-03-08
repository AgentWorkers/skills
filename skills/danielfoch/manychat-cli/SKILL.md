---
name: manychat-cli
summary: Agent-friendly ManyChat automation CLI with playbook support for multi-step workflows.
---

# ManyChat CLI 技能

当您需要从 OpenClaw 或其他 AI 代理中自动化执行 ManyChat 操作时，请使用此技能。

## 该技能提供的功能
- 一个位于 `/Users/danielfoch/manychat-cli/manychat_cli.py` 的本地 CLI 包装器
- 稳定的 JSON 输出和退出代码，便于自动化任务的协调与执行
- 高效的 ManyChat 命令：
  - 查找订阅者并读取其信息
  - 添加/删除标签
  - 更新自定义字段
  - 发送消息或内容
  - 创建/更新订阅者信息
  - 直接访问原始 API 端点
  - 通过 JSON 脚本执行一系列自动化步骤

## 使用要求
- 必须设置 `MANYCHAT_API_KEY` 环境变量。
- 可选：设置 `MANYCHAT_BASE_URL` 以覆盖 API 主机地址。

## 使用方法

- 验证令牌：
```bash
cd /Users/danielfoch/manychat-cli
./manychat_cli.py ping --pretty
```

- 按电子邮件查找订阅者：
```bash
./manychat_cli.py find-system --field-name email --field-value 'lead@example.com' --pretty
```

- 运行多步骤自动化脚本：
```bash
./manychat_cli.py playbook-run \
  --file /Users/danielfoch/manychat-cli/sample_playbook.json \
  --vars-json '{"email":"lead@example.com"}' \
  --pretty
```

## 文件引用
- CLI 工具：`/Users/danielfoch/manychat-cli/manychat_cli.py`
- 自动化脚本示例：`/Users/danielfoch/manychat-cli/sample_playbook.json`
- Shell 脚本示例：`/Users/danielfoch/manychat-cli/example_automation.sh`
- 详细文档：`/Users/danielfoch/manychat-cli/README.md`