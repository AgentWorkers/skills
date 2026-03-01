---
name: iCloud
slug: icloud
version: 1.0.0
homepage: https://clawic.com/skills/icloud
description: 让代理通过本地的双因素认证（2FA）以及明确的确认流程，安全地操作您的 iCloud Drive、照片库（Photos）和“查找我的设备”（Find My）功能。
changelog: Initial release with secure iCloud account integration, read-first workflows, and confirmation gates for risky actions.
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["python3"]},"install":[{"id":"pyicloud","kind":"pip","package":"pyicloud==2.4.1","label":"Install pyicloud 2.4.1 (pip)"}],"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解安全集成指南。

## 使用场景

当用户希望代理程序与其自己的 iCloud 账户进行交互时，可以使用此技能：列出设备、查询“查找我的”（Find My）状态、检查 iCloud Drive 或获取照片元数据/文件。  
该技能适用于需要严格安全控制的操作自动化场景，但不适用于绕过 Apple 账户安全机制的用途。

## 架构

所有数据存储在 `~/icloud/` 目录下。具体结构及状态字段的详细信息请参阅 `memory-template.md`。

```text
~/icloud/
|-- memory.md               # Status, integration mode, and current account scope
|-- operations-log.md       # Executed commands, result checks, and rollback notes
|-- device-map.md           # Known device aliases and stable IDs
|-- drive-map.md            # iCloud Drive folder map and verified paths
`-- safety-events.md        # Confirmed risky actions and explicit approvals
```

## 快速参考

仅加载当前任务所需的文件：

| 任务类型 | 对应文件 |
|---------|---------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 身份验证与会话管理 | `auth-session.md` |
| “查找我的”操作 | `findmy-ops.md` |
| iCloud Drive 操作 | `drive-ops.md` |
| 照片操作 | `photos-ops.md` |
| 安全限制与确认 | `safety-boundaries.md` |

## 核心规则

### 1. 本地身份验证，切勿通过聊天请求用户信息  
- 绝不要在聊天中要求用户输入 Apple 密码、双因素认证（2FA）代码、会话令牌或应用程序密码。  
- 仅使用终端提示或安全的本地输入方式来进行身份验证。

### 2. 先执行只读操作，再逐步升级权限  
- 首先执行只读操作：检查账户是否可访问、列出设备、查看文件夹列表以及元数据。  
- 在完成只读操作并确认权限范围后，才能执行写入操作。

### 3. 对高风险操作需获得明确确认  
- 失去设备模式、发送消息、重命名/删除文件以及批量上传等操作都属于高风险操作。  
- 在执行这些操作前，需向用户说明操作内容、可能产生的影响以及恢复方案，并获得明确确认。

### 4. 每次操作后进行验证  
- 每次操作完成后，需通过再次读取数据来验证操作结果是否正确。  
- 不能仅凭命令退出代码来判断操作是否成功。

### 5. 保持操作范围有限且可重复执行  
- 尽可能每次操作只针对一个设备 ID 或一个文件路径。  
- 优先使用可重复执行的命令，避免使用通配符操作。

### 6. 正常处理双因素认证和会话过期  
- 如果 Apple 使会话失效，应暂停破坏性操作并重新进行身份验证。  
- 只有在会话信任恢复且读取检查通过后，才能继续操作。

### 7. 仅保存必要的操作上下文  
- 仅保存有助于提高可靠性的信息（如设备 ID、已验证的文件路径、操作结果等）。  
- 绝不要将敏感信息或原始凭证存储在本地内存文件中。

## 常见错误  

- 在聊天中请求用户的 Apple 凭据会导致隐私和信任问题。  
- 在执行读操作之前直接进行写操作可能导致操作目标错误。  
- 使用设备名称而非设备 ID 会导致对同名设备的操作混乱。  
- 假设会话状态在几天内始终有效可能导致操作中途失败。  
- 在未创建备份的情况下执行批量文件修改会导致难以恢复的操作结果。  
- 未进行再次验证就声称操作成功会导致用户无法察觉问题。

## 外部接口  

| 接口地址 | 发送的数据 | 用途 |
|---------|---------|---------|
| https://idmsa.apple.com | 登录时发送的 Apple 账户认证信息 | Apple 账户身份验证 |
| https://setup.icloud.com | 会话信息与服务交互 | iCloud 服务初始化 |
| https://www.icloud.com | 服务 API 请求（如 Drive/Photos/Find My） | iCloud 操作 |
| https://idmsa.apple.com.cn | 中国大陆用户的 Apple 账户认证信息 | 中国大陆地区 Apple 账户身份验证 |
| https://setup.icloud.com.cn | 中国大陆用户的会话信息与服务交互 | 中国大陆地区 iCloud 服务初始化 |
| https://pypi.org | 包元数据（仅在安装时发送） | 安装 `pyicloud` 包 |
| https://files.pythonhosted.org | 包下载（仅在安装时发送） | 安装 `pyicloud` 包 |

此技能的工作流程不会向外部发送其他数据。

## 安全与隐私  

**离开您机器的数据：**  
- 用于执行操作的 Apple 账户认证信息和 iCloud API 请求数据。  
- 安装依赖项时产生的包安装流量。

**保留在本地的数据：**  
- 存储在 `~/icloud/` 目录下的操作日志（可选）。  
- 如果用户选择存储密码，`pyicloud` 工具会管理本地密钥链（keyring）中的密码信息。

**此技能不会：**  
- 绕过 Apple 的安全流程或双因素认证要求。  
- 在聊天中请求用户提供未声明的凭证信息。  
- 执行未指定的网络请求。  
- 修改自身的 `SKILL.md` 文件。

## 信任声明  

使用此技能即表示您信任 Apple 的 iCloud 服务及 `pyicloud` 包。  
只有在您确信这些服务能够安全地处理您的账户操作时，才请安装并运行此工作流程。

## 相关技能  
用户可安装以下技能（通过 `clawhub install <slug>` 命令）：  
- `cloud-storage`：跨存储提供商的数据传输与安全检查功能  
- `ios`：用于管理 Apple 设备设置、权限及解决账户相关问题  
- `macos`：针对 macOS 的安全设置、密钥链管理及运行时诊断工具  
- `photos`：当 iCloud Photos 是主要处理任务时使用的媒体管理工具  

## 反馈建议：  
- 如觉得此技能有用，请给 `clawhub` 评分（例如：给它打星）。  
- 为了保持信息更新，请使用 `clawhub sync` 命令。