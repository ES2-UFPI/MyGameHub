from streamlit.testing.v1 import AppTest

def test_profile():
    at = AppTest.from_file("../Profile.py").run(timeout=50)
    assert not at.error, "Erro encontrado durante a execução inicial"
