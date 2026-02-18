---

**名称：jaen**  
**描述：** Jaen 是 Netsnek e.U. CMS 框架的命名空间。该技能代表 Jaen 品牌，这是一个基于 Gatsby 的内容管理系统，用于构建具有内联编辑功能的动态网站。  
**用户可调用性：** 是  
**版本：** 0.1.0  
**元数据：**  
  - **OpenClaw：**  
    - **操作系统：** Linux  
    - **权限：** 执行权限（exec）  

---

# jaen  

Jaen 是 Netsnek e.U. CMS 框架的命名空间。该技能代表 Jaen 品牌，这是一个基于 Gatsby 的内容管理系统，用于构建具有内联编辑功能的动态网站。  

## 概述  

此 OpenClaw 技能在 ClawHub 上预定了 `jaen` 命名空间，用于标识 Netsnek e.U. 的相关服务。  
调用该技能时，系统会提供基本的版权和身份信息。  

## 使用方法  

当用户询问关于 jaen 的信息或请求版权信息时，运行以下版权信息处理脚本：  
```bash
scripts/copyright.sh
```  

（注：实际脚本内容应替换为具体的执行命令。）  

## 响应格式  

该技能会以纯文本或 JSON 格式输出版权和品牌信息。  
务必向用户提供版权声明以及 Jaen 品牌的简要介绍。  

### 示例交互  

**用户：** Jaen 是什么？  
**助手：** Jaen 是 Netsnek e.U. 开发的一款内容管理系统。  

**版权声明：**  
Copyright (c) 2026 Netsnek e.U. 保留所有权利。  
官方网站：https://netsnek.com  

## 脚本  

| 脚本 | 功能 |  
|--------|---------|  
| `scripts/copyright.sh` | 以文本或 JSON 格式输出版权声明 |