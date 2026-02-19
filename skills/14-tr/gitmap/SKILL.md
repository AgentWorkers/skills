# GitMap 技能

该技能为 ArcGIS Web 地图提供类似 Git 的版本控制功能，并以 OpenClaw 的原生工具形式进行封装。

## 概述

GitMap 为 ArcGIS Online 和 Enterprise Portal 的 Web 地图提供了类似 Git 的版本控制功能。它通过薄层 CLI 封装了 `gitmap` 命令行工具（CLI），使得分支管理、提交、差异对比、推送/拉取以及地图查询等操作变得易于使用。

**工具列表** | **功能说明** | **是否需要本地数据库** | **依赖包**  
---  
| `gitmap_list` | 列出 Portal 中可用的 Web 地图（支持过滤） | **不需要** | **无**  
| `gitmap_status` | 显示本地 GitMap 仓库的工作目录状态 | **不需要** | **无**  
| `gitmap_log` | 查看仓库的提交历史记录 | **不需要** | **无**  
| `gitmap_commit` | 提交当前地图的状态并附上说明 | **需要** | `gitmap-core` Python 包  
| `gitmap_branch` | 列出或创建仓库中的分支 | **需要** | `gitmap-core` Python 包  
| `gitmap_diff` | 显示提交或分支之间的差异 | **需要** | `gitmap-core` Python 包  
| `gitmap_push` | 将更改推送到 ArcGIS Portal | **需要** | `gitmap-core` Python 包  
| `gitmap_pull` | 从 ArcGIS Portal 拉取最新的地图数据 | **需要** | `gitmap-core` Python 包  

## 先决条件

### 安装 GitMap Core

```bash
pip install gitmap-core
```  

### 配置凭据

设置以下环境变量：  
```bash
export PORTAL_URL="https://your-org.maps.arcgis.com"
export ARCGIS_USERNAME="your_username"
export ARCGIS_PASSWORD="your_password"
```  

**安全提示：** 尽可能使用 API 令牌而非明文密码。  

## 必需的环境变量

- **PORTAL_URL**：你的 ArcGIS Portal 或 AGOL 的 URL（例如：`https://myorg.maps.arcgis.com`）  
- **ARCGIS_USERNAME**：Portal 的用户名  
- **ARCGIS_PASSWORD**：Portal 的密码（建议使用 API 令牌而非明文密码）  

## 工具说明

### 地图查询与状态检查

- `gitmap_list`：列出 Portal 中可用的 Web 地图（支持过滤）  
- `gitmap_status`：显示本地 GitMap 仓库的工作目录状态  
- `gitmap_log`：查看仓库的提交历史记录  

### 版本控制操作

- `gitmap_commit`：提交当前地图的状态并附上说明  
- `gitmap_branch`：列出或创建仓库中的分支  
- `gitmap_diff`：显示提交或分支之间的差异  

### 与 Portal 的同步

- `gitmap_push`：将更改推送到 ArcGIS Portal  
- `gitmap_pull`：从 ArcGIS Portal 拉取最新的地图数据  

## 工具参考

- `gitmap_list`：列出 Portal 中的 Web 地图。  
- `gitmap_status`：显示仓库的状态。  
- `gitmap_commit`：提交当前更改。  
- `gitmap_branch`：列出或创建分支。  
- `gitmap_diff`：显示版本之间的差异。  
- `gitmap_push`：将更改推送到 Portal。  
- `gitmap_pull`：从 Portal 拉取更改。  
- `gitmap_log`：查看提交历史记录。  

## 使用示例

- **查询地图并克隆**  
- **典型的编辑 → 提交 → 推送流程**  
- **特性分支的工作流程**  
- **查看提交历史记录**  

## 服务器配置

运行时，GitMap 服务通过 `localhost:7400` 提供 HTTP 服务：  
- **API 端点**：  
  - `POST /tools/{tool_name}`：使用 JSON 数据格式调用相应工具  
  - `GET /health`：进行健康检查  

## 安装说明

该技能直接使用 `gitmap_core` Python 包来访问 ArcGIS Portal 的 API。  

## 注意事项与限制

- **大多数命令都需要工作目录**——GitMap 仓库与 Git 一样基于目录结构。  
- **Portal 凭据** 可以在每次调用时传递，也可以通过环境变量（`PORTAL_URL`、`ARCGIS_USERNAME`、`ARCGIS_PASSWORD`）设置。  
- `gitmap_list` 不需要本地仓库，它直接查询 Portal 的数据。  
- **输出为原始的 CLI 文本**，部分情况下会进行简单解析以生成结构化的响应。  
- 该技能不支持 `clone`、`init` 等操作；`merge`、`checkout`、`l`、`setupsm`、`context-repos` 等功能需要直接调用相应的 CLI 命令来完成。  

## 相关资源

- GitMap 项目：[https://github.com/14-TR/gitmap](https://github.com/14-TR/gitmap)  
- Discord 频道：#gitmap