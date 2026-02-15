---
name: sui-decompile
description: 获取 Sui Move 合同的源代码，并让你的代理解释智能合约的工作原理。从 Suivision/Suiscan 探索器中抓取数据，分析 DeFi 协议，以了解 Sui 上的任何合约。
homepage: https://suivision.xyz
metadata:
  openclaw:
    emoji: "🔓"
---

# Sui反编译技能

通过区块浏览器获取链上Sui Move合约的反编译源代码。

**GitHub地址：** <https://github.com/EasonC13-agent/sui-skills/tree/main/sui-decompile>

## Suivision（推荐使用）

当可用时，可能会提供官方验证过的源代码。

```
URL: https://suivision.xyz/package/{package_id}?tab=Code
```

**浏览器使用流程：**
1. 在浏览器中执行 `open profile openclaw targetUrl="https://suivision.xyz/package/{package_id}?tab=Code"` 操作。
2. 如果存在多个模块，请点击左侧的模块标签页。
3. 提取代码：
```javascript
() => {
  const rows = document.querySelectorAll('table tr');
  const lines = [];
  rows.forEach(r => {
    const cells = r.querySelectorAll('td');
    if (cells.length >= 2) lines.push(cells[1].textContent);
  });
  return lines.join('\n');
}
```

## Suiscan（备用方案）

```
URL: https://suiscan.xyz/mainnet/object/{package_id}/contracts
```

**浏览器使用流程：**
1. 在浏览器中执行 `open profile openclaw targetUrl="https://suiscan.xyz/mainnet/object/{package_id}/contracts"` 操作。
2. 点击“Source”标签页（默认可能显示字节码）。
3. 如果存在多个模块，请点击相应的模块标签页。
4. 提取代码：
```javascript
() => {
  const rows = document.querySelectorAll('table tr');
  const lines = [];
  rows.forEach(r => {
    const cells = r.querySelectorAll('td');
    if (cells.length >= 2) lines.push(cells[1].textContent);
  });
  return lines.join('\n') || 'not found';
}
```

## 多个模块的包

像DeepBook（`0xdee9`）这样的包包含多个模块：
1. 从侧边栏中查看所有模块标签页。
2. 点击每个标签页以提取代码。
3. 将提取的代码保存为单独的`.move`文件。

## 示例

| 包名 | Suivision | Suiscan |
|---------|-----------|---------|
| Sui Framework | `suivision.xyz/package/0x2?tab=Code` | `suiscan.xyz/mainnet/object/0x2/contracts` |
| DeepBook | `suivision.xyz/package/0xdee9?tab=Code` | `suiscan.xyz/mainnet/object/0xdee9/contracts` |

## 与其他技能的配合使用

该技能可与Sui开发技能套件完美结合使用：

- **sui-move**：用于编写和部署Move智能合约。使用`sui-decompile`反编译现有合约，再利用`sui-move`创建新的合约。
- **sui-coverage**：用于分析代码的测试覆盖率。先反编译合约，编写测试用例，然后检查覆盖率。

**典型工作流程：**
1. 使用`sui-decompile`了解DeFi协议的工作原理。
2. 使用`sui-move`根据所学知识编写新的合约。
3. 使用`sui-coverage`确保代码经过充分测试。

## 服务器/无头环境下的使用

在无显示功能的服务器（如CI/CD服务器、VPS等）上运行时，可以使用Puppeteer配合虚拟显示器来避免被识别为无头浏览器：

**Puppeteer使用示例：**
```javascript
const puppeteer = require('puppeteer');

async function fetchContractSource(packageId) {
  const browser = await puppeteer.launch({
    headless: false,  // Use 'new' headless or false with xvfb
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto(`https://suivision.xyz/package/${packageId}?tab=Code`);
  await page.waitForSelector('table tr');
  
  const code = await page.evaluate(() => {
    const rows = document.querySelectorAll('table tr');
    const lines = [];
    rows.forEach(r => {
      const cells = r.querySelectorAll('td');
      if (cells.length >= 2) lines.push(cells[1].textContent);
    });
    return lines.join('\n');
  });
  
  await browser.close();
  return code;
}
```

**为什么使用xvfb？** 有些网站会检测无头浏览器。使用`xvfb-run`可以创建虚拟显示器，使浏览器表现得像传统的桌面浏览器。

## 注意事项：
- Suivision提供的源代码可能是经过MovebitAudit验证的。
- Suiscan显示的是Revela工具反编译后的代码。
- 反编译后的代码可能无法直接编译。
- 使用完成后请关闭浏览器标签页！

## 相关技能

该技能属于Sui开发技能套件的一部分：

| 技能 | 描述 |
|-------|-------------|
| **sui-decompile** | 获取并阅读链上合约的源代码 |
| [sui-move](https://clawhub.ai/EasonC13/sui-move) | 编写和部署Move智能合约 |
| [sui-coverage](https://clawhub.ai/EasonC13/sui-coverage) | 分析代码的测试覆盖率并进行安全检查 |
| [sui-agent-wallet](https://clawhub.ai/EasonC13/sui-agent-wallet) | 构建和测试DApp的前端界面 |

**技能套件的完整地址：** <https://github.com/EasonC13-agent/sui-skills>