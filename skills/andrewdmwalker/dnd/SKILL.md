---
name: dnd
description: D&D 5e 工具包，专为玩家和地下城主（DM）设计。支持掷骰子、查询法术和怪物信息、创建角色、设计战斗场景以及生成非玩家角色（NPC）。该工具包使用了官方的 D&D 5e SRD API。
version: 1.0.0
author: captmarbles
---

# D&D 5e 工具包

这是您专用的《龙与地下城》第五版辅助工具！它可以帮您查询法术、怪物信息，掷骰子，生成角色、战斗场景以及非玩家角色（NPC）。

## 主要功能

🎲 **掷骰子** - 可以掷带有修正值的任意骰子  
✨ **法术查询** - 在整个系统参考文档（SRD）中搜索法术  
👹 **怪物资料** - 查看任何怪物的完整属性信息  
⚔️ **角色生成器** - 生成具有随机属性的角色  
🗡️ **战斗场景生成器** - 根据难度等级（CR）生成平衡的战斗场景  
👤 **NPC生成器** - 创建具有独特个性的随机NPC  

## 使用方法

所有命令都需要通过 `dnd.py` 脚本来执行。  

### 掷骰子

```bash
# Roll 2d6 with +3 modifier
python3 dnd.py roll 2d6+3

# Roll d20
python3 dnd.py roll 1d20

# Roll with negative modifier
python3 dnd.py roll 1d20-2

# Roll multiple dice
python3 dnd.py roll 8d6
```

**输出：**
```
🎲 Rolling 2d6+3
   Rolls: [4 + 5] +3
   Total: 12
```

### 查询法术

```bash
# Search for a spell
python3 dnd.py spell --search fireball

# Direct lookup
python3 dnd.py spell fire-bolt

# List all spells
python3 dnd.py spell --list
```

**输出：**
```
✨ Fireball
   Level: 3 Evocation
   Casting Time: 1 action
   Range: 150 feet
   Components: V, S, M
   Duration: Instantaneous
   
   A bright streak flashes from your pointing finger to a point 
   you choose within range and then blossoms with a low roar into 
   an explosion of flame...
```

### 查询怪物

```bash
# Search for a monster
python3 dnd.py monster --search dragon

# Direct lookup
python3 dnd.py monster ancient-red-dragon

# List all monsters
python3 dnd.py monster --list
```

**输出：**
```
👹 Adult Red Dragon
   Huge Dragon, chaotic evil
   CR 17 (18,000 XP)
   
   AC: 19
   HP: 256 (19d12+133)
   Speed: walk 40 ft., climb 40 ft., fly 80 ft.
   
   STR 27 | DEX 10 | CON 25
   INT 16 | WIS 13 | CHA 21
   
   Special Abilities:
   • Legendary Resistance (3/Day): If the dragon fails a saving throw...
   
   Actions:
   • Multiattack: The dragon can use its Frightful Presence...
```

### 生成随机角色

```bash
# Generate character with rolled stats
python3 dnd.py character
```

**输出：**
```
⚔️  Elara
   Race: Elf
   Class: Wizard
   
   Stats:
   STR: 10 (+0)
   DEX: 15 (+2)
   CON: 12 (+1)
   INT: 16 (+3)
   WIS: 13 (+1)
   CHA: 8 (-1)
```

### 生成随机战斗场景

```bash
# Generate encounter with challenge rating
python3 dnd.py encounter --cr 5

# Random CR
python3 dnd.py encounter
```

**输出：**
```
🎲 Random Encounter (CR ~5)

   2x Troll (CR 5)
      AC 15, HP 84
   1x Ogre (CR 2)
      AC 11, HP 59
```

### 生成随机NPC

```bash
python3 dnd.py npc
```

**输出：**
```
👤 Finn Shadowend
   Race: Halfling
   Occupation: Merchant
   Trait: Curious
```

## 对 Clawdbot 的使用示例：

- *"掷2d20骰子，并且具有优势（即第二次掷骰子的结果比第一次高）"*  
- *"查询‘火球术’的相关信息"*  
- *"显示‘魔眼’怪物的全部属性"*  
- *"生成一个随机角色"*  
- *"为5级团队生成一个战斗场景"*  
- *"为我的酒馆场景创建一个随机NPC"*  

## 结构化输出（使用 `--json` 参数）

在命令后添加 `--json` 可以获得结构化的输出格式：  

```bash
python3 dnd.py roll 2d6 --json
python3 dnd.py spell --search fireball --json
python3 dnd.py character --json
```

## API 来源

该工具使用了官方的 [D&D 5e API](https://www.dnd5eapi.co/)，其中包含了所有的系统参考文档（SRD）内容。  

## 使用提示：

- **法术名称** 应使用小写字母并加上连字符：`fireball`、`magic-missile`、`cure-wounds`  
- **怪物名称** 也采用相同的格式：`ancient-red-dragon`、`goblin`、`beholder`  
- 如果不确定名称，可以使用 `--search dragon` 来搜索所有与“dragon”相关的怪物  
- **骰子格式** 非固定：`1d20`、`2d6+5`、`3d8-2`、`100d100`  

## 未来开发计划：

- 添加角色行动顺序追踪功能  
- 开发宝藏生成器  
- 提供任务/剧情线索生成工具  
- 实现随机地下城生成功能  
- 引入团队管理功能  
- 添加战役记录功能  

祝您游戏愉快！🐉⚔️✨