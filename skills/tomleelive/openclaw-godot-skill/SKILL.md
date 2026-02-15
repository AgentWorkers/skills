---
name: godot-plugin
description: 通过 OpenClaw Godot 插件来控制 Godot 编辑器。该插件可用于 Godot 游戏开发任务，包括场景管理、节点操作、输入模拟、调试以及编辑器控制等。它会响应与 Godot 相关的请求，例如查看场景、创建节点、截图、测试游戏玩法或控制编辑器等操作。
---

# Godot插件技能

通过30个内置工具控制Godot 4.x编辑器，支持80多种节点类型。

## 首次设置

如果`godot_execute`工具不可用，请安装gateway扩展：

```bash
# From skill directory
./scripts/install-extension.sh

# Restart gateway
openclaw gateway restart
```

扩展文件位于`extension/`目录中。

## 快速参考

### 核心工具

| 类别 | 关键工具 |
|----------|-----------|
| **场景** | `scene.create`, `scene.current`, `scene.open`, `scene.save` |
| **节点** | `node.find`, `node.create`, `node.delete`, `node.getData` |
| **变换** | `transform.position`, `transform.rotation`, `transform.scale` |
| **调试** | `debug.tree`, `debug.screenshot`, `console.getLogs` |
| **输入** | `input.keyPress`, `input.mouseClick`, `input.actionPress` |
| **编辑器** | `editor.play`, `editor.stop`, `editor.getState` |

## 常见工作流程

### 1. 场景创建

使用`godot_execute`工具：
- `godot_execute/tool="scene.create", parameters={rootType: "Node2D", name: "Level1"})`
- `godot_execute/tool="node.create", parameters={type: "CharacterBody2D", name: "Player"})`
- `godot_execute/tool="scene.save")`

### 2. 查找和修改节点

- `godot_execute/tool="node.find", parameters={name: "Player"})`
- `godot_execute/tool="node getData", parameters={path: "Player"})`
- `godot_execute/tool="transform.position", parameters={path: "Player", x: 100, y: 200})`

### 3. 使用输入进行游戏测试

- `godot_execute/tool="editor.play")`
- `godot_execute/tool="input.keyPress", parameters={key: "W"})`
- `godot_execute/tool="input.actionPress", parameters={action: "jump"})`
- `godot_execute/tool="debug.screenshot")`
- `godot_execute/tool="editor.stop")`

### 4. 检查日志

- `godot_execute/tool="console.getLogs", parameters={limit: 50})`
- `godot_execute/tool="console.getLogs", parameters={type: "error", limit: 20})`

## 工具类别

### 控制台（2个工具）
- `console.getLogs` - 从Godot日志文件中获取日志（`limit: 100`, `type: "error" | "warning" | ""`）
- `console.clear` - 占位符（日志无法通过编程方式清除）

### 场景（5个工具）
- `scene.current` - 获取当前场景信息
- `scene.list` - 列出所有.tscn/.scn文件
- `scene.open` - 按路径打开场景
- `scene.save` - 保存当前场景
- `scene.create` - 创建新场景（`rootType: "Node2D" | "Node3D" | "Control", name: "SceneName"`）

### 节点（6个工具）
- `node.find` - 按名称、类型或组查找节点
- `node.create` - 创建节点（支持80多种类型，如CSGBox3D、MeshInstance3D、ColorRect等）
- `node.delete` - 按路径删除节点
- `node getData` - 获取节点信息、子节点及变换信息
- `node.getProperty` - 获取属性值
- `node.setProperty` - 设置属性值（Vector2/3会自动转换）

### 变换（3个工具）
- `transform.position` - 设置位置（`x, y`）或（`x, y, z`）
- `transform.rotation` - 设置旋转角度
- `transform.scale` - 设置缩放比例

### 编辑器（4个工具）
- `editor.play` - 播放当前场景或自定义场景
- `editor.stop` - 停止播放
- `editor.pause` - 切换暂停状态
- `editor.getState` - 获取播放状态、版本及项目名称

### 调试（3个工具）
- `debug.screenshot` - 截取视图窗口截图
- `debug.tree` - 以文本形式显示场景树结构
- `debug.log` - 打印消息

### 输入（7个工具） - 用于游戏测试
- `input.keyPress` - 按下并释放按键（`key: "W"`）
- `input.keyDown` - 按住按键
- `input.keyUp` - 释放按键
- `input.mouseClick` - 在指定位置点击鼠标（`x, y`, `button: "left" | "right" | "middle"`）
- `input.mouseMove` - 将鼠标移动到指定位置（`x, y`）
- `input.actionPress` - 执行输入操作（`action: "jump"`）
- `input.actionRelease` - 释放输入操作

### 脚本（2个工具）
- `script.list` - 列出所有.gd脚本文件
- `script.read` - 读取脚本内容

### 资源（1个工具）
- `resource.list` - 按扩展名列出所有资源文件

## 支持的输入键

```
A-Z, 0-9, SPACE, ENTER, ESCAPE, TAB, BACKSPACE, DELETE
UP, DOWN, LEFT, RIGHT
SHIFT, CTRL, ALT
F1-F12
```

## 可创建的节点类型

| 类型 | 描述 |
|------|-------------|
| `Node2D` | 2D空间节点 |
| `Node3D` | 3D空间节点 |
| `Sprite2D` | 2D精灵 |
| `CharacterBody2D` | 2D角色 |
| `CharacterBody3D` | 3D角色 |
| `RigidBody2D/3D` | 物理体 |
| `Area2D/3D` | 触发区域 |
| `Camera2D/3D` | 相机 |
| `Label`, `Button` | 用户界面元素 |

## 提示

### 输入模拟
- 仅在**播放模式**下有效
- 使用`input.actionPress`执行映射的操作（来自输入映射）
- 使用`input.keyPress`进行直接按键模拟

### 查找节点
```
node.find {name: "Player"}      # By name substring
node.find {type: "Sprite2D"}    # By exact type
node.find {group: "enemies"}    # By group
```

### 向量属性
`node.setProperty`会自动将字典转换为`Vector2`或`Vector3`类型：
```
{path: "Cam", property: "zoom", value: {x: 2, y: 2}}  # → Vector2(2, 2)
```

### 控制台日志
```
console.getLogs {limit: 50}           # Last 50 lines
console.getLogs {type: "error"}       # Errors only
console.getLogs {type: "warning"}     # Warnings only
```

## 🔐 安全性：模型调用设置

在将项目发布到ClawHub时，可以配置`disableModelInvocation`：

| 设置 | AI自动调用 | 用户明确请求 |
|---------|---------------|----------------------|
| `false`（默认值） | ✅ 允许 | ✅ 允许 |
| `true` | ❌ 禁用 | ✅ 允许 |

### 建议：**设置为`true`**

**原因：**在Godot开发过程中，AI自动执行辅助任务（如检查场景树、截图和检查节点）非常有用。

**何时使用`true`：**对于涉及敏感操作的工具（如支付、删除、发送消息等）。