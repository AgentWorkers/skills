---
name: atl-browser
description: 通过ATL（iOS模拟器）实现移动浏览器和原生应用的自动化操作：在iPhone/iPad模拟器上执行导航、点击、截图等操作，并自动化处理网页和原生应用的相关任务。
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: ["xcrun", "xcodebuild", "curl"]
    install:
      - id: "atl-clone"
        kind: "shell"
        command: "git clone https://github.com/JordanCoin/Atl ~/Atl"
        label: "Clone ATL repository"
      - id: "atl-setup"
        kind: "shell" 
        command: "~/.openclaw/skills/atl-browser/scripts/setup.sh"
        label: "Build and install ATL to simulator"
---

# ATL — 代理触控层（Agent Touch Layer）

> 这是AI代理与iOS系统之间的自动化层

ATL为iOS模拟器提供基于HTTP的自动化功能，支持**浏览器**（移动版Safari）和**原生应用**。可以将其视为Playwright的移动版本。

## 🔀 两个服务器：浏览器（Browser）与原生应用（Native）

ATL为浏览器和原生应用自动化分别使用**两个独立的服务器**：

| 服务器 | 端口 | 用途 | 关键命令 |
|--------|------|----------|--------------|
| **浏览器** | `9222` | 在移动版Safari中进行Web自动化 | `goto`, `markElements`, `clickMark`, `evaluate` |
| **原生应用** | `9223` | 操作iOS应用（如设置、联系人等） | `openApp`, `snapshot`, `tapRef`, `find` |

### 为什么需要两个端口？

原生应用自动化需要使用XCTest API（如`XCUIApplication`, `XCUIElement`），而这些API仅存在于UI测试包中。因此，原生应用自动化服务器以UI测试的形式运行，并提供HTTP API接口。

### 启动服务器

### 端口快速参考

| 功能 | 端口 | 示例 |
|------|------|---------|
| 浏览网站 | 9222 | `curl localhost:9222/command -d '{"method":"goto",...}'` |
| 打开原生应用 | 9223 | `curl localhost:9223/command -d '{"method":"openApp",...}'` |
| 拍摄浏览器截图 | 9222 | `curl localhost:9222/command -d '{"method":"screenshot"}'` |
| 拍摄原生应用截图 | 9223 | `curl localhost:9223/command -d '{"method":"screenshot"}'` |

---

## 📱 原生应用自动化（端口9223）

原生应用自动化使用**端口9223**，通过访问能力树（accessibility tree）来操作**任何iOS应用**——无需DOM或JavaScript，直接与元素交互。

### 打开和关闭应用

### 常用应用包ID

| 应用 | 包ID |
|-----|-----------|
| 设置 | `com.apple.Preferences` |
| 联系人 | `com.apple.MobileAddressBook` |
| 计算器 | `com.apple.calculator` |
| 日历 | `com.apple.mobilecal` |
| 照片 | `com.apple.mobileslideshow` |
| 笔记 | `com.apple.mobilenotes` |
| 提醒事项 | `com.apple.reminders` |
| 时钟 | `com.apple.mobiletimer` |
| 地图 | `com.apple.Maps` |
| Safari | `com.apple.mobilesafari` |

### `snapshot` 命令

`snapshot` 命令会返回访问能力树的信息，包括所有可见元素及其属性和可点击的引用。

**示例输出：**
- `interactiveOnly`（布尔值，默认为`false`）：仅返回可点击的元素
- `maxDepth`（整数，可选）：限制遍历深度

### `tapRef` 命令

根据上一次`snapshot`中的引用来点击元素

### `find` 命令

通过文本查找并操作元素——无需手动解析访问能力树：

**参数：**
- `text`（字符串）：要搜索的文本（匹配标签、值或标识符）
- `action`（字符串）：可选操作：`tap`, `fill`, `exists`, `get`
- `value`（字符串，可选）：要输入的文本（仅当`action`为`fill`时需要）
- `by`（字符串，可选）：搜索条件：`label`, `value`, `identifier`, `type`, 或 `any`（默认）

---

## 🔄 原生应用工作流程示例

以下是一个完整的操作流程：打开设置，导航到Wi-Fi设置，然后拍摄截图：

### 辅助脚本版本

---

## 💡 核心优势：无需视觉模型的自动化

ATL的独特优势在于**无需视觉模型即可实现空间理解**：

**为什么这很重要：**
- **无需调用视觉API**：因此不会产生额外的计算成本
- **更快**：无需与GPT-4V/Claude Vision进行交互
- **结果稳定**：相同的页面每次都会得到相同的坐标
- **精度更高**：坐标精确到像素级别，而非依赖视觉解析

### 无视觉模型的工作流程

**标记用于确定元素的位置，PDF文件用于显示元素的内容。两者结合即可实现页面的全面理解。**

## 🎯 自动化问题解决机制

当自动化遇到问题时，可以按照以下步骤进行排查：

### 何时需要升级解决方案

| 症状 | 可能原因 | 应对措施 |
|---------|--------------|--------|
| 点击成功但页面无变化 | 可能是弹窗或覆盖层遮挡了元素 | 重新拍摄截图并尝试使用`find`命令查找新的元素 |
| 购物车数量未更新 | 可能需要登录或存在机器人检测 | 尝试使用JavaScript进行点击操作 |
| 滚动后仍找不到元素 | 标记是基于页面位置的，而非视口位置的 | 使用`evaluate`命令获取元素的`getBoundingClientRect`属性 |
| 同一问题反复出现 | 可能是UI状态发生了变化 | 重新拍摄截图以确认实际页面状态 |

### 实际应用场景：电子商务结算流程

在Target、Amazon等网站中，点击“加入购物车”后，通常会：
1. 打开一个选择选项的弹窗（尺寸、颜色、数量）
2. 显示促销信息（如保护计划、配件）
3. 显示“查看购物车”或“继续购物”的按钮

**你的原始点击操作是有效的**——只是由于无法看到结果而无法确认操作是否成功。

## 快速入门（30秒内完成）

### 或者使用辅助函数：

### 基本URL：`http://localhost:9222`

### 常用命令

---

## 首次使用前的设置

### 1. 启动模拟器
### 2. 构建并安装AtlBrowser
### 3. 验证服务器连接

## 所有可用方法

### 应用控制（原生模式）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `openApp` | `{bundleId}` | 任意应用→原生模式 | 打开应用并切换到原生模式 |
| `closeApp` | - | 原生模式 | 关闭当前应用，返回浏览器模式 |
| `appState` | - | 任意应用 | 获取当前应用模式和包ID |
| `openBrowser` | - | 原生模式→浏览器模式 | 切换回浏览器模式 |

### 原生应用访问能力操作

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `snapshot` | `{interactiveOnly?, maxDepth?}` | 原生模式 | 获取访问能力树 |
| `tapRef` | `{ref}` | 原生模式 | 根据引用点击元素（例如：“e0”） |
| `find` | `{text, action, value?, by?}` | 原生模式 | 查找元素并执行操作 |
| `fillRef` | `{ref, text}` | 原生模式 | 点击元素并输入文本 |
| `focusRef` | `{ref}` | 原生模式 | 集中元素焦点（无需手动输入）

### 浏览器操作

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `goto` | `{url}` | 浏览器模式 | 导航到指定URL |
| `reload` | - | 浏览器模式 | 刷新页面 |
| `goBack` | - | 浏览器模式 | 向后导航 |
| `goForward` | - | 浏览器模式 | 向前导航 |
| `getURL` | - | 浏览器模式 | 获取当前URL |
| `getTitle` | - | 浏览器模式 | 获取页面标题 |

### 浏览器交互操作

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `click` | `{selector}` | 浏览器模式 | 点击元素 |
| `doubleClick` | `{selector}` | 浏览器模式 | 双击元素 |
| `type` | `{text}` | 浏览器模式 | 在输入框中输入文本 |
| `fill` | `{selector, value}` | 浏览器模式 | 在输入框中输入文本 |
| `press` | `{key}` | 浏览器模式 | 按下指定键 |
| `hover` | `{selector}` | 浏览器模式 | 鼠标悬停在元素上 |
| `scrollIntoView` | `{selector}` | 浏览器模式 | 将元素滚动到可视范围内 |

### 标记系统（浏览器模式）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `markElements` | - | 浏览器模式 | 标记所有可见的可交互元素 |
| `markAll` | - | 浏览器模式 | 标记所有可交互元素 |
| `unmarkElements` | - | 浏览器模式 | 取消标记 |
| `clickMark` | `{label}` | 浏览器模式 | 根据标签编号点击元素 |
| `getMarkInfo` | `{label}` | 浏览器模式 | 根据标签获取元素信息 |

### 截图与捕获

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `screenshot` | `{fullPage?, selector?}` | 两者模式 | 拍摄整个页面的截图 |
| `captureForVision` | `{savePath?, name?}` | 浏览器模式 | 生成适用于视觉分析的PDF文件 |
| `captureJPEG` | `{quality?, fullPage?}` | 两者模式 | 生成JPEG格式的截图 |
| `captureLight` | - | 浏览器模式 | 仅捕获可交互元素的截图 |

### 等待操作（浏览器模式）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `waitForSelector` | `{selector, timeout?}` | 浏览器模式 | 等待指定元素出现 |
| `waitForNavigation` | - | 浏览器模式 | 等待页面加载完成 |
| `waitForReady` | `{timeout?, stabilityMs?}` | 浏览器模式 | 等待页面准备好 |
| `waitForAny` | `{selectors, timeout?}` | 浏览器模式 | 等待任意元素出现 |

### JavaScript操作（浏览器模式）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `evaluate` | `{script}` | 浏览器模式 | 执行JavaScript代码 |
| `querySelector` | `{selector}` | 浏览器模式 | 查找指定元素 |
| `querySelectorAll` | `{selector}` | 浏览器模式 | 查找所有元素 |
| `getDOMSnapshot` | - | 浏览器模式 | 获取页面的HTML结构 |

### Cookies操作（浏览器模式）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `getCookies` | - | 浏览器模式 | 获取所有Cookies |
| `setCookies` | `{cookies}` | 浏览器模式 | 设置Cookies |
| `deleteCookies` | - | 浏览器模式 | 删除所有Cookies |

### 触控手势（两种模式通用）

| 方法 | 参数 | 模式 | 描述 |
|--------|--------|------|-------------|
| `tap` | `{x, y}` | 两者模式 | 在指定坐标处点击 |
| `longPress` | `{x, y, duration?}` | 两者模式 | 长按（默认持续0.5秒） |
| `swipe` | `{direction}` | 两者模式 | 向上/下/左/右滑动 |
| `swipe` | `{fromX, fromY, toX, toY}` | 两者模式 | 在两点之间滑动 |
| `pinch` | `{scale, duration?}` | 两者模式 | 缩放（scale > 1表示放大） |

#### 滑动操作示例

---

## 典型工作流程

---

## 故障排除

### 导航失败（`goto`命令返回成功但页面未改变）

已知问题：`goto`命令可能返回成功结果，但实际上并未触发页面导航。此时可以尝试使用JavaScript进行手动操作：

### 服务器无响应

### 需要重新构建自动化脚本（iOS版本更新）

### 注意：端口9222的使用

ATL服务器在iOS模拟器应用程序内部运行。如果端口9222被其他进程占用，请检查系统进程。

## 最佳实践

### 1. 操作前清理界面

真实用户会关闭弹窗，你也应该这样做。

### 2. 操作后确认状态

不要盲目假设结果，务必验证实际效果。

### 3. 使用视口坐标进行点击操作

标记提供的坐标是基于页面位置的。为了确保点击有效，目标元素必须处于可视范围内。

### 4. 截图是强大的调试工具

遇到疑问时，截图是解决问题的关键工具。

## 其他注意事项

- ATL在iOS模拟器中运行，并使用主机的网络连接。
- 端口9222是默认端口（符合Chrome开发者工具的协议规范）。
- 标记系统会在可交互元素上显示红色编号标签。
- 截图文件采用PNG格式并经过Base64编码；可以使用`base64 -d`命令解码。
- 该工具兼容iOS 26及更高版本（已修复NWListener绑定问题）。

## 系统要求

- 安装了Xcode的macOS系统
- 需要iOS模拟器（随Xcode一起提供）

## 示例

请查看`examples/`文件夹中的示例脚本（如`test-browse.sh`）。

## API文档

完整的API规范请参考[openapi.yaml](../api/openapi.yaml)，其中包含所有命令、参数和响应格式。

## 项目来源

- GitHub仓库：https://github.com/JordanCoin/Atl
- 作者：[@JordanCoin](https://github.com/JordanCoin)