---
name: maven-central-publish
description: "使用现代的 Central Portal (central.sonatype.com) 工作流程，将 Java 构件发布到 Maven Central 的全面指南和工具包。"
version: 1.0.0
metadata:
  openclaw:
    emoji: "📦"
    category: publishing
  clawhub:
    requires:
      bins: ["maven", "gpg"]
---

# 使用Maven Central发布Java/Kotlin库的技能

本技能提供了一种标准化的流程，用于通过现代的**Central Portal**（通过`central-publishing-maven-plugin`）将Java/Kotlin库发布到Maven Central仓库。

## 📋 先决条件

1. **Central Portal账户**：在[central.sonatype.com](https://central.sonatype.com/)注册一个账户。
2. **命名空间已验证**：您必须在Portal中验证您的`groupId`（例如`io.github.username`或`com.yourdomain`）。
3. **用户令牌**：在Central Portal中生成（我的账户 -> 生成用户令牌）。

## 🛠️ 环境设置

### 1. 安装工具
确保已安装`maven`、`gnupg`和`openjdk-17+`。

```bash
# Ubuntu/Debian
apt-get install -y maven gnupg openjdk-17-jdk
```

### 2. GPG配置（至关重要）
Maven需要GPG签名。对于自动化/无头环境，必须使用**Loopback Pinentry**。

```bash
# 1. Generate Key (if none exists)
gpg --gen-key

# 2. Configure Loopback (Prevent UI prompts)
mkdir -p ~/.gnupg
echo "allow-loopback-pinentry" >> ~/.gnupg/gpg-agent.conf
echo "pinentry-mode loopback" >> ~/.gnupg/gpg.conf
gpg-connect-agent reloadagent /bye

# 3. Publish Key
gpg --list-keys # Get your Key ID (last 8 chars or full hex)
gpg --keyserver keyserver.ubuntu.com --send-keys <KEY_ID>
```

### 3. Maven配置（`~/.m2/settings.xml`）
配置您的Central Portal凭据。

```xml
<settings>
  <servers>
    <server>
      <id>central</id>
      <username>USER_TOKEN_USERNAME</username>
      <password>USER_TOKEN_PASSWORD</password>
    </server>
  </servers>
  <profiles>
    <profile>
      <id>release</id>
      <activation>
        <activeByDefault>false</activeByDefault>
      </activation>
      <properties>
        <gpg.executable>gpg</gpg.executable>
        <gpg.passphrase>YOUR_GPG_PASSPHRASE</gpg.passphrase>
      </properties>
    </profile>
  </profiles>
</settings>
```

## 📦 项目配置（`pom.xml`）

您的项目**必须**符合[质量要求](https://central.sonatype.org/publish/requirements/)：
1. **坐标信息**：`groupId`、`artifactId`、`version`。
2. **元数据**：`name`、`description`、`url`、`licenses`、`developers`、`scm`。
3. **插件**：Javadoc、Source、GPG和Central Publishing。

### 推荐的插件配置

将以下配置添加到您的`<build><plugins>`部分：

```xml
<!-- 1. Source Plugin -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-source-plugin</artifactId>
    <version>3.3.0</version>
    <executions>
        <execution>
            <id>attach-sources</id>
            <goals><goal>jar-no-fork</goal></goals>
        </execution>
    </executions>
</plugin>

<!-- 2. Javadoc Plugin -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-javadoc-plugin</artifactId>
    <version>3.6.3</version>
    <configuration>
        <doclint>none</doclint> <!-- Prevent strict checks failing build -->
        <failOnError>false</failOnError>
    </configuration>
    <executions>
        <execution>
            <id>attach-javadocs</id>
            <goals><goal>jar</goal></goals>
        </execution>
    </executions>
</plugin>

<!-- 3. GPG Plugin (Best Practice: wrap in 'release' profile) -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-gpg-plugin</artifactId>
    <version>3.1.0</version>
    <configuration>
        <gpgArguments>
            <arg>--pinentry-mode</arg>
            <arg>loopback</arg>
        </gpgArguments>
    </configuration>
    <executions>
        <execution>
            <id>sign-artifacts</id>
            <phase>verify</phase>
            <goals><goal>sign</goal></goals>
        </execution>
    </executions>
</plugin>

<!-- 4. Central Publishing Plugin (The Magic Sauce) -->
<plugin>
    <groupId>org.sonatype.central</groupId>
    <artifactId>central-publishing-maven-plugin</artifactId>
    <version>0.7.0</version>
    <extensions>true</extensions>
    <configuration>
        <publishingServerId>central</publishingServerId>
        <!-- autoPublish: set to true to skip manual button click in portal -->
        <autoPublish>false</autoPublish> 
    </configuration>
</plugin>
```

## 🚀 部署

使用`release`配置文件运行部署命令：

```bash
mvn clean deploy -P release
```

**成功指示**：
- `[INFO] 包上传成功...`
- `[INFO] 部署...已验证。`

如果`autoPublish`设置为`false`（首次发布时推荐），请登录[central.sonatype.com](https://central.sonatype.com/publishing/deployments)，查看部署信息，然后点击**Publish**。

## ❓ 故障排除

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `401 Unauthorized` | `settings.xml`中的用户令牌无效 | 在Central Portal中生成新的令牌，并确保服务器ID匹配。 |
| GPG签名失败 | 未启用Pinentry或密码错误 | 使用`pinentry-mode loopback`配置；检查`gpg-agent`。 |
| Javadoc生成失败 | HTML检查过于严格 | 在javadoc插件配置中添加`<doclint>none</doclint>`。 |
| 坐标信息无效 | `groupId`不匹配 | 确保`pom.xml`中的`groupId`与Portal中验证的命名空间一致。 |