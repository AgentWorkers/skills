# MailTap – 临时邮箱服务

**版本：** 1.0.4  
**作者：** Web3 Hungry  
**作者账号：** @zororaka00  
**作者简介：** [https://x.com/web3hungry](https://x.com/web3hungry)  
**官方网站：** [https://www.mailtap.org](https://www.mailtap.org)  
**分类：** 工具 → 自动化 → 隐私与验证  
**标签：** `临时邮箱`  

## 概述  

本技能提供了对 MailTap 公共 API 的无缝访问，MailTap 是一个免费的临时邮箱服务，可生成有效期为 30 分钟的临时邮箱地址。  

无需任何身份验证或 API 密钥——所有接口均为公开接口，支持简单的 HTTP GET 请求。  

本技能不会存储、代理或修改任何电子邮件数据。所有操作均直接与官方 MailTap 公共 API 进行通信。  

**适用于以下场景：**  
- 人工智能代理在注册网站/服务时无需暴露真实邮箱地址  
- 收集验证码、一次性链接或确认邮件  
- 自动化需要邮箱验证的 Web3 活动（如空投、表单提交等）  
- 需要避免邮箱追踪的隐私保护工作流程  
- 下载可用的电子邮件附件  

**基础 URL：** `https://api.mailtap.org`  

所有响应均以 JSON 格式返回。  

## 核心功能  

该技能提供了三个主要接口：  
1. **生成** 新的临时邮箱地址  
2. **检索** 现有邮箱地址的详细信息  
3. **获取** 收件箱中的所有邮件（包括附件元数据）  

代理可以自主执行一系列操作（生成 → 等待 → 检查收件箱 → 提取数据 → 下载附件）。  

## 代理使用指南  

代理应使用标准的 HTTP 工具（如 `curl`、`fetch`、`requests` 等）与 API 进行交互。  

### 1. 生成新的临时邮箱  

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

### 2. 获取邮箱详细信息  

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

或  

```bash
wget "https://s3.mailtap.org/attachments/abc123/document.pdf"
```  

## 推荐的代理工作流程模式  

**验证流程：**  
1. 生成临时邮箱  
2. 用于注册  
3. 检查收件箱  
4. 提取验证码  

**附件处理流程：**  
1. 检查收件箱  
2. 如果有附件 → 下载  
3. 处理文件  

**错误处理：**  
- 如果收到 404 错误 → 邮箱已过期 → 生成新邮箱  

## 代理使用示例提示：**  
- “使用 MailTap 生成一个新的临时邮箱”  
- “检查收件箱中 `abc123@mailtap.com` 的邮件并下载附件”  
- “创建临时邮箱，等待 2 分钟后提取验证码”  

## Python 辅助库（增强版）  

```python
import requests
import time
import os
from pathlib import Path
from typing import Optional, Dict, Any

BASE_URL = "https://api.mailtap.org"
ATTACHMENT_BASE = "https://s3.mailtap.org"

# Whitelisted attachment types for security
WHITELISTED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg", "image/png", "image/gif",
    "text/plain", "text/csv", "text/html",
    "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

MAX_FILE_SIZE_MB = 10  # Maximum 10MB for security


def generate_email() -> Dict[str, Any]:
    """Generates a new temporary email address."""
    response = requests.get(f"{BASE_URL}/public/generate")
    response.raise_for_status()
    return response.json()


def get_inbox(address: str) -> Dict[str, Any]:
    """Retrieves the inbox for a given address."""
    response = requests.get(f"{BASE_URL}/public/inbox/{address}")
    if response.status_code == 404:
        return {"error": "Email not found or expired"}
    response.raise_for_status()
    return response.json()


def wait_for_message(address: str, timeout: int = 120, interval: int = 10) -> Dict[str, Any]:
    """Polls the inbox until a message arrives or timeout is reached."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        inbox = get_inbox(address)
        if "error" not in inbox and inbox.get("messages"):
            return inbox["messages"][-1]
        time.sleep(interval)
    return {"error": "Timeout"}


def is_safe_attachment(attachment: Dict[str, Any]) -> bool:
    """Validates attachment safety based on MIME type and size."""
    mime_type = attachment.get("mime_type", "")
    size_mb = attachment.get("size", 0) / (1024 * 1024)
    
    if mime_type not in WHITELISTED_MIME_TYPES:
        return False
    if size_mb > MAX_FILE_SIZE_MB:
        return False
    return True


def download_attachment(r2_key: str, save_path: Optional[str] = None) -> str:
    """Downloads an attachment from the mailtap S3 storage with security checks."""
    
    # Parse attachment info from r2_key
    parts = r2_key.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid r2_key format")
    
    filename = parts[-1]
    if not filename or ".." in filename:
        raise ValueError("Invalid filename detected")
    
    url = f"{ATTACHMENT_BASE}/{r2_key}"
    
    # Get attachment metadata first
    response = requests.head(url, allow_redirects=True)
    response.raise_for_status()
    
    # Validate content type and size
    content_type = response.headers.get("content-type", "")
    content_length = response.headers.get("content-length")
    
    if content_type not in WHITELISTED_MIME_TYPES:
        raise ValueError(f"Unsafe MIME type: {content_type}")
    
    if content_length:
        size_mb = int(content_length) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"File too large: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB)")
    
    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    if save_path is None:
        save_path = filename
    
    # Ensure safe save path
    save_path = Path(save_path)
    save_path = save_path.resolve()
    
    # Create directory if needed
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
    
    return str(save_path)


def list_attachments(address: str) -> list:
    """Lists all attachments in inbox with security validation."""
    inbox = get_inbox(address)
    if "error" in inbox:
        return []
    
    safe_attachments = []
    for message in inbox.get("messages", []):
        for attachment in message.get("attachments", []):
            if is_safe_attachment(attachment):
                safe_attachments.append(attachment)
    
    return safe_attachments
```  

## 安全性增强措施  

### 1. **附件验证**  
- **MIME 类型白名单**：仅允许常见的安全文件类型（PDF、图片、文本、办公文档）  
- **文件大小限制**：每个文件最大 10MB，以防止大文件攻击  
- **文件名清洗**：通过验证文件名来防止路径遍历攻击  

### 2. **安全下载流程**  
- **元数据验证**：在下载前检查文件类型和大小  
- **沙箱下载**：使用安全的路径解析机制来防止目录遍历  
- **分块下载**：分块下载文件以避免内存耗尽  

### 3. **代理安全指南**  
- **切勿自动执行**：代理不应自动执行下载的文件  
- **使用前验证**：在处理文件前务必验证文件类型和内容  
- **在沙箱环境中使用**：对于不可信的文件，应在隔离环境中进行处理  

## 重要说明与限制：**  
- 邮箱地址在 30 分钟后自动失效。  
- 附件内容是公开的。  
- 正常使用情况下没有访问频率限制。  
- **安全优先**：所有下载内容都会经过安全验证。  
- **禁止自动执行**：代理必须手动验证和处理文件。  
- **用户责任**：用户仍需对未知附件保持谨慎。  

## 安全工作流程示例：**  

```python
# Secure attachment handling
address = "test123@mailtap.com"

# Get inbox and list safe attachments
attachments = list_attachments(address)

for attachment in attachments:
    try:
        # Download with validation
        file_path = download_attachment(attachment["r2_key"])
        print(f"Downloaded safe file: {file_path}")
        
        # Process file (in sandbox if possible)
        # process_file(file_path)
        
    except Exception as e:
        print(f"Failed to download {attachment['filename']}: {e}")
```  

## 来源与验证信息：**  
- **官方服务：** [https://www.mailtap.org](https://www.mailtap.org)  
- **API 根地址：** [https://api.mailtap.org](https://api.mailtap.org)  

本技能是对 MailTap 公共 API 的封装，提供了额外的安全增强功能。  

## 免责声明**  
请负责任地使用本技能，并遵守 MailTap 的服务条款。尽管已采取安全措施，用户在处理来自未知来源的电子邮件附件时仍需谨慎。  

由 Web3 Hungry 创建和维护。  
已更新以确保符合安全标准。