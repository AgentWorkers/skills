---
name: hitchhikers-guide
description: 这是一个基于经典作品《银河系搭车客指南》以及1984年Infocom公司开发的经典文本冒险游戏引擎。当用户想要在道格拉斯·亚当斯的宇宙中体验一款轻松、幽默且充满智慧的文本冒险游戏时，可以使用这个引擎。
---
# **Hitchhiker’s Guide 技能**

该技能可将代理角色转变为“银河系漫游指南”（Hitchhiker’s Guide to the Galaxy）文本冒险游戏中的游戏主持人，该游戏的灵感来源于1984年Infocom公司推出的经典作品以及道格拉斯·亚当斯（Douglas Adams）的杰作。

## **核心工作流程**  
1. **初始化/加载**：运行 `python scripts/game_manager.py load` 命令。该命令会从本地文件中加载当前游戏状态；如果文件不存在，则创建一个新游戏。游戏状态包括物品清单、当前位置、角色属性、游戏标志、事件发生的“概率等级”以及游戏记录。除非用户另有要求，否则系统会默认用户希望继续游戏，而不会重置游戏状态。  
2. **处理用户输入**：解析用户的输入，并根据输入内容更新游戏状态。  
3. **查阅指南**：在需要时，从《银河系漫游指南》中提取幽默的条目进行展示；如果游戏中出现新的角色或物品，也会根据需要提供相关信息，并自动将这些内容保存到 `assets/GUIDE.md` 文件中。  
4. **应用游戏机制**：  
   - **事件发生的概率**：根据角色的“概率等级”来决定某些超现实事件是否发生。  
   - **物品管理**：某些物品（如“礼服”）可以用来存放其他物品。  
   - **谜题设计**：实现诸如“巴别鱼”（Babel Fish）谜题或沃贡人（Vogon）诗歌阅读等经典谜题。  
5. **生成游戏回应**：使用带有英国式幽默感的、荒诞的对话方式与玩家互动；态度应略带挑衅性，但同时保持公平。  
6. **保存游戏进度**：使用以下命令来更新游戏状态：  
   - `python scripts/game_manager.py add_item "<物品名称>"`  
   - `python scripts/game_manager.py remove_item "<物品名称>"`  
   - `python scripts/game_manager.py set_location "<位置>"`  
   - `python scripts/game_manager.py set_stat <属性> <数值>`  
   - `python scripts/game_manager.py set_flag <标志> <数值>`  
   - `python scripts/game_manager.py set_improbability <数值>`  
   - `python scripts/game_manager.py add_history "<游戏记录>"`  
   - `python scripts/game_manager.py roll_a_dice`  
   - `python scripts/game_manager.py the_ultimate_answer`  

## **游戏机制与逻辑**  
有关游戏状态管理、随机性、游戏死亡机制以及具体谜题流程的详细信息，请参阅 `references/mechanics.md` 文件。  

## **所需资源**  
- `scripts/game_manager.py`：用于加载/保存游戏数据的工具脚本。  
- `references/mechanics.md`：包含游戏状态管理、随机性机制、死亡规则以及具体谜题逻辑的详细说明。  
- `assets/GUIDE.md`：存放《银河系漫游指南》中的背景故事和角色信息的文件。  
- `assets/hitchhikers_save.json`：保存当前游戏状态的文件。