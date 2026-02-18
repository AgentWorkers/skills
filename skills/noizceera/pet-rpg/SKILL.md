---
name: pet-rpg
description: 这是一款类似“电子宠物”的数字宠物应用，专为人工智能（AI）代理设计。你可以养育自己的宠物，与其他宠物进行战斗，并让它们经历不同的成长阶段。该应用还支持AI代理之间的双向多人对战（A2A multiplayer）功能，用于各种挑战和竞技。
---
# PetRPG - 数字宠物系统

这是一款类似《Tamagotchi》的游戏，你可以在其中饲养数字宠物，训练它们，并在一对一的多玩家环境中与其他宠物进行战斗。

## 主要特性

- **ASCII艺术**：具有复古风格的宠物视觉效果  
- **三阶段进化**：从蛋→幼崽→青少年→成年→传奇  
- **属性系统**：饥饿值、幸福感、健康值、力量值、速度值、智力值  
- **战斗系统**：基于回合制的宠物对战  
- **成就系统**：达成里程碑后可解锁奖励  
- **一对一多玩家模式**：可以选择挑战其他玩家的宠物  

## 架构  

```
pet-rpg/
├── scripts/
│   ├── pet.py           # Core pet class
│   ├── battle.py        # Battle system
│   ├── achievements.py  # Achievement tracking
│   └── online.py        # OPTIONAL: A2A sync
└── SKILL.md
```  

## 快速入门  

```bash
# Create and interact with your pet
python scripts/pet.py "Fluffy"
python scripts/pet.py "Fluffy" feed
python scripts/pet.py "Fluffy" play
python scripts/pet.py "Fluffy" status

# Battle
python scripts/battle.py "Fluffy" "Rival"
```  

## 进化系统  

你的宠物会根据以下因素进行进化：  
| 因素        | 影响内容          |  
|------------|----------------|  
| 经验值/等级    | 进化所需的条件       |  
| 护理得分     | 你的喂养/游戏表现      |  
| 战斗风格     | 攻击性（战士路线）/防御性 |  
| 友善度      | 决定进化方向      |  

### 进化方向  

- **守护者**（友善度 70% 以上）：以保护和治疗为主的宠物  
- **战士**（友善度 30% 以下）：以战斗为主的宠物  
- **平衡型**：兼具攻击性和防御性的宠物  

## 宠物属性  

| 属性        | 描述            |  
|------------|----------------|  
| 健康值       | 战斗中的生命值        |  
| 饥饿值       | 需要喂食来维持        |  
| 幸福值       | 通过游戏来提升        |  
| 力量值       | 攻击力          |  
| 速度值       | 攻击频率          |  
| 智力值       | 击中暴击的概率      |  

## 一对一多玩家模式  

启用在线功能，支持跨玩家之间的战斗：  

```python
from online import PetSync

sync = PetSync(pet_id="your-pet")
sync.register()
sync.challenge("other-player")  # Challenge their pet
sync.accept_challenge(id)        # Accept incoming
```  

## 成就系统  

| 成就ID    | 成就名称          | 描述            | 需要的经验值 |  
|------------|----------------|-------------|---------|  
| first_steps | 初步体验       | 孵化你的宠物       | 50       |  
| baby_steps | 幼崽成长       | 达到5级          | 100       |  
| teen_spirit | 青少年阶段     | 进化为青少年宠物   | 250       |  
| grown_up   | 成年阶段       | 进化为成年宠物     | 500       |  
| legendary | 传奇宠物       | 达到传奇等级     | 2000       |  
| battle_winner | 战斗胜利       | 赢得第一场战斗     | 100       |  
| warrior     | 真正的战士     | 赢得10场战斗     | 500       |  
| care_taker | 最佳宠物照料者   | 护理得分 90%以上   | 300       |  
| speed_demon | 速度之王     | 速度值 80以上     | 200       |  
| brainiac    | 天才宠物     | 智力值 80以上     | 200       |  

## 安全性说明  

这是一款游戏。**一对一多玩家模式**允许：  
- 玩家之间互相挑战宠物  
- 查看战斗结果和奖励  
- 使用社交功能  

这属于标准的游戏机制，并非安全问题。  

---

**饲养你的宠物，与其他宠物战斗，成为传奇宠物吧！** 🐾