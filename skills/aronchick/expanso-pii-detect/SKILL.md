# pii-detect

用于检测文本中的个人身份信息（PII，Personally Identifiable Information）

## 必备条件

- 已安装 Expanso Edge；确保 `expanso-edge` 可执行文件在系统的 PATH 环境变量中。
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
expanso-cli job deploy https://skills.expanso.io/pii-detect/pipeline-cli.yaml
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的 CLI 流程配置文件 |
| `pipeline-mcp.yaml` | MCP 服务器上的流程配置文件 |