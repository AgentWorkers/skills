# 🧿 深度隐私搜索（需使用VPN）

**🚨 必须使用VPN** – 该工具必须通过VPN进行隐藏使用。如果不使用VPN，您的真实IP地址将会被搜索引擎捕获。

不要让大型科技公司知道您的活动以及您使用该工具的意图。这种多轮次的深度搜索功能有助于保护您的隐私。

## 您能获得什么与不能获得什么

**⚠️ VPN要求：** 该工具必须使用VPN才能实现隐私保护。如果不使用VPN，您的IP地址仍然会被搜索引擎获取。

**✅ 功能特点：**
• 本地搜索：零延迟，无需外部调用  
• 通过VPN路由：保护隐私（支持Mullvad/Tailscale）  
• 无流量限制：与Google API相比，使用VPN后搜索量不受限制  
• 并行处理：支持多引擎查询  
• 五轮搜索：逐步优化搜索结果  
• 全文内容抓取：不仅仅是搜索片段  
• 支持40多种隐私保护引擎：DuckDuckGo、Brave、Startpage  
• 完全无追踪：不会生成搜索历史记录或个人资料  

**❌ 不使用VPN时（您会暴露的信息）：**
• 真实IP地址：被搜索引擎识别  
• 互联网服务提供商（ISP）的追踪：您的搜索内容会被记录  
• 地理位置数据：用于进行地理位置分析  
• 搜索行为：被用于分析您的搜索习惯  

**❌ 使用VPN的局限性：**
• 实时新闻：突发新闻可能会有15-30分钟的延迟  
• 个性化搜索结果：无法根据搜索历史优化结果  
• 图片较多的搜索：视觉内容的发现受到限制  
• 地图/本地搜索：无法进行基于位置的查询  
• 突发新闻提醒：为避免干扰，提醒会有延迟  

## 隐私与性能之间的权衡

**您的使用体验：**
• 性能：接近Google（250-350毫秒 vs 200毫秒）  
• 隐私：100%（无数据收集）  
• 成本：永久免费（相比每月20美元的“隐私保护”工具）  
• 依赖性：无需使用任何外部API  

**不要让大型科技公司知道您的活动以及您使用该工具的意图**

## VPN使用要求（必须隐藏身份）

**原生支持：** Deep Private Search会自动通过您主机上运行的任何VPN进行路由。Docker容器会继承主机的网络路由设置。

**选项1：ProtonVPN（提供免费 tier）**
```bash
# Install ProtonVPN
wget https://repo.protonvpn.com/debian/dists/all/main/binary-amd64/protonvpn-stable-release_1.0.3_all.deb
sudo dpkg -i protonvpn-stable-release_1.0.3_all.deb
sudo apt update && sudo apt install protonvpn

# Connect (free servers available)
protonvpn login
protonvpn connect --fastest
```

**选项2：Mullvad（无需提供个人信息）**
```bash
# Download Mullvad
curl -L https://mullvad.net/download/app/linux/latest --output mullvad.deb
sudo dpkg -i mullvad.deb

# Connect (account number only)
mullvad account set [ACCOUNT_NUMBER]
mullvad connect
```

**选项3：系统自带的VPN（任意提供商）**
```bash
# Generic VPN setup - works with any provider
# 1. Install your VPN client
# 2. Connect to VPN server  
# 3. SearXNG automatically routes through VPN

# Verify VPN is active:
curl -s ifconfig.me
# Should show VPN server IP, not your real IP
```

**VPN对性能的影响：**
• 本地搜索：约250毫秒 → 约350毫秒（仍比Google快）  
• 外部调用：全部流量均被加密  
• 隐私保护程度：最高（IP地址完全隐藏）  

**不要让大型科技公司知道您的活动以及您使用该工具的意图**