---
name: skillsign
version: 1.0.0
description: 使用 ed25519 密钥对代理技能文件夹进行签名和验证。检测篡改行为，管理受信任的作者，并追踪来源链（isnād）。
---

# skillsign

这是一个用于对代理技能文件夹进行加密签名和验证的工具，支持使用 ed25519 密钥。该工具可以保护您的技能文件不被篡改，并允许您验证文件的作者身份。

## 安装

```bash
pip3 install cryptography
```

这是该工具唯一的依赖项。整个工具仅包含一个 Python 文件。

## 命令

### 生成签名密钥对
```bash
python3 skillsign.py keygen
python3 skillsign.py keygen --name myagent
```
在 `~/.skillsign/keys/` 目录下生成一个 ed25519 密钥对。请公开分享 `.pub` 文件，而将 `.pem` 文件保密。

### 为技能文件夹签名
```bash
python3 skillsign.py sign ./my-skill/
python3 skillsign.py sign ./my-skill/ --key ~/.skillsign/keys/myagent.pem
```
对文件夹中的所有文件进行哈希处理（使用 SHA-256），生成文件清单（manifest），然后使用您的私钥对清单进行签名。签名完成后，会在文件夹内生成 `.skillsig/` 文件。

### 验证技能文件夹
```bash
python3 skillsign.py verify ./my-skill/
```
检测文件是否被修改、添加或删除，并验证文件的加密签名。同时会显示签名者的可信度。

### 查看签名元数据
```bash
python3 skillsign.py inspect ./my-skill/
```
显示签名者的信息（如指纹、时间戳、文件数量以及所有被签名的文件及其哈希值）。

### 将作者添加到可信列表
```bash
python3 skillsign.py trust ./their-key.pub
```
将某个作者的公钥添加到您的本地可信作者列表中。

### 查看可信作者列表
```bash
python3 skillsign.py trusted
```

### 查看签名历史记录（isnād）
```bash
python3 skillsign.py chain ./my-skill/
```
按顺序显示所有为该文件夹签名的作者信息。

## 使用场景

- **安装新技能后**：验证文件是否被篡改。
- **运行未经验证的代码前**：检查文件的签名者及其可信度。
- **定期**：重新验证技能文件夹，以检测未经授权的修改。
- **发布技能时**：为您的作品添加签名，以便他人确认其真实性。
- **审计代理的完整性时**：对所有技能文件夹执行验证操作。

## 示例工作流程

```bash
# First time: create your identity
python3 skillsign.py keygen --name parker

# Sign your skills
python3 skillsign.py sign ~/.openclaw/skills/my-skill/

# Later: check nothing changed
python3 skillsign.py verify ~/.openclaw/skills/my-skill/
# ✅ Verified — 14 files intact.
#    Signer: ca3458e92b73e432 [TRUSTED]

# Someone tampers with a file:
python3 skillsign.py verify ~/.openclaw/skills/my-skill/
# ❌ TAMPERED — Files changed since signing:
#    ~ main.py (modified)

# Trust another agent's key
python3 skillsign.py trust ./other-agent.pub

# View full provenance
python3 skillsign.py chain ~/.openclaw/skills/my-skill/
# === Isnād: my-skill/ (2 links) ===
#   [1] ca3458e92b73e432 [TRUSTED]
#       ↓
#   [2] f69159d8a25e8e32 [UNTRUSTED]
```