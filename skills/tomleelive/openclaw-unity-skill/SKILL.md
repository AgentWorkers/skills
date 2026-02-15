---
name: unity-plugin
version: 1.6.1
description: 通过 OpenClaw Unity 插件来控制 Unity 编辑器。该插件可用于 Unity 游戏开发任务，包括场景管理、游戏对象/组件的操作、调试、输入模拟以及播放模式的控制。它会在与 Unity 相关的操作被触发时执行相应的功能，例如检查场景、创建对象、截图、测试游戏玩法或控制编辑器。
homepage: https://github.com/TomLeeLive/openclaw-unity-skill
author: Tom Jaejoon Lee
disableModelInvocation: true
---

# Unity 插件技能

通过 **约100个内置工具** 控制 Unity 编辑器。该插件在编辑器和播放模式下均可用。

## 连接方式

### 1. OpenClaw Gateway（远程）
适用于 Telegram、Discord 及其他 OpenClaw 频道：
- 在打开 Unity 时自动连接
- 配置方式：窗口 → OpenClaw 插件 → 设置

### 2. MCP Bridge（本地）
适用于 Claude Code、Cursor 及其他本地 AI 工具：
- 启动方式：窗口 → OpenClaw 插件 → MCP Bridge → 启动
- 默认端口：27182
- 在 Claude Code 中添加配置：`claude mcp add unity -- node <path>/MCP~/index.js`

## 首次设置

如果 `unity_execute` 工具不可用，请安装 gateway 扩展程序：

```bash
# From skill directory
./scripts/install-extension.sh

# Restart gateway
openclaw gateway restart
```

扩展程序文件位于 `extension/` 目录中。

### install-extension.sh 的作用

```bash
# 1. Copies extension files from skill to gateway
#    Source: <skill>/extension/
#    Destination: ~/.openclaw/extensions/unity/

# 2. Files installed:
#    - index.ts     # Extension entry point (HTTP handlers, tools)
#    - package.json # Extension metadata

# After installation, restart gateway to load the extension.
```

## 🔐 安全性

此插件默认设置为 `disableModelInvocation: true`，这意味着 AI 不会自动调用工具，仅执行用户明确请求的操作。
有关设置更改的详细信息，请参阅 [README.md](README.md)。

## 快速参考

### 核心工具

| 类别 | 关键工具 |
|----------|-----------|
| **场景** | `scene.active`, `scene getData`, `scene.load`, `scene.open`, `scene.save` |
| **游戏对象** | `gameobject.find`, `gameobject.getAll`, `gameobject.create`, `gameobject.destroy` |
| **组件** | `component.get`, `component.set`, `component.add`, `component.remove` |
| **变换** | `transform.position`, `transform.rotation`, `transform.scale` |
| **调试** | `debug.hierarchy`, `debug.screenshot`, `console.getLogs` |
| **输入** | `input.clickUI`, `input.type`, `input.keyPress`, `input.mouseClick` |
| **编辑器** | `editor.getState`, `editor.play`, `editor.stop`, `editor.refresh` |
| **材质** | `material.create`, `material.assign`, `material.modify`, `material.getInfo` |
| **预制件** | `prefab.create`, `prefab.instantiate`, `prefab.open`, `prefab.save` |
| **资源** | `asset.find`, `asset.copy`, `asset.move`, `asset.delete` |
| **包** | `package.add`, `package.remove`, `package.list`, `package.search` |
| **测试** | `test.run`, `test.list`, `test.getResults` |

## 常见工作流程

### 1. 场景检查

```
unity_execute: debug.hierarchy {depth: 2}
unity_execute: scene.getActive
```

### 2. 查找和修改对象

```
unity_execute: gameobject.find {name: "Player"}
unity_execute: component.get {name: "Player", componentType: "Transform"}
unity_execute: transform.setPosition {name: "Player", x: 0, y: 5, z: 0}
```

### 3. UI 测试

```
unity_execute: input.clickUI {name: "PlayButton"}
unity_execute: input.type {text: "TestUser", elementName: "UsernameInput"}
unity_execute: debug.screenshot
```

### 4. 播放模式控制

```
unity_execute: editor.play              # Enter Play mode
unity_execute: editor.stop              # Exit Play mode
unity_execute: editor.getState          # Check current state
unity_execute: editor.pause             # Pause
unity_execute: editor.unpause           # Resume
```

### 5. 材质创建

```
unity_execute: material.create {name: "RedMetal", color: "#FF0000", metallic: 0.8}
unity_execute: material.assign {gameObjectName: "Player", materialPath: "Assets/Materials/RedMetal.mat"}
unity_execute: material.modify {path: "Assets/Materials/RedMetal.mat", metallic: 1.0, emission: "#FF4444"}
```

### 6. 预制件操作

```
unity_execute: prefab.create {gameObjectName: "Player", path: "Assets/Prefabs/Player.prefab"}
unity_execute: prefab.instantiate {prefabPath: "Assets/Prefabs/Player.prefab", x: 0, y: 1, z: 0}
unity_execute: prefab.open {path: "Assets/Prefabs/Player.prefab"}
unity_execute: prefab.save
unity_execute: prefab.close
```

### 7. 资源管理

```
unity_execute: asset.find {query: "Player", type: "Prefab"}
unity_execute: asset.copy {sourcePath: "Assets/Prefabs/Player.prefab", destPath: "Assets/Backup/Player.prefab"}
unity_execute: asset.move {sourcePath: "Assets/Old/Item.prefab", destPath: "Assets/New/Item.prefab"}
```

### 8. 包管理

```
unity_execute: package.list
unity_execute: package.search {query: "TextMeshPro"}
unity_execute: package.add {packageName: "com.unity.textmeshpro"}
unity_execute: package.add {gitUrl: "https://github.com/example/package.git"}
```

### 9. 测试运行

```
unity_execute: test.list {testMode: "EditMode"}
unity_execute: test.run {testMode: "EditMode", filter: "PlayerTests"}
unity_execute: test.getResults
```

### 10. 脚本执行（增强版）

```
# Debug logging
unity_execute: script.execute {code: "Debug.Log('Hello')"}

# Time manipulation
unity_execute: script.execute {code: "Time.timeScale = 0.5"}

# PlayerPrefs
unity_execute: script.execute {code: "PlayerPrefs.SetInt('score', 100)"}

# Reflection-based method calls
unity_execute: script.execute {code: "MyClass.MyMethod()"}
unity_execute: script.execute {code: "MyClass.MyStaticMethod('param1', 123)"}
```

## 工具分类（约100个工具）

### 控制台（3个工具）
- `console.getLogs` - 获取日志（可过滤类型：Log/Warning/Error）
- `console.getErrors` - 获取错误/异常日志（包含警告）
- `console.clear` - 清除日志

### 场景（7个工具）
- `scene.list` - 列出构建设置中的场景
- `scene.active` - 获取当前活动场景的信息
- `scene getData` - 获取完整的场景层次结构数据
- `scene.load` - 按名称加载场景（播放模式）
- `scene.open` - 在编辑器模式下打开场景
- `scene.save` - 保存当前活动场景（编辑器模式）
- `scene.saveAll` - 保存所有打开的场景（编辑器模式）

### 游戏对象（8个工具）
- `gameobject.find` - 按名称、标签或组件查找对象
- `gameobject.getAll` - 过滤后获取所有游戏对象
- `gameobject.create` - 创建游戏对象或基本形状（如立方体、球体等）
- `gameobject.destroy` - 删除对象
- `gameobject.delete` - 删除对象
- `gameobject getData` - 获取对象详细信息
- `gameobject.setActive` - 启用/禁用对象
- `gameobject.parent` - 更改对象在层次结构中的位置

### 变换（6个工具）
- `transform.position` - 设置世界坐标（x, y, z）
- `transform.getRotation` - 获取欧拉旋转（x, y, z）
- `transform.getScale` - 获取局部缩放比例（x, y, z）
- `transform.position` - 设置世界坐标（x, y, z）
- `transform.rotation` - 设置欧拉旋转
- `transform.scale` - 设置局部缩放比例

### 组件（5个工具）
- `component.add` - 按类型名称添加组件
- `component.remove` - 删除组件
- `component.get` - 获取组件数据/属性
- `component.set` - 设置组件字段/属性值
- `component.list` - 列出可用的组件类型

### 脚本（3个工具）
- `script.execute` - 执行代码：`Debug.Log`, `Time`, `PlayerPrefs`, **反射调用**
- `script.read` - 读取脚本文件
- `script.list` - 列出项目中的脚本

### 应用程序（4个工具）
- `app.getState` - 获取播放模式、FPS 和时间
- `app.play` - 进入/退出播放模式
- `app.pause` - 切换暂停状态
- `app.stop` - 停止播放模式

### 调试（3个工具）
- `debug.log` - 向控制台输出日志
- `debug.screenshot` - 截取屏幕截图
- `debug.hierarchy` - 以文本形式显示层次结构

### 编辑器（9个工具）
- `editor.refresh` - 刷新 AssetDatabase（会触发重新编译）
- `editor.recompile` - 请求脚本重新编译
- `editor.domainReload` - 强制重新加载域
- `editor.focusWindow` - 突出显示窗口（游戏/场景/控制台/层次结构/项目/检查器）
- `editor.listWindows` - 列出所有打开的窗口
- `editor.getState` - 获取编辑器状态
- `editor.play` - 进入播放模式
- `editor.stop` - 退出播放模式
- `editor.pause` / `editor.unpause` - 暂停/恢复播放

### 输入模拟（10个工具）
- `input.keyPress` - 按下并释放按键
- `input.keyDown` / `input.keyUp` - 按住并释放按键
- `input.type` - 在输入框中输入文本
- `input.mouseMove` - 移动光标
- `input.mouseClick` - 在指定位置点击
- `input.mouseDrag` - 拖动鼠标
- `input.mouseScroll` - 滚动鼠标滚轮
- `input.getMousePosition` - 获取鼠标位置
- `input.clickUI` - 通过名称点击 UI 元素

### 材质（5个工具） - 1.5.0 新功能
- `material.create` - 创建具有着色器、颜色、金属质感和光滑度的材质
- `material.assign` - 将材质应用于游戏对象
- `material.modify` - 修改材质属性（颜色、金属质感、发射光等）
- `material.getInfo` - 获取包含所有着色器属性的详细材质信息
- `material.list` - 过滤后列出项目中的材质

### 预制件（5个工具） - 1.5.0 新功能
- `prefab.create` - 从场景中的游戏对象创建预制件
- `prefab.instantiate` - 在场景中实例化预制件并设置位置
- `prefab.open` - 打开预制件进行编辑
- `prefab.close` - 关闭预制件编辑模式
- `prefab.save` - 保存当前编辑的预制件

### 资源（7个工具） - 1.5.0 新功能
- `asset.find` - 按查询、类型或文件夹搜索资源
- `asset.copy` - 将资源复制到新路径
- `asset.move` - 移动/重命名资源
- `asset.delete` - 删除资源（提供删除选项）
- `asset.refresh` - 刷新 AssetDatabase
- `asset.import` - 导入/重新导入特定资源
- `asset.getPath` - 通过名称获取资源路径

### 包管理器（4个工具） - 1.5.0 新功能
- `package.add` - 按名称或 git URL 安装包
- `package.remove` - 删除已安装的包
- `package.list` - 列出已安装的包
- `package.search` - 在 Unity 包注册表中搜索包

### 测试运行器（3个工具） - 1.5.0 新功能
- `test.run` - 运行带有过滤条件的 EditMode/PlayMode 测试
- `test.list` - 列出可用的测试
- `test.getResults` - 获取上次测试的结果

### 批量执行（1个工具） - 1.6.0 新功能
- `batch.execute` - 一次性执行多个工具（性能提升10-100倍）
  - 使用格式：`commands`: `[tool, params]` 的数组
  - `stopOnError`：在遇到第一个错误时停止（默认值为 `false`）

### 会话（1个工具） - 1.6.0 新功能
- `session.getInfo` - 获取会话信息（项目、processId、machineName、sessionId）

### ScriptableObject（6个工具） - 1.6.0 新功能
- `scriptableobject.create` - 创建新的 ScriptableObject 资源
- `scriptableobject.load` - 加载并检查 ScriptableObject 的字段
- `scriptableobject.save` - 保存 ScriptableObject 的更改
- `scriptableobject.field` - 获取特定字段的值
- `scriptableobject.setField` - 设置字段值并自动保存
- `scriptableobject.list` - 列出项目中的 ScriptableObject

### 着色器（3个工具） - 1.6.0 新功能
- `shader.list` - 列出项目中的着色器
- `shader.getInfo` - 获取着色器的属性和信息
- `shader.getKeywords` - 获取着色器的关键字

### 纹理（5个工具） - 1.6.0 新功能
- `texture.create` - 创建具有填充颜色的新纹理
- `texture.getInfo` - 获取纹理信息（大小、格式、导入设置）
- `texture.setPixels` - 用颜色填充区域
- `texture.resize` - 根据导入设置调整纹理大小
- `texture.list` - 列出项目中的纹理

## 自定义工具 API - 1.6.0

注册项目特定的工具：

```csharp
OpenClawCustomTools.Register(
    "mygame.getScore",
    "Get current score",
    (args) => new { success = true, score = GameManager.Score }
);
```

## MCP 资源 - 1.6.0

通过 MCP 资源 URI 访问 Unity 数据：

| URI | 描述 |
|-----|-------------|
| `unity://scene/hierarchy` | 场景层次结构 |
| `unity://scene/active` | 当前活动场景的信息 |
| `unity://project/scripts` | 脚本列表 |
| `unity://project/scenes` | 场景列表 |
| `unity://editor/state` | 编辑器状态 |
| `unity://console/logs` | 控制台日志 |
| `unity://session/info` | 会话信息 |

## 提示

### 截图模式
- **播放模式**：`ScreenCapture` - 包含所有 UI 覆盖层
- **编辑器模式**：`Camera.main.Render()` - 不包含 UI 覆盖层
- 使用 `{method: "camera"}` 仅捕获相机画面

### 查找对象

```
gameobject.find {name: "Player"}           # By exact name
gameobject.find {tag: "Enemy"}             # By tag
gameobject.find {componentType: "Camera"}  # By component
gameobject.getAll {activeOnly: true}       # All active objects
```

### 脚本重新编译
代码更改后 Unity 可能不会自动重新编译。请使用以下方法：
```
editor.refresh    # Full asset refresh + recompile
```

### 播放模式切换
- 该插件可以在播放模式切换时保持状态（通过 SessionState 实现）
- 如果连接丢失，请等待自动重新连接，或通过窗口 → OpenClaw 插件 → 设置 → 连接来重新连接

### MCP Bridge 使用方法
对于 Claude Code / Cursor 的集成：
1. 启动方式：窗口 → OpenClaw 插件 → MCP Bridge → 启动
2. 注册：`claude mcp add unity -- node /path/to/MCP~/index.js`
3. 验证：`curl http://127.0.0.1:27182/status`

### 输入模拟限制
键盘/鼠标模拟适用于 **UI 操作**，但不适用于 `Input.GetKey()`。对于游戏测试：
- 使用 `transform.position` 直接移动对象
- 或者迁移到 Unity 的 **新输入系统**

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 工具超时 | 检查 Unity 是否响应，尝试使用 `editor.getState` |
| Gateway 无法连接 | 检查窗口 → OpenClaw 插件 → 设置 |
| MCP 无法连接 | 启动 MCP Bridge，并确认端口 27182 是否开放 |
| 脚本未更新 | 使用 `editor.refresh` 强制重新编译 |
- 截图显示不正确 | 使用播放模式获取包含 UI 的游戏画面 |
- MCP 504 超时 | Unity 正在运行或 MCP Bridge 未启动 |
- 无法找到测试运行器 | 安装 `com.unity.test-framework` 包

## 链接

- **技能仓库:** https://github.com/TomLeeLive/openclaw-unity-skill
- **插件仓库:** https://github.com/TomLeeLive/openclaw-unity-plugin
- **OpenClaw 文档:** https://docs.openclaw.ai
- **MCP 设置指南:** 请参阅插件仓库 → Documentation~/SETUP_GUIDE.md

## 许可证

MIT 许可证 - 详见 LICENSE 文件