---
name: clash-node-manager
description: 用于管理 Clash 代理节点。支持查看当前节点的连接状态、列出所有可用节点，以及切换到指定的节点。当用户需要管理 Clash 代理设置、查看可用节点或在它们之间切换时，可以使用该功能。
---
# Clash 节点管理器

## 概述

此技能允许您使用 `check_clash.py` 脚本来管理您的 Clash 代理节点。您可以列出可用的节点、检查当前节点的连接状态，以及切换到另一个节点。

## 使用方法

### 检查节点状态（默认）

要检查 Clash 节点的状态，请输入：

"Check Clash node status"

这将执行 `python check_clash.py`。

### 列出可用节点

要列出 GLOBAL 组中的可用节点，请输入：

"List available Clash nodes"

这将执行 `python check_clash.py --list`

要列出特定组中的可用节点，请输入：

"List available nodes in group <group_name>"

将 `<group_name>` 替换为相应的组名。这将执行 `python check_clash.py --group <group_name> --list`

### 切换到某个节点

要切换到特定的节点，请输入：

"Switch to node <node_name>"

将 `<node_name>` 替换为要切换到的节点名称。这将执行 `python check_clash.py --switch <node_name>`。

### 按索引切换节点

要按节点在列表中的索引切换节点，请输入：

"Switch to node at index <index>"

将 `<index>` 替换为节点在列表中的索引。这将执行 `python check_clash.py --switch-by-index <index>`。

### 资源

*   `check_clash.py`：用于检查和切换 Clash 代理节点的 Python 脚本。