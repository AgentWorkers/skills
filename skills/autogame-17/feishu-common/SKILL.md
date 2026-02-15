# feishu-common 技能

## 描述
这是一个用于 OpenClaw Feishu 技能的共享认证和 API 辅助工具。它提供了以下功能：
- 获取租户令牌并将其缓存
- 处理重试和超时机制
- 提供带有令牌刷新功能的认证请求封装层

## 安装要求
在安装或运行依赖的 Feishu 技能之前，请先安装此技能。

## 使用方法
依赖的技能应从 `feishu-common` 中导入相关模块：

```javascript
const { getToken, fetchWithRetry, fetchWithAuth } = require("../feishu-common/index.js");
```

此外，还提供了兼容性别名：

```javascript
const { getToken, fetchWithAuth } = require("../feishu-common/feishu-client.js");
```

## 文件结构
- `index.js`：主要实现代码。
- `feishu-client.js`：`index.js` 的兼容性别名。