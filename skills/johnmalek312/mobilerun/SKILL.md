---
name: mobilerun
description: 通过 Mobilerun API 控制真实的 Android 手机。支持点击、滑动、输入文本、截图、读取用户界面（UI）的可访问性信息以及管理应用程序。当用户需要自动化操作或远程控制 Android 设备、与移动应用程序交互，或在手机上运行 AI 代理任务时，可以使用该功能。需要一个 Mobilerun API 密钥（前缀为 dr_sk_）以及已连接的设备（可以通过 Portal APK 连接的个人手机或云设备）。
metadata: { "openclaw": { "emoji": "📱", "primaryEnv": "MOBILERUN_API_KEY" } }
tags:
  - mobile
  - android
  - ios
  - automation
  - ai-agent
category: Device Control / Automation
---
# Mobilerun

通过API控制真实的安卓手机——实现点击、滑动、输入文本、截图、查看用户界面（UI）状态、管理应用程序等功能。

## 开始前

在开始操作之前，请勿要求用户提供API密钥或设置设备。请先进行以下检查：

1. **获取API密钥：**
   - 如果`MOBILERUN_API_KEY`不存在，请向用户索取密钥，并将其保存到`~/.openclaw/openclaw.json`文件中的`skills.entries.mobilerun.apiKey`字段（如果已有配置，请合并现有内容，切勿覆盖）。

2. **一次性测试API密钥并检查设备连接状态：**
   ```
   GET https://api.mobilerun.ai/v1/devices
   Authorization: Bearer <key>
   ```
   - 如果返回状态码`200`且设备处于“ready”状态，则表示一切正常，可以直接执行用户请求；
   - 如果返回`200`但设备未连接或所有设备都处于“disconnected”状态，请检查设备连接问题（参见步骤3）；
   - 如果返回`401`，说明API密钥无效、已过期或被撤销，请让用户前往[https://cloud.mobilerun.ai/api-keys]验证密钥。

3. **仅在没有可用设备时**：向用户显示设备状态并提示解决方案：
   - 如果没有设备连接，说明用户尚未连接手机，请引导他们使用Portal APK进行设置（参见[setup.md](./setup.md)；
   - 如果设备处于“disconnected”状态，可能是Portal应用程序断开了连接，请让用户重新打开应用程序。

4. **确认设备是否响应**（可选，仅在初次尝试失败时执行）：
   ```
   GET https://api.mobilerun.ai/v1/devices/{deviceId}/screenshot
   ```
   如果该操作返回PNG格式的截图，说明设备正常工作。

**重要原则：**一旦API密钥设置完成且设备处于可用状态，应立即执行用户的请求，无需再次引导用户完成已完成的设置步骤。

## 快速参考

| 功能 | 对应的API端点          |
|------|----------------------|
| 查看屏幕截图 | `GET /devices/{id}/screenshot`       |
| 查看UI元素信息 | `GET /devices/{id}/ui-state?filter=true`    |
| 点击屏幕某位置 | `POST /devices/{id}/tap`          -- 参数：`{x, y}`     |
| 滑动屏幕 | `POST /devices/{id}/swipe`          -- 参数：`{startX, startY, endX, endY, duration}` |
| 输入文本 | `POST /devices/{id}/keyboard`        -- 参数：`{text, clear}`     |
| 按下按键 | `PUT /devices/{id}/keyboard`        -- 参数：`{key}`     |
| 返回主界面 | `POST /devices/{id}/global`        -- 参数：`{action: 1}`     |
| 返回首页 | `POST /devices/{id}/global`        -- 参数：`{action: 2}`     |
| 打开指定应用程序 | `PUT /devices/{id}/apps/{packageName}`    |
| 列出所有应用程序 | `GET /devices/{id}/apps`        |

所有API请求的基地址为`https://api.mobilerun.ai/v1`，请求头需包含`Authorization: Bearer dr_sk_...`。

## 详细文档

- **[setup.md](./setup.md)**：认证流程、API密钥设置、设备连接方式及故障排除
- **[phone-api.md](./phone-api.md)**：手机控制相关API（截图、UI状态查询、点击、滑动、文本输入、应用程序管理）
- **[subscription.md](./subscription.md)**：订阅服务、价格信息、信用额度、设备类型及升级建议

## 常用操作模式

**观察-行动循环：**  
大多数手机控制操作遵循以下流程：
1. 获取屏幕截图和/或UI状态信息；
2. 确定要执行的操作；
3. 执行相应操作（点击、输入文本、滑动等）；
4. 重新观察操作结果；
5. 重复上述步骤。

**获取点击坐标：**  
使用`GET /devices/{id}/ui-state?filter=true`获取设备的可访问性树（包含元素边界信息），然后计算目标元素的中心坐标以确定点击位置。

**在输入框中输入文本：**  
1. 首先检查`phone_state.isEditable`属性，如果该属性为`false`，则需要先点击输入框；
2. （可选）使用`clear: true`清除输入框中的现有文本；
3. 通过`POST /devices/{id}/keyboard`发送输入的文本。

## 错误处理

| 错误代码 | 可能原因 | 处理方法                |
|--------|------------------|----------------------|
| `401`    | API密钥无效或已过期 | 让用户前往[https://cloud.mobilerun.ai/api-keys]验证密钥 |
| 设备列表为空 | 无设备连接     | 引导用户使用Portal APK连接设备（参见[setup.md]） |
| 设备处于“disconnected”状态 | Portal应用程序关闭或手机网络中断 | 让用户重新打开应用程序或检查网络连接 |
| 在执行`POST /devices`请求时出现计费错误 | 免费账户无法使用该功能；云设备需要订阅 | 告知用户查看[https://cloud.mobilerun.ai/billing]上的计费信息 |
| 在有效设备上执行操作时出现错误 | 设备可能正在使用中、被锁定或无响应 | 先尝试截图以确认设备状态 |
| `403`（提示“limit reached”） | 订阅计划限制（如同时连接设备数量达到上限） | 用户需要终止当前设备的连接或升级订阅（参见[subscription.md]） |