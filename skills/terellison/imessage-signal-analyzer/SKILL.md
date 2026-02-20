---
name: imessage-signal-analyzer
description: 分析 iMessage（macOS）和 Signal 的对话记录，以揭示人际关系的动态变化——包括消息发送的频率、对话的发起模式、沉默期的时长、语音样本以及最近的信息交流情况。该工具可用于分析消息内容、查看对话历史记录、研究对话模式，或根据文本记录来评估人际关系。支持在 macOS（iMessage + Signal）和 Linux/Windows（仅 Signal）平台上使用。
---
# iMessage 与 Signal 分析器

该工具用于分析 iMessage（macOS）和 Signal 对话记录，生成关系分析报告。

## 先决条件

### macOS (iMessage)
iMessage 数据存储在 macOS 的本地设备上。根据您的安全设置，您可能需要授予“全盘访问”权限：
- **选项 1：** 直接使用 Python 运行脚本（如果您有对 `~/Library/Messages/chat.db` 的读取权限，则无需特殊权限）。
- **选项 2：** 如果出现权限错误，请授予“全盘访问”权限：
  - 打开 **系统设置 → 隐私与安全 → 全盘访问**
  - 点击 **+**，然后添加 Python 或您的终端应用程序。

### Linux / Windows (仅 Signal)
- Linux 和 Windows 上不支持 iMessage 功能；
- Signal 数据通过导出的 JSON 文件进行分析。

### Signal (所有平台)
- 安装 `signal-cli`：`brew install signal-cli`（macOS）或访问 [GitHub 链接](https://github.com/AsamK/signal-cli)。
- 将设备与程序关联：`signal-cli link` 并扫描二维码。
- 导出消息：`signal-cli export --output ~/signal_export.json`

## 使用方法

### iMessage 分析
```bash
python3 skills/message-analyzer/scripts/analyze.py imessage <phone_or_handle>
```

**示例：**
```bash
python3 skills/message-analyzer/scripts/analyze.py imessage "+15551234567"
python3 skills/message-analyzer/scripts/analyze.py imessage "+15551234567" --limit 500
```

### Signal 分析
首先，导出您的 Signal 数据（只需执行一次）：
```bash
signal-cli export --output ~/signal_export.json
```

然后进行分析：
```bash
python3 skills/message-analyzer/scripts/analyze.py signal ~/signal_export.json <phone_or_name>
```

**示例：**
```bash
python3 skills/message-analyzer/scripts/analyze.py signal ~/signal_export.json "+15551234567"
python3 skills/message-analyzer/scripts/analyze.py signal ~/signal_export.json "+15559876543"
```

## 查找联系人的电话号码

### iMessage
如果您知道联系人的姓名但不知道电话号码：
```bash
DB=$(ls ~/Library/Application\ Support/AddressBook/Sources/*/AddressBook-v22.abcddb 2>/dev/null | head -1)
sqlite3 "$DB" "SELECT ZFIRSTNAME, ZLASTNAME FROM ZABCDRECORD WHERE ZFIRSTNAME LIKE '%Name%';"
```
如果 AddressBook 无法找到相关信息，请向联系人询问电话号码。

### Signal
Signal 导出的数据中包含电话号码。您可以通过姓名或电话号码进行搜索。

## 关键数据说明

### iMessage
- **您发送的消息** 仅保存在当前设备的设置日期之后；更换设备后，旧消息将会丢失，这会影响数据分析结果。
- **二进制消息**（attributedBody）会被部分解码，因此样本中可能会出现 `+@` 等前缀，这是正常现象。
- **多个联系方式**：同一个联系人可能有多个联系方式（iMessage、SMS、RCS 等），脚本会自动合并这些信息。

### Signal
- **必须先导出数据**：您需要使用 `signal-cli export` 命令导出 Signal 数据。
- **媒体文件**：导出的 JSON 文件中仅包含消息文本，不包含图片或文件。
- **表情反应**：表情反应会作为单独的消息条目显示。

## 分析结果
脚本会生成以下信息：
- 总消息数量（您与对方的消息数量对比）
- 时间范围
- 每年的消息数量（配有条形图）
- 对话发起情况统计（新对话的间隔时间超过 4 小时）
- 长时间未联系的情况（超过 30 天）
- 按年份划分的样本消息
- 最近 10 条消息

## 解读分析结果
运行脚本后，以对话的形式呈现分析结果：
- **消息发送频率**：友谊关系最活跃的时间段是什么时候？是否存在明显的波动？
- **对话发起情况**：谁先发起对话？（注意：旧时期的发送消息可能无法显示）。
- **长时间未联系的原因**：这种沉默是双方共同的选择，还是由于设备更换、平台变更或其他生活事件造成的？
- **对话氛围/内容**：样本消息能反映双方关系的状态如何？
- **用户补充信息**：务必让用户提供相关的背景信息。

请以对话的形式呈现分析结果，而不仅仅是原始数据。尝试给出对关系动态的深入解读。