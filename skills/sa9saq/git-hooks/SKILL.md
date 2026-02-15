---
description: 自动生成并管理用于 pre-commit、pre-push、commit-msg 等操作的 Git 钩子（hooks）。
---

# Git 钩子（Git Hooks）

用于设置和管理任何仓库的 Git 钩子。

**适用场景**：为 Git 工作流程添加自动化检查——代码格式检查（linting）、测试、提交信息验证等。

## 前提条件

- 必须存在 Git 仓库（`.git/` 目录）。
- 不需要 API 密钥。

## 操作步骤

1. **验证仓库根目录**：执行 `test -d .git && echo "OK" || echo "Not a git repo"`。切勿在非 Git 仓库中创建钩子。

2. **在覆盖现有钩子之前，请先备份它们**：
   ```bash
   [ -f .git/hooks/pre-commit ] && cp .git/hooks/pre-commit .git/hooks/pre-commit.bak
   ```

3. **创建钩子** 并确保其可执行：
   ```bash
   cat > .git/hooks/<hook-name> << 'EOF'
   #!/bin/sh
   # hook content here
   EOF
   chmod +x .git/hooks/<hook-name>
   ```

## 常见钩子类型

### `pre-commit`：检查暂存文件的语法格式（Lint Staged Files）
```bash
#!/bin/sh
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
# JavaScript/TypeScript
echo "$STAGED" | grep -E '\.(js|ts|jsx|tsx)$' | xargs -r npx eslint --quiet 2>/dev/null
[ $? -ne 0 ] && echo "❌ ESLint failed" && exit 1
# Python
echo "$STAGED" | grep -E '\.py$' | xargs -r python3 -m py_compile 2>&1
[ $? -ne 0 ] && echo "❌ Python syntax check failed" && exit 1
exit 0
```

### `pre-push`：运行测试（Run Tests）
```bash
#!/bin/sh
[ -f package.json ] && npm test
[ -f pytest.ini ] || [ -d tests/ ] && python3 -m pytest -q
exit $?
```

### `commit-msg`：强制使用规范的提交信息格式（Enforce Conventional Commits）
```bash
#!/bin/sh
MSG=$(cat "$1")
if ! echo "$MSG" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|ci|perf|build)(\(.+\))?: .+'; then
  echo "❌ Commit message must follow Conventional Commits format"
  echo "   Example: feat(auth): add login page"
  exit 1
fi
```

### `pre-commit`：防止敏感信息泄露（Prevent Secret Leaks）
```bash
#!/bin/sh
STAGED=$(git diff --cached --diff-filter=ACM -p)
if echo "$STAGED" | grep -qEi '(api[_-]?key|secret|password|token)\s*[=:]\s*["\x27][^\s]+'; then
  echo "❌ Potential secret detected in staged changes!"
  echo "   Review your changes and use environment variables instead."
  exit 1
fi
```

## 管理命令

```bash
# List active hooks (non-sample)
ls .git/hooks/ | grep -v '\.sample$'

# Disable a hook temporarily
chmod -x .git/hooks/pre-commit

# Re-enable
chmod +x .git/hooks/pre-commit

# Remove a hook
rm .git/hooks/pre-commit
```

## 异常情况与故障排除

- **钩子未执行**：检查文件的执行权限（`chmod +x`）以及 shebang 行（`#!/bin/sh` 或 `#!/bin/bash`）是否正确。
- **需要绕过钩子检查时**：使用 `git commit --no-verify` 来跳过 `pre-commit` 和 `commit-msg` 钩子的检查。
- **团队共享钩子**：不要将钩子文件直接提交到仓库中。可以在仓库根目录下创建 `hooks/` 目录，并通过 `git config core.hooksPath hooks/` 配置全局钩子路径。
- **Windows 兼容性**：为确保跨平台兼容性，请使用 `#!/bin/sh` 而不是 `#!/bin/bash`。避免使用特定于 Bash 的语法。
- **优化钩子执行速度**：确保 `pre-commit` 钩子的执行时间不超过 5 秒。仅检查暂存文件的语法格式，而不是整个项目。

## 安全注意事项

- 添加用于检测敏感信息的钩子（见上文），以防止意外提交包含敏感信息的代码或密码。
- **切勿在钩子脚本中存储 API 密钥或密码**。