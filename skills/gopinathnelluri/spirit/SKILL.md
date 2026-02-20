---
name: spirit
description: >
  **状态保存与身份恢复基础设施工具（SPIRIT）**  
  该工具能够将AI代理的身份信息、内存数据以及相关项目内容保存到私有的Git仓库中。  
  **新功能：**  
  - **工作区模式（Workspace Mode）**：通过创建符号链接（symlink），用户可以在OpenClaw工作区内方便地编辑配置文件。
metadata:
  openclaw:
    requires:
      bins: ["spirit", "git"]
    install:
      - id: spirit-cli
        kind: brew
        tap: TheOrionAI/tap
        package: spirit
        bins: ["spirit"]
        label: Install SPIRIT via Homebrew
---
# SPIRIT 🌌  
> **状态保存与身份恢复基础设施工具**  

该工具能够将AI代理的身份信息、内存数据以及相关项目内容保存在一个可移植的Git仓库中。  
“你的AI灵魂，永远被守护着。”无论发生死亡、迁移还是跨设备切换，你的AI身份始终如一。  

## 新功能：OpenClaw工作区模式 🆕  
SPIRIT现在可以直接与你的OpenClaw工作区关联：  

**优势：**  
- ✅ 可在工作区内直接编辑`.spirit-tracked`配置文件  
- ✅ 所有身份/内存相关文件都集中在一个地方  
- ✅ 通过`SPIRIT_SOURCE_DIR=/root/.openclaw/workspace`命令实现数据同步  

---

## 必需工具及版本要求  
| 工具          | 用途                | 是否必需？ | 安装方式       |  
|------------------|------------------|-----------|-------------|  
| `git`         | 版本控制工具          | **必需**     | 内置于系统      |  
| `spirit`       | 本工具             | **必需**     | `brew install TheOrionAI/tap/spirit` |  
| `gh`          | GitHub命令行工具       | 可选*     | `brew install gh`     |  

*仅在使用GitHub命令行工具进行身份验证时需要`gh`；使用SSH密钥时也可实现同步。*  

---

## 快速入门  

### 选项A：OpenClaw工作区模式（推荐）  
（具体实现代码请参见**CODE_BLOCK_1___**）  

### 选项B：标准模式（旧版本）  
（具体实现代码请参见**CODE_BLOCK_2___**）  

---

## `SPIRIT_SOURCE_DIR`环境变量  
设置此变量后，SPIRIT将从指定目录读取文件，而非默认的`~/.spirit/`目录：  
（具体实现代码请参见**CODE_BLOCK_3___**）  
不过`.spirit-tracked`配置文件仍会从`~/.spirit/`目录读取（该目录可能是指向工作区的符号链接）。  

---

## 被保存的文件内容  
在**OpenClaw工作区模式下**，以下文件内容会被同步：  
| 文件名         | 保存内容                |  
|------------------|------------------|  
| `IDENTITY.md`    | 代理的身份信息          |  
| `SOUL.md`    | 行为/个性设定文件          |  
| `AGENTS.md`    | 代理配置文件            |  
| `USER.md`     | 用户偏好设置            |  
| `memory/*.md`    | 日常对话记录          |  
| `projects/*.md`    | 当前项目文件            |  
| `.spirit-tracked`   | 需要同步的配置文件        |  

**默认的`.spirit-tracked`文件内容：**  
（具体内容请参见**CODE_BLOCK_4___**）  

---

## 认证方式  
### 选项1：SSH密钥（推荐，无需使用`gh`）  
（具体实现代码请参见**CODE_BLOCK_5___**）  

### 选项2：GitHub命令行工具（`gh`）  
（具体实现代码请参见**CODE_BLOCK_6___**）  

### 选项3：Git凭证辅助工具  
（具体实现代码请参见**CODE_BLOCK_7___**）  

---

## 安全注意事项  
- **仓库设置**：务必将仓库设置为私有模式（仅限内部使用），因为其中包含敏感信息。  
- **认证方式**：使用SSH密钥或GitHub命令行工具进行身份验证，切勿在URL中使用API令牌。  
- **同步前检查**：务必先查看`~/.spirit/.spirit-tracked`文件的内容。  
- **测试**：在正式环境中使用前，请先在隔离环境中进行同步测试。  

**严禁使用以下方式：**  
- ❌ 在远程URL中使用`https://TOKEN@github.com/...`  
- ❌ 在shell历史记录或进程列表中显示API令牌。  

---

## 定时同步功能  
（具体实现代码请参见**CODE_BLOCK_8___**）  

## 在新机器上恢复数据  
（具体实现代码请参见**CODE_BLOCK_9___**）  

---

## 相关资源  
- **SPIRIT官方仓库**：https://github.com/TheOrionAI/spirit  
- **GitHub命令行工具**：https://cli.github.com  

**许可证**：MIT许可证