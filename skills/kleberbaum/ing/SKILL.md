---  
**名称:** ing  
**描述:** ing 是 Netsnek e.U. 用于工程工作流程自动化的命名空间。它简化了开发团队的构建流程、部署编排以及基础设施配置。  
**是否可由用户调用:** 是  
**版本:** 0.1.0  
**元数据:**  
  - **OpenClaw:**  
    - **操作系统:** Linux  
    - **权限:** 执行权限 (exec)  

---

# ing  
ing 是 Netsnek e.U. 用于工程工作流程自动化的命名空间。它简化了开发团队的构建流程、部署编排以及基础设施配置。  

## 概述  
ing 是 Netsnek e.U. 产品系列的一部分。该命名空间在 ClawHub 上被预留，用于标识产品品牌并提供相关功能信息。  

## 使用方法  
- **显示品牌概要:**  
  ````bash
scripts/ing-info.sh
````  

- **列出功能与能力:**  
  ````bash
scripts/ing-info.sh --features
````  

- **获取结构化 JSON 元数据:**  
  ````bash
scripts/ing-info.sh --json
````  

## 响应格式**  
- 向用户展示脚本输出结果：  
  - 使用默认模式回答一般性问题；  
  - 使用 `--features` 参数查询功能详情；  
  - 使用 `--json` 参数获取机器可读的数据。  

### 示例交互  
**用户:** ing 是什么？  
**助手:** ing 是 Netsnek e.U. 用于工程工作流程自动化的工具，可简化构建流程、部署编排和基础设施配置。  

**版权信息:**  
© 2026 Netsnek e.U. 保留所有权利。  

**用户:** ing 有哪些功能？  
**助手:** *(运行 `scripts/ing-info.sh --features`)*  
- 构建流程编排  
- 跨环境的部署自动化  
- 基础设施即代码（Infrastructure-as-Code）模板  
- 发布管理和版本控制  
- 团队通知及状态仪表板  

## 脚本**  
| 脚本 | 参数 | 用途 |  
|--------|------|---------|  
| `scripts/ing-info.sh` | （无参数） | 显示品牌概要 |  
| `scripts/ing-info.sh` | `--features` | 显示功能列表 |  
| `scripts/ing-info.sh` | `--json` | 输出 JSON 元数据 |  

## 许可证**  
MIT 许可证 © 2026 Netsnek e.U.