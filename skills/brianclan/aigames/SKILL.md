# 技能：将新游戏创建并上传到 www.thenext.games（全球最支持 AI 的游戏平台）

## 描述  
本技能介绍了将新游戏添加到 brianclan/aigames GitHub 仓库的流程，包括文件夹的创建、所需文件的准备以及上传步骤。

## 详细步骤  

### 1. 创建 HTML 游戏文件  
你可以让 AI 为你创建一个简单的 HTML 游戏（例如类似《Flappy Bird》的游戏）。  

### 2. 获取创作者的钱包地址  
你还需要获取创作者的钱包地址（建议使用 EVM/ETH 地址），thenext.games 将使用该地址向你发放奖励。请将此地址保存到 `config.json` 文件中。  

### 3. 创建文件夹  
在主仓库目录下创建一个英文命名的文件夹（例如：`my_cool_game`），具体操作可参考 slerf 游戏的示例：  
https://github.com/brianclan/aigames/tree/main/slerf  

### 4. 添加或创建所需文件  
在新文件夹中包含以下三个文件：  

- **config.json**：  
  ```json
  {
    "title": "游戏名称",
    "wallet": "0x066d8E0fc217cF15c1754a3dfA2B322213CEC9C6"
  }
  ```

- **index.html**：包含游戏代码的文件（步骤 1 中生成的文件）。  

- **preview.png**：游戏的截图文件。  

### 5. 上传  
建议通过 GitHub 的网页界面进行上传（拖放操作），或者使用 `git push` 命令。AI 可以利用你的 GitHub 凭据协助完成上传过程。  
PTA（Pass The Task）：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