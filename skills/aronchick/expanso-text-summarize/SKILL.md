# text-summarize

使用人工智能将文本总结为3-5个要点。

## 要求

- 已安装 Expanso Edge（`expanso-edge` 可执行文件必须在系统的 PATH 环境变量中）。
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行界面（CLI）流程
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP 流程
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud
```bash
expanso-cli job deploy https://skills.expanso.io/text-summarize/pipeline-cli.yaml
```

## 文件说明

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行界面（CLI）流程配置文件 |
| `pipeline-mcp.yaml` | MCP 服务器相关流程配置文件 |