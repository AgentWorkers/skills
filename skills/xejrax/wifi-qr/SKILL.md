---
name: wifi-qr
description: "生成 Wi-Fi 凭据的 QR 代码"
metadata:
  {
    "openclaw":
      {
        "emoji": "📶",
        "requires": { "bins": ["qrencode"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "qrencode",
              "bins": ["qrencode"],
              "label": "Install via dnf",
            },
          ],
      },
  }
---

# Wi-Fi QR码

生成一个包含Wi-Fi登录凭据的QR码。使用手机扫描该QR码即可立即连接网络，无需输入密码。

## 命令

```bash
# Generate a QR code for a Wi-Fi network (defaults to WPA)
wifi-qr "MyNetwork" "mypassword"

# Specify the security type explicitly
wifi-qr "MyNetwork" "mypassword" --type WPA
```

## 安装

```bash
sudo dnf install qrencode
```