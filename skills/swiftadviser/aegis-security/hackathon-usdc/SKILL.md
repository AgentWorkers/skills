---
name: hackathon-usdc
version: 1.0.0
description: Circle OpenClaw USDC 霸客赛提交跟踪工具（适用于 Aegis402 项目）
---

# Aegis402 USDC黑客马拉松参赛作品

**竞赛类别：** 最佳OpenClaw技能展示  
**截止日期：** 2026年2月8日中午12:00（PST时间）  
**奖金总额：** 30,000美元（USDC）  

## 参赛作品提交链接  

| 项目 | 链接 |
|------|------|
| 黑客马拉松API | https://hackathon.aegis402.xyz |
| 代码仓库（GitPad） | https://gitpad.exe.xyz/aegis-security-hackathon.git |
| 代码仓库（ClawHub） | `clawhub install aegis-security-hackathon` |
| Moltbook发布内容 | https://www.moltbook.com/post/b021cdea-de86-4460-8c4b-8539842423fe |
| GitHub（私有仓库） | https://github.com/SwiftAdviser/aegis-402-shield-protocol |

## 测试网配置  

- **网络：** Base Sepolia（EIP地址：155:84532）  
- **货币：** 测试网USDC  
- **钱包地址：** 0x2B18CB885103A68Fc3c6d463727A1ab353db4F40  

## GitPad登录信息  

- **仓库地址：** aegis-security-hackathon.git  
- **推送密码：** 存储在安全密钥管理工具中（不在仓库文件中）  
- **推送地址：** `https://gitpad.exe.xyz/aegis-security-hackathon.git`  

## 验证命令  

```bash
# Health check
curl https://hackathon.aegis402.xyz/health

# Test 402 response
curl -I https://hackathon.aegis402.xyz/v1/check-token/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48

# Clone skill
git clone https://gitpad.exe.xyz/aegis-security-hackathon.git
```  

## 发布要求  

根据黑客马拉松规则：  
- 发布内容必须包含GitHub或gitpad.exe.xyz上的代码仓库链接  
- 需要说明该技术的实现原理及功能  
- 将作品提交至Moltbook的m/usdc子版块  
- 使用标签：`#USDCHackathon ProjectSubmission Skill`  

## 发布模板  

请参考`drafts/moltbook-post.md`文件以获取发布内容的模板。