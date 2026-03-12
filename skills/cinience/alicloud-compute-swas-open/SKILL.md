---
name: alicloud-compute-swas-open
description: 端到端管理阿里云简单应用服务器（SWAS）的OpenAPI资源。支持查询实例信息、启动/停止/重启实例、执行命令（通过云助手）、管理磁盘/快照/镜像、防火墙规则/模板、密钥对、标签，以及进行监控和简单的数据库操作。
version: 1.0.0
---
**类别：服务**  
# 简单应用服务器（SWAS-OPEN 2020-06-01）  

使用 SWAS-OPEN OpenAPI 来管理所有的 SAS 资源：实例、磁盘、快照、镜像、密钥对、防火墙、Cloud Assistant、监控信息、标签以及轻量级数据库。  

## 先决条件  
- 准备一个具有最低权限的 RAM 用户/角色对应的 AccessKey。  
- 选择正确的区域和相应的端点（公共网络/虚拟私有云 VPC）。`ALICLOUD_REGION_ID` 可以作为默认区域；如果未设置，请选择最合适的区域，如有疑问请咨询用户。  
- 该 OpenAPI 支持 RPC 签名方式；建议使用 Python SDK 或 OpenAPI Explorer 而非手动签名。  

## SDK 优先级  
1) Python SDK（推荐）  
2) OpenAPI Explorer  
3) 其他 SDK  

### Python SDK 快速查询（实例 ID / IP / 计划）  
建议使用虚拟环境（以避免 PEP 668 规定的系统安装限制）。  

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install alibabacloud_swas_open20200601 alibabacloud_tea_openapi alibabacloud_credentials
```  

```python
import os
from alibabacloud_swas_open20200601.client import Client as SwasClient
from alibabacloud_swas_open20200601 import models as swas_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> SwasClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"swas.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
    return SwasClient(config)


def list_regions():
    client = create_client("cn-hangzhou")
    resp = client.list_regions(swas_models.ListRegionsRequest())
    return [r.region_id for r in resp.body.regions]


def list_instances(region_id: str):
    client = create_client(region_id)
    resp = client.list_instances(swas_models.ListInstancesRequest(region_id=region_id))
    return resp.body.instances


def main():
    for region_id in list_regions():
        for inst in list_instances(region_id):
            ip = getattr(inst, "public_ip_address", None) or getattr(inst, "inner_ip_address", None)
            spec = getattr(inst, "plan_name", None) or getattr(inst, "plan_id", None)
            print(inst.instance_id, ip or "-", spec or "-", region_id)


if __name__ == "__main__":
    main()
```  

### Python SDK 脚本（推荐用于资源清单和统计）  
- 所有区域的实例清单（TSV/JSON 格式）：`scripts/list_instances_all_regions.py`  
- 按计划统计实例数量：`scripts/summary_instances_by_plan.py`  
- 按状态统计实例数量：`scripts/summary_instances_by_status.py`  
- 修复基于 SSH 密钥的访问问题（支持自定义端口）：`scripts/fix_ssh_access.py`  
- 获取实例的当前 SSH 端口：`scripts/get_ssh_port.py`  

## CLI 使用说明  
- `aliyun` CLI 可能不会将 `swas-open` 显示为产品名称；建议优先使用 Python SDK。  
- 如果必须使用 CLI，请先在 OpenAPI Explorer 中生成请求示例，然后再切换到 CLI。  

## 工作流程  
1) 确认资源类型和区域（实例/磁盘/快照/镜像/防火墙/命令/数据库/标签）。  
2) 查阅 `references/api_overview.md` 以确定相应的 API 组和操作方法。  
3) 选择调用方式（Python SDK / OpenAPI Explorer / 其他 SDK）。  
4) 操作完成后，使用查询 API 验证状态和结果。  

## 常见操作列表  
- 实例查询/启动/停止/重启：`ListInstances`、`StartInstance(s)`、`StopInstance(s)`、`RebootInstance(s)`  
- 命令执行：`RunCommand` 或 `CreateCommand` + `InvokeCommand`；使用 `DescribeInvocations`/`DescribeInvocationResult`  
- 防火墙：`ListFirewallRules`/`CreateFirewallRule(s)`/`ModifyFirewallRule`/`EnableFirewallRule`/`DisableFirewallRule`  
- 快照/磁盘/镜像：`CreateSnapshot`、`ResetDisk`、`CreateCustomImage` 等  

## Cloud Assistant 使用说明  
- 目标实例必须处于运行状态。  
- 必须安装 Cloud Assistant 代理（使用 `InstallCloudAssistant`）。  
- 对于 PowerShell 命令，请确保 Windows 实例上安装了所需的模块。  
- 执行后，使用 `DescribeInvocations` 或 `DescribeInvocationResult` 获取状态和输出结果。  
详情请参阅 `references/command-assistant.md`。  

## 常见问题解答  
1. 目标区域是什么？是否需要使用 VPC 端点？  
2. 目标实例的 ID 是什么？它们当前是否处于运行状态？  
3. 需要使用哪种命令/脚本？适用于 Linux 还是 Windows？  
4. 是否需要批量执行或定时执行？  

## 输出策略  
如果需要保存结果或响应，请将输出文件保存到：`output/compute-swas-open/`  

## 验证规则  
- 命令执行成功时，命令的返回码应为 0，并且会生成 `output/alicloud-compute-swas-open/validate.txt` 文件。  

## 输出和证据保存  
- 将所有输出文件、命令结果以及 API 响应摘要保存在 `output/alicloud-compute-swas-open/` 目录下。  
- 在证据文件中包含关键参数（区域/资源 ID/时间范围），以便后续复现操作。  

## 先决条件  
- 在执行操作前，请配置最低权限的 Alibaba Cloud 凭据。  
- 建议使用环境变量：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`（可选 `ALICLOUD_REGION_ID`）。  
- 如果区域信息不明确，请在执行操作前咨询用户。  

## 工作流程  
1) 确认用户意图、目标区域、资源标识符以及操作类型（只读/修改）。  
2) 先执行一个最小的只读查询以验证连接性和权限。  
3) 使用明确的参数和有限的范围执行目标操作。  
4) 验证结果并保存输出文件和证据文件。  

## 参考资料  
- API 概述和操作组：`references/api_overview.md`  
- 端点和集成方式：`references/endpoints.md`  
- Cloud Assistant 使用说明：`references/command-assistant.md`  
- 官方资源列表：`references/sources.md`