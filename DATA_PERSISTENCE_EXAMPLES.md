# データ永続化のためのアプリ拡張例

このドキュメントでは、現在のインメモリストレージからAzureのデータストレージサービスへの移行例を示します。

## 📊 推奨データストレージオプション

### 1. Azure Database for PostgreSQL（推奨）
**適用場面**: 本格的な本番環境、複雑なクエリが必要な場合

### 2. Azure Cosmos DB 
**適用場面**: グローバル分散、高可用性が必要な場合

### 3. Azure Table Storage
**適用場面**: 軽量、コスト重視の場合

## 🔧 実装例

### PostgreSQL版 app_with_postgresql.py

```python
"""
PostgreSQL対応版 TODO リスト Web アプリケーション
Azure Database for PostgreSQL を使用
"""

import streamlit as st
import psycopg2
import os
from typing import List, Dict

# データベース設定
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'streamlit-todo-postgres.postgres.database.azure.com'),
    'database': os.environ.get('DB_NAME', 'postgres'),
    'user': os.environ.get('DB_USER', 'todouser@streamlit-todo-postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'sslmode': 'require'
}

def get_db_connection():
    """データベース接続を取得"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        st.error(f"データベース接続エラー: {e}")
        return None

def init_database():
    """データベーステーブルを初期化"""
    conn = get_db_connection()
    if conn:
        try:
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
        except psycopg2.Error as e:
            st.error(f"テーブル作成エラー: {e}")
        finally:
            conn.close()

def add_todo_to_db(todo_text: str) -> bool:
    """TODOをデータベースに追加"""
    conn = get_db_connection()
    if conn and todo_text.strip():
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO todos (text) VALUES (%s) RETURNING id",
                (todo_text.strip(),)
            )
            todo_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            st.error(f"TODO追加エラー: {e}")
            return False
        finally:
            conn.close()
    return False

def get_todos_from_db() -> List[Dict]:
    """データベースからTODO一覧を取得"""
    conn = get_db_connection()
    todos = []
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, text, completed, created_at FROM todos ORDER BY created_at DESC"
            )
            rows = cur.fetchall()
            for row in rows:
                todos.append({
                    'id': row[0],
                    'text': row[1],
                    'completed': row[2],
                    'created_at': row[3]
                })
            cur.close()
        except psycopg2.Error as e:
            st.error(f"TODO取得エラー: {e}")
        finally:
            conn.close()
    return todos

def complete_todo_in_db(todo_id: int) -> bool:
    """TODOを完了状態に更新"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE todos SET completed = TRUE WHERE id = %s",
                (todo_id,)
            )
            conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            st.error(f"TODO更新エラー: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_todo_from_db(todo_id: int) -> bool:
    """TODOをデータベースから削除"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            st.error(f"TODO削除エラー: {e}")
            return False
        finally:
            conn.close()
    return False

def main():
    """メインアプリケーション"""
    st.title("📝 TODO リスト (PostgreSQL版)")
    st.write("Azure Database for PostgreSQL を使用したTODO管理アプリケーション")
    
    # データベース初期化
    init_database()
    
    # TODO追加セクション
    st.header("新しい TODO を追加")
    
    with st.form("add_todo_form"):
        new_todo = st.text_input("TODO項目を入力してください", placeholder="例: 買い物に行く")
        submitted = st.form_submit_button("追加")
        
        if submitted and new_todo:
            if add_todo_to_db(new_todo):
                st.success(f"「{new_todo}」を追加しました！")
                st.rerun()
            else:
                st.error("TODO追加に失敗しました")
    
    # TODO表示セクション
    st.header("TODO リスト")
    
    todos = get_todos_from_db()
    
    if not todos:
        st.info("TODO項目がありません。上記から新しい項目を追加してください。")
    else:
        # 未完了のTODOを表示
        incomplete_todos = [todo for todo in todos if not todo['completed']]
        
        if incomplete_todos:
            st.subheader(f"未完了 ({len(incomplete_todos)}件)")
            
            for todo in incomplete_todos:
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.write(f"• {todo['text']}")
                    st.caption(f"作成日時: {todo['created_at']}")
                
                with col2:
                    if st.button("完了", key=f"complete_{todo['id']}"):
                        if complete_todo_in_db(todo['id']):
                            st.success("TODO項目を完了しました！")
                            st.rerun()
                
                with col3:
                    if st.button("削除", key=f"delete_{todo['id']}"):
                        if delete_todo_from_db(todo['id']):
                            st.success("TODO項目を削除しました！")
                            st.rerun()
        
        # 完了済みTODO表示
        completed_todos = [todo for todo in todos if todo['completed']]
        if completed_todos:
            with st.expander(f"完了済み ({len(completed_todos)}件)"):
                for todo in completed_todos:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"✅ {todo['text']}")
                        st.caption(f"作成日時: {todo['created_at']}")
                    with col2:
                        if st.button("削除", key=f"delete_completed_{todo['id']}"):
                            if delete_todo_from_db(todo['id']):
                                st.success("TODO項目を削除しました！")
                                st.rerun()
        
        # 統計情報
        total_todos = len(todos)
        if total_todos > 0:
            st.divider()
            completion_rate = len(completed_todos) / total_todos * 100
            st.write(f"**統計:** 現在 {len(incomplete_todos)} 件のTODOがあります")
            st.write(f"**完了率:** {completion_rate:.1f}% ({len(completed_todos)}/{total_todos})")

if __name__ == "__main__":
    main()
```

### Azure Table Storage版 app_with_tablestorage.py

```python
"""
Azure Table Storage対応版 TODO リスト Web アプリケーション
軽量なNoSQLストレージを使用
"""

import streamlit as st
import os
from azure.data.tables import TableServiceClient, TableEntity
from datetime import datetime
import uuid

# Table Storage設定
STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
TABLE_NAME = 'todos'

def get_table_client():
    """Table Storageクライアントを取得"""
    try:
        service_client = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        table_client = service_client.get_table_client(table_name=TABLE_NAME)
        return table_client
    except Exception as e:
        st.error(f"Table Storage接続エラー: {e}")
        return None

def init_table():
    """テーブルを初期化（作成）"""
    try:
        service_client = TableServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        service_client.create_table_if_not_exists(table_name=TABLE_NAME)
    except Exception as e:
        st.error(f"テーブル初期化エラー: {e}")

def add_todo_to_table(todo_text: str) -> bool:
    """TODOをTable Storageに追加"""
    table_client = get_table_client()
    if table_client and todo_text.strip():
        try:
            entity = {
                'PartitionKey': 'todos',
                'RowKey': str(uuid.uuid4()),
                'text': todo_text.strip(),
                'completed': False,
                'created_at': datetime.utcnow().isoformat()
            }
            table_client.create_entity(entity)
            return True
        except Exception as e:
            st.error(f"TODO追加エラー: {e}")
            return False
    return False

def get_todos_from_table():
    """Table StorageからTODO一覧を取得"""
    table_client = get_table_client()
    todos = []
    if table_client:
        try:
            entities = table_client.list_entities()
            for entity in entities:
                todos.append({
                    'id': entity['RowKey'],
                    'text': entity['text'],
                    'completed': entity['completed'],
                    'created_at': entity['created_at']
                })
            # 作成日時で降順ソート
            todos.sort(key=lambda x: x['created_at'], reverse=True)
        except Exception as e:
            st.error(f"TODO取得エラー: {e}")
    return todos

def update_todo_in_table(todo_id: str, completed: bool) -> bool:
    """TODOの完了状態を更新"""
    table_client = get_table_client()
    if table_client:
        try:
            entity = table_client.get_entity(partition_key='todos', row_key=todo_id)
            entity['completed'] = completed
            table_client.update_entity(entity)
            return True
        except Exception as e:
            st.error(f"TODO更新エラー: {e}")
            return False
    return False

def delete_todo_from_table(todo_id: str) -> bool:
    """TODOをTable Storageから削除"""
    table_client = get_table_client()
    if table_client:
        try:
            table_client.delete_entity(partition_key='todos', row_key=todo_id)
            return True
        except Exception as e:
            st.error(f"TODO削除エラー: {e}")
            return False
    return False

def main():
    """メインアプリケーション"""
    st.title("📝 TODO リスト (Table Storage版)")
    st.write("Azure Table Storage を使用したTODO管理アプリケーション")
    
    # テーブル初期化
    init_table()
    
    # TODO追加セクション
    st.header("新しい TODO を追加")
    
    with st.form("add_todo_form"):
        new_todo = st.text_input("TODO項目を入力してください", placeholder="例: 買い物に行く")
        submitted = st.form_submit_button("追加")
        
        if submitted and new_todo:
            if add_todo_to_table(new_todo):
                st.success(f"「{new_todo}」を追加しました！")
                st.rerun()
            else:
                st.error("TODO追加に失敗しました")
    
    # TODO表示セクション
    st.header("TODO リスト")
    
    todos = get_todos_from_table()
    
    if not todos:
        st.info("TODO項目がありません。上記から新しい項目を追加してください。")
    else:
        # 未完了のTODOを表示
        incomplete_todos = [todo for todo in todos if not todo['completed']]
        
        if incomplete_todos:
            st.subheader(f"未完了 ({len(incomplete_todos)}件)")
            
            for todo in incomplete_todos:
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.write(f"• {todo['text']}")
                    st.caption(f"作成日時: {todo['created_at']}")
                
                with col2:
                    if st.button("完了", key=f"complete_{todo['id']}"):
                        if update_todo_in_table(todo['id'], True):
                            st.success("TODO項目を完了しました！")
                            st.rerun()
                
                with col3:
                    if st.button("削除", key=f"delete_{todo['id']}"):
                        if delete_todo_from_table(todo['id']):
                            st.success("TODO項目を削除しました！")
                            st.rerun()
        
        # 完了済みTODO表示
        completed_todos = [todo for todo in todos if todo['completed']]
        if completed_todos:
            with st.expander(f"完了済み ({len(completed_todos)}件)"):
                for todo in completed_todos:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"✅ {todo['text']}")
                        st.caption(f"作成日時: {todo['created_at']}")
                    with col2:
                        if st.button("削除", key=f"delete_completed_{todo['id']}"):
                            if delete_todo_from_table(todo['id']):
                                st.success("TODO項目を削除しました！")
                                st.rerun()
        
        # 統計情報
        total_todos = len(todos)
        if total_todos > 0:
            st.divider()
            completion_rate = len(completed_todos) / total_todos * 100
            st.write(f"**統計:** 現在 {len(incomplete_todos)} 件のTODOがあります")
            st.write(f"**完了率:** {completion_rate:.1f}% ({len(completed_todos)}/{total_todos})")

if __name__ == "__main__":
    main()
```

## 📦 依存関係更新

各データストレージオプションに応じて requirements.txt を更新してください。

### PostgreSQL版 requirements.txt
```
streamlit>=1.28.0
psycopg2-binary
```

### Table Storage版 requirements.txt  
```
streamlit>=1.28.0
azure-data-tables
```

### Cosmos DB版 requirements.txt
```
streamlit>=1.28.0
azure-cosmos
```

## 🔧 環境変数設定

Azure App Service での環境変数設定例：

### PostgreSQL用
```bash
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --settings \
    DB_HOST="your-postgres-server.postgres.database.azure.com" \
    DB_NAME="postgres" \
    DB_USER="your-username@your-postgres-server" \
    DB_PASSWORD="your-password"
```

### Table Storage用
```bash
az webapp config appsettings set \
  --resource-group rg-streamlit-todo \
  --name your-app-name \
  --settings \
    AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=your-account;AccountKey=your-key;EndpointSuffix=core.windows.net"
```

## 🚀 移行手順

1. **新しいアプリファイルを準備**
   - `app_with_postgresql.py` または `app_with_tablestorage.py` を作成
   - 必要な依存関係を requirements.txt に追加

2. **Azureリソースを作成**
   - PostgreSQL サーバーまたは Storage Account を作成
   - 必要な環境変数を設定

3. **テストデプロイ**
   - 既存のアプリと並行してテスト環境にデプロイ
   - データ移行スクリプトを実行（必要な場合）

4. **本番切り替え**
   - 新しいバージョンを本番環境にデプロイ
   - DNS切り替えまたはブルーグリーンデプロイメント

この拡張により、アプリケーションの再起動後もTODOデータが永続化され、本格的な本番運用が可能になります。