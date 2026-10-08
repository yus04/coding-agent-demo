"""
簡単な TODO リスト Web アプリケーション
Python Streamlit を使用したシンプルな TODO 管理アプリ

実行方法:
streamlit run app.py
"""

import streamlit as st

PRIORITIES = ["High", "Medium", "Low"]
PRIORITY_LABELS = {
    "High": "高 (High)",
    "Medium": "中 (Medium)",
    "Low": "低 (Low)",
}

def initialize_session_state():
    """セッション状態を初期化"""
    if 'todos' not in st.session_state:
        st.session_state.todos = []

def add_todo(todo_text, priority="Medium"):
    """TODO項目を追加"""
    if todo_text.strip():
        st.session_state.todos.append({
            'id': len(st.session_state.todos),
            'text': todo_text.strip(),
            'completed': False,
            'priority': priority
        })

def delete_todo(todo_id):
    """TODO項目を削除"""
    st.session_state.todos = [
        todo for todo in st.session_state.todos 
        if todo['id'] != todo_id
    ]

def main():
    """メインアプリケーション"""
    st.title("📝 TODO リスト")
    st.write("シンプルな TODO 管理アプリケーション")
    
    # セッション状態を初期化
    initialize_session_state()
    
    # TODO追加セクション
    st.header("新しい TODO を追加")
    
    # 入力フォーム
    with st.form("add_todo_form"):
        new_todo = st.text_input("TODO項目を入力してください", placeholder="例: 買い物に行く")
        priority = st.selectbox(
            "優先度",
            PRIORITIES,
            index=1,
            format_func=lambda value: PRIORITY_LABELS[value]
        )
        submitted = st.form_submit_button("追加")
        
        if submitted and new_todo:
            add_todo(new_todo, priority)
            st.success(f"「{new_todo}」を追加しました！")
            st.rerun()
    
    # TODO表示セクション
    st.header("TODO リスト")
    search_query = st.text_input(
        "TODOを検索",
        placeholder="キーワードを入力",
        key="todo_search",
    )
    
    if not st.session_state.todos:
        st.info("TODO項目がありません。上記から新しい項目を追加してください。")
    else:
        # 未完了のTODOを表示
        incomplete_todos = [todo for todo in st.session_state.todos if not todo['completed']]
        if search_query:
            incomplete_todos = [
                todo for todo in incomplete_todos
                if search_query.casefold() in todo['text'].casefold()
            ]
        incomplete_todos.sort(
            key=lambda todo: PRIORITIES.index(todo.get('priority', 'Medium'))
        )
        
        if incomplete_todos:
            st.subheader(f"未完了 ({len(incomplete_todos)}件)")
            
            for todo in incomplete_todos:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    todo_priority = todo.get('priority', 'Medium')
                    st.write(f"• [{PRIORITY_LABELS[todo_priority]}] {todo['text']}")
                
                with col2:
                    if st.button("完了", key=f"complete_{todo['id']}"):
                        delete_todo(todo['id'])
                        st.success("TODO項目を完了しました！")
                        st.rerun()
        else:
            st.info("該当するTODOがありません。")
        
        # 統計情報
        total_todos = len(st.session_state.todos)
        if total_todos > 0:
            st.divider()
            st.write(f"**統計:** 現在 {len(incomplete_todos)} 件のTODOがあります")

if __name__ == "__main__":
    main()