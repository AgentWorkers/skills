---
name: find-my
version: 1.0.1
description: 通过“Peekaboo”功能控制苹果的“Find My”应用程序，以定位人员、设备以及AirTag标签。该功能可用于查找钥匙、钱包、AirTag标签，定位家人或朋友的位置，对丢失的物品播放提示音，或查看设备当前的位置。完全通过原生应用程序进行控制，无需使用任何第三方API或共享任何凭证信息。
metadata:
  os: [darwin]
  requires:
    bins: [peekaboo, jq]
    env:
      PEEKABOO_BRIDGE_SOCKET: "Path to OpenClaw.app Peekaboo bridge socket (default: ~/Library/Application Support/OpenClaw/bridge.sock)"
    env_optional:
      FM_OUTPUT_DIR: "Directory for screenshot output (default: /tmp)"
  contains_scripts: true
  privacy:
    screenshots: true
    location_data: true
    ui_automation: true
---
# 查找我的物品（Find My）

通过 Peekaboo 来控制原生的“查找我的物品”（Find My）应用程序。无需使用任何不可靠的 API 或共享凭证。

**脚本执行路径：** `cd {skillDir}`

## 系统要求

| 要求 | 详细信息 |
|--------|-----------|
| **操作系统** | 仅支持 macOS |
| **应用程序** | 必须打开 `Find My.app`；`OpenClaw.app`（提供 Peekaboo 桥接功能） |
| **权限** | `OpenClaw.app` 需要“屏幕录制”和“辅助功能”权限 |
| **Peekaboo** | 必须安装并配置好相应的 CLI 工具 |

## 隐私与安全

**本技能访问的内容：**
- 用户的“查找我的物品”应用程序中的人、设备和物品的位置数据 |
- “查找我的物品”窗口的截图（存储在本地 `/tmp/` 目录下）

**本技能不执行以下操作：**
- 不会向第三方服务发送网络请求 |
- 不会存储任何凭证或访问 Apple ID |
- 不会泄露数据——所有操作均为本地 UI 自动化操作

**数据范围：** 本技能可以查看/操作“查找我的物品”应用程序中可见的所有内容，包括：
- 家人/朋友的共享位置信息 |
- 用户自己的设备位置以及家庭共享成员的设备位置 |
- AirTag 或物品的位置信息

**用户感知：** 本技能通过鼠标点击和 UI 自动化来执行操作，用户可以在屏幕上看到这些操作的发生。

## 已知限制

1. 使用 `--app "Find My"` 时，Peekaboo 可能会卡顿——请改用 `--window-id` 参数 |
2. 侧边栏中的物品名称无法通过辅助功能 API 获取 |
3. 只能通过位置（第1个、第2个等）来选择物品，无法按名称选择 |
4. 仅支持 macOS 系统——需要安装 Peekaboo 和 `OpenClaw.app` |
5. 在技能运行期间，用户无法直接操作 Mac（会与鼠标点击操作冲突）

## 快速参考

| 脚本 | 功能 |
|--------|---------|
| `fm-window.sh` | 获取窗口 ID 和边界信息（以 JSON 格式） |
| `fm-screenshot.sh [路径]` | 截取“查找我的物品”窗口的截图 |
| `fm-tab.sh <标签页>` | 切换标签页（“人员”、“设备”、“物品”） |
| `fm-list.sh [标签页]` | 截取窗口截图并显示侧边栏中的物品位置 |
| `fm-select-item.sh <位置> [标签页>` | 按位置（第1个、第2个等）选择物品 |
| `fm-locate.sh <位置> [标签页>` | 选择物品并截取其位置截图 |
| `fm-info.sh [路径]` | 打开物品信息面板并截图 |
| `fm-play-sound.sh <位置>` | 尝试播放物品上的提示音 |
| `fm-click.sh <x> <y>` | 在窗口相对坐标处点击 |

## 工作流程示例

### 列出可用物品

```bash
./scripts/fm-list.sh items
# Screenshots the Items tab - view image to see your AirTags/items
```

### 查找钥匙（如果钥匙是列表中的第2个物品）

```bash
./scripts/fm-locate.sh 2 items
# Shows location on map, outputs screenshot path
```

### 播放钥匙上的提示音

```bash
./scripts/fm-play-sound.sh 2
# Selects 2nd item, attempts to click Play Sound
# May require manual click if button not found
```

### 检查家庭成员的位置

```bash
./scripts/fm-list.sh people
# View screenshot to see who's listed

./scripts/fm-locate.sh 1 people
# Shows first person's location
```

## 用户界面布局参考

### 标签栏（距离窗口顶部约68像素）
| 标签页 | X 坐标 |
|--------|---------|
| 人员 | 约63像素 |
| 设备 | 约154像素 |
| 物品 | 约243像素 |

### 侧边栏物品（距离窗口左侧约150像素）
| 位置 | Y 坐标 |
|--------|---------|
| 第1个物品 | 约120像素 |
| 第2个物品 | 约174像素 |
| 第3个物品 | 约228像素 |
| 第4个物品 | 约282像素 |
| （间距） | 每个物品之间相隔54像素 |

## 手动坐标点击

当自动化操作失败时，可以手动计算坐标：

```bash
# Get window position
./scripts/fm-window.sh
# Output: {"x": 824, "y": 62, "width": 1024, "height": 768, "window_id": 2248}

# Click at relative position within window
./scripts/fm-click.sh 150 174   # 2nd sidebar item
./scripts/fm-click.sh 243 68    # Items tab
```

## 信息面板操作

选择物品后，点击地图弹窗上的 ⓘ 按钮以打开信息面板：

| 操作 | 功能 |
|--------|---------|
| **播放提示音** | 使 AirTag 发出提示音（仅适用于可播放提示音的物品） |
| **导航** | 打开地图并显示导航信息 |
| **共享位置** | 与他人共享位置信息 |
| **丢失模式** | 启用位置信息共享 |
| **通知** | 配置通知设置 |

## 故障排除

**“找不到‘查找我的物品’窗口”**
- 确保 `Find My.app` 已经打开 |
- 检查 `OpenClaw.app` 是否正在运行（提供 Peekaboo 桥接功能）

**点击操作未生效**
- 窗口可能已经移动——重新运行 `fm-window.sh` 以获取最新的坐标 |
- 点击前请确保 `Find My.app` 是当前活动的窗口

**找不到“播放提示音”按钮**
- 手动打开信息面板（点击地图弹窗上的 ⓘ 按钮） |
- 然后重新运行 `fm-play-sound.sh` 脚本

## 未来改进计划

当 Peekaboo 完善 `--app "Find My"` 的支持后：
- 实现无需计算坐标的直接元素定位 |
- 提供更可靠的侧边栏物品访问机制 |
- 优化自动化流程，使其更加简单易用