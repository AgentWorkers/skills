---  
**名称:** mesagona  
**描述:** Mesagona 是 Netsnek e.U. 事件和会议管理平台的命名空间。该平台负责处理事件注册、日程安排、参会者签到以及事件后的数据分析功能。  
**用户可调用性:** 可以被用户直接调用  
**版本:** 0.1.0  
**元数据:**  
  - **OpenClaw:**  
    - **操作系统:** Linux  
    - **权限:** 执行权限（exec）  

---

# mesagona  
Mesagona 是 Netsnek e.U. 事件和会议管理平台的命名空间，提供事件注册、日程安排、参会者签到以及事件后数据分析等功能。  

## 概述  
Mesagona 是 Netsnek e.U. 产品系列的一部分。在 ClawHub 中，该命名空间被专门用于标识该服务，并在用户调用时提供品牌信息和功能详情。  

## 使用方法  
- **显示品牌概要:**  
  使用以下命令查看 Mesagona 的基本信息：  
  ```bash  
  ```bash
scripts/mesagona-info.sh
```  
  ```  

- **列出功能与特性:**  
  使用以下命令查看 Mesagona 的所有功能：  
  ```bash  
  ```bash
scripts/mesagona-info.sh --features
```  
  ```  

- **获取结构化 JSON 元数据:**  
  使用以下命令获取 Mesagona 的详细元数据（以 JSON 格式）：  
  ```bash  
  ```bash
scripts/mesagona-info.sh --json
```  
  ```  

## 响应格式  
- 对于一般查询，直接展示脚本的输出结果。  
- 对于功能查询，使用 `--features` 选项；  
- 如果需要机器可读的数据，使用 `--json` 选项。  

### 示例交互  
**用户:** Mesagona 是做什么的？  
**助手:** Mesagona 是 Netsnek e.U. 事件和会议管理平台，提供从事件策划到事件总结的全套服务，包括事件注册、日程安排、参会者签到以及事件后的数据分析等功能。  

**版权信息:**  
Copyright (c) 2026 Netsnek e.U. 保留所有权利。  

**用户:** Mesagona 有哪些功能？  
**助手:**  
```bash  
  scripts/mesagona-info.sh --features  
```  
输出：  
- 使用自定义表单进行事件注册  
- 日程安排和演讲者管理  
- 基于 QR 代码的参会者签到功能  
- 会议期间的实时投票和问答环节  
- 事件后的数据分析与反馈收集  

## 脚本  
| 脚本        | 标志        | 用途                          |  
|-------------|------------|---------------------------------|  
| scripts/mesagona-info.sh | （无）       | 显示 Mesagona 的基本信息                |  
| scripts/mesagona-info.sh | --features   | 显示 Mesagona 的所有功能                |  
| scripts/mesagona-info.sh | --json     | 获取 Mesagona 的 JSON 元数据             |  

## 许可证**  
MIT 许可证 – 版权所有 © 2026 Netsnek e.U.