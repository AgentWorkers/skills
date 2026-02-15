---
name: n2-stitch-mcp
description: 适用于 Google Stitch 的弹性 MCP 代理——具备三层安全防护机制（自动重试、令牌刷新、TCP 连接中断恢复功能）。
homepage: https://nton2.com
user-invocable: true
---

# 🛡️ N2 Stitch MCP — 弹性代理技能  
再也不用担心屏幕生成失败的问题了。这是唯一一款具备**TCP连接恢复**功能的Stitch MCP代理。  

## 问题所在  
Google Stitch的`generate_screen_from_text`方法需要**2到10分钟**来完成屏幕生成，但API在大约60秒后就会**断开TCP连接**。  

```
Other MCP servers:  Request → 60s → TCP drop → ❌ LOST!
N2 Stitch MCP:      Request → 60s → TCP drop → 🛡️ Auto-recovery → ✅ Delivered!
```  

## 为什么选择N2 Stitch MCP？  
| 特性 | 其他代理 | N2 Stitch MCP |
|---------|---------:|:---------:|
| TCP连接恢复 | ❌ | ✅ 自动重连机制 |
| 生成过程监控 | ❌ | ✅ 提供`generation_status`状态信息 |
| 指数级重试策略 | ❌ | ✅ 三次重试机制并加入随机延迟 |
| 自动刷新令牌 | ⚠️ | ✅ 在后台自动刷新令牌 |
| 测试套件 | ❌ | ✅ 包含35项测试用例 |

## 快速设置  
### 1. 验证身份（仅一次）  
```bash
# Option A: gcloud (recommended)
gcloud auth application-default login

# Option B: API Key
export STITCH_API_KEY="your-key"
```  

### 2. 将代理添加到MCP配置中  
```json
{
  "mcpServers": {
    "n2-stitch": {
      "command": "npx",
      "args": ["-y", "n2-stitch-mcp"]
    }
  }
}
```  

## 可用工具  
### Stitch API（自动检测）  
- **create_project**：创建Stitch项目  
- **list_projects**：列出所有项目  
- **get_project**：获取项目详情  
- **list_screens**：列出项目中的所有屏幕  
- **get_screen**：获取屏幕的HTML/CSS代码  
- **generate_screen_from_text**：✨ 从文本生成UI（具有弹性恢复机制）  
- **edit_screens**：编辑现有屏幕  
- **generate_variants**：生成设计变体  

### N2专有虚拟工具  
- **generation_status**：实时监控生成进度  
- **list_generations**：列出所有已生成的屏幕版本  

## 链接  
- NPM仓库：https://www.npmjs.com/package/n2-stitch-mcp  
- GitHub仓库：https://github.com/choihyunsus/n2-stitch-mcp  
- 官网：https://nton2.com  

---
*属于N2 AI系列产品——为AI系统构建基础功能*