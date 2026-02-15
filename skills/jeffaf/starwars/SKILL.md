---
name: starwars
version: 1.0.0
description: "这是一个用于AI代理的命令行工具（CLI），帮助它们为人类用户查询《星球大战》宇宙中的相关信息。该工具基于SWAPI接口进行开发，无需用户进行身份验证（即无需登录或提供任何认证信息）。"
homepage: https://swapi.dev
metadata:
  openclaw:
    emoji: "⚔️"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["starwars", "swapi", "entertainment", "movies", "cli"]
---

# 星球大战查询工具

这是一个为AI代理设计的命令行工具（CLI），用于帮助用户查询星球大战宇宙中的相关信息。例如：“谁扮演了达斯·维德？”——现在你的AI代理可以回答这个问题了。

该工具使用了[SWAPI](https://swapi.dev)（星球大战官方API），无需注册账户或API密钥。

## 使用方法

```
"Look up Luke Skywalker"
"What planet is Tatooine?"
"List all Star Wars films"
"What species is Chewbacca?"
"Tell me about the Millennium Falcon"
```

## 命令列表

| 功能 | 命令                |
|------|-------------------|
| 查找角色 | `starwars people "名称"`     |
| 查找行星 | `starwars planets "名称"`     |
| 列出电影 | `starwars films`       |
| 查找物种 | `starwars species "名称"`     |
| 查找飞船 | `starwars starships "名称"`     |

### 使用示例

```bash
starwars people "luke"          # Find character by name
starwars planets "tatooine"     # Find planet by name
starwars films                  # List all films
starwars species "wookiee"      # Find species by name
starwars starships "falcon"     # Find starship by name
```

## 查询结果

**角色查询结果：**
```
Luke Skywalker — Human, Tatooine, Height: 172cm
```

**行星查询结果：**
```
Tatooine — Population: 200000, Climate: arid, Terrain: desert
```

**电影查询结果：**
```
Episode 4: A New Hope (1977-05-25) — Director: George Lucas
Episode 5: The Empire Strikes Back (1980-05-17) — Director: Irvin Kershner
```

**物种查询结果：**
```
Wookiee — Classification: mammal, Language: Shyriiwook, Avg Lifespan: 400 years
```

**飞船查询结果：**
```
Millennium Falcon — YT-1300 light freighter, Class: Light freighter, Crew: 4
```

## 注意事项

- 该工具基于SWAPI（swapi.dev）接口开发
- 无需进行身份验证
- 支持查询所有6部正传及前传电影的信息
- 在查询角色时，系统会自动识别其所属物种及母星信息

---

## 代理实现说明

**脚本位置：`{skill_folder}/starwars`（实际脚本位于`scripts/starwars`文件夹）**

**当用户询问与星球大战相关的内容时：**
1. 运行`./starwars people "名称"`以查询角色信息
2. 运行`./starwars planets "名称"`以获取行星详情
3. 运行`./starwars films`以获取电影列表
4. 运行`./starwars species "名称"`以获取物种信息
5. 运行`./starwars starships "名称"`以获取飞船信息

**不适用场景：**
- 后传三部曲（第7-9部）的数据（这些内容未包含在SWAPI接口中）
- 扩展宇宙中的角色或物品
- 电视剧中的相关内容