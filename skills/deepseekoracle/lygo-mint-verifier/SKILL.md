---
name: lygo-mint-verifier
description: "**LYGO-MINT 验证器**：用于冠军/对齐提示包（Champion/alignment prompt packs）  
- 对提示包进行规范化处理；  
- 生成唯一的 SHA-256 哈希值；  
- 创建只读的、规范化的账本（ledgers）；  
- 输出可移植的 Anchor Snippet，以便在任何平台（Moltbook、Moltx、X、Discord、4claw）上使用。  

**功能说明：**  
适用于需要可验证的对齐结果（如冠军包、召唤提示包、工作流程包）的场景，支持生成带有哈希地址的验证凭证，并可选择性地添加锚点数据（anchor backfill）。"
---

# LYGO-MINT 验证工具

该工具可将对齐后的冠军包（或任何提示/工作流程包）转换为可验证的成果：
- 规范化格式
- 确定性哈希值
- 分账记录
- 可移植的 Anchor Snippet（可粘贴到任何地方）

## 工作流程（概述）
1) 创建/对齐包（例如：使用 Champion 对齐系统）。
2) 运行验证工具：
   - 对包内容进行规范化处理
   - 计算哈希值（SHA-256）
   - 将处理结果写入分账系统
   - 生成 Anchor Snippet
3) 将生成的 Anchor Snippet 发布到任意位置。
4) 将 Anchor 的 ID 添加到分账系统中。

详细流程请参阅：`references/process.md`。

## 命令（脚本）
该工具封装了 `tools/lygo_mint` 目录中的本地工具，专为处理非敏感数据而设计。虽然代码中未涉及环境变量或网络操作，但在使用该工具处理敏感数据之前，请务必先自行查看 `tools/lygo_mint/*.py` 文件。

### 铸造并验证包文件
- `python scripts/mint_pack_local.py --pack reference/CHAMPION_PACK_LYRA_V1.md --version 2026-02-07.v1`

### 从现有哈希记录生成 Anchor Snippet
- `python scripts/make_anchor_snippet.py --hash <64-hex> --title "..."`

### 将 Anchor ID 添加到分账系统中
- `python scripts/backfill_anchors.py --hash <64-hex> --channel moltbook --id <post-id-or-url>`

## 分账系统状态文件
- 只读文件：`state/lygo_mint_ledger.jsonl`
- 规范化后的文件（去重处理）：`state/lygo_mint_ledger_canonical.json`

## 参考资料
- 核心模板：`reference/CHAMPION_PROMPT_CORE TEMPLATE_V1.md`
- 发布检查清单：`reference/CHAMPION_PACK_PUBLISH_CHECKLIST.md`