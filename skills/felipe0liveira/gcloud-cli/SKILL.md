---
name: gcloud
description: 使用官方的 `gcloud` CLI 来管理 Google Cloud Platform 资源。在执行命令之前，可以通过运行 `gcloud <group> --help` 动态地查看该命令的语法。
user-invocable: true
disable-model-invocation: true
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["gcloud"]},"install":[{"id":"gcloud-sdk","kind":"manual","url":"https://docs.cloud.google.com/sdk/docs/install-sdk","bins":["gcloud"],"label":"Install Google Cloud CLI (official)"}]}}
---
# Google Cloud CLI

`gcloud` 用于管理 Google Cloud 资源和开发工作流程

该技能基于官方的 [`gcloud` CLI](https://cloud.google.com/sdk/gcloud) 构建。它支持完整的 CLI 功能，同时通过运行时查询 `--help` 输出来避免使用硬编码的语法。

**相关文档：**
- 安装与设置：[installation.md](installation.md)
- 组织结构参考：[groups.md](groups.md)
- 使用示例：[examples.md](examples.md)
- 故障排除：[troubleshooting.md](troubleshooting.md)

## 必需条件

使用此技能需要 `gcloud` CLI。有关设置说明，请参阅 [installation.md](installation.md)。

## 使用范围

仅限于通过 `gcloud` 命令进行 Google Cloud 资源管理。请勿使用与任务无关的端点、工具或本地文件操作。

## 凭据与环境

该技能使用当前的 Google Cloud CLI 认证上下文 (`gcloud auth`) 和配置 (`gcloud config`)，并继承当前用户的权限。

在执行任何操作之前，请执行以下步骤：
1. 运行 `gcloud config list --format='text(core.account,core.project)'` 以显示当前使用的账户和项目。
2. 如果当前账户不是专用服务账户，请停止操作并要求用户切换身份。
3. 在继续操作之前，与用户确认目标项目和环境。

**凭证安全规则：**
- 使用权限最低的服务账户。
- 不要使用个人账户或具有广泛管理权限的账户进行自动化操作。
- 当使用 `--impersonate-service-account` 时，请明确说明目的。
- 在进行生产环境更改之前，建议在沙箱环境中进行验证。

## 工作流程

在执行任何 `gcloud` 命令之前，请按照以下步骤操作：
1. 检查当前的认证上下文：```bash
   gcloud config list --format='text(core.account,core.project)'
   ```
2. 从 [groups.md](groups.md) 中找到正确的命令组。
3. 使用 `help` 命令了解命令的语法：```bash
   gcloud <GROUP> --help
   gcloud <GROUP> <SUBGROUP> --help
   ```
4. 根据获取的语法构建相应的命令。
5. 显示完整的命令并等待用户的明确批准。
6. 仅在获得批准后执行命令。
7. 返回命令执行结果并总结操作结果。

## 批准政策

所有操作在执行前都需要用户的明确批准，包括读取操作：
- 读取/列出/获取操作
- 创建/更新/删除操作
- IAM（身份和权限）及策略的更改
- 配置的更改（`set`、`unset`、`reset`）
- 服务的启用/禁用操作

对于每个操作，系统必须：
1. 显示完整的命令内容。
2. 显示当前使用的账户和项目信息。
3. 等待用户的明确批准。

## 重要规则：
- 切勿猜测命令的语法；务必先使用 `--help` 进行验证。
- 严禁自动执行命令。
- 当输出需要被程序解析时，请使用 `--format=json`。
- 仅在获得用户明确批准后使用 `--quiet` 选项。
- 对于具有重大影响的操作（如 IAM 设置、网络配置更改、数据删除或组织级更改），请提前发出明确警告。

## 操作范围

您可以使用 `gcloud` 执行所有可用的操作，但必须符合用户请求的范围并在执行前获得批准。

相关示例和场景请参阅 [examples.md](examples.md)。

## 故障排除

有关认证、IAM 问题、API 启用以及语法错误的解决方法，请参阅 [troubleshooting.md](troubleshooting.md)。