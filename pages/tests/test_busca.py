from streamlit.testing.v1 import AppTest
def test_busca():
    at = AppTest.from_file("../🔎 Busca.py").run(timeout=50)
    assert not at.error, "Erro encontrado durante a execução inicial"