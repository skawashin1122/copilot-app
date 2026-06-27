import json
import os
import tempfile
from pathlib import Path
import sys

# Mock streamlit before importing app
class MockStreamlit:
    session_state = {}
    def __init__(self):
        self.session_state = {}
    def title(self, text):
        pass
    def text_input(self, label, **kwargs):
        return ""
    def button(self, label, **kwargs):
        return False
    def radio(self, label, options, **kwargs):
        return options[0]
    def divider(self):
        pass
    def columns(self, cols):
        return [self, self]
    def checkbox(self, label, **kwargs):
        return kwargs.get('value', False)
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def rerun(self):
        pass

sys.modules['streamlit'] = MockStreamlit()

# Now test the functions
def test_load_todos_nonexistent():
    """Test that load_todos returns empty list when file doesn't exist"""
    original_file = "todos.json"
    if os.path.exists(original_file):
        os.remove(original_file)
    
    from app import load_todos
    result = load_todos()
    assert result == [], f"Expected empty list, got {result}"
    print("[PASS] test_load_todos_nonexistent passed")


def test_save_and_load_todos():
    """Test that save_todos and load_todos work correctly"""
    test_data = [
        {"text": "Task 1", "done": False},
        {"text": "Task 2", "done": True},
        {"text": "Task 3", "done": False}
    ]
    
    from app import save_todos, load_todos
    
    # Save test data
    save_todos(test_data)
    
    # Load and verify
    loaded = load_todos()
    assert loaded == test_data, f"Expected {test_data}, got {loaded}"
    print("[PASS] test_save_and_load_todos passed")


def test_save_preserves_unicode():
    """Test that save_todos preserves UTF-8 characters"""
    test_data = [
        {"text": "日本語のタスク", "done": False},
        {"text": "😀 絵文字テスト", "done": False}
    ]
    
    from app import save_todos, load_todos
    
    save_todos(test_data)
    loaded = load_todos()
    
    assert loaded == test_data, f"Expected {test_data}, got {loaded}"
    assert loaded[0]["text"] == "日本語のタスク"
    assert loaded[1]["text"] == "😀 絵文字テスト"
    print("[PASS] test_save_preserves_unicode passed")


def test_file_is_created():
    """Test that todos.json is created when saving"""
    if os.path.exists("todos.json"):
        os.remove("todos.json")
    
    from app import save_todos
    
    save_todos([{"text": "test", "done": False}])
    
    assert os.path.exists("todos.json"), "todos.json was not created"
    print("[PASS] test_file_is_created passed")


def test_file_format():
    """Test that the JSON file is properly formatted"""
    test_data = [
        {"text": "Task 1", "done": False},
        {"text": "Task 2", "done": True}
    ]
    
    from app import save_todos
    
    save_todos(test_data)
    
    # Verify the file is valid JSON
    with open("todos.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    
    assert content == test_data
    
    # Verify the file is readable and properly indented
    with open("todos.json", "r", encoding="utf-8") as f:
        raw_content = f.read()
    
    assert "\n" in raw_content, "JSON should be indented (multiline)"
    print("[PASS] test_file_format passed")


if __name__ == "__main__":
    # Clean up before running tests
    if os.path.exists("todos.json"):
        os.remove("todos.json")
    
    try:
        test_load_todos_nonexistent()
        test_save_and_load_todos()
        test_save_preserves_unicode()
        test_file_is_created()
        test_file_format()
        
        print("\n[SUCCESS] All tests passed!")
        
        # Clean up after tests
        if os.path.exists("todos.json"):
            os.remove("todos.json")
    except AssertionError as e:
        print(f"\n[FAILED] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)
