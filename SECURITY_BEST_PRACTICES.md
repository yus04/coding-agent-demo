# セキュリティ設定とベストプラクティス

Azure上でStreamlit TODOアプリを安全に運用するためのセキュリティ設定とベストプラクティスガイドです。

## 🛡️ セキュリティチェックリスト

### ✅ 必須セキュリティ設定

- [ ] HTTPS/TLS暗号化の有効化
- [ ] 環境変数でのシークレット管理
- [ ] アクセス制限の設定
- [ ] セキュリティヘッダーの設定
- [ ] ログ監視の設定
- [ ] 定期的なセキュリティ更新

### ✅ 推奨セキュリティ設定

- [ ] Azure Key Vault使用
- [ ] Azure Active Directory認証
- [ ] ネットワークレベルでの制限
- [ ] WAF（Web Application Firewall）設定
- [ ] セキュリティスキャンの実装

## 🔐 1. HTTPS/TLS設定

### App Service でのSSL証明書設定

```bash
# 無料のApp Service Managed Certificate
az webapp config ssl create \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --hostname your-domain.com

# HTTPS のみでアクセス強制
az webapp update \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --https-only true

# TLS バージョン設定
az webapp config set \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --min-tls-version 1.2
```

### カスタムドメインでのHTTPS設定

```bash
# カスタムドメイン追加
az webapp config hostname add \
  --webapp-name your-app-name \
  --resource-group rg-streamlit-todo \
  --hostname www.yourdomain.com

# SSL バインディング
az webapp config ssl bind \
  --certificate-thumbprint YOUR_CERT_THUMBPRINT \
  --ssl-type SNI \
  --name your-app-name \
  --resource-group rg-streamlit-todo
```

## 🔑 2. シークレット管理

### Azure Key Vault の使用

```bash
# Key Vault 作成
az keyvault create \
  --name kv-streamlit-todo-unique \
  --resource-group rg-streamlit-todo \
  --location japaneast \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true

# データベースパスワードを格納
az keyvault secret set \
  --vault-name kv-streamlit-todo-unique \
  --name db-password \
  --value "your-secure-password"

# ストレージキーを格納
az keyvault secret set \
  --vault-name kv-streamlit-todo-unique \
  --name storage-key \
  --value "your-storage-account-key"

# App Service にKey Vault アクセス権限付与
az webapp identity assign \
  --resource-group rg-streamlit-todo \
  --name your-app-name

# Identity取得
IDENTITY=$(az webapp identity show --resource-group rg-streamlit-todo --name your-app-name --query principalId --output tsv)

# Key Vault アクセスポリシー設定
az keyvault set-policy \
  --name kv-streamlit-todo-unique \
  --object-id $IDENTITY \
  --secret-permissions get list
```

### App Service でKey Vault参照設定

```bash
# 環境変数でKey Vault参照
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --settings \
    DB_PASSWORD="@Microsoft.KeyVault(VaultName=kv-streamlit-todo-unique;SecretName=db-password)" \
    STORAGE_KEY="@Microsoft.KeyVault(VaultName=kv-streamlit-todo-unique;SecretName=storage-key)"
```

## 🚪 3. アクセス制限

### IPアドレス制限

```bash
# 特定のIPレンジからのアクセスのみ許可
az webapp config access-restriction add \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --rule-name "AllowOfficeNetwork" \
  --action Allow \
  --ip-address 203.0.113.0/24 \
  --priority 100

# Azure サービスからのアクセス拒否
az webapp config access-restriction add \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --rule-name "DenyAzureCloud" \
  --action Deny \
  --service-tag AzureCloud \
  --priority 200

# SCM サイト（管理画面）のアクセス制限
az webapp config access-restriction add \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --rule-name "AllowAdminIP" \
  --action Allow \
  --ip-address 203.0.113.100/32 \
  --priority 100 \
  --scm-site true
```

### 地理的制限

```bash
# 特定の国からのアクセスのみ許可
az webapp config access-restriction add \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --rule-name "AllowJapan" \
  --action Allow \
  --service-tag "Regional.Japan" \
  --priority 300
```

## 🔒 4. Azure Active Directory認証

### AAD認証設定

```bash
# Azure AD アプリ登録
az ad app create \
  --display-name "streamlit-todo-app" \
  --homepage "https://your-app-name.azurewebsites.net" \
  --reply-urls "https://your-app-name.azurewebsites.net/.auth/login/aad/callback"

# クライアントID取得
CLIENT_ID=$(az ad app list --display-name "streamlit-todo-app" --query [0].appId -o tsv)

# クライアントシークレット作成
CLIENT_SECRET=$(az ad app credential reset --id $CLIENT_ID --credential-description "StreamlitTODO" --query password -o tsv)

# App Service 認証設定
az webapp auth update \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --enabled true \
  --action LoginWithAzureActiveDirectory \
  --aad-client-id $CLIENT_ID \
  --aad-client-secret $CLIENT_SECRET \
  --aad-tenant-id $(az account show --query tenantId -o tsv)
```

### 特定ユーザーのみアクセス許可

```bash
# 特定のユーザーグループのみアクセス許可
az webapp auth update \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --aad-allowed-token-audiences "api://your-app-client-id" \
  --aad-client-secret-setting-name "AAD_CLIENT_SECRET"
```

## 🛡️ 5. Web Application Firewall (WAF)

### Application Gateway with WAF

```bash
# Application Gateway用のサブネット作成
az network vnet create \
  --resource-group rg-streamlit-todo \
  --name vnet-streamlit \
  --address-prefix 10.0.0.0/16 \
  --subnet-name subnet-agw \
  --subnet-prefix 10.0.1.0/24

# パブリックIP作成
az network public-ip create \
  --resource-group rg-streamlit-todo \
  --name pip-agw-streamlit \
  --allocation-method Static \
  --sku Standard

# Application Gateway作成（WAF有効）
az network application-gateway create \
  --name agw-streamlit-todo \
  --location japaneast \
  --resource-group rg-streamlit-todo \
  --vnet-name vnet-streamlit \
  --subnet subnet-agw \
  --capacity 2 \
  --sku WAF_v2 \
  --http-settings-cookie-based-affinity Disabled \
  --frontend-port 80 \
  --http-settings-port 80 \
  --http-settings-protocol Http \
  --public-ip-address pip-agw-streamlit \
  --servers your-app-name.azurewebsites.net

# WAF ポリシー作成
az network application-gateway waf-policy create \
  --name waf-policy-streamlit \
  --resource-group rg-streamlit-todo \
  --location japaneast

# WAF ルール設定
az network application-gateway waf-policy policy-setting update \
  --policy-name waf-policy-streamlit \
  --resource-group rg-streamlit-todo \
  --state Enabled \
  --mode Prevention \
  --request-body-check true \
  --max-request-body-size 128
```

## 📊 6. ログ監視とアラート

### Application Insights設定

```bash
# Application Insights作成
az monitor app-insights component create \
  --app streamlit-todo-insights \
  --location japaneast \
  --resource-group rg-streamlit-todo \
  --application-type web

# Instrumentation Key 取得
INSTRUMENTATION_KEY=$(az monitor app-insights component show --app streamlit-todo-insights --resource-group rg-streamlit-todo --query instrumentationKey -o tsv)

# App Service と連携
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY \
    APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$INSTRUMENTATION_KEY"
```

### セキュリティアラート設定

```bash
# 異常なアクセスパターンのアラート
az monitor metrics alert create \
  --name "High Error Rate" \
  --resource-group rg-streamlit-todo \
  --resource your-app-name \
  --resource-type "Microsoft.Web/sites" \
  --condition "avg requests/failed > 10" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group "admin-alerts"

# 大量アクセスのアラート
az monitor metrics alert create \
  --name "High Request Volume" \
  --resource-group rg-streamlit-todo \
  --resource your-app-name \
  --resource-type "Microsoft.Web/sites" \
  --condition "avg requests/count > 1000" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group "admin-alerts"
```

## 🔍 7. セキュリティスキャン

### Azure Security Center設定

```bash
# Security Center 有効化
az security auto-provisioning-setting update \
  --name default \
  --auto-provision on

# セキュリティ推奨事項確認
az security task list \
  --resource-group rg-streamlit-todo
```

### Vulnerability Assessment

```bash
# 脆弱性評価有効化（SQL Database用）
az sql server-va update \
  --resource-group rg-streamlit-todo \
  --server your-db-server \
  --storage-account your-storage-account \
  --storage-endpoint "https://yourstorageaccount.blob.core.windows.net/" \
  --state Enabled
```

## 🔧 8. セキュリティヘッダー設定

Streamlitアプリにセキュリティヘッダーを追加：

```python
# security_headers.py
import streamlit as st

def set_security_headers():
    """セキュリティヘッダーを設定"""
    
    # Content Security Policy
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // セキュリティヘッダーの設定
        const meta = document.createElement('meta');
        meta.httpEquiv = 'Content-Security-Policy';
        meta.content = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';";
        document.head.appendChild(meta);
        
        // X-Frame-Options
        const frameOptions = document.createElement('meta');
        frameOptions.httpEquiv = 'X-Frame-Options';
        frameOptions.content = 'DENY';
        document.head.appendChild(frameOptions);
        
        // X-Content-Type-Options
        const contentType = document.createElement('meta');
        contentType.httpEquiv = 'X-Content-Type-Options';
        contentType.content = 'nosniff';
        document.head.appendChild(contentType);
    });
    </script>
    """, unsafe_allow_html=True)

# アプリの先頭で呼び出し
set_security_headers()
```

## 📋 9. セキュリティチェックリスト（運用）

### 日次チェック
- [ ] アプリケーションログの確認
- [ ] 異常なアクセスパターンの確認
- [ ] エラー率の監視

### 週次チェック
- [ ] セキュリティアラートの確認
- [ ] アクセスログの分析
- [ ] パフォーマンス指標の確認

### 月次チェック
- [ ] セキュリティパッチの適用
- [ ] アクセス権限の見直し
- [ ] バックアップの検証

### 四半期チェック
- [ ] セキュリティポリシーの見直し
- [ ] 脆弱性スキャンの実行
- [ ] 災害復旧計画の検証

## 🚨 10. インシデント対応

### セキュリティインシデント発生時の対応手順

1. **即座に実行**
   ```bash
   # アプリケーションの一時停止
   az webapp stop --resource-group rg-streamlit-todo --name your-app-name
   
   # アクセスログの保存
   az webapp log download --resource-group rg-streamlit-todo --name your-app-name
   ```

2. **調査と分析**
   ```bash
   # 直近24時間のログ分析
   az monitor activity-log list \
     --resource-group rg-streamlit-todo \
     --start-time 2024-01-01T00:00:00Z \
     --end-time 2024-01-02T00:00:00Z
   ```

3. **修復と復旧**
   ```bash
   # 安全な設定での再起動
   az webapp config appsettings set \
     --resource-group rg-streamlit-todo \
     --name your-app-name \
     --settings MAINTENANCE_MODE=true
   
   az webapp start --resource-group rg-streamlit-todo --name your-app-name
   ```

## 📝 まとめ

このセキュリティガイドに従うことで、以下の保護が実現されます：

- **データ保護**: 暗号化とアクセス制御
- **認証・認可**: Azure AD による統合認証
- **ネットワークセキュリティ**: WAF とアクセス制限
- **監視と検知**: リアルタイム監視とアラート
- **インシデント対応**: 迅速な対応体制

セキュリティは継続的なプロセスです。定期的な見直しと改善を実施してください。