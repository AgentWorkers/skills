---
name: trust-verifier
description: 验证技能的来源，并为 ClawHub 中的技能生成信任评分。该过程会检查技能的发布历史、版本一致性以及依赖关系的信任链，并生成相应的信任证明文件。
user-invocable: true
metadata: {"openclaw": {"emoji": "🔑", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 信任验证器（Trust Verifier）

信任，但需要验证。通过分析技能的发布者、历史记录、依赖关系以及代码的一致性来评估该技能的可靠性。

## 为何需要这个工具

安全扫描可以检测到已知的恶意行为模式，但对于那些技术上没有问题但由未知作者发布、版本历史不完整或依赖不受信任的包的技能，该怎么办呢？信任验证器填补了“未检测到漏洞”与“可以安全安装”之间的空白。

## 命令

### 评估某个技能目录的信任度
```bash
python3 {baseDir}/scripts/trust_verifier.py assess --path ~/.openclaw/skills/some-skill/
```

### 生成信任证明
```bash
python3 {baseDir}/scripts/trust_verifier.py attest --path ~/.openclaw/skills/some-skill/ --output trust.json
```

### 验证现有的信任证明
```bash
python3 {baseDir}/scripts/trust_verifier.py verify --attestation trust.json --path ~/.openclaw/skills/some-skill/
```

### 检查依赖关系的信任链
```bash
python3 {baseDir}/scripts/trust_verifier.py deps --path ~/.openclaw/skills/some-skill/
```

## 信任评估指标

- **发布者声誉**：是否为知名发布者；账户使用时长；发布的技能数量
- **版本一致性**：更新是否符合预期模式？是否存在突然的权限变更？
- **内容完整性**：所有文件的 SHA-256 哈希值是否一致；构建过程是否可重复
- **依赖关系链**：依赖的包是否来自可信来源？
- **社区反馈**：Moltbook 上的提及次数、用户评分以及来自社区的认可度

## 信任等级

- **已验证（VERIFIED）**：满足所有信任标准，信任证明有效
- **受信任（TRUSTED）**：大部分评估指标均为正面，仅存在轻微问题
- **未知（UNKNOWN）**：数据不足，无法评估信任度
- **可疑（SUSPICIOUS）**：一个或多个信任指标未通过
- **不可信（UNTRUSTED）**：多个信任指标未通过，切勿安装