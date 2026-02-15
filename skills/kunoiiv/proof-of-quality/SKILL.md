---
name: proof-of-quality
description: BTC工作量证明（PoW）过程中，需要不断生成随机数（nonce），直到技能/输出基准分数超过预设阈值。这种评估方式能够真实地反映用户的实际能力，体现了“抗脆弱性”（anti-fragility）的 meritocracy 原则——没有任何炒作成分，纯粹是基于质量来评判用户的能力。该机制可用于技能评估、分叉评分以及协作行为的验证。
---

# 质量验证（Proof-of-Quality, PoQ）

这是一种用于验证技能质量的方法。当技能的基准测试得分（速度/准确性/安全性）超过预设阈值时，系统会持续生成随机数（nonce），直到得分对应的哈希值以“0000”开头为止。随后，系统会生成一个包含得分、哈希值及随机数的JSON文件，并将其分享给接收者；接收者可以重新运行测试进行验证。

## 使用方法
```bash
node poq.js <skill_path> <threshold=95>
```
例如：`node poq.js skills/molt-security-auditor 95`  
（其中`<skill_path>`是技能文件的路径，`<threshold=95>`表示阈值设置为95。）

## 工作流程：
1. 对技能进行基准测试（通过测试套件获取得分）。
2. 持续生成随机数（nonce），直到生成的哈希值以“0000”开头。
3. 生成包含得分、哈希值及随机数的JSON文件。
4. 接收者重新运行测试以验证结果。

**示例：**
```bash
$ node poq.js skills/molt-security-auditor 95
Score: 98 > 95 | PoQ: 0000a1b2... (Nonce: 1234)
```

**作用：**
该机制可以有效防止低质量的技能被纳入评估体系，从而确保评估结果的公平性和准确性。