# Azure デプロイメント完全ガイド - 目次

Streamlit TODO アプリをAzureにデプロイするための包括的なドキュメント集です。

## 📚 ドキュメント一覧

### 🚀 デプロイメント関連

1. **[Azure デプロイメントガイド](./AZURE_DEPLOYMENT_GUIDE.md)**
   - 推奨Azureサービスの比較と選択
   - App Service, Container Instances, Container Apps の詳細手順
   - 前提条件とツールの準備
   - ステップバイステップのデプロイ手順
   - トラブルシューティングガイド

2. **[データ永続化の例](./DATA_PERSISTENCE_EXAMPLES.md)**
   - Azure Database for PostgreSQL 統合例
   - Azure Table Storage 軽量実装
   - Azure Cosmos DB NoSQL オプション
   - 既存アプリからの移行手順
   - パフォーマンス最適化Tips

3. **[セキュリティベストプラクティス](./SECURITY_BEST_PRACTICES.md)**
   - HTTPS/TLS設定
   - Azure Key Vault によるシークレット管理
   - Azure Active Directory 認証
   - WAF（Web Application Firewall）設定
   - ネットワークセキュリティ
   - インシデント対応手順

4. **[コスト見積もりガイド](./AZURE_COST_GUIDE.md)**
   - 規模別コスト見積もり
   - サービス別料金詳細
   - コスト最適化戦略
   - 監視とアラート設定

### 🔧 設定ファイル

- **[startup.sh](./startup.sh)** - Azure App Service 起動スクリプト
- **[Dockerfile](./Dockerfile)** - コンテナ化用Dockerファイル
- **[deploy-azure.sh](./deploy-azure.sh)** - 自動デプロイスクリプト
- **[azure-container-instance.yaml](./azure-container-instance.yaml)** - Container Instances設定

## 🎯 用途別クイックガイド

### 👨‍💻 開発者向け（初回デプロイ）

1. [前提条件の確認](./AZURE_DEPLOYMENT_GUIDE.md#前提条件)
2. [Azure CLI セットアップ](./AZURE_DEPLOYMENT_GUIDE.md#事前準備)
3. [クイックデプロイ実行](./AZURE_DEPLOYMENT_GUIDE.md#方法1-azure-app-service推奨)

```bash
# 最速デプロイ手順
az login
chmod +x deploy-azure.sh
./deploy-azure.sh
```

### 🏢 運用担当者向け

1. [セキュリティ設定](./SECURITY_BEST_PRACTICES.md#セキュリティチェックリスト)
2. [コスト監視](./AZURE_COST_GUIDE.md#コスト監視のベストプラクティス)
3. [データバックアップ](./DATA_PERSISTENCE_EXAMPLES.md#移行手順)

### 📊 経営層向け

1. [コスト比較表](./AZURE_COST_GUIDE.md#コスト見積もり月額東日本リージョン)
2. [セキュリティ対策一覧](./SECURITY_BEST_PRACTICES.md#セキュリティチェックリスト)
3. [スケーラビリティ指標](./AZURE_DEPLOYMENT_GUIDE.md#推奨azureサービス)

## 📋 デプロイメント手順チェックリスト

### 事前準備
- [ ] Azure サブスクリプション確認
- [ ] Azure CLI インストール
- [ ] Docker インストール（コンテナ使用時）
- [ ] Git リポジトリ準備

### 基本デプロイ
- [ ] リソースグループ作成
- [ ] App Service 作成
- [ ] アプリケーションデプロイ
- [ ] 動作確認

### セキュリティ設定
- [ ] HTTPS 有効化
- [ ] アクセス制限設定
- [ ] 環境変数設定
- [ ] ログ監視設定

### データ永続化（オプション）
- [ ] データベースサービス選択
- [ ] データベース作成
- [ ] アプリケーション修正
- [ ] データ移行

### 運用準備
- [ ] 監視設定
- [ ] アラート設定
- [ ] バックアップ設定
- [ ] 災害復旧計画

## 🆘 サポートとトラブルシューティング

### よくある問題

1. **デプロイエラー**
   - [トラブルシューティング](./AZURE_DEPLOYMENT_GUIDE.md#トラブルシューティング)参照

2. **パフォーマンス問題**
   - [コスト最適化](./AZURE_COST_GUIDE.md#コスト最適化戦略)参照

3. **セキュリティ問題**
   - [インシデント対応](./SECURITY_BEST_PRACTICES.md#インシデント対応)参照

### 技術サポート

- **Azure サポート**: [Azure Portal](https://portal.azure.com/) からサポートリクエスト
- **コミュニティサポート**: [Microsoft Q&A](https://docs.microsoft.com/answers/)
- **Streamlit サポート**: [Streamlit Community](https://discuss.streamlit.io/)

## 🔄 定期メンテナンス

### 週次タスク
- [ ] セキュリティログ確認
- [ ] パフォーマンス指標確認
- [ ] コスト使用量確認

### 月次タスク
- [ ] セキュリティパッチ適用
- [ ] バックアップ検証
- [ ] コスト最適化レビュー

### 四半期タスク
- [ ] 災害復旧テスト
- [ ] セキュリティ監査
- [ ] アーキテクチャレビュー

---

📝 **注意**: このドキュメントは継続的に更新されます。最新情報については各個別ドキュメントを確認してください。

🔗 **関連リンク**:
- [Azure公式ドキュメント](https://docs.microsoft.com/azure/)
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Python Azure SDK](https://docs.microsoft.com/python/api/overview/azure/)