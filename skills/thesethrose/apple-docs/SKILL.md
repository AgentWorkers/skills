---
name: apple-docs
description: 查询苹果开发者文档、API以及2014-2025年的WWDC视频。可以搜索SwiftUI、UIKit、Objective-C、Swift框架相关的内容，以及观看相关的会议录像。
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":["node"]}}}
---

# Apple Docs Skill

该工具可用于查询苹果开发者文档、框架、API以及WWDC视频。

## 设置

无需安装，直接使用内置的`fetch`功能即可使用。

## 可用工具

### 文档搜索

| 命令 | 描述 |
|---------|-------------|
| `apple-docs search "查询内容"` | 在苹果开发者文档中搜索指定内容 |
| `apple-docs symbols "UIView"` | 搜索框架中的类、结构体和协议 |
| `apple-docs doc "/path/to/doc"` | 根据路径获取详细文档 |

### API探索

| 命令 | 描述 |
|---------|-------------|
| `apple-docs apis "UIViewController"` | 查看`UIViewController`的继承关系和协议遵循情况 |
| `apple-docs platform "UIScrollView"` | 检查`UIScrollView`的兼容性（平台/版本） |
| `apple-docs similar "UIPickerView"` | 查找苹果推荐的替代方案 |

### 技术浏览

| 命令 | 描述 |
|---------|-------------|
| `apple-docs tech` | 按类别列出所有苹果技术 |
| `apple-docs overview "SwiftUI"` | 获取SwiftUI的全面技术指南 |
| `apple-docs samples "SwiftUI"` | 浏览Swift/Objective-C示例项目 |

### WWDC视频

| 命令 | 描述 |
|---------|-------------|
| `apple-docs wwdc-search "async"` | 搜索2014年至2025年的WWDC会议内容 |
| `apple-docs wwdc-video 2024-100` | 获取视频的文字记录、代码示例和资源 |
| `apple-docs wwdc-topics` | 列出20个WWDC主题类别 |
| `apple-docs wwdc-years` | 列出包含视频的WWDC年份 |

## 选项

| 选项 | 描述 |
|--------|-------------|
| `--limit <n>` | 限制结果数量 |
| `--category` | 按技术类别过滤 |
| `--framework` | 按框架名称过滤 |
| `--year` | 按WWDC年份过滤 |
| `--no-transcript` | 跳过WWDC视频的文字记录 |
| `--no-inheritance` | 跳过API命令中的继承信息 |
| `--no-conformances` | 跳过API命令中的协议遵循信息 |

## 示例

### 搜索文档

```bash
# Search for SwiftUI animations
apple-docs search "SwiftUI animation"

# Find UITableView delegate methods
apple-docs symbols "UITableViewDelegate"
```

### 检查平台兼容性

```bash
# Check iOS version support for Vision framework
apple-docs platform "VNRecognizeTextRequest"

# Find all SwiftUI views that support iOS 15+
apple-docs search "SwiftUI View iOS 15"
```

### 探索API

```bash
# Get inheritance hierarchy for UIViewController
apple-docs apis "UIViewController"

# Find alternatives to deprecated API
apple-docs similar "UILabel"
```

### 浏览WWDC视频

```bash
# Search for async/await sessions
apple-docs wwdc-search "async await"

# Get specific video details with transcript
apple-docs wwdc-video 2024-100

# List all available years
apple-docs wwdc-years
```

### 浏览技术

```bash
# List all Apple technologies
apple-docs tech

# Get SwiftUI overview guide
apple-docs overview "SwiftUI"

# Find Vision framework samples
apple-docs samples "Vision"
```

## 缓存

该工具使用的MCP服务器提供以下缓存机制：
- API文档缓存30分钟 |
- 搜索结果缓存10分钟 |
- 框架信息缓存1小时 |
- 提供超过1,260个WWDC视频的离线版本（总计35MB）

## 资源链接

- MCP服务器：https://github.com/kimsungwhee/apple-docs-mcp |
- 苹果开发者文档：https://developer.apple.com/documentation/ |
- 苹果开发者官网：https://developer.apple.com/