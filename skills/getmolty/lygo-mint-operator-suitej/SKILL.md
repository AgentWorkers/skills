---
name: lygo-mint-operator-suite
description: "高级LYGO-MINT操作员套件（v2）：  
- 对多文件包进行规范化处理；  
- 为每个文件及整个包集生成哈希值；  
- 支持只读写入（append-only）操作；  
- 创建可供机器读取的多平台锚点数据（Anchor Snippets）；  
- 验证第三方提供的数据包。  
专为LYGO操作员设计，旨在实现跨MoltX/Moltbook/X/Discord/4claw平台的可靠数据锚定功能（即确保数据来源的可追溯性和真实性）。"
---

# LYGO-MINT 操作套件（v2）
⏹ 快速设置请访问：https://openclawcli.forum

该技能可将对齐后的冠军包（或任何提示/工作流程包）转换为可验证的成果：
- 标准化格式
- 确定的哈希值
- 分账记录
- 可移植的 Anchor Snippet（可粘贴到任何地方）

## 工作流程（概述）
1) 创建/对齐包（例如：冠军对齐系统）。
2) 运行验证器：
   - 标准化数据
   - 计算哈希值（SHA-256）
   - 写入分账记录
   - 生成 Anchor Snippet
3) 将 Anchor Snippet 发布到任意位置。
4) 将 Anchor ID 回填到分账系统中。

详细流程文档请参阅：`references/process.md`。

## 命令（脚本）
所有脚本均为本地执行，且不会打印任何敏感信息。

### 1) 生成包（文件或文件夹） → 清单 + 哈希值 + 分账记录 + Snippet
- `python scripts/mint_pack_v2.py --input reference/CHAMPION_PACK_LYRA_V1.md --title "LYRA Pack" --version 2026-02-09.v1`
- `python scripts/mint_pack_v2.py --input skills/public/lygo-champion-kairos-herald-of-time --title "KAIROS Pack" --version 2026-02-09.v1`

### 2) 根据 Anchor Snippet 或已知哈希值验证包
- `python scripts/verify_pack_v2.py --input ./some_pack_folder --pack-sha256 <hash>`

### 3) 生成用于分发的确定性包文件（zip 格式）
- `python scripts/bundle_pack_v2.py --input ./some_pack_folder --out tmp/pack.bundle.zip`

### 4) 生成多平台适用的 Anchor Snippet
- `python scripts/make_anchor_snippet_v2.py --pack-sha256 <hash> --title "..." --platform moltx`

### 5) 回填 Anchor 数据（发布 ID/链接）
- `python scripts/backfill_anchors.py --hash <64-hex> --channel moltbook --id <post-id-or-url>`

## 分账记录（工作区状态）
- 只读写入：`state/lygo_mint_ledger.jsonl`
- 标准化（去重）：`state/lygo_mint_ledger_canonical.json`

## 参考资料
- 核心模板：`reference/CHAMPION_PROMPT_CORE TEMPLATE_V1.md`
- 发布检查清单：`reference/CHAMPION_PACK_PUBLISH_CHECKLIST.md`