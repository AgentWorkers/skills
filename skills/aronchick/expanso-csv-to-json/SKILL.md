# csv-to-json

**功能描述：**  
将 CSV 数据转换为 JSON 格式的对象数组。

## 使用要求：  
- 确保已安装 Expanso Edge（`expanso-edge` 可执行文件必须在系统的 PATH 环境变量中）。  
- 安装方法：`clawhub install expanso-edge`

## 使用方式：  
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
expanso-cli job deploy https://skills.expanso.io/csv-to-json/pipeline-cli.yaml
```

## 相关文件：  
| 文件名 | 用途 |  
|------|---------|  
| `skill.yaml` | 技能元数据（输入参数、输出结果、认证信息） |  
| `pipeline-cli.yaml` | 独立的命令行管道配置文件 |  
| `pipeline-mcp.yaml` | MCP 服务器上的管道配置文件 |