# pii-redact

“从文本中删除个人身份信息（PII），并将敏感数据替换为占位符”

## 要求

- 已安装 Expanso Edge（`expanso-edge` 可执行文件需添加到 PATH 环境变量中）  
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行接口（CLI）流程  
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP（Master Control Panel）流程  
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud  
```bash
expanso-cli job deploy https://skills.expanso.io/pii-redact/pipeline-cli.yaml
```

## 文件说明

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行接口（CLI）流程文件 |
| `pipeline-mcp.yaml` | MCP 服务器相关的流程文件 |