---
name: zededa
description: 完整的 ZEDEDA 边缘管理 API 客户端——提供了 11 个服务领域的 473 个终端点，涵盖边缘节点、应用程序、集群、存储、网络、Kubernetes、诊断以及用户管理等功能。
author: Kristopher Clark <krisclarkdev@krisbox.org>
version: 1.0.0
homepage: https://github.com/krisclarkdev/zededa
license: MIT
files: ["scripts/*"]
metadata:
  clawdbot:
    requires:
      env:
        - ZEDEDA_API_TOKEN
    optional_env:
      - ZEDEDA_BASE_URL
      - ZEDEDA_LOG_LEVEL
---
# ZEDEDA Skill

这是一个用于ZEDEDA边缘计算管理平台的完整API客户端。它实现了11个服务域内的**473个端点**，支持Bearer令牌认证、自定义错误类型、结构化日志记录以及重试逻辑。

**作者：** Kristopher Clark  
**许可证：** MIT  
**版本：** 1.0.0

## 设置

主要工具是`scripts/zededa.py`。可以通过以下命令来运行它：

## 服务与命令

### 节点服务 (`node`) — 91个端点

用于管理边缘节点、硬件型号、项目、品牌以及PCR模板。

### 应用服务 (`app`) — 123个端点

用于管理应用程序包、实例（v1+v2）、镜像、工件、数据存储、卷以及补丁包。

### 用户服务 (`user`) — 67个端点

包括用户管理、角色管理、企业信息、会话管理、登录功能、凭证管理以及报告生成。

### 存储服务 (`storage`) — 33个端点

用于管理补丁包、认证策略以及部署策略。

### 编排服务 (`orchestration`) — 37个端点

用于管理集群实例、数据流、插件以及Azure部署相关操作。

### Kubernetes服务 (`k8s`) — 36个端点

用于管理Kubernetes部署、GitOps操作、Helm图表/仓库以及ZKS集群。

### 诊断服务 (`diag`) — 21个端点

用于获取设备配置信息、事件日志以及云健康状况。

### 应用配置服务 (`app-profile`) — 19个端点

用于管理应用程序配置及其状态。

### 网络服务 (`network`) — 16个端点

用于管理网络配置及网络状态。

### 作业服务 (`job`) — 17个端点

用于执行针对设备、应用程序及硬件型号的批量操作。

### 边缘节点集群服务 (`cluster`) — 13个端点

用于管理边缘节点集群的配置及状态。

## 程序化使用

所有473个端点都可以通过Python服务类进行访问。

## 安全性与隐私

### 外部端点

| URL | 发送的数据 | 目的 |
|:----|:----------|:--------|
| `https://zedcontrol.zededa.net/api` (可配置) | API令牌、请求数据 | 执行ZEDEDA API操作 |

### 数据处理

仅会将作为参数传递的数据以及`ZEDEDA_API_TOKEN`环境变量中的值发送到ZEDEDA API。令牌会在所有日志输出中经过清洗处理。除非使用了`--body-file`选项，否则不会读取或写入任何本地文件。

### 模型调用说明

此技能设计为可由OpenClaw代理自动调用。您也可以通过禁用该技能来选择不使用它。

### 信任声明

使用此技能时，发送的数据仅限于所提供的参数，并会直接发送给ZEDEDA。只有在您信任ZEDEDA能够妥善处理您提供的信息的情况下，才应安装此技能。