# Azure コンテナデプロイメント手段の調査

## 概要

このドキュメントでは、Microsoft Learn から Azure のコンテナをデプロイする主要な手段について調査した結果をまとめます。Azure では、様々なニーズに応じて複数のコンテナデプロイメントオプションが提供されています。

## Azure コンテナデプロイメントサービス一覧

### 1. Azure Container Instances (ACI)

#### 概要
Azure Container Instances は、仮想マシンの管理なしに Azure でコンテナを実行するための最速かつ最簡単な方法を提供するサーバーレスプラットフォームです。

#### 主な特徴
- **高速起動**: 数秒でコンテナを起動可能
- **サーバーレス**: インフラ管理が不要
- **秒単位課金**: 実行時間に応じた課金モデル
- **Linux と Windows コンテナのサポート**
- **パブリック IP アドレスと FQDN の提供**
- **VNet デプロイメント対応**
- **可用性ゾーンサポート**
- **マネージド ID 対応**
- **機密コンテナのサポート**

#### 適用ケース
- 短時間実行ワークロード
- タスク自動化
- ビルドジョブ
- バースト処理
- 分離されたコンテナで動作可能なシナリオ
- テストやプロトタイピング

#### デプロイメント方法
- Azure ポータル
- Azure CLI
- ARM テンプレート
- REST API

#### 特殊機能
- **Spot コンテナ**: 最大70%の割引価格で中断可能なワークロードを実行
- **NGroups**: 複数の関連コンテナグループの高度な管理機能
- **仮想ノード**: AKS クラスター内でのポッド実行
- **スタンバイプール**: より高速な起動時間の実現

### 2. Azure Kubernetes Service (AKS)

#### 概要
Azure Kubernetes Service は、マネージド Kubernetes サービスで、コンテナ化されたアプリケーションの迅速なデプロイと管理を可能にします。

#### 主な特徴
- **マネージド Kubernetes**: Kubernetesの複雑性を抽象化
- **自動スケーリング**: クラスターとポッドの自動スケーリング
- **複数ノードプールサポート**: 混在OS環境の対応
- **GPU サポート**: GPU ワークロード対応
- **機密コンピューティングノード**: ハードウェアベースの信頼できる実行環境
- **豊富なストレージオプション**: Azure Disks、Azure Files、Azure NetApp Files
- **ネットワーキングオプション**: CNI プラグインの柔軟な選択
- **開発ツール統合**: Helm、Visual Studio Code、Istio サポート

#### 適用ケース
- マイクロサービスアーキテクチャ
- 複雑なコンテナオーケストレーション
- 大規模なコンテナアプリケーション
- CI/CD パイプライン
- カナリアリリース戦略
- エンタープライズ級のワークロード

#### デプロイメント方法
- Azure ポータル
- Azure CLI
- ARM テンプレート
- Bicep
- Terraform
- Helm

#### 高度な機能
- **RBAC統合**: Microsoft Entra ID との統合
- **Azure Policy**: コンプライアンス制御
- **Container Insights**: 監視とパフォーマンス分析
- **自動デプロイメント**: GitHub Actions、Azure DevOps 統合

### 3. Azure Container Apps

#### 概要
Azure Container Apps は、Kubernetes やオープンソース技術（Dapr、KEDA、Envoy）を基盤とした、完全マネージドなサーバーレスコンテナサービスです。

#### 主な特徴
- **サーバーレス**: インフラ管理不要
- **Kubernetes ベース**: Kubernetes API への直接アクセスなし
- **マイクロサービス最適化**: 複数のマイクロサービスにまたがるアプリケーション向け
- **イベントドリブン**: トラフィックやイベントソースベースのスケーリング
- **ゼロスケール**: トラフィックがない場合の自動停止
- **リビジョン管理**: アプリケーションバージョン管理
- **トラフィック分割**: カナリアデプロイメント対応
- **内蔵認証**: 認証・認可機能

#### 適用ケース
- マイクロサービスアプリケーション
- API サービス
- イベントドリブンアプリケーション
- バックグラウンド処理
- スケジュールジョブ
- Web アプリケーション

#### リソースタイプ
- **Apps**: 継続実行サービス（ASP.NET Core Web API、バックグラウンドサービス）
- **Jobs**: 完了まで実行する短時間タスク（コンソールアプリケーション、画像最適化）

#### デプロイメント方法
- Azure ポータル
- Azure CLI
- Visual Studio
- GitHub Actions
- Azure DevOps

### 4. Azure App Service for Containers (Web Apps for Containers)

#### 概要
Azure App Service for Containers は、コンテナ化されたウェブアプリケーションをホストするための完全マネージドプラットフォームです。

#### 主な特徴
- **Web アプリケーション最適化**: ウェブサイトと Web API に特化
- **CI/CD 統合**: Docker Hub、Azure Container Registry、GitHub との統合
- **デプロイメントスロット**: ゼロダウンタイムアップグレード
- **自動スケーリング**: トラフィックに応じた自動スケーリング
- **SSL/TLS サポート**: セキュリティ機能内蔵
- **カスタムドメイン**: 独自ドメインの使用可能
- **Windows と Linux コンテナのサポート**
- **マネージド ID**: セキュアな認証機能

#### 適用ケース
- Web アプリケーション
- RESTful API
- 従来アプリのコンテナ化（Lift and Shift）
- 継続的デプロイメントが必要なアプリケーション
- カスタムランタイム環境が必要なアプリケーション

#### デプロイメント方法
- Azure ポータル
- Azure CLI
- Visual Studio
- Azure DevOps
- GitHub Actions

#### CI/CD 機能
- **継続的デプロイメント**: レジストリからの自動デプロイ
- **Webhook サポート**: イメージ更新時の自動デプロイ
- **ステージング環境**: デプロイメントスロットによるテスト環境

## サービス比較表

| 特徴 | ACI | AKS | Container Apps | App Service |
|------|-----|-----|----------------|-------------|
| **管理レベル** | サーバーレス | マネージド | サーバーレス | マネージド |
| **オーケストレーション** | 単一コンテナ | Kubernetes | 簡素化されたK8s | 単一コンテナ |
| **スケーリング** | 手動 | 自動 | 自動 | 自動 |
| **適用ケース** | 短時間タスク | 複雑なアプリ | マイクロサービス | Web アプリ |
| **価格モデル** | 秒単位課金 | ノード課金 | 使用量課金 | プラン課金 |
| **学習コスト** | 低 | 高 | 中 | 低 |

## デプロイメント戦略とベストプラクティス

### 1. サービス選択の指針

#### Azure Container Instances を選ぶべき場合
- 短時間実行されるタスク
- シンプルなワークロード
- インフラ管理を避けたい場合
- 迅速なプロトタイピング

#### Azure Kubernetes Service を選ぶべき場合
- 複雑なマイクロサービスアーキテクチャ
- 高度なオーケストレーション機能が必要
- Kubernetes の知識がある場合
- エンタープライズ級のワークロード

#### Azure Container Apps を選ぶべき場合
- Kubernetes の複雑性を避けたいマイクロサービス
- イベントドリブンアプリケーション
- 自動スケーリングが重要
- サーバーレスの利点を活用したい場合

#### Azure App Service for Containers を選ぶべき場合
- Web アプリケーション
- 既存アプリのコンテナ化
- CI/CD パイプラインとの統合
- 従来の PaaS の利点を活用したい場合

### 2. 共通のベストプラクティス

#### セキュリティ
- マネージド ID の使用
- Azure Container Registry でのプライベートレジストリ利用
- RBAC の適切な設定
- ネットワークセキュリティグループの活用

#### 監視とログ
- Azure Monitor の統合
- Application Insights の活用
- ログ収集の設定
- パフォーマンス監視

#### CI/CD
- GitHub Actions や Azure DevOps の活用
- 自動デプロイメントの設定
- ステージング環境の利用
- カナリアデプロイメント戦略

#### コスト最適化
- 適切なサイジング
- 自動スケーリングの活用
- リソースの監視と最適化
- Spot インスタンスの活用（該当する場合）

## まとめ

Azure では、様々なニーズに応じて4つの主要なコンテナデプロイメントオプションが提供されています：

1. **Azure Container Instances (ACI)**: 最もシンプルで高速なコンテナ実行環境
2. **Azure Kubernetes Service (AKS)**: 本格的なコンテナオーケストレーション
3. **Azure Container Apps**: マイクロサービス向けサーバーレスプラットフォーム
4. **Azure App Service for Containers**: Web アプリケーション特化型プラットフォーム

各サービスは異なる使用ケースと要件に最適化されており、プロジェクトの規模、複雑さ、チームのスキルレベル、予算に応じて適切な選択を行うことが重要です。

## 参考資料

- [Azure Container Instances の概要](https://learn.microsoft.com/ja-jp/azure/container-instances/container-instances-overview)
- [Azure Kubernetes Service とは](https://learn.microsoft.com/ja-jp/azure/aks/what-is-aks)
- [Azure Container Apps の概要](https://learn.microsoft.com/ja-jp/azure/container-apps/)
- [Azure App Service での Web Apps for Containers](https://azure.microsoft.com/ja-jp/products/app-service/containers/)