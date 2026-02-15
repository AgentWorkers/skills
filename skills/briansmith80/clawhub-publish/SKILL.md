---
name: clawhub-publish
description: 将代理技能发布并更新到 ClawHub 注册表中。适用于发布新技能版本、更新现有技能或管理 ClawHub 的发布内容。该功能负责版本控制、Git 提交、GitHub 推送以及 ClawHub 的发布流程。
---

# ClawHub 发布工作流程

自动化将代理技能发布到 ClawHub 的整个流程，包括版本管理、Git 操作以及注册表发布。

## 先决条件

- 安装了 ClawHub CLI (`npm install -g clawhub`)
- 已经登录 ClawHub (`clawhub login`)
- 在 Notion 密码管理器中保存了 GitHub 个人访问令牌
- Git 仓库已配置远程仓库（origin）

## 使用方法

**发布新版本：**
```bash
python3 scripts/publish-skill.py /path/to/skill-folder --version 2.3.0 --changelog "Bug fixes and improvements"
```

**模拟运行（不实际发布）：**
```bash
python3 scripts/publish-skill.py /path/to/skill-folder --version 2.3.0 --dry-run
```

**自动递增补丁版本：**
```bash
python3 scripts/publish-skill.py /path/to/skill-folder --bump patch --changelog "Minor fixes"
```

## 工作流程步骤

脚本按以下顺序执行这些步骤：

1. **版本检查**
   - 验证版本号是否符合 semver 格式
   - 检查该版本是否已存在于 ClawHub 上
   - 更新 README.md 及其他相关文件中的版本信息

2. **Git 操作**
   - 将所有更改提交到 Git
   - 创建包含版本号和更改日志的提交
   - 从 Notion 密码管理器中获取 GitHub 令牌
   - 将更改推送到 GitHub 的 origin/main 仓库

3. **ClawHub 发布**
   - 将技能发布到 ClawHub 注册表
   - 应用相应的标签（如 `latest`、`security-fix` 等）
   - 返回发布 ID

4. **更新 Notion 任务状态**
   - 将相关的 Notion 任务标记为“已完成”
   - 如有需要，为下一个版本创建新任务

## 示例

**安全更新：**
```bash
python3 scripts/publish-skill.py ~/skills/my-skill \
  --version 2.2.1 \
  --changelog "SECURITY FIX: Patched command injection vulnerability" \
  --tags "latest,security-fix"
```

**重大版本发布：**
```bash
python3 scripts/publish-skill.py ~/skills/my-skill \
  --bump major \
  --changelog "Breaking changes: New API, removed deprecated methods"
```

**功能更新：**
```bash
python3 scripts/publish-skill.py ~/skills/my-skill \
  --bump minor \
  --changelog "Added OAuth2 support and batch operations"
```

## 选项

- `--version <semver>` - 显式指定版本号（例如：2.3.0）
- `--bump <major|minor|patch>` - 自动递增版本号
- `--changelog <text>` - 提供更改日志描述（必填）
- `--tags <tags>` - 以逗号分隔的标签（默认：`latest`）
- `--dry-run` - 进行模拟运行（不实际发布）
- `--skip-git` - 跳过 Git 提交/推送操作
- `--skip-clawhub` - 跳过 ClawHub 发布操作
- `--notion-task <id>` - 将特定的 Notion 任务标记为已完成

## 配置信息

**GitHub 令牌存储位置：**
- 存储在 Notion 密码管理器中
- 数据库 ID：`26c29e15-c2b5-810e-97b8-dcd41413d230`
- 搜索关键词：`GitHub 个人访问令牌`

**ClawHub 认证：**
- 需要先登录 ClawHub
- 令牌存储在 `~/.config/clawhub/` 文件中

## 常见工作流程

### 安全补丁工作流程

1. 修复代码中的安全漏洞
2. 更新 `SECURITY.md` 文件以记录详细信息
3. 运行测试以验证修复效果
4. 使用相应的标签发布更新：```bash
   python3 scripts/publish-skill.py /path/to/skill \
     --bump patch \
     --changelog "Security fix: [description]" \
     --tags "latest,security-fix"
   ```

### 新功能发布工作流程

1. 开发并测试新功能
2. 更新 `README.md` 文件以提供使用示例
3. 更新 `CHANGELOG.md` 文件
4. 发布小版本：```bash
   python3 scripts/publish-skill.py /path/to/skill \
     --bump minor \
     --changelog "Added [feature name] with [capabilities]"
   ```

### 兼容性破坏性更改工作流程

1. 进行可能破坏现有功能的 API 更改
2. 更新 `CHANGELOG.md` 文件以提供迁移指南
3. 更新文档
4. 发布重大版本：```bash
   python3 scripts/publish-skill.py /path/to/skill \
     --bump major \
     --changelog "BREAKING: [changes] - see CHANGELOG for migration"
   ```

## 错误处理

- **“版本已存在”：**
  - 自动递增版本号
  - 或使用 `--bump patch` 选项自动递增版本号

- **“Git 认证失败”：**
  - 在 Notion 中验证 GitHub 令牌
  - 确保令牌具有访问仓库的权限
  - 确保令牌未过期

- **“ClawHub 发布超时”：**
  - 用相同的版本重新尝试
  - 可能是 ClawHub 缓存了之前的尝试

- **“Notion API 错误”：**
  - 检查 `~/.config/notion/api_key` 文件中的 Notion API 密钥
  - 确认数据库 ID 是否正确

## 安全注意事项

- GitHub 令牌在 Notion 中安全存储（已加密）
- 仅在需要执行 Git 推送时才获取令牌
- 令牌不会被记录或显示
- Notion API 密钥的权限设置为 0600（仅限读取）

## 自动化操作

- **每月自动更新技能信息：**
```bash
# Add to cron or OpenClaw scheduler
0 9 1 * * cd /root/clawd/skills/my-skill && python3 /root/clawd/skills/clawhub-publish/scripts/publish-skill.py . --bump patch --changelog "Monthly maintenance update"
```

- **在 Git 提交时自动发布：**
```bash
# Add to .git/hooks/post-commit
python3 /root/clawd/skills/clawhub-publish/scripts/publish-skill.py . --auto-version
```