# AOI Sandbox Shield (Lite)

S-DNA: `AOI-2026-0215-SDNA-SS02`

## 功能简介
AOI Sandbox Shield (Lite) 是一款 **公开安全版** 的工具，专注于以下功能：
- 为关键的工作区/配置文件创建快照；
- 验证 JSON 配置文件的语法及所需的关键字段；
- 生成审计日志文件，可将其附加到发布说明中。

## 注意事项（按设计原则）：
- 该工具 **不会** 应用任何配置设置；
- 该工具 **不会** 重启网关；
- 该工具 **不会** 修改 cron 任务；
- 该工具 **不会** 向外部发送任何消息。

## 命令说明
### 创建快照
```bash
node skill.js snapshot --reason="before publishing" 
```

### 验证 JSON 配置文件（语法及所需字段）
```bash
node skill.js validate-config --path="$HOME/.openclaw/openclaw.json"
```

## 输出方式
所有命令会将结果以 JSON 格式输出到标准输出（stdout），便于日志记录。

## 许可证
MIT 许可证（基于 AOI 的原始许可证）。