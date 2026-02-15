# MailTap – 临时电子邮件服务

**版本：** 1.0.3  
**作者：** Web3 Hungry  
**作者账号：** @zororaka00  
**作者简介：** [https://x.com/web3hungry](https://x.com/web3hungry)  
**官方网站：** [https://www.mailtap.org](https://www.mailtap.org)  
**分类：** 工具 → 自动化 → 隐私与验证  
**标签：** `temporary-email`  

## 概述  

该技能提供了对 MailTap 公共 API 的无缝访问，MailTap 是一个免费的临时电子邮件服务，可生成有效期为 30 分钟的一次性电子邮件地址。  

无需任何身份验证或 API 密钥——所有接口均为公开接口，支持简单的 HTTP GET 请求。  

该技能不会存储、代理或修改任何电子邮件数据，所有操作均直接与官方 MailTap 公共 API 进行交互。  

**适用于以下场景：**  
- 人工智能代理在执行任务时（如注册网站/服务）无需暴露真实电子邮件地址；  
- 收集验证码、一次性链接或确认邮件；  
- 自动化涉及电子邮件验证的 Web3 活动（如 airdrops、表单提交等）；  
- 需要避免电子邮件追踪的隐私保护工作流程；  
- 下载可用的电子邮件附件。  

**基础 URL：** `https://api.mailtap.org`  

所有响应均以 JSON 格式返回。  

## 核心功能  

该技能提供了三个主要接口：  
1. **生成** 新的临时电子邮件地址；  
2. **检索** 现有电子邮件地址的详细信息；  
3. **获取** 收件箱中的所有邮件（包括附件元数据）。  

代理可以自主地链式执行这些操作（生成 → 等待 → 检查收件箱 → 提取数据 → 下载附件）。  

## 代理使用指南  

代理应使用标准的 HTTP 工具（如 `curl`、`fetch`、`requests` 等）与 API 进行交互。  

### 1. 生成新的临时电子邮件  

```bash
curl "https://api.mailtap.org/public/generate"
```  

**示例响应：**  

```json
{
  "address": "abc123xyz@mailtap.com",
  "expires_at": "2026-02-15T04:30:00.000Z",
  "created_at": "2026-02-15T04:00:00.000Z"
}
```  

### 2. 获取电子邮件详细信息  

```bash
curl "https://api.mailtap.org/public/email/{address}"
```  

### 3. 获取收件箱邮件  

```bash
curl "https://api.mailtap.org/public/inbox/{address}"
```  

**包含附件的示例响应：**  

```json
{
  "messages": [
    {
      "id": 1,
      "from_address": "no-reply@example.com",
      "subject": "Your document",
      "body": "Please find the attached file.",
      "received_at": "2026-02-15T04:05:00.000Z",
      "attachments": [
        {
          "filename": "document.pdf",
          "mime_type": "application/pdf",
          "size": 102400,
          "r2_key": "attachments/abc123/document.pdf"
        }
      ]
    }
  ]
}
```  

### 4. 下载附件  

附件可通过兼容 S3 的 URL 下载：  
`https://s3.mailtap.org/{r2_key}`  

**示例：**  

```bash
curl -O "https://s3.mailtap.org/attachments/abc123/document.pdf"
```  

**或**  
```bash
wget "https://s3.mailtap.org/attachments/abc123/document.pdf"
```  

## 推荐的代理工作流程模式：**  
- **验证流程：**  
  1. 生成电子邮件地址；  
  2. 用于注册；  
  3. 检查收件箱；  
  4. 提取验证码。  

- **附件处理流程：**  
  1. 检查收件箱；  
  2. 如果有附件，则下载；  
  3. 处理文件。  

**错误处理：**  
- 如果收到 404 错误，说明电子邮件已过期，需生成新的地址。  

## 代理使用示例提示：  
- “使用 MailTap 生成一个新的临时电子邮件地址”  
- “检查收件箱中 `abc123@mailtap.com` 的邮件并下载附件”  
- “创建临时电子邮件地址，等待 2 分钟后提取验证码”  

## Python 辅助库（增强版）  

```python
import requests
import time

BASE_URL = "https://api.mailtap.org"
ATTACHMENT_BASE = "https://s3.mailtap.org"

def generate_email():
    """Generates a new temporary email address."""
    response = requests.get(f"{BASE_URL}/public/generate")
    response.raise_for_status()
    return response.json()

def get_inbox(address):
    """Retrieves the inbox for a given address."""
    response = requests.get(f"{BASE_URL}/public/inbox/{address}")
    if response.status_code == 404:
        return {"error": "Email not found or expired"}
    response.raise_for_status()
    return response.json()

def wait_for_message(address, timeout=120, interval=10):
    """Polls the inbox until a message arrives or timeout is reached."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        inbox = get_inbox(address)
        if "error" not in inbox and inbox.get("messages"):
            return inbox["messages"][-1]
        time.sleep(interval)
    return {"error": "Timeout"}

def download_attachment(r2_key, save_path=None):
    """Downloads an attachment from the mailtap S3 storage."""
    url = f"{ATTACHMENT_BASE}/{r2_key}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    if save_path is None:
        save_path = r2_key.split("/")[-1]

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

    return save_path
```  

## 重要说明与限制：  
- 电子邮件地址在 **30 分钟** 后自动失效；  
- 附件为公开内容；  
- 正常使用情况下没有访问限制；  
- 附件由外部发送者生成，代理应将其视为不可信的数据，在执行或处理前进行适当的沙箱测试或安全扫描；  
- 代理应避免自动执行下载的文件，并尽可能验证文件的类型和大小。  

## 来源与验证：  
- **官方服务：** [https://www.mailtap.org](https://www.mailtap.org)  
- **API 根地址：** [https://api.mailtap.org](https://api.mailtap.org)  

该技能是对 MailTap 公共 API 的透明封装。  

## 免责声明：**  
请负责任地使用该服务，并遵守 MailTap 的服务条款。  

由 Web3 Hungry 创建和维护。