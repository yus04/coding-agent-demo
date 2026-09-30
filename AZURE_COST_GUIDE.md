# Azure コスト見積もりガイド

Streamlit TODO アプリをAzureで運用する際のコスト見積もりと最適化の指針です。

## 💰 コスト見積もり（月額、東日本リージョン）

### 🔸 小規模運用（開発・テスト環境）

#### オプション1: Container Instances + Table Storage
- **Azure Container Instances (1 vCPU, 1GB RAM)**: 約 ¥2,500/月
- **Azure Table Storage (1GB未満)**: 約 ¥15/月
- **帯域幅 (1GB/月)**: 約 ¥15/月
- **合計**: **約 ¥2,530/月**

#### オプション2: App Service Basic + PostgreSQL Basic
- **App Service (Basic B1)**: 約 ¥1,800/月
- **Azure Database for PostgreSQL (Basic B1)**: 約 ¥1,500/月
- **ストレージ (5GB)**: 約 ¥150/月
- **合計**: **約 ¥3,450/月**

### 🔸 中規模運用（本番環境）

#### 推奨構成: App Service Standard + PostgreSQL General Purpose
- **App Service (Standard S1)**: 約 ¥7,200/月
- **Azure Database for PostgreSQL (GP GP_Gen5_2)**: 約 ¥12,000/月
- **Application Insights**: 約 ¥1,500/月
- **Key Vault**: 約 ¥150/月
- **Azure CDN (Standard)**: 約 ¥300/月
- **SSL証明書 (App Service Managed)**: 無料
- **合計**: **約 ¥21,150/月**

### 🔸 大規模運用（エンタープライズ）

#### 高可用性構成
- **App Service (Premium P1V3)**: 約 ¥18,000/月
- **Azure Database for PostgreSQL (GP GP_Gen5_4)**: 約 ¥24,000/月
- **Application Gateway + WAF**: 約 ¥4,500/月
- **Azure CDN (Premium)**: 約 ¥1,200/月
- **Azure Monitor + Log Analytics**: 約 ¥2,000/月
- **Key Vault**: 約 ¥150/月
- **合計**: **約 ¥49,850/月**

## 📊 詳細コスト内訳

### Azure App Service料金

| プラン | vCPU | RAM | ストレージ | 月額料金 | 適用シーン |
|--------|------|-----|------------|----------|------------|
| Free F1 | 共有 | 1GB | 1GB | 無料 | 開発・学習 |
| Basic B1 | 1 | 1.75GB | 10GB | ¥1,800 | 小規模 |
| Basic B2 | 2 | 3.5GB | 10GB | ¥3,600 | 中小規模 |
| Standard S1 | 1 | 1.75GB | 50GB | ¥7,200 | 本番環境 |
| Standard S2 | 2 | 3.5GB | 50GB | ¥14,400 | 高負荷 |
| Premium P1V3 | 2 | 8GB | 250GB | ¥18,000 | エンタープライズ |

### Azure Database for PostgreSQL料金

| プラン | vCPU | RAM | ストレージ | 月額料金 | IOPS |
|--------|------|-----|------------|----------|------|
| Basic B1 | 1 | 2GB | 5GB | ¥1,500 | 35 |
| Basic B2 | 2 | 4GB | 5GB | ¥3,000 | 70 |
| GP GP_Gen5_2 | 2 | 10GB | 5GB | ¥12,000 | 640 |
| GP GP_Gen5_4 | 4 | 20GB | 5GB | ¥24,000 | 1280 |

### その他のサービス料金

| サービス | 料金体系 | 月額目安 |
|----------|----------|----------|
| Azure Table Storage | ¥15/GB/月 | ¥15-150 |
| Azure Blob Storage | ¥6/GB/月 | ¥30-300 |
| Application Insights | ¥300/GB/月 | ¥500-2000 |
| Azure CDN Standard | ¥75/100GB/月 | ¥300-1500 |
| Key Vault | ¥150/月 + ¥15/1万トランザクション | ¥150-500 |
| Application Gateway | ¥2,700/月 + ¥450/処理時間 | ¥4500-8000 |

## 💡 コスト最適化戦略

### 1. 開発環境のコスト削減

```bash
# 開発環境を自動停止（平日18時に停止、9時に開始）
az webapp config appsettings set \
  --resource-group rg-streamlit-todo-dev \
  --name streamlit-todo-dev \
  --settings AUTO_STOP_SCHEDULE="0 18 * * 1-5" \
           AUTO_START_SCHEDULE="0 9 * * 1-5"

# 週末は完全停止
az automation schedule create \
  --automation-account-name "auto-streamlit" \
  --resource-group rg-streamlit-todo-dev \
  --name "weekend-shutdown" \
  --frequency Weekly \
  --week-days Saturday,Sunday
```

### 2. データベースの最適化

```bash
# 開発環境でのデータベース自動停止
az postgres server configuration set \
  --resource-group rg-streamlit-todo-dev \
  --server-name streamlit-todo-postgres-dev \
  --name autovacuum \
  --value on

# バックアップ保持期間を最小に（開発環境）
az postgres server update \
  --resource-group rg-streamlit-todo-dev \
  --name streamlit-todo-postgres-dev \
  --backup-retention 7
```

### 3. 監視とアラートでコスト管理

```bash
# コスト管理アラートの設定
az consumption budget create \
  --resource-group rg-streamlit-todo \
  --budget-name "streamlit-monthly-budget" \
  --amount 10000 \
  --time-grain Monthly \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --threshold 80 \
  --contact-emails admin@yourcompany.com
```

### 4. リザーブドインスタンスの活用

```bash
# 1年リザーブドインスタンス購入（約30%割引）
az reservations reservation-order purchase \
  --reserved-resource-type VirtualMachines \
  --sku Standard_B1s \
  --location japaneast \
  --quantity 1 \
  --term P1Y
```

## 📈 使用量ベースの見積もり

### トラフィック予測とスケーリング

#### 小規模 (月間1,000セッション)
- **データ転送**: 約10GB/月
- **データベース要求**: 約10,000クエリ/月
- **推奨構成**: Basic プラン

#### 中規模 (月間10,000セッション)  
- **データ転送**: 約100GB/月
- **データベース要求**: 約100,000クエリ/月
- **推奨構成**: Standard プラン

#### 大規模 (月間100,000セッション)
- **データ転送**: 約1TB/月
- **データベース要求**: 約1,000,000クエリ/月
- **推奨構成**: Premium プラン + CDN

## 🎯 推奨コスト構成

### 🏃‍♂️ スタートアップ向け（月額 ¥5,000以下）

```yaml
構成:
  App Service: Basic B1
  Database: Table Storage
  監視: 基本メトリクス
  セキュリティ: 基本SSL

月額コスト: ¥3,000-5,000
適用ユーザー: ~1,000セッション/月
```

### 🏢 SMB向け（月額 ¥15,000-25,000）

```yaml
構成:
  App Service: Standard S1
  Database: PostgreSQL Basic
  監視: Application Insights
  セキュリティ: Key Vault + SSL
  CDN: Azure CDN Standard

月額コスト: ¥15,000-25,000
適用ユーザー: ~10,000セッション/月
```

### 🏭 エンタープライズ向け（月額 ¥40,000以上）

```yaml
構成:
  App Service: Premium P1V3 (冗長化)
  Database: PostgreSQL General Purpose (HA)
  監視: Application Insights + Log Analytics
  セキュリティ: WAF + Key Vault + AAD
  CDN: Azure CDN Premium
  バックアップ: GRS ストレージ

月額コスト: ¥40,000-80,000
適用ユーザー: 100,000+セッション/月
```

## 📋 コスト監視のベストプラクティス

### 1. 日次コスト確認

```bash
# 日次コスト取得
az consumption usage list \
  --start-date $(date -d "1 day ago" +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --resource-group rg-streamlit-todo
```

### 2. 月次コストレビュー

```bash
# 月次コストレポート生成
az consumption usage list \
  --start-date $(date -d "1 month ago" +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --resource-group rg-streamlit-todo \
  --output table > monthly-cost-report.txt
```

### 3. 自動コスト最適化

```python
# Azure Functions でのコスト最適化自動化例
import azure.functions as func
from azure.mgmt.web import WebSiteManagementClient

def main(timer: func.TimerRequest) -> None:
    """平日夜間と週末の自動停止"""
    import datetime
    
    now = datetime.datetime.now()
    
    # 平日18時以降または週末は開発環境を停止
    if (now.hour >= 18 and now.weekday() < 5) or now.weekday() >= 5:
        # 開発環境停止処理
        stop_development_resources()
    
    # 平日9時に開発環境を開始
    if now.hour == 9 and now.weekday() < 5:
        start_development_resources()
```

## 🔍 コスト分析ツール

### Azure Cost Management

```bash
# Cost Management API でコスト分析
az costmanagement query \
  --type Usage \
  --dataset-aggregation '{"totalCost":{"name":"PreTaxCost","function":"Sum"}}' \
  --dataset-grouping name="ResourceGroup" type="Dimension" \
  --timeframe MonthToDate \
  --scope "/subscriptions/{subscription-id}"
```

### サードパーティツール

- **CloudHealth**: 総合的なクラウドコスト管理
- **Cloudyn**: Microsoftが提供するコスト最適化ツール
- **Azure Advisor**: 組み込みの推奨事項

## 📝 まとめ

### コスト最適化のポイント

1. **適切なサイジング**: 過剰なリソースを避ける
2. **自動スケーリング**: 需要に応じた動的調整
3. **開発環境の管理**: 使用しない時間の停止
4. **ストレージの最適化**: 適切なストレージタイプの選択
5. **監視とアラート**: 予算超過の早期検知

### 段階的アプローチ

1. **Phase 1**: 基本構成で開始（¥3,000-5,000/月）
2. **Phase 2**: 本番要件に応じてスケールアップ（¥15,000-25,000/月）
3. **Phase 3**: エンタープライズ機能追加（¥40,000+/月）

適切な計画と監視により、コストを予測可能で管理しやすい範囲に保つことができます。