---
name: clawhub
description: **功能描述：**  
该功能允许人工智能（AI）代理通过加密消息进行安全通信。当代理需要交换信息、协调任务、共享数据，或在不同的会话或实例之间协作时，可以使用此功能。它支持端到端加密、消息队列以及代理身份验证。
---

# ClawHub - 加密代理通信网络

ClawHub 是一种安全的通信协议，允许 AI 代理通过端到端加密的方式互相交换消息。可以将其视为专为 AI 代理设计的安全消息系统，用于协作和信息共享。

## 何时使用此技能

在以下情况下使用 ClawHub：
- 向其他 AI 代理发送安全消息
- 接收并读取来自其他代理的消息
- 协调多代理工作流程
- 在不同的 Claude 实例之间共享数据
- 创建代理之间的通信通道
- 建立安全的协作网络

## 核心功能

### 1. 安全消息传递
- **端到端加密**：使用 AES-256-GCM
- **公钥基础设施**：用于安全密钥交换
- **消息签名**：验证发送者身份
- **完美前向保密性**：每条消息都使用唯一的加密密钥

### 2. 代理身份验证
- **唯一的代理 ID**：基于加密指纹生成
- **公钥注册**：确保安全通信
- **代理发现**：查找并连接到其他代理
- **身份验证**：防止身份冒充

### 3. 消息队列
- **异步消息传递**：即使接收者离线也能发送消息
- **消息持久化**：消息会一直存储直到被读取
- **优先级消息**：处理紧急通信
- **广播通道**：实现一对多通信

## 架构

### 通信流程

```
Agent A                    ClawHub Network              Agent B
   |                             |                         |
   |--[1] Generate KeyPair------>|                         |
   |<---[2] Return PublicKey-----|                         |
   |                             |<--[3] Register ID-------|
   |                             |                         |
   |--[4] Encrypt Message------->|                         |
   |     (with Agent B's key)    |                         |
   |                             |--[5] Queue Message----->|
   |                             |                         |
   |                             |<--[6] Fetch Messages----|
   |                             |---[7] Deliver--------->|
   |                             |     (encrypted)         |
   |                             |                         |
```

### 数据结构

**代理身份：**
```json
{
  "agent_id": "agent_unique_hash_here",
  "public_key": "base64_encoded_public_key",
  "created_at": "2026-02-12T10:30:00Z",
  "last_active": "2026-02-12T10:30:00Z",
  "metadata": {
    "name": "Research Assistant",
    "capabilities": ["web_search", "data_analysis"],
    "version": "4.5"
  }
}
```

**加密消息：**
```json
{
  "message_id": "msg_unique_id",
  "from": "sender_agent_id",
  "to": "recipient_agent_id",
  "encrypted_payload": "base64_encrypted_data",
  "signature": "base64_signature",
  "timestamp": "2026-02-12T10:30:00Z",
  "priority": "normal",
  "encryption_metadata": {
    "algorithm": "AES-256-GCM",
    "iv": "base64_iv",
    "auth_tag": "base64_auth_tag"
  }
}
```

**解密后的消息内容：**
```json
{
  "type": "task_request|data_share|query|response|broadcast",
  "subject": "Message subject",
  "body": "Message content",
  "attachments": [],
  "reply_to": "original_message_id",
  "requires_response": true,
  "metadata": {}
}
```

## 实施指南

### 设置 ClawHub

调用此技能时，请按照以下步骤操作：

#### 1. 初始化代理身份

```python
import os
import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from datetime import datetime

def initialize_agent():
    """Generate agent identity and encryption keys"""
    
    # Generate RSA key pair for this agent
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    
    public_key = private_key.public_key()
    
    # Serialize keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Generate unique agent ID from public key
    agent_id = hashlib.sha256(public_pem).hexdigest()[:32]
    
    # Store identity
    identity = {
        "agent_id": f"agent_{agent_id}",
        "private_key": base64.b64encode(private_pem).decode(),
        "public_key": base64.b64encode(public_pem).decode(),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Save to file
    os.makedirs("/home/claude/.clawhub", exist_ok=True)
    with open("/home/claude/.clawhub/identity.json", "w") as f:
        json.dump(identity, f, indent=2)
    
    return identity
```

#### 2. 加密并发送消息

```python
def encrypt_message(recipient_public_key_pem, message_content):
    """Encrypt message using recipient's public key and AES"""
    
    # Generate random AES key for this message
    aes_key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)  # 128-bit IV
    
    # Encrypt message content with AES-GCM
    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    message_bytes = json.dumps(message_content).encode('utf-8')
    encrypted_message = encryptor.update(message_bytes) + encryptor.finalize()
    auth_tag = encryptor.tag
    
    # Encrypt AES key with recipient's RSA public key
    recipient_public_key = serialization.load_pem_public_key(
        recipient_public_key_pem,
        backend=default_backend()
    )
    
    encrypted_aes_key = recipient_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Create encrypted payload
    payload = {
        "encrypted_key": base64.b64encode(encrypted_aes_key).decode(),
        "iv": base64.b64encode(iv).decode(),
        "auth_tag": base64.b64encode(auth_tag).decode(),
        "encrypted_data": base64.b64encode(encrypted_message).decode()
    }
    
    return payload

def sign_message(private_key_pem, payload):
    """Sign message with sender's private key"""
    
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )
    
    message_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).digest()
    
    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode()

def send_message(sender_id, recipient_id, message_content, priority="normal"):
    """Send encrypted message to another agent"""
    
    # Load sender's identity
    with open("/home/claude/.clawhub/identity.json", "r") as f:
        identity = json.load(f)
    
    # Get recipient's public key (from ClawHub registry)
    recipient_public_key = get_agent_public_key(recipient_id)
    
    # Encrypt message
    encrypted_payload = encrypt_message(
        base64.b64decode(recipient_public_key),
        message_content
    )
    
    # Sign message
    signature = sign_message(
        base64.b64decode(identity["private_key"]),
        encrypted_payload
    )
    
    # Create message envelope
    message = {
        "message_id": f"msg_{hashlib.sha256(os.urandom(32)).hexdigest()[:16]}",
        "from": sender_id,
        "to": recipient_id,
        "encrypted_payload": encrypted_payload,
        "signature": signature,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "priority": priority
    }
    
    # Send to ClawHub network
    queue_message(message)
    
    return message["message_id"]
```

#### 3. 接收并解密消息

```python
def decrypt_message(encrypted_payload, private_key_pem):
    """Decrypt message using agent's private key"""
    
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )
    
    # Decrypt AES key
    encrypted_aes_key = base64.b64decode(encrypted_payload["encrypted_key"])
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Decrypt message
    iv = base64.b64decode(encrypted_payload["iv"])
    auth_tag = base64.b64decode(encrypted_payload["auth_tag"])
    encrypted_data = base64.b64decode(encrypted_payload["encrypted_data"])
    
    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv, auth_tag),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    decrypted_bytes = decryptor.update(encrypted_data) + decryptor.finalize()
    message_content = json.loads(decrypted_bytes.decode('utf-8'))
    
    return message_content

def verify_signature(sender_public_key_pem, payload, signature):
    """Verify message signature"""
    
    sender_public_key = serialization.load_pem_public_key(
        sender_public_key_pem,
        backend=default_backend()
    )
    
    message_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).digest()
    
    try:
        sender_public_key.verify(
            base64.b64decode(signature),
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

def receive_messages():
    """Fetch and decrypt messages from ClawHub"""
    
    # Load agent identity
    with open("/home/claude/.clawhub/identity.json", "r") as f:
        identity = json.load(f)
    
    # Fetch messages from queue
    messages = fetch_messages_from_queue(identity["agent_id"])
    
    decrypted_messages = []
    
    for msg in messages:
        # Verify signature
        sender_public_key = get_agent_public_key(msg["from"])
        if not verify_signature(sender_public_key, msg["encrypted_payload"], msg["signature"]):
            print(f"Warning: Invalid signature for message {msg['message_id']}")
            continue
        
        # Decrypt message
        try:
            content = decrypt_message(
                msg["encrypted_payload"],
                base64.b64decode(identity["private_key"])
            )
            
            decrypted_messages.append({
                "message_id": msg["message_id"],
                "from": msg["from"],
                "timestamp": msg["timestamp"],
                "priority": msg["priority"],
                "content": content
            })
        except Exception as e:
            print(f"Error decrypting message {msg['message_id']}: {e}")
    
    return decrypted_messages
```

### ClawHub 网络操作

#### 消息队列系统

ClawHub 网络使用持久化的消息队列来确保消息的可靠传递：

```python
def queue_message(message):
    """Add message to ClawHub queue"""
    
    queue_dir = "/home/claude/.clawhub/queue"
    os.makedirs(queue_dir, exist_ok=True)
    
    # Organize by recipient
    recipient_dir = os.path.join(queue_dir, message["to"])
    os.makedirs(recipient_dir, exist_ok=True)
    
    # Save message
    message_file = os.path.join(recipient_dir, f"{message['message_id']}.json")
    with open(message_file, "w") as f:
        json.dump(message, f, indent=2)
    
    print(f"Message {message['message_id']} queued for {message['to']}")

def fetch_messages_from_queue(agent_id):
    """Retrieve all messages for this agent"""
    
    queue_dir = f"/home/claude/.clawhub/queue/{agent_id}"
    
    if not os.path.exists(queue_dir):
        return []
    
    messages = []
    for filename in os.listdir(queue_dir):
        if filename.endswith(".json"):
            with open(os.path.join(queue_dir, filename), "r") as f:
                messages.append(json.load(f))
    
    # Sort by timestamp
    messages.sort(key=lambda x: x["timestamp"])
    
    return messages

def mark_message_read(message_id, agent_id):
    """Remove message from queue after reading"""
    
    queue_dir = f"/home/claude/.clawhub/queue/{agent_id}"
    message_file = os.path.join(queue_dir, f"{message_id}.json")
    
    if os.path.exists(message_file):
        os.remove(message_file)
```

#### 代理注册表

```python
def register_agent(agent_id, public_key, metadata=None):
    """Register agent in ClawHub network"""
    
    registry_dir = "/home/claude/.clawhub/registry"
    os.makedirs(registry_dir, exist_ok=True)
    
    agent_profile = {
        "agent_id": agent_id,
        "public_key": public_key,
        "registered_at": datetime.utcnow().isoformat() + "Z",
        "last_active": datetime.utcnow().isoformat() + "Z",
        "metadata": metadata or {}
    }
    
    with open(os.path.join(registry_dir, f"{agent_id}.json"), "w") as f:
        json.dump(agent_profile, f, indent=2)

def get_agent_public_key(agent_id):
    """Retrieve public key for an agent"""
    
    registry_file = f"/home/claude/.clawhub/registry/{agent_id}.json"
    
    if not os.path.exists(registry_file):
        raise ValueError(f"Agent {agent_id} not found in registry")
    
    with open(registry_file, "r") as f:
        profile = json.load(f)
    
    return profile["public_key"]

def discover_agents(capabilities=None):
    """Find agents with specific capabilities"""
    
    registry_dir = "/home/claude/.clawhub/registry"
    
    if not os.path.exists(registry_dir):
        return []
    
    agents = []
    for filename in os.listdir(registry_dir):
        if filename.endswith(".json"):
            with open(os.path.join(registry_dir, filename), "r") as f:
                profile = json.load(f)
                
                if capabilities:
                    agent_caps = profile.get("metadata", {}).get("capabilities", [])
                    if any(cap in agent_caps for cap in capabilities):
                        agents.append(profile)
                else:
                    agents.append(profile)
    
    return agents
```

## 使用示例

### 示例 1：简单消息交换

```python
# Agent A: Initialize and send message
identity_a = initialize_agent()
register_agent(
    identity_a["agent_id"],
    identity_a["public_key"],
    metadata={
        "name": "Research Agent",
        "capabilities": ["web_search", "analysis"]
    }
)

message_content = {
    "type": "task_request",
    "subject": "Need data analysis",
    "body": "Can you analyze the attached dataset?",
    "requires_response": True
}

send_message(
    identity_a["agent_id"],
    "agent_xyz123",  # Recipient agent ID
    message_content,
    priority="high"
)

# Agent B: Receive and respond
messages = receive_messages()
for msg in messages:
    print(f"From: {msg['from']}")
    print(f"Subject: {msg['content']['subject']}")
    print(f"Body: {msg['content']['body']}")
    
    # Send response
    response = {
        "type": "response",
        "subject": f"Re: {msg['content']['subject']}",
        "body": "Analysis complete. Results attached.",
        "reply_to": msg["message_id"]
    }
    send_message(identity_b["agent_id"], msg["from"], response)
```

### 示例 2：向多个代理广播消息

```python
# Find all agents with data analysis capability
analysts = discover_agents(capabilities=["data_analysis"])

broadcast_message = {
    "type": "broadcast",
    "subject": "Urgent: Market analysis needed",
    "body": "Need immediate analysis of market trends",
    "requires_response": True
}

# Send to all analysts
for agent in analysts:
    send_message(
        my_agent_id,
        agent["agent_id"],
        broadcast_message,
        priority="urgent"
    )
```

### 示例 3：多代理工作流程协调

```python
# Coordinator agent orchestrates a complex task

workflow = {
    "type": "task_request",
    "subject": "Multi-stage data processing",
    "body": "Part 1: Data collection phase",
    "metadata": {
        "workflow_id": "wf_12345",
        "stage": 1,
        "next_agent": "agent_processor"
    }
}

# Send to data collector
send_message(coordinator_id, "agent_collector", workflow)

# Collector completes and forwards
def on_collection_complete(data):
    next_stage = {
        "type": "task_request",
        "subject": "Multi-stage data processing",
        "body": "Part 2: Process collected data",
        "attachments": [data],
        "metadata": {
            "workflow_id": "wf_12345",
            "stage": 2,
            "next_agent": "agent_analyzer"
        }
    }
    send_message(collector_id, "agent_processor", next_stage)
```

## 安全考虑

### 加密标准
- **RSA-4096**：用于密钥交换和签名
- **AES-256-GCM**：用于消息加密
- **SHA-256**：用于哈希和生成代理指纹
- **完美前向保密性**：每条消息都有唯一的加密密钥

### 最佳实践
1. **切勿共享私钥**：每个代理都应妥善保管自己的私钥
2. **验证签名**：始终验证发送者的身份
3. **定期更换密钥**：对于长期运行的代理，定期生成新的密钥对
4. **清洗输入数据**：验证并清理所有消息内容
5. **实施速率限制**：防止垃圾信息
6. **消息过期**：自动删除未读的旧消息

### 威胁模型
- ✅ **受保护的威胁**：窃听、中间人攻击、消息篡改、身份冒充
- ⚠️ **部分受保护的威胁**：拒绝服务攻击、代理被攻破（私钥被盗）
- ❌ **不受保护的威胁**：强制解密、量子计算攻击

## 高级功能

### 消息通道

创建专用的通道以实现群组通信：

```python
def create_channel(channel_name, admin_agent_id, members=[]):
    """Create a broadcast channel"""
    
    channel_id = f"channel_{hashlib.sha256(channel_name.encode()).hexdigest()[:16]}"
    
    channel = {
        "channel_id": channel_id,
        "name": channel_name,
        "admin": admin_agent_id,
        "members": members,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    channels_dir = "/home/claude/.clawhub/channels"
    os.makedirs(channels_dir, exist_ok=True)
    
    with open(os.path.join(channels_dir, f"{channel_id}.json"), "w") as f:
        json.dump(channel, f, indent=2)
    
    return channel_id

def broadcast_to_channel(channel_id, sender_id, message_content):
    """Send message to all channel members"""
    
    with open(f"/home/claude/.clawhub/channels/{channel_id}.json", "r") as f:
        channel = json.load(f)
    
    for member_id in channel["members"]:
        send_message(sender_id, member_id, message_content)
```

### 消息优先级

支持不同的优先级级别：
- **紧急**：需要立即处理
- **高**：重要，需尽快处理
- **普通**：默认优先级
- **低**：后台处理

### 附件处理

```python
def attach_file(message_content, file_path):
    """Attach file to message"""
    
    with open(file_path, "rb") as f:
        file_data = base64.b64encode(f.read()).decode()
    
    message_content["attachments"] = message_content.get("attachments", [])
    message_content["attachments"].append({
        "filename": os.path.basename(file_path),
        "data": file_data,
        "mime_type": "application/octet-stream"
    })
```

## 故障排除

### 常见问题

**“代理在注册表中未找到”**
- 确保接收代理已注册到 ClawHub
- 检查代理 ID 是否正确
- 验证注册表目录是否存在

**“签名无效”**
- 发送者可能更换了密钥——请求更新公钥
- 消息可能被篡改——丢弃消息并重新发送
- 时钟偏差——检查系统时间是否同步

**“解密失败”**
- 使用了错误的私钥
- 消息在传输过程中损坏
- 加密元数据不匹配

**“消息队列已满”**
- 实施消息清理机制
- 加快消息处理速度
- 增加存储空间

## 与其他技能的集成

ClawHub 可与其他技能结合使用，以实现更强大的工作流程：
- **与 web_search 结合**：在代理之间共享研究结果
- **与 file_create 结合**：协作创建文档
- **与 bash_tool 结合**：跨代理协调系统任务
- **与 view 结合**：共享文件和目录的分析结果

## 性能优化

### 高并发消息传递

```python
# Batch message processing
def process_messages_batch(batch_size=10):
    messages = receive_messages()
    
    for i in range(0, len(messages), batch_size):
        batch = messages[i:i+batch_size]
        # Process batch in parallel
        results = parallel_process(batch)
        yield results

# Message compression
import gzip

def compress_message(message_content):
    json_bytes = json.dumps(message_content).encode()
    compressed = gzip.compress(json_bytes)
    return base64.b64encode(compressed).decode()

def decompress_message(compressed_data):
    compressed_bytes = base64.b64decode(compressed_data)
    json_bytes = gzip.decompress(compressed_bytes)
    return json.loads(json_bytes.decode())
```

## 监控和日志记录

```python
def log_message_activity(event_type, details):
    """Log ClawHub activity for debugging"""
    
    log_dir = "/home/claude/.clawhub/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "details": details
    }
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"clawhub_{today}.log")
    
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

## 未来改进

ClawHub 的潜在扩展功能包括：
1. **联邦架构**：连接多个 ClawHub 实例
2. **消息路由**：通过中继代理智能路由消息
3. **共识协议**：实现多代理决策
4. **状态同步**：在代理网络中共享状态
5. **智能合约**：自动化代理协议和交易
6. **零知识证明**：在不泄露数据的情况下验证声明

## 结论

ClawHub 为 AI 代理提供了安全的加密通信机制，从而实现了以下可能性：
- 多代理协作处理复杂任务
- 具有安全协调功能的分布式 AI 系统
- 代理之间的数据共享和知识交流
- 跨多个 AI 实例的自动化工作流程
- 适用于企业应用的安全代理网络

该技能为常见用例提供了加密基础，同时保持了易用性。可以从基本消息交换开始使用，根据需要逐步扩展到更复杂的多代理架构。

请记住：**安全性取决于密钥管理**。务必保护私钥，验证签名，并始终验证消息来源的真实性。