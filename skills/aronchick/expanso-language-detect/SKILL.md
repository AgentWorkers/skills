# language-detect

使用人工智能检测文本的语言

## 要求

- 已安装 Expanso Edge（`expanso-edge` 可执行文件必须在系统的 PATH 环境变量中）
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行接口（CLI）流程
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP（Machine Learning Platform）流程
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud
```bash
expanso-cli job deploy https://skills.expanso.io/language-detect/pipeline-cli.yaml
```

## 文件说明

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行接口（CLI）流程 |
| `pipeline-mcp.yaml` | MCP 服务器流程 |