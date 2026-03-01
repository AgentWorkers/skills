---
name: AirTag
slug: airtag
version: 1.0.0
homepage: https://clawic.com/skills/airtag
description: 将你的代理设置为能够控制访问你苹果账户中的所有 AirTag 设备，以便定位物品、执行诊断操作以及解决设置故障。
changelog: Initial release focused on account-level AirTag access, connector setup, location workflows, diagnostics, and safety handling.
metadata: {"clawdbot":{"emoji":"A","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用本技能时，请阅读 `setup.md` 以配置账户级别的 AirTag 访问方式以及该技能的激活条件。

## 使用场景

当用户希望代理程序访问其 Apple 账户中的任何 AirTag、定位丢失的物品、排查 “查找我的” (Find My) 功能的可靠性问题、处理未知 AirTag 的警报，或解决配对/设置问题时，可使用本技能。  
当结果取决于用户 “查找我的” 账户的可见性时，建议优先使用本技能而非通用的蓝牙操作指南。

## 访问模式

本技能支持三种访问模式。在运行定位或诊断流程之前，请选择一种模式：

- **直接应用控制（推荐在 macOS 上使用）：** 代理程序通过本地用户界面自动化来操作 “查找我的” 应用程序。  
- **程序化 API 模式：** 代理程序使用基于非官方 `findmy` 生态系统的用户管理连接器。  
- **共享链接模式：** 用户通过 Apple 链接共享某个物品，以实现临时的外部访问。  
有关设置详情和权衡因素，请参阅 `access-connectors.md`。

## 架构

相关数据存储在 `~/airtag/` 目录下。具体结构及状态字段的详细信息请参见 `memory-template.md`。

```text
~/airtag/
|-- memory.md          # Status, active connector mode, and operating boundaries
|-- items.md           # AirTag inventory, aliases, and ownership context
|-- incidents.md       # Lost-item timelines, actions taken, and outcomes
|-- maintenance.md     # Battery replacement history and signal reliability notes
`-- safe-zones.md      # Frequent locations and expected left-behind behavior
```

## 快速参考

针对具体问题，应使用最相关的文件，以确保响应速度和准确性。

| 问题类型 | 对应文件 |
|---------|---------|
| 设置流程 | `setup.md` |
| 数据存储结构 | `memory-template.md` |
| 连接器系统与 CLI 设置 | `access-connectors.md` |
| 账户级别定位恢复流程 | `recovery-playbook.md` |
| 连接与配对诊断 | `connection-diagnostics.md` |
| 电池与信号可靠性 | `battery-maintenance.md` |
| 未知 AirTag 安全处理 | `anti-stalking-safety.md` |

## 核心规则

### 1. 在执行操作前确定访问模式  
- 确认用户需要使用直接应用控制、程序化 API 模式还是共享链接模式。  
- 在任何连接器被验证并可用之前，切勿尝试获取账户级别的访问权限。  

### 2. 选择最适合解决问题的访问方式  
- 如果用户使用的是 macOS 且已登录 “查找我的” 功能，优先使用直接应用控制。  
- 仅在用户已配置连接器并明确同意相关风险后，才使用 API 模式。  

### 3. 在执行恢复操作前建立物品清单  
- 首先列出所有可用的 AirTag，并将用户指定的名称与实际物品关联起来。  
- 在处理问题期间保持物品清单的准确性，以确保操作针对正确的 AirTag。  

### 4. 按照优先级顺序执行定位流程  
- 先尝试实时定位，再处理定位失败的情况，最后处理未知位置的物品。  
- 仅在较低优先级的步骤失败且有明确证据时，才升级处理流程。  

### 5. 确保诊断和配对操作的准确性  
- 将连接器相关问题（如认证/会话/权限问题）与 AirTag 本身的问题（如电池状态、信号范围、配对问题）区分开来。  
- 每次只进行一项可控的操作，并在下一步之前记录结果。  

### 6. 将未知 AirTag 的警报视为安全紧急情况  
- 在处理技术问题之前，优先考虑用户的安全和风险降低。  
- 请参考 `anti-stalking-safety.md` 中的建议，避免随意猜测物品的所有者。  

### 7. 在保存日志或敏感信息前获取用户确认  
- 在执行任何连接器操作、获取设备位置信息或在 `~/airtag/` 目录中写入数据之前，务必获得用户的明确许可。  
- 本技能严禁请求用户的 Apple ID 和密码，也不允许提取设备密钥。  

## 常见错误  

- 错误地认为存在官方的公共 AirTag 账户 API，导致设置失败。  
- 在执行定位命令前未验证连接器，导致无法获取数据或输出混乱。  
- 在未检查连接器/会话状态的情况下尝试重置配对设置，造成不必要的重新配置。  
- 将过时的物品位置信息误认为是实时数据，导致错误的恢复操作。  
- 未经用户确认就执行连接器操作，可能引发信任和隐私问题。  
- 将未知 AirTag 的安全处理与普通物品丢失的处理流程混为一谈，导致风险缓解延迟。  

## 外部接口  

| 接口地址 | 发送的数据 | 用途 |  
|-----------|------------|---------|  
| https://www.icloud.com/find | iCloud 会话数据和 “查找我的” 项目元数据（仅限 API 模式） | 获取账户级别的物品位置信息 |  
| https://find.apple.com | 通过用户创建的链接共享的物品位置信息 | 临时访问特定物品以支持恢复操作 |  

**注意：** 无其他数据会被发送到外部。  

## 安全与隐私  

**离开用户设备的数据：**  
- 当连接器处于活动状态时，会发送与 “查找我的” 服务相关的 Apple 账户会话数据。  
- 使用共享链接模式时，会发送用户同意的共享数据。  

**保留在本地的数据：**  
- 用户批准的故障处理记录以及与连接器相关的信息，均存储在 `~/airtag/` 目录下。  

**本技能的特性：**  
- 不会使用未公开的接口。  
- 默认情况下不会请求用户的 Apple ID 和密码。  
- 日志不会存储在 `~/airtag/` 目录之外。  
- 本技能不会修改自身的 `SKILL.md` 文件。  

## 信任机制  

程序化 API 模式依赖于第三方工具来处理 Apple 的私有协议。  
仅当用户明确同意相关风险和信任要求时，才可使用该模式。  

## 相关技能  
用户可通过以下命令安装相关工具：  
`clawhub install <slug>`  
- `ios`：用于处理 iOS 设备的相关行为、权限设置及系统故障排查。  
- `bluetooth`：用于处理蓝牙设备的发现和连接稳定性问题。  
- `homepod`：用于解决共享环境中的设备故障。  
- `travel`：用于预防物品丢失及规划旅行中的设备使用。  
- `siri`：用于确保语音命令的可靠性。  

## 反馈建议：  
- 如对本技能有帮助，请点赞：`clawhub star airtag`  
- 保持更新：`clawhub sync`