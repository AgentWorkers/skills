# json-flatten

用于扁平化嵌套的 JSON 对象

## 前提条件

- 已安装 Expanso Edge（`expanso-edge` 可执行文件必须在系统的 PATH 环境变量中）。
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行管道（CLI Pipeline）
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP 管道（MCP Pipeline）
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud
```bash
expanso-cli job deploy https://skills.expanso.io/json-flatten/pipeline-cli.yaml
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行管道配置文件 |
| `pipeline-mcp.yaml` | MCP 服务器管道配置文件 |