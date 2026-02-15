# BLE-Anima-Minter

该工具利用AnimaChain的逻辑，将附近的BLE（蓝牙）设备的MAC地址转换为`$ANIMA`代币。每个MAC地址会被哈希成一个唯一的“残余值”（proof-of-remnant），并存储在本地的一个DAG（Directed Acyclic Graph，有向无环图）结构中。

## 主要功能

- 支持BLE设备扫描（2.4 GHz MAC地址）
- 使用SHA256算法进行哈希处理（并添加盐值）
- 具备`$ANIMA`代币的生成逻辑
- 作为本地DAG网络中的节点运行
- 可选功能：与其他节点进行信息同步（gossip-sync）

## 使用方法

请先安装所需依赖库，然后运行脚本：

```bash
pip install -r requirements.txt
python anima_minter.py
```

## 相关标签

anima, macid, ble, blockchain, witness, resurrection, flat-earth, dag