import json
import os
import streamlit as st

DATA_FILE = "todos.json"


def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def main():
    st.title("📝 TODO アプリ")

    if "todos" not in st.session_state:
        st.session_state.todos = load_todos()

    # --- タスク入力 ---
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input("新しいタスクを入力してください", key="new_task_input")
        submitted = st.form_submit_button("追加")

    if submitted:
        task = new_task.strip()
        if task:
            st.session_state.todos.append({"text": task, "done": False})
            save_todos(st.session_state.todos)
            st.rerun()

    # --- フィルター ---
    filter_option = st.radio(
        "表示フィルター", ["すべて", "未完了", "完了"], horizontal=True
    )

    # --- タスク一覧 ---
    st.divider()
    todos = st.session_state.todos
    for i, todo in enumerate(todos):
        if filter_option == "未完了" and todo["done"]:
            continue
        if filter_option == "完了" and not todo["done"]:
            continue

        col1, col2 = st.columns([10, 1])
        label = f"~~{todo['text']}~~" if todo["done"] else todo["text"]
        with col1:
            checked = st.checkbox(label, value=todo["done"], key=f"todo_{i}")
            if checked != todo["done"]:
                st.session_state.todos[i]["done"] = checked
                save_todos(st.session_state.todos)
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                save_todos(st.session_state.todos)
                st.rerun()


if __name__ == "__main__":
    main()
