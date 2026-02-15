---
name: stratos-storage
description: >
  Upload and download files to/from Stratos Decentralized Storage (SDS) network.
  Use when the user wants to store files on Stratos, retrieve files from Stratos,
  upload to decentralized storage, or download from SDS.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [STRATOS_SPFS_GATEWAY, STRATOS_NODE_DIR]
      bins: [curl]
    primaryEnv: STRATOS_SPFS_GATEWAY
---

# Stratos去中心化存储

## 使用场景
- 用户希望将文件上传到Stratos SDS网络
- 用户希望通过文件哈希或共享链接从Stratos SDS下载文件
- 用户提及“Stratos”、“SDS”、“SPFS”或“去中心化存储上传/下载”

## 操作步骤

### 上传文件
1. 确认ppd或SPFS网关是否可用
2. 运行上传脚本：`bash $SKILL_DIR/scripts/upload.sh <file_path>`
3. 将文件哈希（CID）返回给用户

### 下载文件
1. 确认ppd或SPFS网关是否可用
2. 运行下载脚本：`bash $SKILL_DIR/scripts/download.sh <file_hash_or_cid> <output_path>`
3. 确认下载成功

## 示例
上传文件：
→ 命令：`bash scripts/upload.sh /tmp/report.pdf`
→ 输出：文件已上传。CID：Qm...xxx

下载文件：
→ 命令：`bash scripts/download.sh Qm...xxx ~/Downloads/report.pdf`
→ 输出：文件已下载到~/Downloads/report.pdf

## 限制条件
- 上传前务必与用户确认文件路径
- 未经用户确认，切勿覆盖现有文件
- 操作前请确认SDS节点正在运行
- 大文件可能需要较长时间完成下载；请向用户反馈下载进度