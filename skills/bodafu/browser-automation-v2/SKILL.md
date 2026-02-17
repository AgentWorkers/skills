# 浏览器自动化 v2

专为 OpenClaw 设计的企业级浏览器自动化工具，具备强大的资源管理功能。

## 主要特性

- ✅ **自动清理标签页**：避免标签页过多导致的性能问题  
- ✅ **超时与重试机制**：在网络错误时采用指数级重试策略  
- ✅ **智能等待**：支持 `waitForLoadState` 和 `waitForSelector` 等等待函数  
- ✅ **并发控制**：防止多个浏览器实例之间的配置冲突  
- ✅ **结构化日志记录**：通过设置 `DEBUG=1` 可输出详细日志  
- ✅ **高度可配置**：支持通过环境变量调整超时时间、重试次数和浏览器配置  

## 相关文件

- `browser-manager.v2.js`：核心管理类  
- `search-google.js`：用于执行谷歌搜索并保存截图及 PDF 文件  
- `fetch-summary.js`：用于获取页面内容（无论是静态还是动态内容）  
- `multi-pages.js`：批量处理多个 URL  
- `fill-form.js`：根据字段名称自动填写表单  

## 使用方法

```bash
# Set environment (optional)
export BROWSER_PROFILE=openclaw
export BROWSER_TIMEOUT=30000
export BROWSER_RETRIES=2
export DEBUG=1

cd ~/.openclaw/workspace/skills/browser-automation-v2

# Search Google
node search-google.js "OpenClaw automation"

# Batch process
node multi-pages.js "https://example.com" "https://github.com"

# Fill form
node fill-form.js "https://example.com/form" '{"email":"test@xx.com"}'
```

## 集成方式

- 作为 OpenClaw 的技能进行注册：  
  ```bash
openclaw skills install ~/.openclaw/workspace/skills/browser-automation-v2
```  
- 或者直接从代理程序中调用该功能：  
  ```
run search-google.js "query"
```  

## 系统要求

- OpenClaw 版本需达到 v2026.2.15 或以上  
- 已配置浏览器配置文件（默认为 `openclaw`）  
- 确保 Gateway 服务正在运行  

## 常见问题解决方法

- **超时错误**：增加 `BROWSER_TIMEOUT` 的值  
- **配置冲突**：等待其他浏览器实例完成操作  
- **元素未找到**：使用 `snapshot --format ai` 命令进行调试  

---

*创建日期：2026-02-16*  
*版本：2.0.0*  
*许可证：MIT*