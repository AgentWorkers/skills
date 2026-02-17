---
name: xrpl-token-mint
description: Create and manage XRPL tokens (issued currencies) and NFTs. Use for: (1) Minting new tokens, (2) Setting up token issuers, (3) Creating NFTs, (4) Managing trust lines.
---

# XRPL代币发行

## 设置

```bash
npm install xrpl
```

## 发行的货币（可互换代币）

### 第1步：创建信任线（用户）
```typescript
{
  TransactionType: 'TrustSet',
  Account: 'rUserAddress',
  LimitAmount: {
    currency: 'USD',
    issuer: 'rIssuerAddress',
    value: '1000000'
  }
}
```

### 第2步：发行代币（发行者）
```typescript
{
  TransactionType: 'Payment',
  Account: 'rIssuerAddress',
  Destination: 'rUserAddress',
  Amount: {
    currency: 'USD',
    issuer: 'rIssuerAddress',
    value: '1000'
  }
}
```

## NFT（非可互换代币）

### 发行NFT
```typescript
{
  TransactionType: 'NFTokenMint',
  Account: 'rCreatorAddress',
  NFTokenTaxon: 0, // Collection ID
  Issuer: 'rCreatorAddress', // or different issuer
  TransferFee: 2500, // 2.5% royalty on secondary sales
  Flags: {
    tfBurnable: true,
    tfOnlyXRP: false,
    tfTrustLine: false
  },
  URI: 'ipfs://Qm...' // Metadata URL
}
```

### 创建出售报价
```typescript
{
  TransactionType: 'NFTokenCreateOffer',
  Account: 'rSellerAddress',
  NFTokenID: '00080000...',
  Amount: '1000000', // 1 XRP
  Flags: tfSellNFToken
}
```

### 接受报价（购买）
```typescript
{
  TransactionType: 'NFTokenAcceptOffer',
  Account: 'rBuyerAddress',
  NFTokenOfferID: 'offerID...'
}
```

## 标志

- **tfBurnable**：发行者可以销毁代币
- **tfOnlyXRP**：代币不能用于支付欠条（IOUs）
- **tfTransferable**：代币可以转让
- **tfSellNFToken**：创建的报价为出售报价

## 关键点

- 代币名称：3个字符的代码（例如“USD”）或完整的40个字符的十六进制代码
- 精度：最多16位小数
- 转移费用：0-50000（0-50%）
- NFT分类：用户自定义的收藏ID