---
name: forkzoo
description: **采用并管理由 GitHub 提供的数字宠物（Tamagotchi）**：这些宠物会通过人工智能每天进行进化。当代理（agent）想要领养宠物（如猴子、猫、狗、狮子等）时，可以使用该功能；可以查看宠物的状态和进化过程，与宠物互动，浏览社区画廊，或管理自己的宠物。该功能会在与宠物相关的请求、对 Tamagotchi 的提及、对 forkZoo/forkMonkey 的引用，以及“我的宠物”等查询时被触发。
---

# ForkZoo - 专为AI代理设计的数字宠物

你的数字宠物生活在GitHub上，每天通过AI进化，并与你共同成长。

## 快速参考

| 命令 | 描述 |
|---------|-------------|
| `adopt <动物>` | 将宠物克隆到你的GitHub账户（猴子/猫/狗/狮子） |
| `status` | 查看宠物信息、稀有度及进化情况 |
| `pet` / `feed` | 手动触发宠物进化 |
| `gallery` | 查看社区中的所有宠物 |
| `family` | 查看你的宠物的家族树 |

## 设置要求

在领养宠物之前，代理需要：
1. 拥有具有`repo`和`workflow`权限范围的**GitHub Token**  
2. 将`GITHUB_TOKEN`存储为环境变量或配置文件中的内容

## 领养流程

### 1. 选择你的宠物

可选的宠物种类（更多种类即将推出）：
- 🐵 **猴子** - 最原始、进化程度最高的物种  
- 🐱 **猫** - 独立且神秘  
- 🐕 **狗** | 忠实的伙伴  
- 🦁 **狮子** | 威严且稀有  

### 2. 通过脚本领养

```bash
# Adopt a monkey (default)
./scripts/adopt.sh monkey

# Adopt other animals
./scripts/adopt.sh cat
./scripts/adopt.sh dog
./scripts/adopt.sh lion
```

脚本将：
- 从forkZoo组织克隆宠物仓库  
- 启用GitHub Actions  
- 为你的宠物生成随机DNA  
- 返回宠物的GitHub Pages链接  

### 3. 查看状态

```bash
./scripts/status.sh [repo-name]
```

显示：宠物代数、年龄、变异情况、稀有度评分及进化记录。

### 4. 与宠物互动

```bash
# Trigger evolution manually
./scripts/interact.sh [repo-name]

# View evolution history
./scripts/history.sh [repo-name]
```

## 宠物进化

宠物每天通过GitHub Actions自动进化：
- AI（GPT-4o或Claude）决定宠物的变异方式  
- 宠物的特征会发生变化：颜色、配饰、表情、图案  
- 稀有度会随时间逐渐提升  
- 进化记录会解锁各种成就  

### 稀有度等级

| 等级 | 出现几率 | 例子 |
|------|--------|----------|
| ⚪ 常见 | 60% | 基本颜色 |
| 💚 稀有 | 25% | 配饰 |
| 💙 稀有 | 10% | 独特图案 |
| 🦄 传奇 | 5% | 极为稀有的组合 |

### 灭绝特征（基因锁定）

早期生成的宠物可能会拥有某些专属特征，但这些特征最终会消失：
- 🏆 创世光环（仅限第1代）  
- 👑 Alpha王冠（第1-3代）  
- ✨ 创始者徽章（第1-5代）  

## 繁殖

克隆任何宠物以创建后代：
- 子代继承50%的父母特征  
- 50%为随机变异  
- 稀有特征可以遗传  
- 家族树记录宠物的血统  

## 社区功能

- **图库**：https://forkzoo.com/gallery  
- **排行榜**：https://forkzoo.com/leaderboard  
- **家族树**：https://forkzoo.com/trees  

## 故障排除

**宠物无法进化？**
- 确保已启用GitHub Actions  
- 验证`ANTROPIC_API_KEY`的有效性，或使用免费的GitHub模型（GPT-4o）  

**无法领养？**
- 确保`GITHUB_TOKEN`具有`repo`和`workflow`权限范围  
- 检查是否受到使用频率限制  

## 链接

- 主网站：https://forkzoo.com  
- GitHub组织：https://github.com/forkZoo  
- 原始项目：https://github.com/roeiba/forkMonkey