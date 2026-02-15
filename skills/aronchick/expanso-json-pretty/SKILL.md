# json-pretty

**功能：** 以美观的格式（包含缩进）输出 JSON 数据。

## 系统要求

- 必须安装了 Expanso Edge 插件（确保 `expanso-edge` 可执行文件已添加到系统的 PATH 环境变量中）。
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行（CLI）管道
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP（Management Console）管道
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud
```bash
expanso-cli job deploy https://skills.expanso.io/json-pretty/pipeline-cli.yaml
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行管道配置文件 |
| `pipeline-mcp.yaml` | MCP 服务器相关的管道配置文件 |