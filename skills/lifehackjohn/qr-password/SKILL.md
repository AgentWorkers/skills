---
name: qr-password
description: Air-gapped credential bridge using QR codes. Use when transferring credentials between networked and air-gapped devices via QR codes. Triggers on: generating QR from credentials, reading QR codes containing credentials, air-gapped password transfer, credential QR codes, vault-to-QR, camera-to-credential.
---

# QR密码——安全隔离的凭证传输机制

通过二维码作为光学通道实现双向凭证传输。确保没有任何敏感信息直接接触到网络。

## 安全规则（强制执行）

- **切勿将凭证信息记录到聊天历史或内存文件中**
- **从所有对话输出中隐藏密码内容**——用`****`代替密码
- **使用定时功能在30秒后自动清除显示的二维码**
- **二维码为临时文件**——使用`rm`命令在使用后立即删除
- **切勿将解码后的凭证信息存储在任何文件中**

## 模式A：凭证库 → QR码（出站）

为需要安全隔离的设备生成一个二维码，以便其扫描。

```bash
echo '{"username":"USER","password":"PASS","domain":"DOMAIN"}' | \
  python3 skills/qr-password/scripts/generate-qr.py /tmp/qr-out.png
```

然后通过显示屏显示该二维码，并在30秒后自动清除：

```
canvas present /tmp/qr-out.png
# Wait 30s
canvas hide
rm /tmp/qr-out.png
```

在向用户报告结果时，只需说明“二维码已显示”，切勿重复显示密码内容。

## 模式B：摄像头 → 凭证（入站）

从摄像头图像中读取二维码以提取凭证信息：

1. 拍摄图像：`nodes camera_snap`（或接受用户提供的图像）
2. 解码二维码：
```bash
python3 skills/qr-password/scripts/read-qr.py /path/to/image.png
```

3. 解码后的数据格式为JSON：`{"username":"...","password":"...","domain":"..."}`
4. 使用提取到的凭证信息（进行填充、复制或传递）——**切勿在聊天中显示密码**
5. 删除拍摄的图像：`rm /path/to/image.png`

## 离线二维码生成器

为需要安全隔离的设备提供`assets/qr-generator.html`——这是一个独立的离线HTML页面，可以在浏览器中本地生成二维码，无需网络连接。

## 所需依赖库

Python 3及以下库：`qrcode`、`Pillow`、`opencv-python-headless`

安装方式：`python3 -m pip install --user qrcode Pillow opencv-python-headless`