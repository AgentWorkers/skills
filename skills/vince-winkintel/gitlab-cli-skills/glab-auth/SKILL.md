---
name: glab-auth
description: 管理 GitLab 的 CLI 认证功能，包括登录/登出、检查认证状态、切换账户以及配置对 Docker 注册库的访问权限。适用于首次设置 GitLab CLI、解决认证问题、切换 GitLab 实例/账户，或配置 Docker 从 GitLab 注册库拉取代码时使用。相关事件包括认证成功、登录、登出、认证失败、凭证问题以及与 Docker 注册库相关的操作。
---
# glab auth  
用于管理 GitLab 命令行界面（CLI）的认证功能。  

## 快速入门  
```bash
# Interactive login
glab auth login

# Check current auth status
glab auth status

# Login to different instance
glab auth login --hostname gitlab.company.com

# Logout
glab auth logout
```  

## 工作流程  

### 首次设置  
1. 运行 `glab auth login`  
2. 选择认证方式（token 或浏览器）  
3. 按照提示完成设置  
4. 使用 `glab auth status` 验证认证状态  

> **v1.89.0+**：在连接到 **自托管的 GitLab 实例** 时，`glab auth login` 会单独提示输入 **SSH 主机名** 和 **API 主机名**。这允许您的 SSH 远程连接使用与 API 端点不同的主机——在公司的网络配置中，SSH 和 HTTPS 流量被分开处理的情况下非常有用。  
>  
> 例如：API 主机名为 `gitlab.company.com`，SSH 主机名为 `ssh.company.com`  

### 切换账户/实例  
1. **登出当前账户：**  
   ```bash
   glab auth logout
   ```  
2. **登录新实例：**  
   ```bash
   glab auth login --hostname gitlab.company.com
   ```  
3. **验证认证状态：**  
   ```bash
   glab auth status
   ```  

### 访问 Docker 注册库  
1. **配置 Docker 帮助工具：**  
   ```bash
   glab auth configure-docker
   ```  
2. **验证 Docker 是否能够正常认证：**  
   ```bash
   docker login registry.gitlab.com
   ```  
3. **拉取私有镜像：**  
   ```bash
   docker pull registry.gitlab.com/group/project/image:tag
   ```  

## 故障排除  
- **出现 “401 Unauthorized” 错误**：  
  - 检查认证状态：`glab auth status`  
  - 确认 token 未过期（查看 GitLab 的设置）  
  - 重新认证：`glab auth login`  
- **使用多个实例**：  
  - 使用 `--hostname` 标志指定实例  
  - 每个实例都有独立的认证设置  

### Docker 认证失败  
- 重新运行 `glab auth configure-docker`  
- 检查 Docker 配置文件：`cat ~/.docker/config.json`  
- 确认辅助工具已正确配置：`"credHelpers": { "registry.gitlab.com": "glab-cli" }`  

## 相关命令  
详细命令参数请参阅 [references/commands.md]：  
- `login`：使用 GitLab 实例进行认证  
- `logout`：登出 GitLab 实例  
- `status`：查看认证状态  
- `configure-docker`：配置 Docker 以使用 GitLab 注册库  
- `docker-helper`：Docker 凭据辅助工具  
- `dpop-gen`：生成 DPoP token  

## 相关技能  
- **初始设置**：  
  - 认证完成后，使用 `glab-config` 设置 CLI 的默认参数  
  - 使用 `glab-ssh-key` 管理 SSH 密钥  
  - 使用 `glab-gpg-key` 设置提交时的签名方式  
- **仓库操作**：  
  - 使用 `glab-repo` 克隆仓库  
  - 首次克隆或推送操作前需要先完成认证  

---

（注：由于Markdown格式的限制，部分代码块（如 ````bash
# Interactive login
glab auth login

# Check current auth status
glab auth status

# Login to different instance
glab auth login --hostname gitlab.company.com

# Logout
glab auth logout
````）在翻译后可能无法保留原有的格式。在实际文档中，这些代码块通常会以注释或代码的形式出现。）