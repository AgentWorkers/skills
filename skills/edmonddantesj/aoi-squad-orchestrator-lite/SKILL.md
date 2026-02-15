# AOI Squad Orchestrator (Lite)

S-DNA: `AOI-2026-0215-SDNA-SQUAD01`

## 产品简介
这是一个经过商业化的、安全性较高的编排工具，具备以下特点：
- 提供 **3种可选的预设配置**（每种配置包含3个角色）；
- 为每个角色分配一个 **固定的化名**（不使用AOI内部的昵称）；
- 允许用户 **重命名团队成员**；
- 生成 **统一的JSON报告格式**，便于解析和测试。

## 产品限制
- 该工具不支持任何外部发布、网络爬取或表单提交功能；
- 不涉及钱包管理、交易或购买操作；
- 不会自动提升用户权限。

## 可用预设配置
- `planner-builder-reviewer`  
- `researcher-writer-editor`  
- `builder-security-operator`

## 命令列表
### 列出所有预设配置
```bash
aoi-squad preset list
```

### 查看当前团队的名称（每个预设配置下的团队名称固定不变）
```bash
aoi-squad team show --preset planner-builder-reviewer
```

### 重命名团队成员
```bash
aoi-squad team rename --preset planner-builder-reviewer --role reviewer --name "Sentinel Kestrel"
```

### 运行工具（生成结构化报告）
```bash
aoi-squad run --preset planner-builder-reviewer --task "Draft a launch checklist"
```

## 数据存储
团队名称的映射信息存储在本地文件中：
- `~/.openclaw/aoi/squad_names.json`

## 技术支持
- 如有疑问、发现漏洞或需要功能请求，请访问：https://github.com/edmonddantesj/aoi-skills/issues
- 请在问题描述中注明该工具的名称：`aoi-squad-orchestrator-lite`

## 许可证
MIT许可证