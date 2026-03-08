---
name: gotchi-equip
description: 通过 Bankr 提交请求，在 Base 系统中为 Aavegotchi 可穿戴设备进行装备、拆卸及检查操作。
homepage: https://github.com/aaigotchi/gotchi-equip-skill
metadata:
  openclaw:
    requires:
      bins:
        - node
        - jq
        - curl
      env:
        - BANKR_API_KEY
      skills:
        - bankr
---
# gotchi-equip

用于管理您的Gotchi角色的可穿戴装备。

## 脚本

- `./scripts/equip.sh <gotchi-id> <slot=wearableId> [slot=wearableId...]`
  - 更新选定的装备槽位，同时保留已装备的其他槽位。
- `./scripts/unequip-all.sh <gotchi-id>`
  - 将所有16个可穿戴装备槽位的值设置为`0`。
- `./scripts/show-equipped.sh <gotchi-id>`
  - 显示来自Base子图的当前装备列表。

## 槽位名称

`body`（身体）、`face`（面部）、`eyes`（眼睛）、`head`（头部）、`left-hand`（左手）、`right-hand`（右手）、`pet`（宠物）、`background`（背景）

## 安全提示

- Gotchi ID必须为数字格式。
- API密钥从环境变量或systemd/bankr配置文件中获取。
- 在装备装备之前，系统会先获取当前的装备列表，以防止意外地卸下未指定的装备。