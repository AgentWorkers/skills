---
name: icloud-findmy
description: 通过 iCloud 查询家庭成员设备的地理位置和电池状态。
homepage: https://github.com/picklepete/pyicloud
metadata: {"clawdbot":{"emoji":"📍","requires":{"bins":["icloud"]},"install":[{"id":"pipx","kind":"shell","command":"brew install pipx && pipx install pyicloud","bins":["icloud"],"label":"Install PyiCloud (pipx)"}]}}
---

# iCloud “查找我的设备”功能

通过iCloud CLI（pyicloud）可以查询设备的地理位置和电池电量状态。

## 设置

1. **安装pyicloud：**
```bash
brew install pipx
pipx install pyicloud
```

2. **身份验证（一次性）：**

请求用户提供Apple ID，然后运行以下命令：
```bash
icloud --username their.email@example.com --with-family --list
```

用户需要输入密码并完成两步验证（2FA）。验证后的会话信息会保存下来，有效期为1-2个月。

3. **保存Apple ID：**

将Apple ID添加到您的`TOOLS.md`文件或工作区配置文件中，以便日后查询时使用：
```markdown
## iCloud Find My
Apple ID: their.email@example.com
```

## 使用方法

### 列出所有设备

```bash
icloud --username APPLE_ID --with-family --list
```

**输出格式：**
```
------------------------------
Name           - Liam's iPhone
Display Name   - iPhone 15 Pro
Location       - {'latitude': 52.248, 'longitude': 0.761, 'timeStamp': 1767810759054, ...}
Battery Level  - 0.72
Battery Status - NotCharging
Device Class   - iPhone
------------------------------
```

**解析提示：**
- 设备信息之间用`------------------------------`分隔
- 地理位置信息以Python字典的形式返回（可以使用`eval()`函数或正则表达式进行解析）
- 电池电量范围为0.0-1.0（乘以100即可转换为百分比）
- 电池状态显示为“Charging”（充电中）或“NotCharging”（未充电）
- 地理位置字段包括：`latitude`（纬度）、`longitude`（经度）、`timeStamp`（时间戳，单位为毫秒）、`horizontalAccuracy`（水平精度）

### 查找特定设备

通过解析输出结果来查找特定的设备：
```bash
icloud --username APPLE_ID --with-family --list | grep -A 10 "iPhone"
```

### 解析地理位置数据

提取并格式化地理位置信息：
```bash
icloud --username APPLE_ID --with-family --list | \
  grep -A 10 "Device Name" | \
  grep "Location" | \
  sed "s/Location.*- //"
```

可以使用Python代码或正则表达式来解析返回的Python字典中的地理位置数据。

### 解析电池电量信息

```bash
icloud --username APPLE_ID --with-family --list | \
  grep -A 10 "Device Name" | \
  grep "Battery Level"
```

## 设备名称

设备名称来源于iCloud，可能包含以下情况：
- 使用Unicode引号（`U+2019 `'`）代替普通的ASCII引号
- 完全不使用引号（例如：“Lindas iPhone”）

请使用不区分大小写的匹配方式，并在需要时对引号进行规范化处理。

## 会话管理

- 会话有效期为1-2个月
- 会话信息存储在用户的home目录中
- 会话过期后需要重新进行身份验证
- PyiCloud会在每次请求时自动验证用户身份

## 常用场景

- **出门前检查电池电量：**
```bash
# Get battery for specific device
icloud --username ID --with-family --list | \
  grep -B 2 -A 5 "iPhone" | \
  grep "Battery Level"
```

- **获取当前位置：**
```bash
# Extract location dict and parse coordinates
icloud --username ID --with-family --list | \
  grep -A 10 "iPhone" | \
  grep "Location" | \
  sed "s/.*- //" | \
  python3 -c "import sys; loc = eval(sys.stdin.read()); print(f\"{loc['latitude']}, {loc['longitude']}\")"
```

- **检查设备是否正在充电：**
```bash
icloud --username ID --with-family --list | \
  grep -A 10 "iPhone" | \
  grep "Battery Status"
```

## 实用案例

- **电池电量提醒：** 在外出前查看设备电量
- **提供位置信息：** 根据用户当前位置回答“附近有什么”之类的查询
- **判断用户是否在家：** 根据设备坐标判断用户是否在家
- **电池电量低警告：** 当电池电量低于30%且设备未充电时发出警报

## 故障排除

- **身份验证错误：** 会话过期——重新进行身份验证
- 输入的Apple ID错误——检查保存的ID是否正确
- 需要完成两步验证——按照提示完成验证流程

- **无法获取地理位置信息：**
  - 设备处于离线状态
  - “查找我的设备”功能被禁用
  - 设备的位置服务未开启

- **设备未找到：**
  - 使用`--list`命令检查设备名称是否正确
  - 设备名称区分大小写
  - 设备名称可能包含Unicode引号

## 注意事项

- 该功能需要macOS系统支持（iCloud API的特殊要求）
- 需要启用家庭共享功能才能查看家庭成员的设备信息
- 设备处于活动状态时，位置信息会每1-5分钟更新一次
- 电池电量数据可能被缓存（请查看时间戳确认数据的实时性）