# 代理信任协议（Agent Trust Protocol, ATP）

该协议用于在AI代理之间建立、验证并维护信任关系。它采用了贝叶斯信任评分机制，并结合了领域特定的信任评估规则、信任撤销机制、遗忘曲线以及可视化仪表板等功能。

## 安装

```bash
git clone https://github.com/FELMONON/trust-protocol.git
# No dependencies beyond Python 3.8+ stdlib
# Pair with skillsign for identity: https://github.com/FELMONON/skillsign
```

## 快速入门

```bash
# Add an agent to your trust graph
python3 atp.py trust add alpha --fingerprint "abc123" --score 0.7

# Record interactions — trust evolves via Bayesian updates
python3 atp.py interact alpha positive --note "Delivered clean code"
python3 atp.py interact alpha positive --domain code --note "Tests passing"

# Check trust
python3 atp.py trust score alpha
python3 atp.py trust domains alpha

# View the full graph
python3 atp.py status
python3 atp.py graph export --format json

# Run the full-stack demo (identity → trust → dashboard)
python3 demo.py --serve
```

## 命令

### 信任管理
```bash
atp.py trust add <agent> --fingerprint <fp> [--domain <d>] [--score <0-1>]
atp.py trust list
atp.py trust score <agent>
atp.py trust remove <agent>
atp.py trust revoke <agent> [--reason <reason>]
atp.py trust restore <agent> [--score <0-1>]
atp.py trust domains <agent>
```

### 交互行为
```bash
atp.py interact <agent> <positive|negative> [--domain <d>] [--note <note>]
```

### 挑战与响应机制
```bash
atp.py challenge create <agent>
atp.py challenge respond <challenge_file>
atp.py challenge verify <response_file>
```

### 图表展示
```bash
atp.py graph show
atp.py graph path <from> <to>
atp.py graph export [--format json|dot]
atp.py status
```

### 仪表板
```bash
python3 serve_dashboard.py          # localhost:8420
python3 demo.py --serve             # full demo + dashboard
```

### 与skillsign的集成
```bash
python3 moltbook_trust.py verify <agent>    # check agent trust via Moltbook profile
```

## 信任机制的工作原理

- **贝叶斯更新**：每次交互都会导致信任分数发生变化，但变化幅度逐渐减小（防止信任值剧烈波动）。
- **负面交互的影响**：负面交互对信任分数的负面影响大于正面交互的正面影响。
- **领域特定性**：可以信任某个代理提供的代码，但不一定能信任其提供的安全建议。
- **遗忘曲线**：如果没有交互，信任度会逐渐下降（公式：R = e^(-t/S)）。
- **信任撤销**：一旦信任被撤销，信任度会立即降为最低值，但可以通过再次交互恢复到较低的水平。
- **传递性信任**：如果你信任A，且A信任B，那么你也会部分信任B（不过信任度会随时间衰减）。

## 与skillsign的集成

ATP基于[skillsign](https://github.com/FELMONON/skillsign)来实现身份验证功能：
1. 代理使用skillsign生成ed25519密钥对。
2. 代理对技能进行签名，其他代理验证这些签名。
3. 经过验证的代理会被添加到ATP的信任图中。
4. 交互行为会随着时间的推移更新信任分数。

## 可用的命令

- `check trust`：检查当前信任状态。
- `trust score`：查看信任分数。
- `trust graph`：查看信任关系图。
- `verify agent`：验证代理的身份。
- `agent trust`：获取代理的信任信息。
- `trust status`：显示代理的信任状态。
- `who do I trust`：查询我信任的代理列表。
- `trust report`：生成信任报告。