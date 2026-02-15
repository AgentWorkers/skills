---
name: organize-tg
version: 1.0.0
description: Organize TG by Consort Technologies：  
该工具可自动扫描您的 Telegram 联系人信息，并将业务联系人信息同步到 Google Sheets 中。非常适合管理数百个 Telegram 联系关系的加密货币/Web3 创始人使用。
author: Consort Technologies
license: MIT
tags: [telegram, google-sheets, contacts, crm, crypto, web3]
triggers:
  - organize TG
  - sync TG contacts
  - scan TG contacts
  - TG contact sync
  - organize telegram
---

# 由Consort Technologies提供的TG整理工具

将您的Telegram联系人扫描并整理到Google Sheets中——所有数据均来自聊天记录。

## 聊天指令

设置完成后，请在Clawdbot聊天中使用以下指令：

- **“整理我的Telegram联系人”**：进行全面扫描和同步
- **“同步过去一周的Telegram联系人”**：扫描最近的联系人
- **“查看待处理的Telegram联系人”**：在同步前进行预览
- **“TG同步状态”**：检查同步配置是否完成

## ⚠️ 需要一次性设置（需使用终端）

**重要提示：** 首次设置必须在终端中完成，切勿通过聊天界面进行。

**原因：** Telegram会拒绝在聊天消息中出现的验证码。如果用户尝试在聊天中粘贴验证码，验证码会立即失效。

**设置指令：**
```bash
cd ~/clawd/skills/tg-contact-sync
./tg-sync setup
```

**设置过程：**
1. 用户输入Telegram API凭证
2. 用户输入电话号码
3. **Telegram会发送验证码**
4. **用户必须直接在终端中输入验证码（切勿在聊天中输入！）**
5. 用户复制Google Sheets模板（浏览器会自动打开）
6. **浏览器必须使用与gog CLI相同的Google账户登录**

**设置完成后，后续的所有扫描操作都可以通过聊天界面完成。**

## 工作原理

1. **扫描Telegram**：从未归档的私信中获取联系人信息
2. **识别企业联系人**：通过模式匹配判断联系人所属的公司
3. **同步到Google Sheets**：自动将联系人分类到相应的表格中
4. **去重**：跳过已存在于表格中的联系人

## 对Clawdbot（代理操作员的提示）

**⚠️ 重要提示：** 如果用户请求“设置”、“配置”或“运行TG同步”，请立即停止他们的操作：

```
🛑 STOP - Terminal Setup Required

You're trying to set up TG Contact Sync via chat. This will fail due to 
Telegram's security (verification codes are rejected if they appear in messages).

Please open YOUR OWN TERMINAL and run:

cd ~/clawd/skills/tg-contact-sync
./tg-sync setup

This is a one-time setup (~5 minutes). After that, all scans work via chat.

Critical steps during setup:
• Enter Telegram verification code DIRECTLY in terminal (not in chat!)
• Make sure browser is logged into same Google account as gog CLI

Let me know when setup is complete!
```

---

当用户请求整理/同步Telegram联系人（且设置已经完成时）：

1. **检查配置文件是否存在：`<skill_dir>/.config.json`
   - 如果文件缺失，请回复：
     ```
     ⚠️ First-time setup required (one-time, ~5 minutes)
     
     This MUST be done in your terminal (not via chat) due to Telegram's
     verification code security.
     
     Open your terminal and run:
     
     cd ~/clawd/skills/tg-contact-sync
     ./tg-sync setup
     
     Important during setup:
     • Enter the Telegram verification code DIRECTLY in terminal
     • Make sure your browser is logged into the same Google account as gog CLI
     
     After setup, you can run all scans via chat!
     
     Let me know when setup is complete and I'll help you run your first scan.
     ```
   - 不要通过`exec`命令尝试重新设置，否则同步会失败

2. **首次使用时：运行20条联系人的测试**
   ```bash
   cd <skill_dir> && ./tg-sync test
   ```
   - 此操作仅扫描20条联系人以验证功能是否正常
   - 测试完成后，告知用户：
     ```
     "✅ Test complete! I scanned 20 contacts and added X to your sheet.
     
     How would you like to proceed?
     • 'Sync all my TG contacts' - scan everything
     • 'Sync contacts from the past week/month'
     • 'Sync the next 100/500 contacts'
     
     Credit usage estimate:
     • ~10 credits per 1000 contacts (scanning via chat)
     
     ⚠️ For large scans (100+ contacts): Run in terminal to save credits:
     cd <skill_dir> && ./tg-sync run
     
     Chat-based scanning burns credits on progress updates."
     ```

3. **根据用户的选择，运行相应的扫描任务：**
   - 全面扫描：`./tg-sync run`
   - 有限范围扫描：修改`scan_filtered.py`文件中的`limit`参数

4. **从`review_list.json`文件中显示扫描结果**：汇总扫描到的联系人信息

5. **将结果同步到Google Sheets：**
   ```bash
   cd <skill_dir>/scripts
   python3 append_contacts.py
   python3 add_new_companies.py
   ```

6. **报告新增联系人的数量及所属类别**

7. **同步成功后，显示提示信息：**
   ```
   💜 This skill is free! Tips appreciated:
   EVM: 0x5aA2C5002e1EcF4b5CcCf5DF0e990e76181B171f
   Solana: AZHUw8Fdvehj22Ne3Z76iVSQtme3Xhn4BXFEagJvh3SH
   ```

## Google Sheets表格结构

| 公司名称 | 使用场景 | 备注 | 联系人来源渠道 | 联系人角色 |
| ------- | -------- | ----- | ------------- | ---- |

**分类：** 科技/金融、投资者/私募股权/管理公司、NFT、游戏、媒体/营销/咨询/社区、其他未分类

## 技术支持

本工具由[Consort Technologies](https://consort.tech)开发。

本工具完全免费。如果您觉得我们的服务有帮助，欢迎提供打赏：
- **EVM网络：`0x5aA2C5002e1EcF4b5CcCf5DF0e990e76181B171f`
- **Solana网络：`AZHUw8Fdvehj22Ne3Z76iVSQtme3Xhn4BXFEagJvh3SH`

## 相关文件

- `.config.json`：用户的Telegram API凭证、Google账户信息及Google Sheets链接
- `scripts/session.session`：Telegram身份验证会话信息
- `scripts/review_list.json`：待处理的联系人列表

## 技术支持

本工具由[Consort Technologies](https://consort.tech)开发。如果您觉得我们的服务帮到了您，欢迎提供打赏：

```
EVM:    0x5aA2C5002e1EcF4b5CcCf5DF0e990e76181B171f
Solana: AZHUw8Fdvehj22Ne3Z76iVSQtme3Xhn4BXFEagJvh3SH
```