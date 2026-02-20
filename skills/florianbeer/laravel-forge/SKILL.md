---
name: laravel-forge
description: 通过 Forge API，您可以管理 Laravel Forge 服务器、网站、部署环境、数据库以及各种集成功能等。
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: [LARAVEL_FORGE_API_TOKEN]
    credentials:
      primary:
        env: LARAVEL_FORGE_API_TOKEN
        file: ~/.openclaw/credentials/laravel-forge/config.json
        description: Laravel Forge API token + default org (generate at forge.laravel.com → Profile → API)
    scripts:
      laravel-forge:
        path: scripts/laravel-forge.sh
        description: Laravel Forge CLI wrapper
---
# Laravel Forge API 使用指南

本文档将 Laravel Forge 的 API（https://forge.laravel.com/docs/api-reference/introduction）封装成一个简单的 Bash 脚本，采用 JSON:API 格式进行交互。该脚本仅适用于特定组织（organization）范围内的操作。

## 设置

**选项 1 — 环境变量：**
（请参考相应的代码块内容）

**选项 2 — 凭据文件（推荐使用）：**
（请参考相应的代码块内容）

您可以在 [forge.laravel.com → Profile → API] 生成 API 密钥。`org` 字段是可选的；如果省略，CLI 会自动检测您的第一个组织。如果您拥有多个组织或希望跳过额外的 API 调用，请明确设置该字段。您也可以通过 `--org` 参数在命令级别进行覆盖。

## 使用方法

（请参考相应的代码块内容）

所有命令都支持使用 `--org ORG_SLUG` 参数来覆盖默认的组织名称。

## 资源概览

| 资源          | 描述                                      |
|---------------|-------------------------------------------|
| `user`        | 当前用户信息                                      |
| `organizations`    | 组织列表/查询                                   |
| `providers`     | 云服务提供商信息（地区、资源规模等）                        |
| `servers`      | 服务器管理（创建、删除、事件处理、归档等）                        |
| `services`     | 服务管理（Nginx、MySQL、PostgreSQL、Redis、PHP、Supervisor 等）            |
| `php`        | PHP 版本管理及配置（CLI/FPM/进程池配置、OPcache）                   |
| `background-processes` | 后台进程管理（Supervisor 服务）                        |
| `firewall`      | 防火墙规则设置                                  |
| `jobs`        | 计划任务（服务器级和站点级）                               |
| `keys`        | SSH 密钥管理                                    |
| `databases`     | 数据库架构及用户管理                               |
| `db-users`     | 数据库用户管理                                   |
| `backups`      | 备份配置及管理                                 |
| `monitors`     | 服务器监控（CPU、内存、磁盘使用情况）                         |
| `nginx-templates`   | Nginx 模板配置                                |
| `logs`        | 服务器日志管理                                   |
| `sites`       | 站点管理                                    |
| `domains`      | 站点域名管理                                   |
| `composer-credentials` | 站点特定的 Composer 凭据                         |
| `npm-credentials` | 站点特定的 NPM 凭据                         |
| `heartbeats`     | 站点心跳检测                                   |
| `deployments`    | 部署配置及脚本管理                             |
| `webhooks`     | 部署触发器配置                               |
| `commands`     | 在站点上运行命令                                 |
| `redirects`    | 重定向规则配置                               |
| `security`     | 安全设置（基于 HTTP 基本认证）                         |
| `integrations`   | Laravel 集成（Horizon、Octane、Reverb、Pulse 等）                |
| `recipes`     | 配置模板及部署流程                             |
| `storage-providers` | 备份存储服务提供商                             |
| `teams`       | 团队管理                                    |
| `roles`       | 权限管理                                    |
| `server-credentials` | 服务器访问凭证及 VPC 配置                         |

## 快速示例

### 用户与组织管理
（请参考相应的代码块内容）

### 服务器管理
（请参考相应的代码块内容）

### PHP 配置管理
（请参考相应的代码块内容）

### 站点管理
（请参考相应的代码块内容）

### 域名管理
（请参考相应的代码块内容）

### 部署管理
（请参考相应的代码块内容）

### 集成管理
（请参考相应的代码块内容）

### 命令执行
（请参考相应的代码块内容）

### 数据库管理
（请参考相应的代码块内容）

### 备份管理
（请参考相应的代码块内容）

### 防火墙配置
（请参考相应的代码块内容）

### 计划任务管理
（请参考相应的代码块内容）

### 配置模板管理
（请参考相应的代码块内容）

### 团队管理
（请参考相应的代码块内容）

### 存储服务管理
（请参考相应的代码块内容）

### 服务管理
（请参考相应的代码块内容）

### 帮助文档
（请参考相应的代码块内容）

## 资源层次结构

**顶级资源**（无需指定组织或服务器）：
- `user`        |
- `providers`     |

**组织级资源：**
- `organizations`    |
- `recipes`     |
- `storage-providers` |
- `teams`       |
- `roles`       |
- `server-credentials` |

**服务器级资源：**
- `servers`      |
- `services`     |
- `php`        |
- `background-processes` |
- `firewall`      |
- `jobs`        |
- `keys`        |
- `databases`     |
- `db-users`     |
- `backups`      |
- `monitors`     |
- `nginx-templates`   |
- `logs`        |

**站点级资源：**
- `sites`       |
- `domains`      |
- `composer-credentials` |
- `npm-credentials` |
- `heartbeats`     |
- `deployments`    |
- `webhooks`     |
- `commands`     |
- `redirects`    |
- `security`     |
- `integrations`   |
- `jobs`        |

## 所需依赖库

- `curl`        | 用于发送 HTTP 请求                      |
- `jq`        | 用于解析 JSON 数据                      |

## 注意事项：

- 所有路径均属于特定组织范围（`org` 参数指定范围内）（`user`、`providers` 以及预定义的角色/权限除外）。
- 服务相关操作使用 POST 请求，请求体格式为 `{"action":"..."}`。
- 域名证书现在按站点而非组织进行管理。
- PHP 配置管理功能得到显著增强（包括 CLI/FPM/进程池配置、PHP 版本管理）。
- 支持与 Laravel 的所有主要第三方包集成。
- 团队和角色机制提供了细粒度的访问控制。