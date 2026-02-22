---
name: hide-my-email
description: Generate Apple Hide My Email addresses from the terminal and copy to clipboard.
version: "1.0.0"
homepage: https://github.com/manikal/hide-my-email
metadata:
  openclaw:
    emoji: "\U+1F4E7"
    os: ["macos"]
    requires:
      bins: ["hme"]
    install:
      - id: curl
        kind: shell
        command: "curl -fsSL https://raw.githubusercontent.com/manikal/hide-my-email/main/install.sh | sh"
        label: "Install hme (curl)"
---

# Hide My Email CLI

该命令行工具（CLI）用于从终端生成 Apple iCloud+ 的“Hide My Email”地址。生成的地址会自动复制到您的剪贴板中。

## 使用方法

```bash
hme <label> [note]
```

- **label**（必填）：地址的名称（例如，您正在注册的服务名称）
- **note**（可选）：地址的描述或提示信息

## 示例

```bash
# Create an address labeled "Twitter"
hme "Twitter"

# Create an address with a note
hme "Shopping" "For online orders"
```

## 输出结果

成功时，会打印出经过加密处理的电子邮件地址，并将其完整内容复制到剪贴板中：

```
✓ abc****@icloud.com (copied to clipboard)
```

失败时，会向标准错误输出（stderr）打印错误信息，并以非零状态退出程序。

## 使用要求：

- 搭配具有 iCloud+ 订阅资格的 macOS 系统
- 确保您的终端应用程序获得了系统设置中的“无障碍访问”权限