# coding-agent-demo

## 📝 TODO リスト Web アプリ

PythonのStreamlitを使用したシンプルなTODO管理Webアプリケーションです。

### 機能

- ✅ TODO項目の追加
- 📋 TODO項目の一覧表示
- ✔️ TODO項目の完了・削除
- 🔖 優先度（高・中・低）の設定と優先度順での表示

### 優先度の設定

TODOを追加する際に「優先度」から「高 (High)」「中 (Medium)」「低 (Low)」を選択できます。
TODO一覧は高・中・低の順で表示されます。

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