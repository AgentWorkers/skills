# OpenClaw Unreal 技能

通过 OpenClaw AI 助手控制 Unreal 编辑器。

## 概述

该技能通过 OpenClaw Unreal 插件实现 AI 辅助的 Unreal Engine 开发。该插件通过 HTTP 轮询（`/unreal/*` 端点）与 OpenClaw Gateway 进行通信。

## 架构

```
┌──────────────────┐     HTTP      ┌─────────────────────┐
│  OpenClaw        │ ←──────────→  │  Unreal Editor      │
│  Gateway:18789   │  /unreal/*    │  (C++ Plugin)       │
└──────────────────┘               └─────────────────────┘
         ↑
         │ Extension
┌──────────────────┐
│  extension/      │
│  index.ts        │
└──────────────────┘
```

## 先决条件

1. 拥有 Unreal Engine 5.x 项目
2. 项目中已安装 OpenClaw Unreal 插件
3. OpenClaw Gateway 正在运行（默认端口：18789）

## 安装

### 插件安装

1. 将 `openclaw-unreal-plugin` 文件夹复制到项目的 `Plugins` 目录中
2. 重启 Unreal 编辑器
3. 在“编辑”（Edit）→“插件”（Plugins）→“OpenClaw”中启用该插件
4. 打开“窗口”（Window）→“OpenClaw”以查看连接状态

### 技能安装

```bash
# Copy skill to OpenClaw workspace
cp -r openclaw-unreal-skill ~/.openclaw/workspace/skills/unreal-plugin
```

## 可用工具

### 级别管理
- `level.current` - 获取当前关卡信息
- `level.list` - 列出所有关卡
- `level.open` - 通过路径打开关卡
- `level.save` - 保存当前关卡

### 角色操作
- `actor.find` - 通过名称查找角色
- `actor.getAll` - 获取所有角色
- `actor.create` - 创建新角色（立方体、点光源、相机等）
- `actor.delete` / `actor.destroy` - 删除角色
- `actor.getData` - 获取角色详细信息
- `actor.setProperty` - 修改角色属性

### 变换（Transform）
- `transform.position` / `setPosition` - 设置/获取角色位置
- `transform.getRotation` / `setRotation` - 设置/获取角色旋转
- `transform.getScale` / `setScale` - 设置/获取角色缩放

### 组件（Component）
- `component.get` - 获取角色组件
- `component.add` - 添加组件
- `component.remove` - 删除组件

### 编辑器控制
- `editor.play` - 开始 PIE（在编辑器中播放）
- `editor.stop` - 停止 PIE
- `editor.pause` / `resume` - 暂停/恢复游戏播放
- `editor.getState` - 检查是否正在播放或编辑

### 调试
- `debug.hierarchy` - 世界层次结构树
- `debug.screenshot` - 捕获视图窗口截图
- `debug.log` - 输出日志信息

### 输入模拟
- `input.simulateKey` - 模拟键盘输入（W、A、S、D、空格键等）
- `input.simulateMouse` - 模拟鼠标点击/移动/滚动
- `input.simulateAxis` - 模拟游戏手柄/轴输入

### 资产（Assets）
- `asset.list` - 浏览资源浏览器
- `asset.import` - 导入外部资源

### 控制台（Console）
- `console.execute` - 运行控制台命令
- `console.getLogs` - 获取输出日志信息

### 蓝图（Blueprint）
- `blueprint.list` - 列出项目中的蓝图
- `blueprint.open` - 在编辑器中打开蓝图

## 示例用法

```
User: Create a cube at position (100, 200, 50)
AI: [Uses unreal_execute tool="actor.create" parameters={type:"Cube", x:100, y:200, z:50}]

User: Move the player start to the center
AI: [Uses unreal_execute tool="actor.find" parameters={name:"PlayerStart"}]
    [Uses unreal_execute tool="transform.setPosition" parameters={name:"PlayerStart", x:0, y:0, z:0}]

User: Take a screenshot
AI: [Uses unreal_execute tool="debug.screenshot"]

User: Start the game
AI: [Uses unreal_execute tool="editor.play"]
```

## 配置

在项目根目录下创建 `openclaw.json` 文件（可选）：

```json
{
  "host": "127.0.0.1",
  "port": 18789,
  "autoConnect": true
}
```

或者将配置信息放在 `~/.openclaw/unreal-plugin.json` 文件中以实现全局配置。

## HTTP 端点

该插件在 OpenClaw Gateway 上注册了以下端点：

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/unreal/register` | POST | 注册新会话 |
| `/unreal/poll` | GET | 轮询待处理的命令 |
| `/unreal/heartbeat` | POST | 保持会话活跃 |
| `/unreal/result` | POST | 发送工具执行结果 |
| `/unreal/status` | GET | 获取所有会话的状态 |

## 故障排除

### 插件无法连接
- 检查输出日志中是否有 `[OpenClaw]` 相关信息
- 确认 Gateway 是否正在运行：`openclaw gateway status`
- 确认端口 18789 是否可访问
- 打开“窗口”→“OpenClaw”以查看连接状态

### 会话过期
- 插件会在会话过期时自动重新连接
- 确认 Gateway 是否已重新启动

### 工具无法使用
- 确保插件已启用（“编辑”→“插件”）
- 在修改角色时确保编辑器未处于 PIE 模式
- 确认角色名称完全匹配（区分大小写）

## 🔐 安全性：模型调用设置

在将数据发布到 ClawHub 时，可以配置 `disableModelInvocation`：

| 设置 | AI 自动调用 | 用户明确请求 |
|---------|---------------|----------------------|
| `false`（默认） | ✅ 允许 | ✅ 允许 |
| `true` | ❌ 禁用 | ✅ 允许 |

### 建议：**设置为 `false`**（默认值）

**原因：** 在 Unreal 开发过程中，AI 自动执行辅助任务（如检查角色层次结构、截图、检查组件等）非常有用。

**何时使用 `true`：** 对于敏感操作（如支付、删除、发送消息等）。

## 命令行接口（CLI）命令

```bash
# Check Unreal connection status
openclaw unreal status
```

## 许可证

MIT 许可证 - 详见 LICENSE 文件