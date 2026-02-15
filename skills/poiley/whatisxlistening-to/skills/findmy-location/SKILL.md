---
name: findmy-location
description: 通过 Apple Find My 功能追踪共享联系人的位置，可精确到街道级别。该功能能够根据地图上的地标信息返回联系人的地址、所在城市以及当前所处的环境（如家中、工作场所或外出地点）。同时支持配置已知的位置信息，并在未知地点时使用视觉识别技术作为备用方案。
---

# 查找我的位置

通过 Apple 的“查找我的设备”功能，可以高精度地追踪共享的联系人信息（精确到街道拐角）。

## 系统要求

- **macOS 13** 及更高版本，并安装了“查找我的设备”应用程序
- **Python 3.9** 及更高版本
- 在您的 Mac 上登录了 iCloud 账户（用于访问“查找我的设备”功能）
- 要追踪的联系人已启用位置共享功能
- **peekaboo** – 用于屏幕阅读的命令行工具（[GitHub](https://github.com/steipete/peekaboo)）
- **Hammerspoon**（可选）– 用于确保点击操作的准确性（[hammerspoon.org](https://www.hammerspoon.org/)）

## 先决条件

### 1. 设置 iCloud 和“查找我的设备”

您的 Mac 必须已登录 iCloud 账户，并且启用了“查找我的设备”功能：
- 系统设置 → Apple ID → iCloud → “查找我的 Mac”（已启用）
- 要追踪的人必须通过“查找我的设备”功能与您的 iCloud 账户共享他们的位置信息

### 2. 安装 peekaboo

```bash
brew install steipete/tap/peekaboo
```

按照提示授予 **辅助功能** 和 **屏幕录制** 权限（系统设置 → 隐私与安全）。

### 3. 安装 Hammerspoon（可选，但推荐）

Hammerspoon 可确保在所有应用程序中点击操作的准确性。如果没有安装 Hammerspoon，点击操作可能会偶尔指向错误的窗口。

```bash
brew install hammerspoon
open -a Hammerspoon
```

将以下代码添加到 `~/.hammerspoon/init.lua` 文件中：
```lua
local server = hs.httpserver.new(false, false)
server:setPort(9090)
server:setCallback(function(method, path, headers, body)
    local data = body and hs.json.decode(body) or {}
    if path == "/click" then
        hs.eventtap.leftClick({x=data.x, y=data.y})
        return hs.json.encode({status="clicked", x=data.x, y=data.y}), 200, {}
    end
    return hs.json.encode({error="not found"}), 404, {}
end)
server:start()
```

重新加载配置文件（Hammerspoon 菜单 → 重新加载配置），然后创建 `~/.local/bin/hsclick` 文件：
```bash
#!/bin/bash
curl -s -X POST localhost:9090/click -d "{\"x\":$2,\"y\":$3}"
chmod +x ~/.local/bin/hsclick
```

## 安装方法

#### 通过命令行安装：
```bash
git clone https://github.com/poiley/findmy-location.git
cd findmy-location
./install.sh
```

#### 或者通过 ClawdHub 安装：
```bash
clawdhub install findmy-location
```

## 配置

创建 `~/.config/findmy-location/config.json` 文件：
```json
{
  "target": "John",
  "known_locations": [
    {
      "name": "home",
      "address": "123 Main St, City, ST",
      "markers": ["landmark near home"]
    },
    {
      "name": "work",
      "address": "456 Office Blvd, City, ST",
      "markers": ["landmark near work"]
    }
  ]
}
```

| 字段 | 说明 |
|-------|-------------|
| `target` | 要追踪的联系人名称（可选，默认为第一个共享的联系人） |
| `known_locations` | 需要标注地址的位置列表 |
| `markers` | 在该位置时，在“查找我的设备”地图上显示的地标 |

## 使用方法

```bash
findmy-location          # Human-readable output
findmy-location --json   # JSON output
```

### 示例输出

```
123 Main St, City, ST (home) - Now
```

```json
{
  "person": "contact@email.com",
  "address": "Main St & 1st Ave",
  "city": "Anytown",
  "state": "WA",
  "status": "Now",
  "context": "out",
  "screenshot": "/tmp/findmy-12345.png",
  "needs_vision": false
}
```

| 字段 | 说明 |
|-------|-------------|
| `context` | `home`（家）、`work`（工作）、`out`（外出）或 `unknown`（未知） |
| `needs_vision` | 如果设置为 `true`，则使用 AI 技术从截图中读取街道名称 |
| `screenshot` | 捕获的地图图片路径 |

## 工作原理

1. 打开“查找我的设备”应用程序并选择目标联系人。
2. 捕获地图图像并读取辅助功能相关的数据。
3. 将地图上的地标与配置中的已知位置进行匹配。
4. 返回地址和上下文信息，或提示是否需要使用视觉识别功能进行分析。

## 常见问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| 点击操作指向错误的窗口 | 安装 Hammerspoon（参见先决条件） |
| 未找到目标联系人 | 确保目标联系人已启用位置共享功能 |
| 始终显示 `needs_vision: true` | 为经常访问的位置添加地标标记 |
| 权限问题 | 授予 peekaboo 辅助功能及屏幕录制权限 |

## 许可证

MIT 许可证