---
name: bring-add
description: **使用说明：**  
当用户希望向 Bring! 购物清单中添加商品时，可以使用该工具。支持添加单个商品、批量添加商品，或从标准输入（stdin）/文件中导入商品信息。该工具还提供“干运行”预览功能（dry-run preview）以及 JSON 格式的输出结果。
---

# Bring! 添加商品到购物清单的命令行工具（Bring! Add Items CLI）

## 概述

这是一个用于向 Bring! 购物清单中添加商品的命令行工具。支持单件商品添加、批量添加、通过标准输入（stdin）或管道输入，以及交互式添加模式。

## 使用场景

**适用情况：**
- 用户希望向 Bring! 购物清单中添加商品。
- 单个商品添加时可以指定详细信息（例如：“1升燕麦奶”）。
- 一次性添加多个商品（批量模式）。
- 从文件或其他命令中批量导入商品信息。
- 需要预览添加操作的效果。
- 需要将添加结果以 JSON 格式输出以便脚本处理。

**不适用情况：**
- 用户想要浏览食谱（请使用 `bring-recipes` 工具）。
- 用户想要从清单中删除商品。
- 用户想要查看当前的购物清单内容。

## 快速参考

| 命令 | 功能 |
|---------|---------|
| `bring-add "商品名称 "详细信息"` | 添加单个商品并指定详细信息 |
| `bring-add --batch "商品1, 商品2 1L, 商品3"` | 以逗号分隔的方式添加多个商品 |
| `bring-add -` | 从标准输入读取商品信息 |
| `bring-add` | 交互式添加模式（仅支持终端输入） |
| `bring-add lists` | 显示可用的购物清单 |
| `bring-add --dry-run ...` | 预览添加操作而不进行实际修改 |

## 环境变量：**
```bash
export BRING_EMAIL="your@email.com"
export BRING_PASSWORD="yourpassword"
export BRING_DEFAULT_LIST="Shopping"  # optional
```

## 安装方法：**
```bash
cd skills/bring-add
npm install
```

## 常见操作流程

- **添加单个商品：**  
```bash
node index.js "Tomatoes" "500g"
node index.js "Milk"
```

- **添加到特定清单：**  
```bash
node index.js --list "Party" "Chips" "3 bags"
```

- **批量添加多个商品：**  
```bash
node index.js --batch "Tomatoes 500g, Onions, Cheese 200g"
```

- **从文件中批量导入商品：**  
```bash
cat shopping-list.txt | node index.js -
echo -e "Milk 1L\nBread\nButter" | node index.js -
```

- **添加前预览：**  
```bash
node index.js --dry-run --batch "Apples 1kg, Pears"
```

- **获取 JSON 输出：**  
```bash
node index.js --json --batch "Milk, Bread" 2>/dev/null
```

- **列出所有可用清单：**  
```bash
node index.js lists
node index.js --json lists
```

## 常用参数说明

| 参数 | 说明 |
|------|-------------|
| `-l, --list <清单名称>` | 目标清单的名称或 UUID |
| `-b, --batch <商品列表>` | 以逗号分隔的商品列表 |
| `-n, --dry-run` | 预览操作而不进行实际修改 |
| `-q, --quiet` | 忽略非错误信息 |
| `-v, --verbose` | 显示详细进度信息 |
| `--json` | 将输出结果以 JSON 格式输出到标准输出 |
| `--no-color` | 禁用颜色显示 |
| `--no-input` | 不提示用户输入；如果需要输入则直接失败 |

## 输入格式

商品信息的格式为：`商品名称 [详细信息]`  
例如：  
`Tomatoes 500g`  表示 “500克番茄”  
`Oat milk 1L`  表示 “1升燕麦奶”  
`Red onions 3`  表示 “3个红洋葱”  
如果详细信息包含数字或单位（如 g、kg、L、ml、Stück、pck），则该部分将被视为商品的具体规格。

## 错误代码

| 代码 | 含义 |
|------|---------|
| `0` | 操作成功 |
| `1` | 一般性错误（API 错误、网络问题） |
| `2` | 使用方式错误（参数错误、缺少输入） |
| `3` | 认证失败 |
| `4` | 未找到相应的清单 |
| `130` | 操作被中断（按下 Ctrl-C） |

## 常见错误

- **注意事项：**
  - 运行前请确保设置了 `BRING_EMAIL` 和 `BRING_PASSWORD` 环境变量。
- 如果指定了错误的清单名称，请使用 `bring-add lists` 命令查看所有可用清单及其名称。
- 请注意：只有当详细信息包含数量单位时（如 g、kg、L、ml 等），该部分才会被解析为实际的商品规格。例如，“Red onions” 会被视为一个商品，而 “Red onions 3” 会被解析为 “3个红洋葱”。
- 在脚本中使用交互式添加模式时，请使用 `--no-input` 参数，以避免脚本因等待用户输入而挂起。

## 实现细节

- 该工具基于 `node-bring-api` 和其中的 `batchUpdateList()` API 实现。
- 需要 Node.js 18.0.0 或更高版本。
- 所有输出（数据、进度信息及错误消息）都会显示在标准输出（stdout）中。
- 支持 JSON 格式输出，便于自动化处理。
- 交互式添加模式仅在通过终端（TTY）输入时生效。