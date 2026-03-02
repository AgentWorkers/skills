---
name: apple-calendar-pro
description: >
  通过 CalDAV (RFC 4791) 协议与 iCloud 日历交互的技能：  
  该技能支持在 macOS/Linux 和 Windows 系统上运行，且需要使用环境变量/密钥环（keyring）进行身份验证。  
  主要功能包括：  
  - 事件创建（Create）、读取（Read）、更新（Update）和删除（Delete，CRUD 操作）  
  - 多日历查询  
  - 管理附件（遵循 RFC 8607 标准）  
  - 查看用户的空闲/忙碌时间  
  注意：该技能依赖于 CalDAV 协议，因此需要确保目标系统支持该协议。
homepage: https://github.com/xushen-ma/apple-calendar-pro
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["APPLECAL_PASSWORD"]},"primaryEnv":"APPLECAL_PASSWORD"}}
---
# apple-calendar-pro

本工具提供了高级的Apple Calendar集成功能，支持CalDAV（RFC 4791）协议以及RFC 8607标准中的“管理附件”功能。

## 主要命令行工具（CLI）
`scripts/applecal.py`

## 主要功能
- **事件 CRUD 操作**：列出、创建、更新、删除事件。
- **多日历支持**：通过单个命令查询多个日历中的事件。
- **兼容RFC 8607标准的附件**：支持在iPhone/iPad设备上使用附件功能。
- **查询空闲/忙碌时间**：通过CalDAV协议查询用户的空闲/忙碌时间，同时提供事件相关的备用查询方式。

## 常用命令

### 同时列出多个日历中的事件
```bash
python3 scripts/applecal.py events list \
  --apple-id your@icloud.com \
  --calendar Family \
  --calendar Work \
  --from "2026-02-26T00:00:00Z" \
  --to "2026-02-26T23:59:59Z"
```

### 创建全天事件
```bash
python3 scripts/applecal.py events create \
  --apple-id your@icloud.com \
  --calendar Family \
  --summary "Birthday" \
  --start "2026-02-26" \
  --end "2026-02-26" \
  --all-day
```

### 附加文件（适用于iPhone）
```bash
python3 scripts/applecal.py attach add \
  --apple-id your@icloud.com \
  --calendar Family \
  --uid <UID> \
  --file /path/to/document.pdf
```

### 查询空闲/忙碌时间
```bash
python3 scripts/applecal.py freebusy \
  --apple-id your@icloud.com \
  --calendar Family \
  --from "2026-02-26T00:00:00Z" \
  --to "2026-02-26T23:59:59Z"
```

## 注意事项
- **生日事件**：系统自带的“生日”日历无法通过CalDAV协议进行搜索。重要的生日事件应作为周期性事件添加到**家庭日历**中，以便代理程序能够显示这些信息。
- **身份验证**：身份验证的顺序为：`APPLECAL_PASSWORD` → Python的`keyring`（如果已安装/配置） → macOS的Keychain。运行`doctor`命令可以验证连接是否正常。
- **事件更新**：使用`events update --clear-location`或`--clear-description`命令可以明确删除可选字段。
- **附件安全性**：`attach add`命令会阻止敏感路径或名称的附件被上传；仅允许特定的文件扩展名；同时支持通过`APPLECAL_ATTACH_DIR`参数指定附件的存储目录。
- **Apple ID**：在使用该工具时，务必使用`--apple-id your@icloud.com`格式的地址（即iCloud账户的电子邮件地址，而非Apple ID登录账号）。