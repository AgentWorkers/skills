---
name: trending-skills
description: 用于获取 `skills.sh` 文件中的技能排名信息。在查询技能排名或热门工具时可以使用该功能。
---

# 热门技能

`FetchSkills.sh` 可用于获取技能的热门排名及详细信息。

## 快速入门

```
# View rankings
今天技能排行榜
Top 10 skills
技能榜单
```

## 查询类型

| 类型 | 例子 | 说明 |
|------|----------|-------------|
| 排名 | `今天技能排行榜` `Top 10` | 显示当前的热门技能排名 |
| 详情 | `xxx是什么` `xxx介绍` | 查看技能的详细信息（需要额外依赖包） |

## 工作流程

```
- [ ] Step 1: Parse query type
- [ ] Step 2: Fetch data from skills.sh
- [ ] Step 3: Format and display results
```

---

## 第一步：解析查询类型

| 用户输入 | 查询类型 | 执行操作 |
|------------|------------|--------|
| `今天技能排行榜` | rankings | 显示排名前 N 的技能 |
| `Top 10 技能` | rankings | 显示排名前 N 的技能 |
| `xxx是什么` | detail | 查看技能的详细信息 |

---

## 第二步：获取数据

### 获取排名信息

```bash
cd skills/trending-skills
python src/skills_fetcher.py
```

**要求**：

- 对于基本排名信息：
```bash
pip install playwright
playwright install chromium --with-deps
```

- 对于技能详细信息（可选）：
```bash
pip install beautifulsoup4 lxml requests
```

**注意**：`--with-deps` 选项会自动安装所需的系统库。

### 获取技能详细信息（可选）

```bash
python src/detail_fetcher.py <skill-name>
```

---

## 第三步：格式化结果

### 排名结果输出

```markdown
# Skills Trending

| # | Skill | Owner | Installs |
|---|-------|-------|----------|
| 1 | remotion-best-practices | remotion-dev | 5.6K |
| 2 | react-best-practices | vercel-labs | 5.4K |
| 3 | web-design-guidelines | vercel-labs | 4.0K |
```

### 详情输出（可选）

```markdown
# remotion-best-practices

**Owner**: remotion-dev/skills
**Installs**: 5.6K

**When to use**:
[Usage description from skills.sh]

**Rules** (27 total):
- 3d.md: 3D content in Remotion...
- audio.md: Audio processing...

**URL**: https://skills.sh/remotion-dev/remotion-best-practices
```

---

## 配置

无需进行任何配置。

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| Playwright 错误 | 运行 `playwright install chromium` |
| 网络超时 | 检查网络连接 |
| 技能未找到 | 在 `skills.sh` 中验证技能名称是否正确 |

---

## 命令行接口（CLI）参考

```bash
# Fetch rankings
python skills/trending-skills/src/skills_fetcher.py

# Fetch skill detail (optional)
python skills/trending-skills/src/detail_fetcher.py <skill-name>
```