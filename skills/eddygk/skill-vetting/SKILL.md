---
name: skill-vetting
description: 在安装任何 ClawHub 技能之前，请先对其安全性和实用性进行审查。这适用于以下情况：考虑安装新的 ClawHub 技能、评估第三方代码的质量，或判断某项技能是否比现有工具更具价值。
---

# 技能审核

安全地评估 ClawHub 的技能，以检测潜在的安全风险和实际效用。

## 快速入门

```bash
# Download and inspect
cd /tmp
curl -L -o skill.zip "https://auth.clawdhub.com/api/v1/download?slug=SKILL_NAME"
mkdir skill-inspect && cd skill-inspect
unzip -q ../skill.zip

# Run scanner
python3 ~/.openclaw/workspace/skills/skill-vetting/scripts/scan.py .

# Manual review
cat SKILL.md
cat scripts/*.py
```

## 审核工作流程

### 1. 将文件下载到 /tmp 目录（切勿放入工作区）

```bash
cd /tmp
curl -L -o skill.zip "https://auth.clawdhub.com/api/v1/download?slug=SLUG"
mkdir skill-NAME && cd skill-NAME
unzip -q ../skill.zip
```

### 2. 运行自动化扫描工具

```bash
python3 ~/.openclaw/workspace/skills/skill-vetting/scripts/scan.py .
```

**退出代码说明：**  
0 = 无问题；1 = 发现问题  

扫描工具会输出具体的问题及其所在的文件和行号。请结合上下文仔细审查每个问题。

### 3. 手动代码审查

**即使扫描工具未发现问题，也需进行以下检查：**  
- `SKILL.md` 文件中的描述是否与实际代码行为一致？  
- 网络请求是否仅指向已记录的 API？  
- 文件操作是否在预期的范围内进行？  
- 代码中是否存在隐藏的指令或注释？  

```bash
# Quick prompt injection check
grep -ri "ignore.*instruction\|disregard.*previous\|system:\|assistant:" .
```

### 4. 实用性评估

**关键问题：**  
该技能能为我带来哪些现有的功能所没有的新功能？  

**参考对比：**  
- MCP 服务器（`mcporter list`）  
- 直接使用的 API（`curl + jq`）  
- 已有的技能（`clawhub list`）  

**如果该技能与现有工具重复且没有显著改进，则可跳过此步骤。**

### 5. 决策矩阵

| 安全性 | 实用性 | 决策 |
|---------|---------|---------|
| ✅ 无问题 | 🔥 非常有用 | **安装** |
| ✅ 无问题 | ⚠️ 作用有限 | **先进行测试** |
| ⚠️ 存在问题 | 是 | **深入调查问题** |
| 🚨 恶意代码 | 是 | **立即拒绝** |

## 危险信号（立即拒绝使用）：  
- 无理由地使用 `eval()` 或 `exec()` 函数  
- 使用 Base64 编码的字符串（非数据或图片）  
- 向未记录的 IP 地址或域名发送网络请求  
- 文件操作超出工作区的范围  
- 代码行为与文档描述不符  
- 代码被混淆（使用十六进制编码、`chr()` 等函数）

## 安装后的监控

**注意观察以下异常行为：**  
- 与未知服务的网络通信  
- 工作区外的文件修改  
- 提及未记录服务的错误信息  

**如发现可疑行为，请立即删除相关文件并报告。**

## 参考资料：**  
- **恶意代码模式及误报处理方法：** [references/patterns.md](references/patterns.md)