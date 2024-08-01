from streamlit.testing.v1 import AppTest

def test_profile():
    at = AppTest.from_file("../🤖 Mario.py").run(timeout=20)
    assert not at.error