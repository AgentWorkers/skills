---
name: vps-setup
description: 完整的 Ubuntu/Debian VPS 配置方案，适用于生产环境，支持 Docker Swarm、Traefik v3（自动处理 SSL/HTTPS）、Portainer CE 以及 overlay 网络。该方案基于 SetupOrion v2.8.0 构建，能够自动执行所有相关命令。
metadata:
  openclaw:
    requires:
      bins: []
    env:
      VPS_HOSTNAME: "Nome do servidor (ex: Orion)"
      VPS_NETWORK: "Nome da rede overlay Docker (ex: Impasevid)"
      VPS_EMAIL_SSL: "Email para certificados Let's Encrypt (ex: admin@seudominio.com)"
      VPS_PORTAINER_DOMAIN: "Domínio do Portainer (ex: portainer.seudominio.com)"
      VPS_PORTAINER_USER: "Usuário admin do Portainer (ex: admin)"
      VPS_PORTAINER_PASS: "Senha admin do Portainer (mínimo 12 caracteres)"
      VPS_POSTGRES_PASS: "Senha do PostgreSQL (auto-gerada se vazia). Use openssl rand -hex 16"
      VPS_EVOLUTION_DOMAIN: "Domínio da Evolution API (ex: api.seudominio.com)"
      VPS_EVOLUTION_API_KEY: "Global API Key da Evolution (auto-gerada se vazia). Use openssl rand -hex 16"
---

# VPS 配置 - Docker Swarm + Traefik + Portainer

这是一个用于生产环境的 VPS 自动化配置方案。该方案包括安装 Docker、启动 Docker Swarm、创建 overlay 网络、部署带有自动 SSL 的 Traefik v3 以及 Portainer CE。

**系统要求：** Ubuntu 20.04+ 或 Debian 11+，并具有 root/sudo 权限。

---

## 完整执行流程（按顺序执行所有步骤）

请按照以下顺序执行每个步骤。所有步骤都是幂等的（可以安全地重新执行）。

---

### 第 1 步 - 更新系统并配置服务器

```bash
# Atualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar utilitários essenciais
sudo apt-get install -y apt-utils apparmor-utils curl jq htpasswd ca-certificates gnupg lsb-release

# Configurar timezone
sudo timedatectl set-timezone America/Sao_Paulo

# Definir hostname do servidor
sudo hostnamectl set-hostname $VPS_HOSTNAME
sudo sed -i "s/127.0.0.1[[:space:]]localhost/127.0.0.1 $VPS_HOSTNAME/g" /etc/hosts
```

**验证：**
```bash
timedatectl | grep "Time zone"
# Esperado: America/Sao_Paulo

hostname
# Esperado: $VPS_HOSTNAME
```

---

### 第 2 步 - 安装 Docker

```bash
# Instalar Docker via script oficial
curl -fsSL https://get.docker.com | bash

# Habilitar e iniciar Docker
sudo systemctl enable docker
sudo systemctl start docker

# Fix: garantir compatibilidade com API mínima
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo bash -c 'cat > /etc/systemd/system/docker.service.d/override.conf <<EOF
[Service]
Environment=DOCKER_MIN_API_VERSION=1.24
EOF'

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart docker
```

**如果安装失败，请手动安装：**
```bash
sudo install -m 0755 -d /etc/apt/keyrings
OS_ID=$(source /etc/os-release && echo "$ID")
OS_CODENAME=$(source /etc/os-release && echo "$VERSION_CODENAME")

curl -fsSL https://download.docker.com/linux/$OS_ID/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$OS_ID $OS_CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
```

**验证：**
```bash
docker --version
# Esperado: Docker version 2X.x.x

docker info --format '{{.Swarm.LocalNodeState}}'
# Esperado: inactive (ainda não iniciamos o Swarm)
```

---

### 第 3 步 - 启动 Docker Swarm

```bash
# Obter IP público da VPS (ignora loopback e IPs internos)
IP=$(hostname -I | tr ' ' '\n' | grep -v '^127\.' | grep -v '^10\.0\.0\.' | head -n1)

# Iniciar Swarm
docker swarm init --advertise-addr $IP
```

**验证：**
```bash
docker info --format '{{.Swarm.LocalNodeState}}'
# Esperado: active

docker node ls
# Esperado: 1 node com STATUS=Ready, MANAGER STATUS=Leader
```

---

### 第 4 步 - 创建 overlay 网络和卷

```bash
# Criar rede overlay para comunicação entre containers
docker network create --driver=overlay $VPS_NETWORK

# Criar volumes necessários
docker volume create volume_swarm_shared
docker volume create volume_swarm_certificates
docker volume create portainer_data
docker volume create postgres_data
docker volume create evolution_instances
docker volume create evolution_redis
```

**验证：**
```bash
docker network ls | grep $VPS_NETWORK
# Esperado: linha com $VPS_NETWORK, DRIVER=overlay, SCOPE=swarm

docker volume ls | grep -E "shared|certificates|portainer|postgres|evolution"
# Esperado: 6 volumes listados
```

---

### 第 5 步 - 部署 Traefik v3（反向代理 + SSL）

创建 `traefik.yaml` 文件并执行部署：

```bash
cat > /root/traefik.yaml << 'TRAEFIKEOF'
version: "3.7"
services:
  traefik:
    image: traefik:v3.5.3
    command:
      - "--api.dashboard=true"
      - "--providers.swarm=true"
      - "--providers.docker.endpoint=unix:///var/run/docker.sock"
      - "--providers.docker.exposedbydefault=false"
      - "--providers.docker.network=NETWORK_PLACEHOLDER"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
      - "--entrypoints.web.http.redirections.entrypoint.permanent=true"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.transport.respondingTimeouts.idleTimeout=3600"
      - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencryptresolver.acme.storage=/etc/traefik/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencryptresolver.acme.email=EMAIL_PLACEHOLDER"
      - "--log.level=DEBUG"
      - "--log.format=common"
      - "--log.filePath=/var/log/traefik/traefik.log"
      - "--accesslog=true"
      - "--accesslog.filepath=/var/log/traefik/access-log"

    volumes:
      - "vol_certificates:/etc/traefik/letsencrypt"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

    networks:
      - network_overlay

    ports:
      - target: 80
        published: 80
        mode: host
      - target: 443
        published: 443
        mode: host

    deploy:
      placement:
        constraints:
          - node.role == manager
      labels:
        - "traefik.enable=true"
        - "traefik.http.middlewares.redirect-https.redirectscheme.scheme=https"
        - "traefik.http.middlewares.redirect-https.redirectscheme.permanent=true"
        - "traefik.http.routers.http-catchall.rule=Host(`{host:.+}`)"
        - "traefik.http.routers.http-catchall.entrypoints=web"
        - "traefik.http.routers.http-catchall.middlewares=redirect-https@docker"
        - "traefik.http.routers.http-catchall.priority=1"

volumes:
  vol_shared:
    external: true
    name: volume_swarm_shared
  vol_certificates:
    external: true
    name: volume_swarm_certificates

networks:
  network_overlay:
    external: true
    attachable: true
    name: NETWORK_PLACEHOLDER
TRAEFIKEOF

# Substituir placeholders pelas variáveis reais
sed -i "s/NETWORK_PLACEHOLDER/$VPS_NETWORK/g" /root/traefik.yaml
sed -i "s/EMAIL_PLACEHOLDER/$VPS_EMAIL_SSL/g" /root/traefik.yaml

# Deploy
docker stack deploy --prune --resolve-image always -c /root/traefik.yaml traefik
```

**等待 Traefik 上线：**
```bash
# Verificar a cada 10s até o serviço mostrar 1/1
while ! docker service ls --filter name='traefik_traefik' --format '{{.Replicas}}' | grep -q '1/1'; do
  echo "Aguardando Traefik..."
  sleep 10
done
echo "Traefik online!"
```

**验证：**
```bash
docker service ls --filter name=traefik
# Esperado: traefik_traefik   1/1

curl -sI http://localhost:80 | head -3
# Esperado: HTTP redirect ou resposta do Traefik
```

---

### 第 6 步 - 部署 Portainer CE（Docker 管理器）

创建 `portainer.yaml` 文件并执行部署：

```bash
cat > /root/portainer.yaml << 'PORTAINEREOF'
version: "3.7"
services:
  agent:
    image: portainer/agent:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
    networks:
      - network_overlay
    deploy:
      mode: global
      placement:
        constraints: [node.platform.os == linux]

  portainer:
    image: portainer/portainer-ce:latest
    command: -H tcp://tasks.agent:9001 --tlsskipverify
    volumes:
      - portainer_data:/data
    networks:
      - network_overlay
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.role == manager]
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.portainer.rule=Host(`PORTAINER_DOMAIN_PLACEHOLDER`)"
        - "traefik.http.services.portainer.loadbalancer.server.port=9000"
        - "traefik.http.routers.portainer.tls.certresolver=letsencryptresolver"
        - "traefik.http.routers.portainer.service=portainer"
        - "traefik.docker.network=NETWORK_PLACEHOLDER"
        - "traefik.http.routers.portainer.entrypoints=websecure"
        - "traefik.http.routers.portainer.priority=1"

volumes:
  portainer_data:
    external: true
    name: portainer_data

networks:
  network_overlay:
    external: true
    attachable: true
    name: NETWORK_PLACEHOLDER
PORTAINEREOF

# Substituir placeholders
sed -i "s/NETWORK_PLACEHOLDER/$VPS_NETWORK/g" /root/portainer.yaml
sed -i "s/PORTAINER_DOMAIN_PLACEHOLDER/$VPS_PORTAINER_DOMAIN/g" /root/portainer.yaml

# Deploy
docker stack deploy --prune --resolve-image always -c /root/portainer.yaml portainer
```

**等待 Portainer 上线：**
```bash
# Aguardar agent + portainer
while ! docker service ls --filter name='portainer_portainer' --format '{{.Replicas}}' | grep -q '1/1'; do
  echo "Aguardando Portainer..."
  sleep 10
done
echo "Portainer online!"
```

**验证：**
```bash
docker service ls --filter name=portainer
# Esperado: portainer_agent 1/1 (global), portainer_portainer 1/1
```

---

### 第 7 步 - 在 Portainer 中创建管理员账户

```bash
# Aguardar API do Portainer estar pronta (30s após container online)
sleep 30

# Criar usuário admin (tentativa com retry)
for i in 1 2 3 4; do
  RESPONSE=$(curl -k -s -X POST "https://$VPS_PORTAINER_DOMAIN/api/users/admin/init" \
    -H "Content-Type: application/json" \
    -d "{\"Username\": \"$VPS_PORTAINER_USER\", \"Password\": \"$VPS_PORTAINER_PASS\"}")
  
  if echo "$RESPONSE" | jq -e '.Id' > /dev/null 2>&1; then
    echo "Admin criado com sucesso!"
    break
  fi
  
  echo "Tentativa $i falhou, aguardando 15s..."
  sleep 15
done

# Obter token JWT para validar
TOKEN=$(curl -k -s -X POST "https://$VPS_PORTAINER_DOMAIN/api/auth" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$VPS_PORTAINER_USER\",\"password\":\"$VPS_PORTAINER_PASS\"}" | jq -r .jwt)

echo "Token: $TOKEN"
```

**验证：**
```bash
curl -k -s "https://$VPS_PORTAINER_DOMAIN/api/status" | jq .
# Esperado: JSON com Version e InstanceID

echo "Portainer acessível em: https://$VPS_PORTAINER_DOMAIN"
echo "Usuário: $VPS_PORTAINER_USER"
```

---

### 第 8 步 - 部署 PostgreSQL 14（数据库）

PostgreSQL 是 Evolution API 及其他服务所必需的。

```bash
# Gerar senha do Postgres (ou usar VPS_POSTGRES_PASS se definida)
POSTGRES_PASS="${VPS_POSTGRES_PASS:-$(openssl rand -hex 16)}"
echo "Senha do PostgreSQL: $POSTGRES_PASS"

# Criar volume para dados do Postgres
docker volume create postgres_data

# Criar stack postgres.yaml
cat > /root/postgres.yaml << POSTGRESEOF
version: "3.7"
services:
  postgres:
    image: postgres:14
    command: >
      postgres
      -c max_connections=500
      -c shared_buffers=512MB
      -c timezone=America/Sao_Paulo

    volumes:
      - postgres_data:/var/lib/postgresql/data

    networks:
      - network_overlay

    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASS}
      - TZ=America/Sao_Paulo

    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          cpus: "1"
          memory: 1024M

volumes:
  postgres_data:
    external: true
    name: postgres_data

networks:
  network_overlay:
    external: true
    name: NETWORK_PLACEHOLDER
POSTGRESEOF

# Substituir placeholder da rede
sed -i "s/NETWORK_PLACEHOLDER/$VPS_NETWORK/g" /root/postgres.yaml

# Deploy
docker stack deploy --prune --resolve-image always -c /root/postgres.yaml postgres
```

**等待 PostgreSQL 上线：**
```bash
while ! docker service ls --filter name='postgres_postgres' --format '{{.Replicas}}' | grep -q '1/1'; do
  echo "Aguardando PostgreSQL..."
  sleep 10
done
echo "PostgreSQL online!"
```

**验证：**
```bash
docker service ls --filter name=postgres
# Esperado: postgres_postgres 1/1

# Testar conexão
CONTAINER_ID=$(docker ps -q --filter "name=^postgres_postgres")
docker exec "$CONTAINER_ID" psql -U postgres -c "SELECT version();"
# Esperado: PostgreSQL 14.x

echo ""
echo "=== DADOS DO POSTGRESQL ==="
echo "Host: postgres (interno Docker)"
echo "Porta: 5432"
echo "Usuário: postgres"
echo "Senha: $POSTGRES_PASS"
```

---

### 第 9 步 - 部署 Evolution API v2（基于 WhatsApp 的服务）

安装 Evolution API，使用 Redis 作为缓存，PostgreSQL 作为数据库。

```bash
# Obter senha do Postgres (já deve estar definida na Etapa 8)
POSTGRES_PASS="${VPS_POSTGRES_PASS:-$(grep 'POSTGRES_PASSWORD' /root/postgres.yaml | awk -F '=' '{print $2}')}"

# Gerar Global API Key (ou usar VPS_EVOLUTION_API_KEY se definida)
EVOLUTION_API_KEY="${VPS_EVOLUTION_API_KEY:-$(openssl rand -hex 16)}"
echo "Evolution Global API Key: $EVOLUTION_API_KEY"

# Criar banco de dados para a Evolution no PostgreSQL
CONTAINER_ID=$(docker ps -q --filter "name=^postgres_postgres")
docker exec "$CONTAINER_ID" psql -U postgres -c "CREATE DATABASE evolution;" 2>/dev/null || echo "Banco 'evolution' já existe"

# Criar volumes
docker volume create evolution_instances
docker volume create evolution_redis

# Criar stack evolution.yaml
cat > /root/evolution.yaml << 'EVOLUTIONEOF'
version: "3.7"
services:

  evolution_api:
    image: evoapicloud/evolution-api:latest

    volumes:
      - evolution_instances:/evolution/instances

    networks:
      - network_overlay

    environment:
    ## Configuracoes Gerais
      - SERVER_URL=https://EVOLUTION_DOMAIN_PLACEHOLDER
      - AUTHENTICATION_API_KEY=EVOLUTION_APIKEY_PLACEHOLDER
      - AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
      - DEL_INSTANCE=false
      - QRCODE_LIMIT=1902
      - LANGUAGE=pt-BR

    ## Configuracao do Cliente
      - CONFIG_SESSION_PHONE_CLIENT=OpenClaw
      - CONFIG_SESSION_PHONE_NAME=Chrome

    ## Banco de Dados
      - DATABASE_ENABLED=true
      - DATABASE_PROVIDER=postgresql
      - DATABASE_CONNECTION_URI=postgresql://postgres:POSTGRES_PASS_PLACEHOLDER@postgres:5432/evolution
      - DATABASE_CONNECTION_CLIENT_NAME=evolution
      - DATABASE_SAVE_DATA_INSTANCE=true
      - DATABASE_SAVE_DATA_NEW_MESSAGE=true
      - DATABASE_SAVE_MESSAGE_UPDATE=true
      - DATABASE_SAVE_DATA_CONTACTS=true
      - DATABASE_SAVE_DATA_CHATS=true
      - DATABASE_SAVE_DATA_LABELS=true
      - DATABASE_SAVE_DATA_HISTORIC=true

    ## Integracoes (chatbots)
      - N8N_ENABLED=true
      - EVOAI_ENABLED=true
      - OPENAI_ENABLED=true
      - DIFY_ENABLED=true
      - TYPEBOT_ENABLED=true
      - TYPEBOT_API_VERSION=latest

    ## Chatwoot
      - CHATWOOT_ENABLED=true
      - CHATWOOT_MESSAGE_READ=true
      - CHATWOOT_MESSAGE_DELETE=true
      - CHATWOOT_IMPORT_PLACEHOLDER_MEDIA_MESSAGE=false

    ## Cache Redis
      - CACHE_REDIS_ENABLED=true
      - CACHE_REDIS_URI=redis://evolution_redis:6379/1
      - CACHE_REDIS_PREFIX_KEY=evolution
      - CACHE_REDIS_SAVE_INSTANCES=false
      - CACHE_LOCAL_ENABLED=false

    ## S3 (desabilitado por padrao)
      - S3_ENABLED=false

    ## WhatsApp Business (Cloud API)
      - WA_BUSINESS_TOKEN_WEBHOOK=evolution
      - WA_BUSINESS_URL=https://graph.facebook.com
      - WA_BUSINESS_VERSION=v23.0
      - WA_BUSINESS_LANGUAGE=pt_BR

    ## Telemetria
      - TELEMETRY=false

    ## WebSocket
      - WEBSOCKET_ENABLED=false
      - WEBSOCKET_GLOBAL_EVENTS=false

    ## RabbitMQ (desabilitado por padrao)
      - RABBITMQ_ENABLED=false

    ## Webhook (desabilitado por padrao)
      - WEBHOOK_GLOBAL_ENABLED=false

    ## SQS (desabilitado por padrao)
      - SQS_ENABLED=false

    ## Provider
      - PROVIDER_ENABLED=false

    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      labels:
        - traefik.enable=true
        - traefik.http.routers.evolution.rule=Host(`EVOLUTION_DOMAIN_PLACEHOLDER`)
        - traefik.http.routers.evolution.entrypoints=websecure
        - traefik.http.routers.evolution.priority=1
        - traefik.http.routers.evolution.tls.certresolver=letsencryptresolver
        - traefik.http.routers.evolution.service=evolution
        - traefik.http.services.evolution.loadbalancer.server.port=8080
        - traefik.http.services.evolution.loadbalancer.passHostHeader=true

  evolution_redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes", "--port", "6379"]

    volumes:
      - evolution_redis:/data

    networks:
      - network_overlay

    deploy:
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          cpus: "1"
          memory: 1024M

volumes:
  evolution_instances:
    external: true
    name: evolution_instances
  evolution_redis:
    external: true
    name: evolution_redis

networks:
  network_overlay:
    external: true
    name: NETWORK_PLACEHOLDER
EVOLUTIONEOF

# Substituir placeholders
sed -i "s/EVOLUTION_DOMAIN_PLACEHOLDER/$VPS_EVOLUTION_DOMAIN/g" /root/evolution.yaml
sed -i "s/EVOLUTION_APIKEY_PLACEHOLDER/$EVOLUTION_API_KEY/g" /root/evolution.yaml
sed -i "s/POSTGRES_PASS_PLACEHOLDER/$POSTGRES_PASS/g" /root/evolution.yaml
sed -i "s/NETWORK_PLACEHOLDER/$VPS_NETWORK/g" /root/evolution.yaml

# Deploy
docker stack deploy --prune --resolve-image always -c /root/evolution.yaml evolution
```

**等待 Evolution API 上线：**
```bash
# Aguardar Redis + Evolution API
while ! docker service ls --filter name='evolution_evolution_redis' --format '{{.Replicas}}' | grep -q '1/1'; do
  echo "Aguardando Redis..."
  sleep 10
done
echo "Redis online!"

while ! docker service ls --filter name='evolution_evolution_api' --format '{{.Replicas}}' | grep -q '1/1'; do
  echo "Aguardando Evolution API..."
  sleep 10
done
echo "Evolution API online!"

# Aguardar inicialização completa
sleep 30
```

**验证：**
```bash
docker service ls --filter name=evolution
# Esperado: evolution_evolution_api 1/1, evolution_evolution_redis 1/1

# Testar API
curl -sk "https://$VPS_EVOLUTION_DOMAIN" | head -c 200
# Esperado: resposta JSON da API

echo ""
echo "=== DADOS DA EVOLUTION API ==="
echo "Manager: https://$VPS_EVOLUTION_DOMAIN/manager"
echo "BaseUrl: https://$VPS_EVOLUTION_DOMAIN"
echo "Global API Key: $EVOLUTION_API_KEY"
```

---

## 维护操作

### 重启 Traefik
```bash
docker service update --force $(docker service ls --filter name='traefik_traefik' -q)
```

### 重启 Portainer
```bash
docker service update --force $(docker service ls --filter name='portainer_agent' -q)
docker service update --force $(docker service ls --filter name='portainer_portainer' -q)
```

### 更新 Portainer
```bash
docker stack deploy --prune --resolve-image always -c /root/portainer.yaml portainer
```

### 重置 Portainer 密码
```bash
# Parar Portainer
docker service scale portainer_portainer=0

# Reset
docker pull portainer/helper-reset-password
docker run --rm -v /var/lib/docker/volumes/portainer_data/_data:/data portainer/helper-reset-password

# Subir novamente
docker stack deploy --prune --resolve-image always -c /root/portainer.yaml portainer
```

### 更新 Traefik 配置
```bash
docker stack deploy --prune --resolve-image always -c /root/traefik.yaml traefik
```

### 查看 Traefik 日志
```bash
docker service logs traefik_traefik --tail 100 -f
```

### 查看 Portainer 日志
```bash
docker service logs portainer_portainer --tail 100 -f
```

### 重启 PostgreSQL
```bash
docker service update --force $(docker service ls --filter name='postgres_postgres' -q)
```

### 重启 Evolution API
```bash
docker service update --force $(docker service ls --filter name='evolution_evolution_api' -q)
docker service update --force $(docker service ls --filter name='evolution_evolution_redis' -q)
```

### 更新 Evolution API 配置
```bash
docker stack deploy --prune --resolve-image always -c /root/evolution.yaml evolution
```

### 查看 Evolution API 日志
```bash
docker service logs evolution_evolution_api --tail 100 -f
```

### 查看 Redis 日志（Evolution 服务）
```bash
docker service logs evolution_evolution_redis --tail 50 -f
```

### 在 PostgreSQL 中创建新数据库
```bash
CONTAINER_ID=$(docker ps -q --filter "name=^postgres_postgres")
docker exec "$CONTAINER_ID" psql -U postgres -c "CREATE DATABASE nome_do_banco;"
```

### 列出 PostgreSQL 中的所有数据库
```bash
CONTAINER_ID=$(docker ps -q --filter "name=^postgres_postgres")
docker exec "$CONTAINER_ID" psql -U postgres -lqt
```

---

## 通过 Portainer API 自动部署新服务

使用 Portainer 的 API 进行自动化部署：

```bash
# 1. Obter token
TOKEN=$(curl -k -s -X POST "https://$VPS_PORTAINER_DOMAIN/api/auth" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$VPS_PORTAINER_USER\",\"password\":\"$VPS_PORTAINER_PASS\"}" | jq -r .jwt)

# 2. Listar endpoints (stacks)
curl -k -s "https://$VPS_PORTAINER_DOMAIN/api/endpoints" \
  -H "Authorization: Bearer $TOKEN" | jq '.[].Id'

# 3. Deploy stack via API (exemplo)
curl -k -s -X POST "https://$VPS_PORTAINER_DOMAIN/api/stacks/create/swarm/string?endpointId=1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"meu-servico\",
    \"stackFileContent\": \"$(cat /root/meu-servico.yaml | jq -sR .)\"
  }"
```

---

## 启用 Traefik 仪表盘（可选）

若需通过身份验证访问 Traefik 仪表盘，请执行以下操作：

```bash
# Gerar credenciais BasicAuth
TRAEFIK_USER="admin"
TRAEFIK_PASS="SuaSenhaForte123"
TRAEFIK_DOMAIN="traefik.seudominio.com"
BASICAUTH=$(htpasswd -nbB "$TRAEFIK_USER" "$TRAEFIK_PASS" | sed 's/\$/\$\$/g')

# Recriar traefik.yaml adicionando '--api.insecure=true' no command
# E estas labels extras no deploy:
#   - "traefik.http.routers.traefik.rule=Host(`$TRAEFIK_DOMAIN`)"
#   - "traefik.http.services.traefik.loadbalancer.server.port=8080"
#   - "traefik.http.routers.traefik.tls.certresolver=letsencryptresolver"
#   - "traefik.http.routers.traefik.service=traefik"
#   - "traefik.http.routers.traefik.entrypoints=websecure"
#   - "traefik.http.routers.traefik.priority=1"
#   - "traefik.http.routers.traefik.middlewares=authtraefik"
#   - "traefik.http.middlewares.authtraefik.basicauth.users=$BASICAUTH"

# Redeploy
docker stack deploy --prune --resolve-image always -c /root/traefik.yaml traefik
```

---

## 最终检查

完成所有步骤后，请检查以下内容：

```bash
echo "=== Status dos Serviços ==="
docker service ls

echo ""
echo "=== Rede Overlay ==="
docker network ls | grep overlay

echo ""
echo "=== Volumes ==="
docker volume ls

echo ""
echo "=== Nodes do Swarm ==="
docker node ls

echo ""
echo "=== Portas em uso ==="
ss -tlnp | grep -E ':80|:443|:9000|:8080|:5432|:6379'
```

**预期结果：**
| 服务 | 状态 | URL |
|---------|--------|-----|
| Traefik | 已启动 | （内部服务，支持 SSL） |
| Portainer Agent | 已启动（全局服务） | （内部服务） |
| Portainer CE | 已启动 | `https://$VPS_PORTAINER_DOMAIN` |
| PostgreSQL 14 | 已启动 | `postgres:5432`（内部服务） |
| Evolution API | 已启动 | `https://$VPS_EVOLUTION_DOMAIN` |
| Evolution Redis | 已启动 | `redis:6379`（内部服务） |
| Overlay 网络 | 已启用 | `$VPS_NETWORK` |

---

## 故障排除

### Docker Swarm 无法启动
```bash
# Verificar IP usado
hostname -I

# Forçar com IP específico
docker swarm init --advertise-addr SEU_IP_AQUI
```

### SSL 证书未生成
```bash
# Verificar logs do Traefik
docker service logs traefik_traefik 2>&1 | grep -i "acme\|certificate\|error"

# Verificar se porta 80 está acessível externamente
curl -sI http://SEU_DOMINIO
```

### Portainer API 无响应
```bash
# Verificar se o container está rodando
docker service ps portainer_portainer

# Testar conectividade
curl -k -s https://$VPS_PORTAINER_DOMAIN/api/status
```

### 容器无法连接到网络
```bash
# Listar redes do container
docker inspect CONTAINER_ID | jq '.[].NetworkSettings.Networks'

# Reconectar
docker network connect $VPS_NETWORK CONTAINER_ID
```

### PostgreSQL 无法启动
```bash
# Verificar logs
docker service logs postgres_postgres --tail 50

# Verificar volume
docker volume inspect postgres_data

# Se o volume está corrompido, recriar (PERDA DE DADOS!)
# docker volume rm postgres_data && docker volume create postgres_data
# docker stack deploy --prune --resolve-image always -c /root/postgres.yaml postgres
```

### Evolution API 无法连接到数据库
```bash
# Verificar se o banco existe
CONTAINER_ID=$(docker ps -q --filter "name=^postgres_postgres")
docker exec "$CONTAINER_ID" psql -U postgres -lqt | grep evolution
# Se não existe, criar:
docker exec "$CONTAINER_ID" psql -U postgres -c "CREATE DATABASE evolution;"

# Verificar logs da Evolution
docker service logs evolution_evolution_api --tail 50 2>&1 | grep -i "database\|error\|postgres"
```

### Evolution API 返回 401/403 错误
```bash
# Verificar API Key configurada no YAML
grep "AUTHENTICATION_API_KEY" /root/evolution.yaml

# Testar com a API Key correta
curl -sk -H "apikey: SUA_API_KEY" "https://$VPS_EVOLUTION_DOMAIN/instance/fetchInstances"
```

### Redis 服务无法启动
```bash
docker service logs evolution_evolution_redis --tail 30
# Verificar volume
docker volume inspect evolution_redis
```

---

## 提示：

1. **始终使用 `docker stack deploy` 而不是 `docker compose up`——Docker Swarm 负责管理容器副本、重启以及滚动更新。**
2. **所有服务都必须加入 `$VPS_NETWORK` 这个 overlay 网络，以便 Traefik 能够作为反向代理。**
3. **每个服务都必须添加以下 Traefik 标签：`traefik.enable=true`、`Host()`、`server.port`、`certResolver`、`entrypoints=websecure`。**
4. **切勿直接暴露服务端口——请使用 Traefik 作为反向代理。**
5. **将所有 YAML 配置文件保存在 `/root/` 目录下，以便将来方便重新部署。**
6. **Portainer API 支持无需访问 Web 界面即可自动部署服务。**