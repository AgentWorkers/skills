---
name: telegram-ascii-table
description: 将表格数据格式化为适用于 Telegram 的 ASCII 箱式表格。仅使用标准输入（stdin）可以消除 shell 注入的风险。该工具支持智能调整列宽、文本换行以及为等宽显示提供适当的填充效果。
---

# Telegram ASCII 表格

将表格数据格式化为 ASCII 箱形绘制表格，以便在 Telegram 代码块中正确显示。

## 快速入门

```bash
{baseDir}/scripts/ascii-table.py <<'EOF'
Name|Value|Status
Server|web-01|Online
Database|db-01|Syncing
EOF
```

在发送到 Telegram 时，需要将输出内容用三引号括起来。

## 使用方法

### Heredoc（推荐）

```bash
# Desktop mode (default): Unicode box chars, 58 char width
ascii-table <<'EOF'
Server|Status|Uptime
web-01|Online|14d 3h
db-01|Syncing|2d 12h
EOF

# Mobile mode: ASCII chars, 48 char width
ascii-table --mobile <<'EOF'
Task|Status
Deploy|Done
Test|Pending
EOF

# Custom width
ascii-table --width 80 <<'EOF'
Column|Another Column
data|more data
EOF
```

### 管道（Pipe）

```bash
cat data.txt | ascii-table
echo -e 'Name|Value\nRow1|Data1' | ascii-table
some-command | ascii-table --mobile
```

## 选项

```
┌───────────┬───────┬────────────────────────────────────────────┐
│ Flag      │ Short │ Description                                │
├───────────┼───────┼────────────────────────────────────────────┤
│ --desktop │ -d    │ Unicode box chars, 58 char width (DEFAULT) │
├───────────┼───────┼────────────────────────────────────────────┤
│ --mobile  │ -m    │ ASCII chars, 48 char width                 │
├───────────┼───────┼────────────────────────────────────────────┤
│ --width N │ -w N  │ Override default width                     │
└───────────┴───────┴────────────────────────────────────────────┘
```

## 模式比较

```
┌───────────────┬──────────────────────┬─────────────────────┐
│ Aspect        │ Desktop (default)    │ Mobile              │
├───────────────┼──────────────────────┼─────────────────────┤
│ Characters    │ Box drawing          │ ASCII (+ - chars)   │
├───────────────┼──────────────────────┼─────────────────────┤
│ Default width │ 58 chars             │ 48 chars            │
├───────────────┼──────────────────────┼─────────────────────┤
│ Rendering     │ Clean on desktop     │ Reliable everywhere │
├───────────────┼──────────────────────┼─────────────────────┤
│ Use when      │ Recipient on desktop │ Recipient on mobile │
└───────────────┴──────────────────────┴─────────────────────┘
```

在移动版 Telegram 中，Unicode 箱形绘制字符的显示宽度可能不一致。对于移动设备接收者，可以使用 `--mobile` 选项。

## 输入格式

- 每行表示一条数据
- 列之间用 `|` 分隔
- 空行会被忽略
- 单元格周围的空白字符会被去除

## 输出示例

### 桌面版
```
┌──────────┬──────────┬──────────┐
│ Server   │ Status   │ Uptime   │
├──────────┼──────────┼──────────┤
│ web-01   │ Online   │ 14d 3h   │
├──────────┼──────────┼──────────┤
│ db-01    │ Syncing  │ 2d 12h   │
└──────────┴──────────┴──────────┘
```

### 移动版
```
+------------+----------+----------+
| Server     | Status   | Uptime   |
+------------+----------+----------+
| web-01     | Online   | 14d 3h   |
+------------+----------+----------+
| db-01      | Syncing  | 2d 12h   |
+------------+----------+----------+
```

### 带有换行符的情况
```
┌─────────┬────────┬──────────────────────────────────────┐
│ Task    │ Status │ Notes                                │
├─────────┼────────┼──────────────────────────────────────┤
│ Deploy  │ Done   │ Rolled out to prod successfully      │
│ API     │        │                                      │
├─────────┼────────┼──────────────────────────────────────┤
│ Fix bug │ WIP    │ Waiting on upstream OAuth fix        │
└─────────┴────────┴──────────────────────────────────────┘
```

## 设计说明：仅支持标准输入（stdin）

该脚本故意不接受通过命令行参数（CLI）输入的数据。

Shell 参数解析会在脚本执行之前完成。在双引号中包含的字符（如 ``` ` ``, `$`, `!`）会被 Shell 解释或执行，而不是由接收这些参数的脚本处理。例如，``` `whoami` `` 会在脚本看到其内容之前就被执行并替换结果。

由于要求通过标准输入（stdin）传递数据，用户输入可以完全绕过 Shell 的解析过程。使用带引号的 Heredoc（`<<'EOF'`）格式时，所有内容都会原样传递——无需进行任何转义或执行操作。

## 限制

- **管道分隔符**：使用 `|` 来分隔列（但该字符不能出现在单元格内容中）
- **单词分割**：较长的单词可能会在中间被分割
- **宽字符**：表情符号（emoji）和汉字可能会导致对齐问题
- **仅支持左对齐**：不支持数字的右对齐