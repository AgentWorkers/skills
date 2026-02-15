# Feishu Whiteboard Skill

该技能允许通过编程方式创建和操作 Feishu Whiteboards。

## 配置要求
需要环境变量或 `config.json` 文件中包含 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。
所需权限：`board:whiteboard:node:create`

## 使用方法

### 创建白板
```bash
node skills/feishu-whiteboard/create.js "My Architecture Diagram"
```
输出：包含 `whiteboard_id` 的 JSON 数据。

### 添加节点（示例）
```bash
node skills/feishu-whiteboard/draw.js <whiteboard_id> demo
```
添加一个矩形和一个圆形，并用一条线将它们连接起来。

### 编程使用方法
```javascript
const { createWhiteboard } = require('./create');
const { addNodes, createShape, createConnector } = require('./draw');

const board = await createWhiteboard("System Design");
const nodes = [
  createShape("web", "rect", 0, 0, 200, 100, "Web Server"),
  createShape("db", "cylinder", 0, 300, 100, 100, "Database"),
  createConnector("link1", "web", "db")
];
await addNodes(board.whiteboard_id, nodes);
```

## 故障排除
如果遇到 “404 页面未找到”的错误，通常表示您的租户尚未启用 Whiteboard API，或者端点 URL 发生了变化。当前实现的端点为 `/open-apis/board/v1/whiteboards`。