---
name: hippius
description: Hippius去中心化存储系统运行在Bittensor子网75上，支持通过兼容S3的API上传文件、查询存储状态、管理存储桶。适用于以下场景：用户需要将文件上传至Hippius系统、查看存储状态、设置Hippius的访问凭据、列出所有存储桶或文件，或对比IPFS与S3的存储方案。
---

# Hippius 存储服务

Hippius 是基于 Bittensor SN75 架构的分布式云存储服务，提供与 S3 兼容的 API。

**推荐使用路径：** S3 端点（`s3.hippius.com`）—— 公共 IPFS 节点已弃用。

## 快速参考

| 关键参数 | 值         |
|---------|------------|
| S3 端点    | `https://s3.hippius.com` |
| S3 区域    | `decentralized`   |
| 访问密钥格式 | `hip_xxxxxxxxxxxx` |
| 控制台    | [console.hippius.com](https://console.hippius.com) |
| Python CLI  | `pip install hippius`（需要自托管的 IPFS 节点） |

## 设置

1. 从 [console.hippius.com](https://console.hippius.com/dashboard/settings) 的“设置”→“API 密钥”中获取 S3 凭据。
2. 设置环境变量：
   ```bash
   export HIPPIUS_S3_ACCESS_KEY="hip_your_access_key"
   export HIPPIUS_S3_SECRET_KEY="your_secret_key"
   ```
3. 测试：`aws --endpoint-url https://s3.hippius.com --region decentralized s3 ls`

## 常用操作

### 上传文件
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized \
    s3 cp <file> s3://<bucket>/<key>
```

### 下载文件
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized \
    s3 cp s3://<bucket>/<key> <local_path>
```

### 列出桶
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized s3 ls
```

### 列出对象
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized s3 ls s3://<bucket>/ --recursive
```

### 创建桶
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized s3 mb s3://<bucket>
```

### 同步目录
```bash
aws --endpoint-url https://s3.hippius.com --region decentralized \
    s3 sync ./local-dir/ s3://<bucket>/remote-dir/
```

## Python（使用 boto3 库）

```python
import boto3
import os

s3 = boto3.client(
    's3',
    endpoint_url='https://s3.hippius.com',
    aws_access_key_id=os.environ['HIPPIUS_S3_ACCESS_KEY'],
    aws_secret_access_key=os.environ['HIPPIUS_S3_SECRET_KEY'],
    region_name='decentralized'
)

# Upload
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# Download
s3.download_file('my-bucket', 'remote.txt', 'downloaded.txt')

# List
for obj in s3.list_objects_v2(Bucket='my-bucket').get('Contents', []):
    print(f"{obj['Key']} ({obj['Size']} bytes)")
```

## 脚本

- `scripts/query_storage.py` — 查询 S3 桶和对象信息，以及 RPC 账户信息

使用方法：
```bash
# List S3 buckets
python scripts/query_storage.py --s3-buckets

# List objects in bucket
python scripts/query_storage.py --s3-objects my-bucket

# Query blockchain credits (requires account address)
python scripts/query_storage.py --account 5Grwva... --credits
```

## 参考资料

- `references/storage_guide.md` — S3 与 IPFS 的对比，代码示例（Python、JavaScript）
- `references/cli_commands.md` — `hippius` CLI 使用手册（需要自托管的 IPFS 节点）

## 故障排除

**“公共存储服务 hippius.network 已被弃用”**
请改用 S3。`hippius` CLI 的 IPFS 命令需要自托管的 IPFS 节点。

**S3 认证错误**
- 访问密钥必须以 `hip_` 开头。
- 区域必须设置为 `decentralized`（不能是 `us-east-1`）。
- 端点必须设置为 `https://s3.hippius.com`。

## 外部链接

- [Hippius 文档](https://docs.hippius.com)
- [Hippius 控制台](https://console.hippius.com)
- [Hippius 统计数据](https://hipstats.com)
- [Hippius CLI GitHub 仓库](https://github.com/thenervelab/hippius-cli)