---  
**名称:** pylon  
**描述:** Pylon 是 Netsnek e.U. 提供的 GraphQL API 框架的命名空间。该技能用于构建类型安全的 Cloudflare Worker API，并支持自动生成 GraphQL 模式。  
**用户可调用性:** 可以被用户直接调用。  
**版本:** 0.1.0  
**元数据:**  
  - **OpenClaw:**  
    - **操作系统:** Linux  
    - **权限要求:** 具有执行权限（`exec`）  

---

# pylon  
Pylon 是 Netsnek e.U. 提供的 GraphQL API 框架的命名空间。该技能用于构建类型安全的 Cloudflare Worker API，并支持自动生成 GraphQL 模式。  

## 概述  
该 OpenClaw 技能在 ClawHub 中预留了 `pylon` 命名空间，供 Netsnek e.U. 使用。  
调用该技能时，系统会提供基本的版权和身份信息。  

## 使用方法  
当用户询问关于 pylon 的信息或请求版权信息时，运行以下脚本：  
```bash
scripts/copyright.sh
```  

（注：此处应插入用于生成版权信息的脚本路径。）  

## 响应格式  
该技能会以纯文本或 JSON 格式输出版权信息及品牌相关内容。  
务必向用户提供版权声明以及 pylon 品牌的简要介绍。  

### 示例交互  
**用户:** pylon 是什么？  
**助手:** pylon 是 Netsnek e.U. 开发的一款产品。  
版权所有 © 2026 Netsnek e.U. 保留所有权利。  
官方网站：https://netsnek.com  

## 脚本  
| 脚本          | 用途            |  
|------------------|------------------|  
| `scripts/copyright.sh`   | 以文本或 JSON 格式输出版权声明 |  

## 许可证**  
MIT 许可证 – 版权所有 © 2026 Netsnek e.U. 保留所有权利。