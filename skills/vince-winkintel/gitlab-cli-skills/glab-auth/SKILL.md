---
name: glab-auth
description: 管理 GitLab 命令行界面（CLI）的认证功能，包括登录/登出、检查认证状态、切换账户以及配置对 Docker 注册表的访问权限。适用于首次设置 GitLab、解决认证问题、切换 GitLab 实例/账户，或配置 Docker 以从 GitLab 注册表拉取代码时。相关操作会在认证、登录、登出、凭证更新、令牌生成以及 Docker 注册表相关事件发生时触发。
---

# glab auth  
用于管理 GitLab 命令行工具（CLI）的认证功能。  

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
2. 选择认证方式（令牌或浏览器）  
3. 按照提示完成 GitLab 实例的设置  
4. 使用 `glab auth status` 验证认证状态  

### 切换账户/实例  
1. **从当前账户登出：**  
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

### 访问 Docker 注册表  
1. **配置 Docker 帮助程序：**  
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
**出现 “401 Unauthorized” 错误时：**  
- 检查认证状态：`glab auth status`  
- 确保令牌未过期（查看 GitLab 设置）  
- 重新认证：`glab auth login`  

**使用多个 GitLab 实例时：**  
- 使用 `--hostname` 标志指定目标实例  
- 每个实例使用独立的认证信息  

**Docker 认证失败时：**  
- 重新运行 `glab auth configure-docker`  
- 检查 Docker 配置文件（`~/.docker/config.json`）  
- 确认配置中包含以下内容：`"credHelpers": { "registry.gitlab.com": "glab-cli" }`  

## 子命令  
详细的使用方法请参考 [references/commands.md](references/commands.md)：  
- `login`：使用指定 GitLab 实例进行认证  
- `logout`：登出当前 GitLab 实例  
- `status`：查看认证状态  
- `configure-docker`：配置 Docker 以使用 GitLab 注册表  
- `docker-helper`：管理 Docker 的认证信息  
- `dpop-gen`：生成 DPoP 令牌  

## 相关技能  
- **初始设置：**  
  认证完成后，使用 `glab-config` 设置 CLI 的默认配置  
  通过 `glab-ssh-key` 管理 SSH 密钥  
  使用 `glab-gpg-key` 设置提交时的签名方式  

**仓库操作：**  
- 使用 `glab-repo` 克隆仓库  
- 首次克隆或推送仓库前需要完成认证  

---