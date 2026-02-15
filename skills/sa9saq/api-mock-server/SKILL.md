---
description: 根据 OpenAPI/Swagger 规范启动模拟 API 服务器，并自动生成测试数据。
---

# API模拟服务器

能够根据OpenAPI/Swagger规范立即创建一个模拟API服务器。

## 使用说明

### 第1步：获取规范
从用户处获取以下信息：
- 规范文件的路径（JSON或YAML格式）
- 规范的URL
- 内嵌的端点定义（需要转换为OpenAPI 3.0格式）

如果不存在规范文件，可以协助用户交互式地定义端点并自动生成规范文件。

### 第2步：启动模拟服务器
```bash
# Primary: Prism (Stoplight)
npx @stoplight/prism-cli mock <spec-file> --port ${PORT:-4010} --dynamic

# Alternative: json-server for simple REST
npx json-server --watch db.json --port ${PORT:-4010}
```
- 使用`--dynamic`选项可以根据规范中的约束生成真实的模拟数据
- 默认端点地址：4010

### 第3步：验证模拟服务器的功能
```bash
# Test a sample endpoint
curl -s http://localhost:4010/api/resource | jq .

# List all routes (Prism logs them on startup)
```

### 备用方案：自定义Express服务器
如果Prism不可用，可以生成一个简单的Express服务器：
```javascript
const express = require('express');
const app = express();
app.use(express.json());
// Auto-generate routes from spec...
```

## 注意事项

- **CORS（跨源资源共享）**：为浏览器测试添加`--cors`参数，或设置`Access-Control-Allow-Origin: *`以允许跨源请求
- **身份验证模拟**：对于需要身份验证的端点，如果没有提供令牌，则返回401错误代码
- **大型规范文件**：Prism能够顺利处理这类文件；但如果规范文件过大，可能需要使用json-server进行分片处理
- **端口冲突**：在启动服务器前使用`lsof -i :<端点地址>`命令检查端口是否已被占用

## 安全性注意事项

- 模拟服务器仅用于开发用途，切勿将其暴露在公共互联网上
- 模拟响应中不要包含真实的API密钥或认证信息

## 系统要求

- Node.js 16及以上版本（用于运行npx命令）
- 不需要API密钥