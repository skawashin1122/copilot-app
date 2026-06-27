import json
from pathlib import Path

import streamlit as st

DATA_FILE = Path(__file__).resolve().with_name("todos.json")
FILTER_OPTIONS = ("すべて", "未完了", "完了")


def load_todos():
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as f:
        todos = json.load(f)

    return todos if isinstance(todos, list) else []


def save_todos(todos):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def get_filtered_todos(todos, filter_option):
    if filter_option == "未完了":
        return [(i, todo) for i, todo in enumerate(todos) if not todo["done"]]
    if filter_option == "完了":
        return [(i, todo) for i, todo in enumerate(todos) if todo["done"]]
    return list(enumerate(todos))


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
    filter_option = st.radio("表示フィルター", FILTER_OPTIONS, horizontal=True)

    # --- タスク一覧 ---
    st.divider()
    todos = st.session_state.todos
    for i, todo in get_filtered_todos(todos, filter_option):
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
