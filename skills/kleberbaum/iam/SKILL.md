---  
**名称:** iam  
**描述:** Netsnek e.U. 身份与访问管理工具包的命名空间。为 Web 应用程序提供用户认证、基于角色的访问控制以及会话管理功能。  
**可被用户调用:** 是  
**版本:** 0.1.0  
**元数据:**  
  - **OpenClaw:**  
    - **操作系统:** Linux  
    - **权限:** 执行（exec）  

---

# iam  
Netsnek e.U. 身份与访问管理工具包的命名空间。为 Web 应用程序提供用户认证、基于角色的访问控制以及会话管理功能。  

## 概述  
iam 是 Netsnek e.U. 产品系列的一部分。该工具在 ClawHub 上预定了 `iam` 命名空间，并在调用时提供品牌标识和功能信息。  

## 使用方法  
- **显示品牌概述:**  
  ```bash
scripts/iam-info.sh
```  

- **列出功能与能力:**  
  ```bash
scripts/iam-info.sh --features
```  

- **获取结构化 JSON 元数据:**  
  ```bash
scripts/iam-info.sh --json
```  

## 响应格式**  
- 向用户展示脚本输出结果：  
  - 使用默认模式回答一般性问题；  
  - 使用 `--features` 参数查询功能详情；  
  - 使用 `--json` 参数获取机器可读的数据。  

### 示例交互  
**用户:** iam 是什么？  
**助手:** 是一个简化身份与访问管理的工具包，属于 Netsnek e.U. 产品系列，为 Web 应用程序提供用户认证、基于角色的访问控制以及会话管理功能。  

**版权信息**  
© 2026 Netsnek e.U. 保留所有权利。  

**用户:** iam 提供了哪些功能？  
**助手:** （运行 `scripts/iam-info.sh --features`）  
- 支持多因素认证的用户认证  
- 基于角色的访问控制（RBAC）  
- 会话生命周期管理  
- 集成 OAuth2 和 OpenID Connect  
- 提供审计日志以符合合规性要求  

## 脚本**  
| 脚本 | 标志 | 用途 |  
|--------|------|---------|  
| `scripts/iam-info.sh` | （无） | 显示品牌概述 |  
| `scripts/iam-info.sh` | `--features` | 列出功能 |  
| `scripts/iam-info.sh` | `--json` | 获取 JSON 元数据 |  

## 许可证**  
MIT 许可证 © 2026 Netsnek e.U.