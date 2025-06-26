# Azure デプロイメントガイド - Streamlit TODO アプリ

このガイドでは、既存のStreamlit TODO リストアプリをAzureにデプロイするための包括的な情報を提供します。

## 📋 目次

1. [推奨Azureサービス](#推奨azureサービス)
2. [前提条件](#前提条件)
3. [デプロイメント方法](#デプロイメント方法)
4. [データ永続化](#データ永続化)
5. [セキュリティ設定](#セキュリティ設定)
6. [運用と監視](#運用と監視)
7. [トラブルシューティング](#トラブルシューティング)

## 🔧 推奨Azureサービス

### 1. Azure Container Instances (ACI) - 推奨度: ★★★★☆
**最適な用途**: 開発・テスト環境、小規模運用

**メリット**:
- 最も簡単で迅速なデプロイメント
- サーバーレス的な運用（使用した分だけ課金）
- Dockerコンテナをそのまま実行可能

**デメリット**:
- カスタムドメインの設定が複雑
- 高可用性オプションが限定的

### 2. Azure App Service - 推奨度: ★★★★★
**最適な用途**: 本番環境、継続的な運用

**メリット**:
- PaaS（Platform as a Service）による完全管理
- 自動スケーリング機能
- カスタムドメインとSSL証明書の簡単設定
- 継続的デプロイメント（CI/CD）サポート
- Application Insights との統合

**デメリット**:
- コンテナ化よりもわずかに設定が複雑

### 3. Azure Container Apps - 推奨度: ★★★★☆
**最適な用途**: モダンなクラウドネイティブアプリケーション

**メリット**:
- Kubernetes ベースの最新プラットフォーム
- 自動スケーリング（ゼロスケールを含む）
- マイクロサービス対応

**デメリット**:
- 比較的新しいサービス
- 単純なアプリには機能過多の可能性

## 📝 前提条件

### 必要なツール
- **Azure CLI** (バージョン 2.30.0 以降)
- **Docker Desktop** （コンテナ化デプロイメントの場合）
- **Git** 
- **Python 3.8+**

### Azureアカウント要件
- アクティブなAzureサブスクリプション
- リソースグループ作成権限
- App Service または Container Instances 作成権限

### 事前準備
```bash
# Azure CLI のインストール確認
az --version

# Azure にログイン
az login

# 使用するサブスクリプション設定
az account set --subscription "your-subscription-id"
```

## 🚀 デプロイメント方法

### 方法1: Azure App Service（推奨）

#### ステップ1: 必要なファイルを追加

**requirements.txt** (既存)
```
streamlit>=1.28.0
```

**startup.sh** (新規作成)
```bash
#!/bin/bash
python -m streamlit run app.py --server.port=8000 --server.address=0.0.0.0 --server.headless=true
```

#### ステップ2: App Service作成とデプロイ
```bash
# リソースグループ作成
az group create --name rg-streamlit-todo --location japaneast

# App Service プラン作成
az appservice plan create \
  --name plan-streamlit-todo \
  --resource-group rg-streamlit-todo \
  --sku B1 \
  --is-linux

# Web App 作成
az webapp create \
  --resource-group rg-streamlit-todo \
  --plan plan-streamlit-todo \
  --name streamlit-todo-app-unique \
  --runtime "PYTHON|3.11" \
  --startup-file startup.sh

# ソースコードデプロイ
az webapp deployment source config-zip \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --src deployment.zip
```

#### ステップ3: アプリケーション設定
```bash
# アプリケーション設定
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --settings \
    STREAMLIT_SERVER_PORT=8000 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true
```

**アクセスURL**: `https://streamlit-todo-app-unique.azurewebsites.net`

### 方法2: Azure Container Instances

#### ステップ1: Dockerfile作成
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

#### ステップ2: コンテナレジストリとデプロイ
```bash
# Azure Container Registry 作成
az acr create \
  --resource-group rg-streamlit-todo \
  --name streamlittodoregistry \
  --sku Basic

# Docker イメージビルドとプッシュ
az acr build \
  --registry streamlittodoregistry \
  --image streamlit-todo:latest .

# Container Instance 作成
az container create \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-container \
  --image streamlittodoregistry.azurecr.io/streamlit-todo:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server streamlittodoregistry.azurecr.io \
  --registry-username streamlittodoregistry \
  --registry-password $(az acr credential show --name streamlittodoregistry --query passwords[0].value -o tsv) \
  --ip-address public \
  --ports 8501
```

**アクセスURL**: Container Instances の パブリックIPアドレス:8501

### 方法3: Azure Container Apps

#### ステップ1: Container Apps環境作成
```bash
# Container Apps 拡張機能インストール
az extension add --name containerapp --upgrade

# Container Apps 環境作成
az containerapp env create \
  --name containerapp-env-streamlit \
  --resource-group rg-streamlit-todo \
  --location japaneast

# Container App 作成
az containerapp create \
  --name streamlit-todo-containerapp \
  --resource-group rg-streamlit-todo \
  --environment containerapp-env-streamlit \
  --image streamlittodoregistry.azurecr.io/streamlit-todo:latest \
  --target-port 8501 \
  --ingress external \
  --registry-server streamlittodoregistry.azurecr.io
```

## 💾 データ永続化

現在のアプリはセッション状態にデータを保存しており、アプリ再起動時にデータが失われます。永続化のための推奨オプション：

### 1. Azure Database for PostgreSQL（推奨）

#### 設定手順
```bash
# PostgreSQL サーバー作成
az postgres server create \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-postgres \
  --location japaneast \
  --admin-user todouser \
  --admin-password SecurePassword123! \
  --sku-name GP_Gen5_2 \
  --version 13
```

#### アプリケーション修正例
```python
# requirements.txt に追加
# psycopg2-binary

import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )

def init_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
```

### 2. Azure Cosmos DB（NoSQL）

```python
# requirements.txt に追加
# azure-cosmos

from azure.cosmos import CosmosClient

def get_cosmos_client():
    return CosmosClient(
        os.environ.get('COSMOS_URL'),
        os.environ.get('COSMOS_KEY')
    )
```

### 3. Azure Table Storage（軽量オプション）

```python
# requirements.txt に追加  
# azure-data-tables

from azure.data.tables import TableServiceClient

def get_table_client():
    return TableServiceClient(
        account_url=os.environ.get('STORAGE_ACCOUNT_URL'),
        credential=os.environ.get('STORAGE_ACCOUNT_KEY')
    )
```

## 🔒 セキュリティ設定

### 1. HTTPS/SSL証明書

#### App Service での設定
```bash
# カスタムドメイン追加
az webapp config hostname add \
  --webapp-name streamlit-todo-app-unique \
  --resource-group rg-streamlit-todo \
  --hostname www.yourdomain.com

# SSL証明書設定（App Service Managed Certificate）
az webapp config ssl create \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --hostname www.yourdomain.com
```

### 2. 環境変数とシークレット管理

#### Azure Key Vault 使用
```bash
# Key Vault 作成
az keyvault create \
  --name kv-streamlit-todo \
  --resource-group rg-streamlit-todo \
  --location japaneast

# シークレット追加
az keyvault secret set \
  --vault-name kv-streamlit-todo \
  --name db-password \
  --value "SecurePassword123!"

# App Service での Key Vault 参照設定
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --settings DB_PASSWORD="@Microsoft.KeyVault(VaultName=kv-streamlit-todo;SecretName=db-password)"
```

### 3. ネットワーク制限

#### App Service でのIP制限
```bash
# 特定IPのみアクセス許可
az webapp config access-restriction add \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --rule-name "AllowOfficeIP" \
  --action Allow \
  --ip-address 203.0.113.0/24 \
  --priority 100
```

### 4. Azure Active Directory 認証

```bash
# AAD 認証設定
az webapp auth update \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --enabled true \
  --action LoginWithAzureActiveDirectory \
  --aad-client-id "your-client-id" \
  --aad-client-secret "your-client-secret" \
  --aad-tenant-id "your-tenant-id"
```

## 📊 運用と監視

### 1. Application Insights 設定

```bash
# Application Insights 作成
az monitor app-insights component create \
  --app streamlit-todo-insights \
  --location japaneast \
  --resource-group rg-streamlit-todo

# App Service と連携
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="your-instrumentation-key"
```

### 2. ログ監視

```bash
# ログストリーム表示
az webapp log tail \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique

# ログダウンロード
az webapp log download \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique
```

### 3. 自動スケーリング

```bash
# 自動スケーリング設定
az monitor autoscale create \
  --resource-group rg-streamlit-todo \
  --resource /subscriptions/{subscription-id}/resourceGroups/rg-streamlit-todo/providers/Microsoft.Web/serverfarms/plan-streamlit-todo \
  --name autoscale-streamlit \
  --min-count 1 \
  --max-count 3 \
  --count 1
```

## 🐛 トラブルシューティング

### よくある問題と解決方法

#### 1. ポート設定エラー
**問題**: アプリケーションが起動しない
**解決**: Streamlit のポート設定を確認
```bash
# App Service の場合
--server.port=$PORT または --server.port=8000
```

#### 2. 静的ファイルの読み込みエラー
**問題**: CSS/JSファイルが読み込まれない
**解決**: Azure での静的ファイル設定
```bash
az webapp config set \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --use-32bit-worker-process false
```

#### 3. データベース接続エラー
**問題**: PostgreSQL に接続できない
**解決**: ファイアウォール設定とSSL設定確認
```bash
# PostgreSQL ファイアウォール設定
az postgres server firewall-rule create \
  --resource-group rg-streamlit-todo \
  --server streamlit-todo-postgres \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

#### 4. メモリ不足エラー
**問題**: アプリケーションがクラッシュする
**解決**: App Service プランのアップグレード
```bash
az appservice plan update \
  --resource-group rg-streamlit-todo \
  --name plan-streamlit-todo \
  --sku S1
```

### デバッグコマンド

```bash
# App Service のログ確認
az webapp log show \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique

# リソース使用状況確認
az webapp show \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique \
  --query "{state: state, resourceGroup: resourceGroup, defaultHostName: defaultHostName}"

# 設定値確認
az webapp config appsettings list \
  --resource-group rg-streamlit-todo \
  --name streamlit-todo-app-unique
```

## 📝 まとめ

### 推奨デプロイメント構成

**開発・テスト環境**:
- Azure Container Instances
- Azure Table Storage （データ永続化）

**本番環境**:
- Azure App Service（S1以上）
- Azure Database for PostgreSQL
- Azure Key Vault（シークレット管理）
- Application Insights（監視）
- Azure CDN（パフォーマンス向上）

### 注意事項

1. **コスト最適化**: 不要なリソースは定期的に削除
2. **セキュリティ**: 定期的なパスワートキーローテーション
3. **バックアップ**: データベースの定期バックアップ設定
4. **モニタリング**: アラート設定による異常検知

このガイドに従って、安全で効率的なStreamlit TODOアプリのAzureデプロイメントを実現してください。