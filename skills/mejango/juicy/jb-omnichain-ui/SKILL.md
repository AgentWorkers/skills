---
name: jb-omnichain-ui
description: 为 Juicebox 项目构建多链用户界面（UI），实现单次支付即可部署到多个区块链上，并显示统一的跨链数据。
---

# Juicebox V5 全链 UI 开发

使用 viem 和共享样式，构建能够部署并在多个链上与 Juicebox 项目交互的前端界面。

## 开发理念

> **在任何链上支付一次，即可部署到所有地方；查询统一的数据。**

### 什么是全链项目（Omnichain Project）？

“全链项目”是指部署在多个链上的 Juicebox 项目的集合，这些项目通过 Suckers 实现代币桥接功能。

**关键概念：** 项目 ID 无法在不同链之间进行协调——每个链会独立分配下一个可用的 ID。例如，在 Ethereum 上部署的项目可能被赋予 ID #42，而在 Optimism 上部署的项目可能被赋予 ID #17。Suckers 将这些独立的项目连接起来，使它们作为一个逻辑上的项目运行，并实现代币的统一桥接。

全链 UI 支持以下功能：
- 通过 Relayr 实现单次支付即可跨多个链进行部署
- 通过 Bendystraw 实现所有链上的项目数据统一展示
- 通过 Sucker Groups 实现跨链代币的可见性

## 工具参考

有关完整的 API 文档，请参阅：
- `/jb-relayr` - 多链交易打包 API
- `/jb-bendystraw` - 跨链数据聚合 API

---

## 快速入门

### Relayr（交易）

```javascript
const RELAYR_API = 'https://api.relayr.ba5ed.com';

// 1. Sign forward requests for each chain
// 2. POST /v1/bundle/prepaid to get payment options
// 3. User pays on one chain
// 4. Poll /v1/bundle/{uuid} for completion

// No API key required
```

### Bendystraw（数据）

```javascript
const BENDYSTRAW_API = 'https://bendystraw.xyz/{API_KEY}/graphql';

// API key required - use server-side proxy
// Contact @peripheralist on X for key
```

---

## 全链部署 UI 模板

用于将项目部署到多个链的完整 HTML 模板。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Deploy Omnichain Project</title>
  <link rel="stylesheet" href="/shared/styles.css">
  <style>
    body { max-width: 640px; margin: 0 auto; }
    .subtitle { color: var(--text-muted); margin-bottom: 1.5rem; }
    .chain-select { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
    .chain-chip { padding: 0.5rem 1rem; border: 1px solid var(--border); border-radius: 4px; cursor: pointer; font-size: 0.875rem; background: var(--bg-secondary); }
    .chain-chip:hover { border-color: var(--jb-yellow); }
    .chain-chip.selected { background: var(--accent); border-color: var(--accent); }
    .chain-chip.payment { background: var(--success); border-color: var(--success); }
    h2 { font-size: 1rem; color: var(--text-muted); margin-bottom: 1rem; }
  </style>
</head>
<body>
  <h1>Deploy Omnichain Project</h1>
  <p class="subtitle">Deploy to multiple chains with a single payment</p>

  <div class="card">
    <button id="connect-btn" class="btn" onclick="connectWallet()">Connect Wallet</button>
    <div id="wallet-status" class="hidden">
      Connected: <span id="wallet-address"></span>
    </div>
  </div>

  <div class="card">
    <h2>Select Target Chains</h2>
    <div class="chain-select" id="target-chains">
      <div class="chain-chip" data-chain="1" onclick="toggleChain(this)">Ethereum</div>
      <div class="chain-chip" data-chain="10" onclick="toggleChain(this)">Optimism</div>
      <div class="chain-chip" data-chain="8453" onclick="toggleChain(this)">Base</div>
      <div class="chain-chip" data-chain="42161" onclick="toggleChain(this)">Arbitrum</div>
    </div>
  </div>

  <div class="card">
    <label>Project Name</label>
    <input type="text" id="project-name" placeholder="My Omnichain Project">
    <label>Token Symbol</label>
    <input type="text" id="token-symbol" placeholder="OMNI">
  </div>

  <div class="card hidden" id="payment-section">
    <h2>Select Payment Chain</h2>
    <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1rem;">Pay gas on one chain. Relayr handles the rest.</p>
    <div class="chain-select" id="payment-chains"></div>
    <div style="background: var(--bg-primary); padding: 0.75rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.875rem;">
      <div class="stat-row"><span class="stat-label">Total Gas Cost</span><span class="stat-value" id="total-cost">-</span></div>
    </div>
  </div>

  <div class="card">
    <button id="deploy-btn" class="btn" onclick="startDeploy()" disabled>Step 1: Sign for Each Chain</button>
  </div>

  <div class="card hidden" id="tx-status">
    <h2>Deployment Status</h2>
    <div id="chain-statuses"></div>
  </div>

  <script type="module">
    import { createWalletClient, custom, formatEther, encodeFunctionData } from 'https://esm.sh/viem';
    import { mainnet, optimism, base, arbitrum } from 'https://esm.sh/viem/chains';
    import { CHAIN_CONFIGS, truncateAddress } from '/shared/wallet-utils.js';

    const RELAYR_API = 'https://api.relayr.ba5ed.com';

    const CHAINS = {
      1: { name: 'Ethereum', chain: mainnet, explorer: 'https://etherscan.io' },
      10: { name: 'Optimism', chain: optimism, explorer: 'https://optimistic.etherscan.io' },
      8453: { name: 'Base', chain: base, explorer: 'https://basescan.org' },
      42161: { name: 'Arbitrum', chain: arbitrum, explorer: 'https://arbiscan.io' }
    };

    let walletClient, address;
    let selectedChains = new Set();
    let currentQuote = null;

    window.toggleChain = function(el) {
      const chainId = el.dataset.chain;
      if (selectedChains.has(chainId)) {
        selectedChains.delete(chainId);
        el.classList.remove('selected');
      } else {
        selectedChains.add(chainId);
        el.classList.add('selected');
      }
      document.getElementById('deploy-btn').disabled = selectedChains.size === 0;
    };

    window.connectWallet = async function() {
      if (!window.ethereum) { alert('Please install MetaMask'); return; }
      walletClient = createWalletClient({ chain: mainnet, transport: custom(window.ethereum) });
      const [addr] = await walletClient.requestAddresses();
      address = addr;

      document.getElementById('wallet-address').textContent = truncateAddress(address);
      document.getElementById('wallet-status').classList.remove('hidden');
      document.getElementById('connect-btn').classList.add('hidden');
    };

    window.startDeploy = async function() {
      if (selectedChains.size === 0) return;

      const btn = document.getElementById('deploy-btn');
      btn.disabled = true;
      btn.textContent = 'Signing...';

      try {
        const signedRequests = [];

        for (const chainId of selectedChains) {
          btn.textContent = `Signing for ${CHAINS[chainId].name}...`;

          const calldata = buildLaunchCalldata();
          const forwarder = CHAIN_CONFIGS[parseInt(chainId)]?.contracts?.JBForwarder;
          const controller = CHAIN_CONFIGS[parseInt(chainId)]?.contracts?.JBController;

          const signed = await signForwardRequest(parseInt(chainId), calldata, forwarder, controller);

          signedRequests.push({
            chain: parseInt(chainId),
            target: forwarder,
            data: signed.encodedData,
            value: '0'
          });
        }

        btn.textContent = 'Getting quote...';
        currentQuote = await getRelayrQuote(signedRequests);

        showPaymentOptions(currentQuote);
        btn.textContent = 'Step 2: Select Payment Chain';

      } catch (error) {
        console.error(error);
        btn.textContent = 'Error - Try Again';
        btn.disabled = false;
      }
    };

    async function signForwardRequest(chainId, calldata, forwarder, controller) {
      const domain = {
        name: 'Juicebox',
        version: '1',
        chainId: chainId,
        verifyingContract: forwarder
      };

      const types = {
        ForwardRequest: [
          { name: 'from', type: 'address' },
          { name: 'to', type: 'address' },
          { name: 'value', type: 'uint256' },
          { name: 'gas', type: 'uint256' },
          { name: 'nonce', type: 'uint256' },
          { name: 'deadline', type: 'uint48' },
          { name: 'data', type: 'bytes' }
        ]
      };

      const deadline = Math.floor(Date.now() / 1000) + 48 * 60 * 60;

      const message = {
        from: address,
        to: controller,
        value: '0',
        gas: '1000000',
        nonce: 0,
        deadline: deadline,
        data: calldata
      };

      const signature = await walletClient.signTypedData({
        account: address,
        domain,
        types,
        primaryType: 'ForwardRequest',
        message
      });

      const encodedData = encodeFunctionData({
        abi: [{ name: 'execute', type: 'function', inputs: [
          { name: 'request', type: 'tuple', components: [
            { name: 'from', type: 'address' }, { name: 'to', type: 'address' },
            { name: 'value', type: 'uint256' }, { name: 'gas', type: 'uint256' },
            { name: 'nonce', type: 'uint256' }, { name: 'deadline', type: 'uint48' },
            { name: 'data', type: 'bytes' }
          ]},
          { name: 'signature', type: 'bytes' }
        ]}],
        functionName: 'execute',
        args: [[message.from, message.to, message.value, message.gas, message.nonce, message.deadline, message.data], signature]
      });

      return { message, signature, encodedData };
    }

    function buildLaunchCalldata() {
      // Build launchProjectFor calldata - see /jb-project for full struct encoding
      return '0x';
    }

    async function getRelayrQuote(signedRequests) {
      const response = await fetch(`${RELAYR_API}/v1/bundle/prepaid`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transactions: signedRequests, virtual_nonce_mode: 'Disabled' })
      });
      if (!response.ok) throw new Error('Failed to get quote');
      return await response.json();
    }

    function showPaymentOptions(quote) {
      document.getElementById('payment-section').classList.remove('hidden');

      const container = document.getElementById('payment-chains');
      container.innerHTML = '';

      quote.payment_info.forEach(payment => {
        const chain = CHAINS[payment.chain];
        if (!chain) return;

        const costEth = formatEther(BigInt(payment.amount));
        const chip = document.createElement('div');
        chip.className = 'chain-chip';
        chip.innerHTML = `${chain.name}<br><small>${parseFloat(costEth).toFixed(4)} ETH</small>`;
        chip.onclick = () => selectPaymentChain(payment, chip);
        container.appendChild(chip);
      });
    }

    async function selectPaymentChain(payment, chip) {
      document.querySelectorAll('#payment-chains .chain-chip').forEach(c => c.classList.remove('payment'));
      chip.classList.add('payment');

      const btn = document.getElementById('deploy-btn');
      btn.textContent = `Pay on ${CHAINS[payment.chain].name}`;
      btn.disabled = false;
      btn.onclick = () => executePayment(payment);
    }

    async function executePayment(payment) {
      const btn = document.getElementById('deploy-btn');
      btn.disabled = true;
      btn.textContent = 'Confirm in wallet...';

      try {
        const hash = await walletClient.sendTransaction({
          account: address,
          to: payment.target,
          value: BigInt(payment.amount),
          data: payment.calldata,
          chain: CHAINS[payment.chain].chain
        });

        btn.textContent = 'Payment sent...';
        showStatusPanel();
        pollBundleStatus(currentQuote.bundle_uuid);

      } catch (error) {
        console.error(error);
        btn.textContent = 'Error - Try Again';
        btn.disabled = false;
      }
    }

    function showStatusPanel() {
      document.getElementById('tx-status').classList.remove('hidden');
      const container = document.getElementById('chain-statuses');
      container.innerHTML = '';

      for (const chainId of selectedChains) {
        const item = document.createElement('div');
        item.className = 'stat-row';
        item.id = `status-${chainId}`;
        item.innerHTML = `<span class="stat-label">${CHAINS[chainId].name}</span><span class="stat-value status-badge">Pending</span>`;
        container.appendChild(item);
      }
    }

    async function pollBundleStatus(bundleUuid) {
      const poll = async () => {
        try {
          const response = await fetch(`${RELAYR_API}/v1/bundle/${bundleUuid}`);
          const status = await response.json();

          status.transactions.forEach((tx, i) => {
            const chainId = Array.from(selectedChains)[i];
            const statusEl = document.querySelector(`#status-${chainId} .status-badge`);
            if (!statusEl) return;

            if (tx.status === 'Success' || tx.status === 'Completed') {
              statusEl.textContent = 'Complete';
              statusEl.style.color = 'var(--success)';
            } else if (tx.status === 'Failed') {
              statusEl.textContent = 'Failed';
              statusEl.style.color = 'var(--error)';
            } else {
              statusEl.textContent = tx.status;
            }
          });

          const allDone = status.transactions.every(tx => ['Success', 'Completed', 'Failed'].includes(tx.status));
          if (!allDone) setTimeout(poll, 2000);
          else document.getElementById('deploy-btn').textContent = 'Deployment Complete!';

        } catch (error) {
          console.error('Poll error:', error);
          setTimeout(poll, 2000);
        }
      };

      poll();
    }
  </script>
</body>
</html>
```

---

## 全链仪表盘 UI 模板

使用 Bendystraw 在所有链上显示统一的数据统计信息。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Omnichain Dashboard</title>
  <link rel="stylesheet" href="/shared/styles.css">
  <style>
    body { max-width: 900px; margin: 0 auto; }
    .subtitle { color: var(--text-muted); margin-bottom: 2rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
    .metric-card { text-align: center; }
    .metric-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem; }
    .metric-value { font-size: 1.5rem; font-weight: 600; }
    .metric-sub { font-size: 0.875rem; color: var(--text-muted); margin-top: 0.25rem; }
    h2 { font-size: 1rem; color: var(--text-muted); margin-bottom: 1rem; }
    .chain-breakdown { display: flex; gap: 1rem; flex-wrap: wrap; }
    .chain-card { flex: 1; min-width: 200px; background: var(--bg-primary); border-radius: 4px; padding: 1rem; }
    .chain-name { font-weight: 600; margin-bottom: 0.5rem; }
    .chain-stat { display: flex; justify-content: space-between; font-size: 0.875rem; padding: 0.25rem 0; }
    .activity-item { display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
    .activity-item:last-child { border-bottom: none; }
  </style>
</head>
<body>
  <h1 id="project-name">Loading...</h1>
  <p class="subtitle">Omnichain Project Dashboard</p>

  <div class="grid">
    <div class="card metric-card">
      <div class="metric-label">Total Balance</div>
      <div class="metric-value" id="total-balance">-</div>
      <div class="metric-sub">across all chains</div>
    </div>
    <div class="card metric-card">
      <div class="metric-label">Total Volume</div>
      <div class="metric-value" id="total-volume">-</div>
      <div class="metric-sub">all-time</div>
    </div>
    <div class="card metric-card">
      <div class="metric-label">Token Supply</div>
      <div class="metric-value" id="total-supply">-</div>
      <div class="metric-sub">total issued</div>
    </div>
    <div class="card metric-card">
      <div class="metric-label">Contributors</div>
      <div class="metric-value" id="total-contributors">-</div>
      <div class="metric-sub">unique addresses</div>
    </div>
  </div>

  <div class="card">
    <h2>Chain Breakdown</h2>
    <div class="chain-breakdown" id="chain-breakdown">
      <div class="loading">Loading chain data...</div>
    </div>
  </div>

  <div class="card">
    <h2>Recent Activity</h2>
    <div id="activity-feed">
      <div class="loading">Loading activity...</div>
    </div>
  </div>

  <script type="module">
    import { truncateAddress, formatEth, formatNumber } from '/shared/wallet-utils.js';

    const SUCKER_GROUP_ID = '0x...'; // Your sucker group ID
    const API_PROXY = '/api/bendystraw';

    const CHAINS = {
      1: { name: 'Ethereum' },
      10: { name: 'Optimism' },
      8453: { name: 'Base' },
      42161: { name: 'Arbitrum' }
    };

    async function query(graphql, variables = {}) {
      const response = await fetch(API_PROXY, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: graphql, variables })
      });
      return (await response.json()).data;
    }

    async function loadDashboard() {
      try {
        const data = await query(`
          query($id: String!) {
            suckerGroup(id: $id) {
              volume volumeUsd balance tokenSupply
              paymentsCount contributorsCount
              projects_rel {
                projectId chainId name balance volume paymentsCount
              }
            }
          }
        `, { id: SUCKER_GROUP_ID });

        const group = data.suckerGroup;

        document.getElementById('project-name').textContent = group.projects_rel[0]?.name || 'Omnichain Project';
        document.getElementById('total-balance').textContent = formatEth(group.balance) + ' ETH';
        document.getElementById('total-volume').textContent = formatEth(group.volume) + ' ETH';
        document.getElementById('total-supply').textContent = formatNumber(group.tokenSupply);
        document.getElementById('total-contributors').textContent = formatNumber(group.contributorsCount);

        document.getElementById('chain-breakdown').innerHTML = group.projects_rel.map(project => `
          <div class="chain-card">
            <div class="chain-name">${CHAINS[project.chainId]?.name || 'Chain ' + project.chainId}</div>
            <div class="chain-stat"><span>Balance</span><span>${formatEth(project.balance)} ETH</span></div>
            <div class="chain-stat"><span>Volume</span><span>${formatEth(project.volume)} ETH</span></div>
            <div class="chain-stat"><span>Payments</span><span>${formatNumber(project.paymentsCount)}</span></div>
          </div>
        `).join('');

        if (group.projects_rel.length > 0) {
          const first = group.projects_rel[0];
          await loadActivity(first.projectId, first.chainId);
        }

      } catch (error) {
        console.error('Failed to load:', error);
        document.getElementById('project-name').textContent = 'Error loading';
      }
    }

    async function loadActivity(projectId, chainId) {
      const data = await query(`
        query($projectId: Int!, $chainId: Int!) {
          payEvents(
            where: { projectId: $projectId, chainId: $chainId }
            orderBy: "timestamp"
            orderDirection: "desc"
            limit: 10
          ) {
            items { timestamp from amount memo }
          }
        }
      `, { projectId, chainId });

      const events = data.payEvents.items;

      if (events.length === 0) {
        document.getElementById('activity-feed').innerHTML = '<div class="loading">No recent activity</div>';
        return;
      }

      document.getElementById('activity-feed').innerHTML = events.map(e => `
        <div class="activity-item">
          <div>
            <div>${truncateAddress(e.from)} paid</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">
              ${e.memo || 'No memo'} · ${new Date(parseInt(e.timestamp) * 1000).toLocaleDateString()}
            </div>
          </div>
          <div style="font-weight: 600;">${formatEth(e.amount)} ETH</div>
        </div>
      `).join('');
    }

    loadDashboard();
  </script>
</body>
</html>
```

---

## 服务器端代理

Bendystraw 需要一个 API 密钥。请使用服务器端代理来保护该密钥的安全性。

### Next.js

```typescript
// pages/api/bendystraw.ts
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const response = await fetch(
    `https://bendystraw.xyz/${process.env.BENDYSTRAW_API_KEY}/graphql`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    }
  );

  res.json(await response.json());
}
```

### Express

```javascript
app.post('/api/bendystraw', async (req, res) => {
  const response = await fetch(
    `https://bendystraw.xyz/${process.env.BENDYSTRAW_API_KEY}/graphql`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    }
  );

  res.json(await response.json());
});
```

---

## 常用开发模式

### 获取项目信息并检查是否支持全链功能

```javascript
async function loadProject(projectId, chainId) {
  const project = await bendystrawQuery(`
    query($projectId: Int!, $chainId: Int!) {
      project(projectId: $projectId, chainId: $chainId) {
        name balance volume suckerGroupId
      }
    }
  `, { projectId, chainId });

  if (project.suckerGroupId) {
    const group = await bendystrawQuery(`
      query($id: String!) {
        suckerGroup(id: $id) {
          volume balance tokenSupply
          projects_rel { chainId balance }
        }
      }
    `, { id: project.suckerGroupId });

    return { project, omnichainStats: group };
  }

  return { project, omnichainStats: null };
}
```

### 在 Relayr 部署后进行轮询

```javascript
async function deployAndWaitForIndex(walletClient, chains, calldata) {
  // Deploy via Relayr
  const quote = await relayrClient.createBundle(/* ... */);
  await payForBundle(quote);
  await relayrClient.waitForCompletion(quote.bundle_uuid);

  // Wait for Bendystraw to index (~1 minute)
  console.log('Waiting for indexer...');
  await new Promise(r => setTimeout(r, 60000));

  // Now fetch from Bendystraw
  const project = await bendystrawQuery(/* ... */);
  return project;
}
```

---

---

## 重要限制：聚合支付限额

**全链项目中的支付限额是针对每个链单独设置的，而不是汇总的。**

如果您为一个跨 4 个链的项目设置了 10 ETH 的支付限额，那么您最多只能支付 40 ETH（10 ETH × 4 个链），而不是 10 ETH。

这是跨链系统的一个基本限制——目前没有方法可以跨链统一执行聚合支付限额。

**请参阅 `/jb-omnichain-payout-limits` 以了解：**
- 该限制存在的原因
- 实际可行的解决方案（监控、定时任务自动化、预言机）
- 各种解决方案的权衡
- 根据使用场景的建议

**快速指南：**
- **软性限制**：为每个链设置合计约为目标限额 80% 的限额
- **需要自动化处理**：使用定时任务和 Relayr 在接近限额时暂停支付
- **严格的合规性要求**：考虑仅在一个链上部署项目，或构建预言机基础设施

---

## 相关技能

- `/jb-omnichain-payout-limits` - 聚合支付限额的相关限制及解决方法
- `/jb-suckers` - 核心的代币桥接机制（准备、发送、领取流程）
- `/jb-v5-currency-types` - 用于确保跨链货币一致性的处理逻辑
- `/jb-relayr` - Relayr 的完整 API 参考文档
- `/jb-bendystraw` - Bendystraw 的 GraphQL 完整参考文档
- `/jb-deploy-ui` - 单链部署 UI
- `/jb-interact-ui` - 项目交互 UI