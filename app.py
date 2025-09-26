"""
簡単な TODO リスト Web アプリケーション
Python Streamlit を使用したシンプルな TODO 管理アプリ

実行方法:
streamlit run app.py
"""

import streamlit as st

def initialize_session_state():
    """セッション状態を初期化"""
    if 'todos' not in st.session_state:
        st.session_state.todos = []
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'  # デフォルトはライトモード

def apply_theme_css():
    """テーマに応じたCSSを適用"""
    if st.session_state.theme_mode == 'dark':
        dark_css = """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stTextInput > div > div > input {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #565656;
        }
        .stButton > button {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #565656;
        }
        .stButton > button:hover {
            background-color: #565656;
            border: 1px solid #fafafa;
        }
        .stAlert > div {
            background-color: #1e2328;
            color: #fafafa;
            border: 1px solid #565656;
        }
        .stSuccess > div {
            background-color: #0e4429;
            color: #7ce38b;
        }
        .element-container div[data-testid="stMarkdownContainer"] p {
            color: #fafafa;
        }
        h1, h2, h3 {
            color: #fafafa !important;
        }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    else:
        light_css = """
        <style>
        .stApp {
            background-color: #ffffff;
            color: #262730;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #262730;
            border: 1px solid #cccccc;
        }
        .stButton > button {
            background-color: #ffffff;
            color: #262730;
            border: 1px solid #cccccc;
        }
        .stButton > button:hover {
            background-color: #f0f2f6;
            border: 1px solid #262730;
        }
        </style>
        """
        st.markdown(light_css, unsafe_allow_html=True)

def toggle_theme():
    """テーマを切り替える"""
    if st.session_state.theme_mode == 'light':
        st.session_state.theme_mode = 'dark'
    else:
        st.session_state.theme_mode = 'light'
    st.rerun()

def render_theme_toggle():
    """画面右上にテーマ切り替えスイッチを表示"""
    # 右上にテーマ切り替えボタンを配置
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col3:
        if st.session_state.theme_mode == 'light':
            if st.button("🌙", key="theme_toggle", help="ダークモードに切り替え"):
                toggle_theme()
        else:
            if st.button("☀️", key="theme_toggle", help="ライトモードに切り替え"):
                toggle_theme()

def add_todo(todo_text):
    """TODO項目を追加"""
    if todo_text.strip():
        st.session_state.todos.append({
            'id': len(st.session_state.todos),
            'text': todo_text.strip(),
            'completed': False
        })

def delete_todo(todo_id):
    """TODO項目を削除"""
    st.session_state.todos = [
        todo for todo in st.session_state.todos 
        if todo['id'] != todo_id
    ]

def main():
    """メインアプリケーション"""
    # セッション状態を初期化
    initialize_session_state()
    
    # テーマCSSを適用
    apply_theme_css()
    
    # テーマ切り替えスイッチを右上に表示
    render_theme_toggle()
    
    st.title("📝 TODO リスト")
    st.write("シンプルな TODO 管理アプリケーション")
    
    # TODO追加セクション
    st.header("新しい TODO を追加")
    
    # 入力フォーム
    with st.form("add_todo_form"):
        new_todo = st.text_input("TODO項目を入力してください", placeholder="例: 買い物に行く")
        submitted = st.form_submit_button("追加")
        
        if submitted and new_todo:
            add_todo(new_todo)
            st.success(f"「{new_todo}」を追加しました！")
            st.rerun()
    
    # TODO表示セクション
    st.header("TODO リスト")
    
    if not st.session_state.todos:
        st.info("TODO項目がありません。上記から新しい項目を追加してください。")
    else:
        # 未完了のTODOを表示
        incomplete_todos = [todo for todo in st.session_state.todos if not todo['completed']]
        
        if incomplete_todos:
            st.subheader(f"未完了 ({len(incomplete_todos)}件)")
            
            for todo in incomplete_todos:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"• {todo['text']}")
                
                with col2:
                    if st.button("完了", key=f"complete_{todo['id']}"):
                        delete_todo(todo['id'])
                        st.success("TODO項目を完了しました！")
                        st.rerun()
        
        # 統計情報
        total_todos = len(st.session_state.todos)
        if total_todos > 0:
            st.divider()
            st.write(f"**統計:** 現在 {len(incomplete_todos)} 件のTODOがあります")

if __name__ == "__main__":
    main()