# tls-inspect

用于检查TLS证书（有效期、SANs、证书链以及使用的加密算法）

## 必备条件

- 已安装Expanso Edge（`expanso-edge`二进制文件需添加到PATH环境变量中）
- 安装方法：`clawhub install expanso-edge`

## 使用方法

### 命令行管道（CLI Pipeline）
```bash
# Run standalone
echo '<input>' | expanso-edge run pipeline-cli.yaml
```

### MCP管道（MCP Pipeline）
```bash
# Start as MCP server
expanso-edge run pipeline-mcp.yaml
```

### 部署到Expanso Cloud
```bash
expanso-cli job deploy https://skills.expanso.io/tls-inspect/pipeline-cli.yaml
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |
| `pipeline-cli.yaml` | 独立的命令行管道配置文件 |
| `pipeline-mcp.yaml` | MCP服务器相关的管道配置文件 |