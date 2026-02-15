---
name: awscli
description: "使用 AWS CLI 管理 AWS Lightsail 和 EC2 实例"
version: 1.0.0
author: RajithSanjaya
---

# AWS CLI 控制技能

此技能用于管理 AWS Lightsail 实例。

## 要求

- 主机上已安装 AWS CLI
- 配置了 AWS 凭据（IAM 用户或角色）
- 需要以下环境变量：

  - AWS_REGION
  - ALLOWED_INSTANCES

## 环境变量

此技能需要以下环境变量：

- AWS_REGION（例如：ap-southeast-1）
- ALLOWED_INSTANCES（以逗号分隔的实例名称列表）

示例：

AWS_REGION=ap-southeast-1
ALLOWED_INSTANCES=Ubuntu,Binami

## 可用的操作

### 1. 列出实例

操作：`list`

示例：
{
  "action": "list"
}

---

### 2. 重启实例

操作：`reboot`  
实例：`<实例名称>`

示例：
{
  "action": "reboot",
  "instance": "Ubuntu-1"
}

---

### 3. 启动实例

操作：`start`  
实例：`<实例名称>`

---

### 4. 停止实例

操作：`stop`  
实例：`<实例名称>`

---

## 注意事项

- 仅使用结构化的 JSON 输入。
- 请勿自动生成 AWS CLI 命令。
- 实例名称必须与现有的 Lightsail 实例完全匹配。