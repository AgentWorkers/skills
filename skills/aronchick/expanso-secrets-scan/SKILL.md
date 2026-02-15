# secrets-scan

用于检测文本或代码中硬编码的敏感信息（如 API 密钥、令牌、密码等）

## 必备条件

- 已安装 Expanso Edge 插件（确保 `expanso-edge` 可执行文件在系统的 PATH 环境变量中）  
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行界面（CLI）流程  
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP（Microservices Cluster Platform）流程  
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到 Expanso Cloud  
```bash
expanso-cli job deploy https://skills.expanso.io/secrets-scan/pipeline-cli.yaml
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的 CLI 流程配置文件 |
| `pipeline-mcp.yaml` | MCP 服务器上的流程配置文件 |