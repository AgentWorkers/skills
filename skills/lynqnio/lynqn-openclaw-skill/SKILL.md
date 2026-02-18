# LYNQN 技能

**支持从任何 OpenClaw 代理程序中分享文本、生成二维码以及缩短 URL。**

- **名称**: lynqn  
- **版本**: 1.0.1  
- **类别**: 生产力工具  
- **许可证**: MIT  
- **官方网站**: https://lynqn.io/agents  

## 安装  

```bash
openclaw skill install lynqn
```  

## 命令  

| 命令 | 描述 | 使用方法 |
|---------|-------------|-------|
| `/lynqn share` | 创建可分享的文本或代码片段 | `/lynqn share <文本> [--语法选项] [--有效期 1天\|1周\|1个月\|3个月]` |
| `/lynqn qr` | 从文本或 URL 生成二维码 | `/lynqn qr <内容> [--尺寸 200-800] [--错误级别 L\|M\|Q\|H]` |
| `/lynqn shorten` | 缩短长 URL | `/lynqn shorten <URL>` |
| `/lynqn stats` | 获取 LYNQN 平台统计信息 | `/lynqn stats` |

## 快速示例  

```bash
# Share text with a 1-week expiry
/lynqn share Hello from my agent!

# Share code with syntax highlighting
/lynqn share const x = 42; console.log(x); --syntax --expires 1w

# Generate a QR code
/lynqn qr https://lynqn.io --size 400 --error H

# Shorten a URL
/lynqn shorten https://example.com/very/long/path/to/resource

# Check platform stats
/lynqn stats
```  

## 配置  

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `LYNQN_API_URL` | `https://lynqn.io/api` | API 端点地址 |

## 所需权限  

- `network.http` — 允许向 LYNQN API 发送 HTTP 请求  

## 速率限制  

| 等级 | 每小时请求次数 | 有效期 | 备注 |
|------|--------------|------------|-------|
| 免费 | 100 | 90 天 | 无需令牌 |
| 专业版（10 万美元以上） | 1,000 | 180 天 | 包含分析数据 |
| 高级版（100 万美元以上） | 10,000 | 365 天 | 支持自定义二维码品牌 |

## API 端点  

### POST /api/share  
创建可分享的文本或代码片段。  

```json
{
  "content": "Your text here",
  "format": "text",
  "expiresIn": 604800
}
```  

### POST /api/shorten  
缩短 URL。  

```json
{
  "url": "https://example.com/long/path"
}
```  

### GET /api/stats  
获取平台统计信息。  

## 链接  

- 官网: https://lynqn.io  
- 代理程序文档: https://lynqn.io/agents  
- 代币经济系统: https://lynqn.io/tokenomics  
- 问题报告: https://github.com/lynqn/lynqn-openclaw-skill/issues