---
name: bring-shopping-list
description: 当被问及购物清单、食品杂货相关的问题时（例如“添加到购物清单中”、“清单上有什么物品”、“从清单中删除某项物品”等），请使用该功能。该功能可与 Bring! 购物清单应用程序集成使用。
argument-hint: "[add|remove|list] [items...]"
user-invocable: false
metadata:
  openclaw:
    requires:
      env:
        - BRING_EMAIL
        - BRING_PASSWORD
      bins:
        - uv
    primaryEnv: BRING_EMAIL
---

# Bring! 购物清单

管理您的 Bring! 购物清单——可以添加商品、删除商品、将商品标记为已完成状态，以及查看清单上的商品。

## 设置

1. 如果尚未安装 [uv](https://docs.astral.sh/uv/)，请先进行安装。
2. 设置与您的 Bring! 账户相关的环境变量：
   ```bash
   export BRING_EMAIL="your-email@example.com"
   export BRING_PASSWORD="your-password"
   ```
   或者将这些变量添加到项目根目录下的 `.env` 文件中。

> 如果您使用 Google 登录方式访问 Bring!，请先进入您的 Bring! 账户设置并设置一个单独的密码。

## 使用方法

所有命令都依赖于该技能目录中的 `bring.py` 文件。请根据您安装该技能的位置调整路径。

### 使用 uv（推荐）

```bash
uv run --with bring-api --with python-dotenv python bring.py list --json
uv run --with bring-api --with python-dotenv python bring.py add "Milk" "Eggs" "Butter:Irish"
uv run --with bring-api --with python-dotenv python bring.py remove "Milk"
uv run --with bring-api --with python-dotenv python bring.py complete "Eggs"
```

### 使用 pip

```bash
pip install -r requirements.txt
python bring.py list --json
python bring.py add "Milk" "Eggs" "Butter:Irish"
python bring.py remove "Milk"
python bring.py complete "Eggs"
```

## 处理请求

1. 解析用户的输入信息：
   - 要添加的商品（例如：“在清单中添加牛奶和鸡蛋”）
   - 要删除的商品（例如：“从清单中删除牛奶”）
   - 查看清单上的商品（例如：“清单上有哪些商品？”）
   - 商品的详细信息/规格（例如：“牛奶，低脂” -> `Milk:low fat`）

2. 运行相应的命令行（CLI）命令。

3. 以自然的方式确认用户的操作。

## 注意事项

- 需要 `BRING_EMAIL` 和 `BRING_PASSWORD` 环境变量。
- 商品可以包含可选的规格信息，格式为 `名称:规格`。
- 该工具会使用账户中的第一个购物清单。
- 所需依赖库（`bring-api`、`python-dotenv`）可以通过 `uv run --with` 命令直接安装，或者通过 `pip install -r requirements.txt` 进行安装。