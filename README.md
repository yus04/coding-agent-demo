# coding-agent-demo

## 📝 TODO リスト Web アプリ

PythonのStreamlitを使用したシンプルなTODO管理Webアプリケーションです。

### 機能

- ✅ TODO項目の追加
- 📋 TODO項目の一覧表示
- ✔️ TODO項目の完了・削除
- 🚦 TODO項目の優先度設定（高・中・低）と優先度順の表示

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

### 使い方

1. 「TODO項目を入力してください」にTODOの内容を入力します。
2. 「優先度を選択してください」から「高 (High)」「中 (Medium)」「低 (Low)」のいずれかを選択します。
3. 「追加」ボタンを押すと、TODOリストに優先度付きで追加されます。
4. TODOリストは優先度の高い順（高 → 中 → 低）に表示されます。

### 技術仕様

- **フレームワーク**: Python + Streamlit
- **データ保存**: インメモリ（アプリ起動中のみ有効）
- **対応ブラウザ**: モダンブラウザ全般