# coding-agent-demo

## 📝 TODO リスト Web アプリ

PythonのStreamlitを使用したシンプルなTODO管理Webアプリケーションです。

### 機能

- ✅ TODO項目の追加
- 📋 TODO項目の一覧表示
- ✔️ TODO項目の完了・削除

### 実行方法

1. 必要なライブラリをインストール:
```bash
pip install -r requirements.txt
```

2. アプリケーションを起動:
```bash
streamlit run app.py
```

3. ブラウザで http://localhost:8501 にアクセス

### 技術仕様

- **フレームワーク**: Python + Streamlit
- **データ保存**: インメモリ（アプリ起動中のみ有効）
- **対応ブラウザ**: モダンブラウザ全般

## ☁️ Azure デプロイメント

このアプリケーションをAzureにデプロイするための包括的なガイドを提供しています：

### 📖 完全ガイド
**[📚 Azure デプロイメント完全ガイド](./AZURE_DEPLOYMENT_INDEX.md)** - すべてのドキュメントの総合案内

### 📚 デプロイメント関連ドキュメント

- **[Azure デプロイメントガイド](./AZURE_DEPLOYMENT_GUIDE.md)** - Azure App Service、Container Instances、Container Apps での詳細なデプロイ手順
- **[データ永続化の例](./DATA_PERSISTENCE_EXAMPLES.md)** - PostgreSQL、Cosmos DB、Table Storage を使用したデータ永続化の実装例
- **[セキュリティベストプラクティス](./SECURITY_BEST_PRACTICES.md)** - Azure でのセキュリティ設定と運用ガイドライン
- **[コスト見積もりガイド](./AZURE_COST_GUIDE.md)** - 規模別のコスト見積もりと最適化戦略

### 🚀 クイックデプロイ

Azure App Service への最速デプロイ：

```bash
# Azure CLI でログイン
az login

# デプロイスクリプト実行
chmod +x deploy-azure.sh
./deploy-azure.sh
```

### 📦 利用可能なデプロイメントオプション

1. **Azure App Service** (推奨) - PaaS による完全管理環境
2. **Azure Container Instances** - シンプルなコンテナ実行
3. **Azure Container Apps** - モダンなサーバーレスコンテナ

### 💾 データ永続化オプション

- **Azure Database for PostgreSQL** - 本格的なリレーショナルデータベース
- **Azure Cosmos DB** - グローバル分散NoSQLデータベース  
- **Azure Table Storage** - 軽量で経済的なNoSQLストレージ

### 🔒 セキュリティ機能

- HTTPS/TLS 暗号化
- Azure Active Directory 認証
- Key Vault によるシークレット管理
- Web Application Firewall (WAF)
- IP アクセス制限