---
name: preview
description: **Docusaurus集成用文档查看专家**  
该工具专为Docusaurus平台设计，能够为SpecWeave生成的动态文档提供交互式展示功能。支持热重载、自动生成的侧边栏以及Mermaid图表的展示。适用于所有SpecWeave项目，并可自动完成配置。支持内部访问（端口3015）和公开访问（端口3016）。主要功能包括：预览文档、查看文档内容、管理Docusaurus服务器、优化文档用户界面、搭建本地文档服务器以及实现文档的热重载功能。此外，还支持静态站点生成（static site build）。
---

# 文档查看技能

擅长为 SpecWeave 项目启动和管理 Docusaurus 文档服务器。

## 我的工作内容

我帮助您使用 Docusaurus 查看 SpecWeave 的实时文档：

### 主要功能
- **零配置设置** - 可自动应用于任何 SpecWeave 项目
- **内部文档与公共文档** - 内部文档通过端口 3015 提供，公共文档通过端口 3016 提供
- **缓存安装** - Docusaurus 的缓存文件存储在 `.specweave/cache/docs-site/`（该目录被 Git 忽略）
- **热重载** - 编辑 Markdown 代码后可以立即看到更改效果
- **Mermaid 图表** - 架构图能够以美观的方式展示
- **自动生成侧边栏** - 侧边栏内容根据文件夹结构自动生成
- **绕过私有注册库** - 使用公共 npm 注册库以避免与 Azure DevOps 或企业内部环境相关的问题

## 工作原理

1. **首次运行（约 30 秒）**：
   - 在 `.specweave/cache/docs-site/`（内部文档）或 `.specweave/cache/docs-site-public/`（公共文档）目录下创建 Docusaurus 服务器
   - 从公共 npm 注册库安装所需依赖项
   - 配置 Docusaurus 从 `.specweave/docs/internal/` 或 `.specweave/docs/public/` 文件夹中读取文档内容

2. **后续运行（立即生效）**：
   - 使用已缓存的配置文件
   - 立即启动文档服务器

## 可用的命令

### 查看内部文档（默认设置）
```bash
/sw-docs:view
```

**功能说明：**
1. 检查是否存在 `.specweave/docs/internal/` 文件夹
2. 进行预验证（自动修复常见问题）
3. 如果是首次运行，将文档内容缓存到缓存目录
4. 在 `http://localhost:3015` 上启动开发服务器
5. 启用热重载功能

### 查看公共文档
```bash
/sw-docs:view --public
```

**功能说明：**
1. 检查是否存在 `.specweave/docs/public/` 文件夹
2. 进行预验证（自动修复常见问题）
3. 如果是首次运行，将文档内容缓存到缓存目录
4. 在 `http://localhost:3016` 上启动开发服务器
5. 启用热重载功能

### 构建静态网站
```bash
/sw-docs:build
```

**功能说明：**
1. 构建可用于部署的静态网站
2. 将生成的静态文件输出到 `.specweave/cache/docs-site/build/` 目录
3. 静态网站可部署到任何支持静态文件服务的服务器上

## 适用场景

- “查看我的文档”
- “预览我的文档”
- “在浏览器中展示我的文档”
- “启动 Docusaurus 服务器”
- “查看实时更新的文档”
- “查看内部文档”
- “查看公共文档”

### 工作流程

```
User: "I want to preview my docs"
You: "I'll launch the documentation view server."
     [Run: /sw-docs:view]
```

```
User: "Show me my public documentation"
You: "I'll launch the public documentation server."
     [Run: /sw-docs:view --public]
```

## 端口参考

| 文档类型 | 端口 | 文件路径 |
|-----------|------|------|
| 内部文档（默认） | 3015 | `.specweave/docs/internal/` |
| 公共文档 | 3016 | `.specweave/docs/public/` |

## 故障排除

### 如果端口 3015 或 3016 已被占用
```bash
# For internal docs
lsof -i :3015 && kill -9 $(lsof -t -i :3015)

# For public docs
lsof -i :3016 && kill -9 $(lsof -t -i :3016)
```

### 从头开始重新安装
```bash
# For internal docs
rm -rf .specweave/cache/docs-site
# Then run /sw-docs:view again

# For public docs
rm -rf .specweave/cache/docs-site-public
# Then run /sw-docs:view --public again
```

### npm 注册库相关问题
该设置明确使用 `--registry=https://registry.npmjs.org` 来绕过私有或企业内部的 npm 注册库配置。

## 相关命令

- `/sw-docs:build` - 构建用于部署的静态网站
- `/sw-docs:organize` - 为大型文件夹生成主题化的索引
- `/sw-docs:health` - 提供文档健康状况报告
- `/sw-docs:validate` - 在查看文档前进行验证