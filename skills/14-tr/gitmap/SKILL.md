# GitMap 技能

**功能简介：**  
GitMap 为 ArcGIS Web 地图提供类似 Git 的版本控制功能，这些功能以 OpenClaw 的原生工具形式对外提供。

## 概述  
GitMap 为 ArcGIS Online 和 Enterprise Portal 中的 Web 地图提供了 Git 风格的版本控制功能。该技能通过封装 `gitmap` CLI 命令，将其作为轻量级的子进程调用，从而实现了分支管理、提交、差异比较、推送/拉取以及地图信息查询等操作。

**支持的工具：**  
- `gitmap_list`  
- `gitmap_status`  
- `gitmap_commit`  
- `gitmap_branch`  
- `gitmap_diff`  
- `gitmap_push`  
- `gitmap_pull`  
- `gitmap_log`  

**特点：**  
- **无需本地数据库**  
- **依赖 `gitmap-core` Python 包**  

## 先决条件  

### 安装 GitMap Core  
（安装命令请参考相关文档或 GitHub 仓库。）  

### 配置凭据  
请设置以下环境变量：  
- `PORTAL_URL`：您的 ArcGIS Portal 或 AGOL URL  
- `ARCGIS_USERNAME`：Portal 用户名  
- `ARCGIS_PASSWORD`：Portal 密码（建议使用 API 令牌而非明文密码）  

## 必需的环境变量：  
- `PORTAL_URL`：您的 ArcGIS Portal 或 AGOL URL（例如：`https://myorg.maps.arcgis.com`）  
- `ARCGIS_USERNAME`：Portal 用户名  
- `ARCGIS_PASSWORD`：Portal 密码（推荐使用 API 令牌）  

## 工具说明：  

### 地图信息查询与状态显示  
- `gitmap_list`：列出 Portal 中可用的 Web 地图（支持可选过滤条件）  
- `gitmap_status`：显示本地 GitMap 仓库的工作目录状态  
- `gitmap_log`：查看仓库的提交历史记录  

### 版本控制操作  
- `gitmap_commit`：提交当前地图的状态并附上注释  
- `gitmap_branch`：列出或创建仓库中的分支  
- `gitmap_diff`：显示提交或分支之间的差异  

### 与 Portal 的同步  
- `gitmap_push`：将已提交的更改推送到 ArcGIS Portal  
- `gitmap_pull`：从 ArcGIS Portal 拉取最新的地图数据  

## 工具参考：  
- `gitmap_list`：查询 Portal 中的 Web 地图  
- `gitmap_status`：显示仓库的状态  
- `gitmap_commit`：提交当前更改  
- `gitmap_branch`：列出或创建分支  
- `gitmap_diff`：显示不同版本之间的差异  
- `gitmap_push`：将更改推送到 Portal  
- `gitmap_pull`：从 Portal 拉取更改  
- `gitmap_log`：查看提交历史记录  

## 使用示例：  
- **查询并克隆地图**  
- **常规编辑 → 提交 → 推送流程**  
- **特性分支的工作流程**  
- **查看提交历史记录**  

## 服务器配置  
该技能运行在 `localhost:7400` 的 HTTP 服务器上。  

**API 端点：**  
- `POST /tools/{tool_name}`：使用 JSON 数据格式调用相应工具  
- `GET /health`：执行健康检查  

## 安装说明：  
该技能直接使用 `gitmap_core` Python 包来访问 ArcGIS Portal 的 API 接口。  

## 注意事项与限制：  
- **大多数命令需要指定工作目录**（因为 GitMap 仓库是基于目录结构的）  
- **Portal 凭据可以通过每次调用传递或通过环境变量设置（PORTAL_URL、ARCGIS_USERNAME、ARCGIS_PASSWORD）**  
- `gitmap_list` 不需要本地仓库，直接从 Portal 查询数据  
- **输出为原始的 CLI 文本**，部分情况下会进行简单解析以生成结构化响应  
- 该技能不支持 `clone` 和 `init` 操作；`merge`、`checkout`、`l`、`setupsm`、`context-repos` 等功能需通过直接调用 CLI 来实现  

## 相关资源：  
- GitMap 项目仓库：[https://github.com/14-TR/gitmap](https://github.com/14-TR/gitmap)