---
name: scanwow-sync
description: 将您的 OpenClaw 代理与 ScanWow iOS 应用程序进行同步。启动一个 HTTP Webhook，以便直接从您的手机接收高质量的 OCR 扫描结果，并将其传输到代理的工作区中。
metadata: {"clawdbot":{"emoji":"📸"}}
---
# ScanWow 同步

使用 **ScanWow** iOS 应用程序将您的 OpenClaw 代理连接到手机的摄像头。在手机上扫描文档，让 AI 提取文本，并通过安全 API 导出功能将其即时传输到代理的工作区。

## 设置说明

1. 在您的 OpenClaw 服务器上（或通过反向代理）启动一个 Webhook 服务器。您可以使用 Python、Node.js 或 netcat 来实现。以下是一个简单的 Python Webhook 示例，用于保存传入的扫描结果：

```python
# save_scans.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

TOKEN = "YOUR_SECRET_TOKEN"

class ScanHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth = self.headers.get("Authorization")
        if auth != f"Bearer {TOKEN}":
            self.send_response(401)
            self.end_headers()
            return
            
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)
        
        # Save the OCR text
        filename = f"scan_{data.get('id', 'doc')}.md"
        with open(filename, 'w') as f:
            f.write(data.get('text', ''))
            
        print(f"✅ Saved scan: {filename}")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"success":true}')

print("Listening for ScanWow scans on port 8000...")
HTTPServer(('', 8000), ScanHandler).serve_forever()
```

2. 运行服务器：
   `python3 save_scans.py`
   *（确保端口 8000 可以从互联网访问，例如使用 ngrok、Cloudflare Tunnels 或您的公共 IP）*

3. **配置 ScanWow 应用程序**：
   - 打开您的 iOS 设备上的 ScanWow 应用程序
   - 点击设置齿轮 ⚙️
   - 转到 **安全 API 导出**（Secure API Export）
   - 输入您的公共端点 URL（例如：`https://your-server.com/api/scan`）
   - 输入您的令牌（`YOUR_SECRET_TOKEN`）
   - 确保该功能处于 **启用**（ON）状态

## 数据格式

当您在 ScanWow 中捕获文档并保存后，它会自动发送一个包含以下 JSON 数据的 POST 请求：

```json
{
  "id": "uuid-string",
  "text": "Extracted document text...",
  "confidence": 0.98,
  "pages": 1,
  "timestamp": 1708531200000,
  "isEnhanced": true
}
```

现在，您在手机上进行的任何扫描操作都会神奇地出现在 OpenClaw 代理的工作区中！