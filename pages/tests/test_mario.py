from streamlit.testing.v1 import AppTest

def test_mario():
    at = AppTest.from_file("../🤖 Mario.py").run(timeout=50)
    assert not at.error, "Erro encontrado durante a execução inicial"
    
    at.text_input[0].input("Qual jogo de corrida você recomenda?").run(timeout=50)
    at.button[0].click().run(timeout=20)
    assert at.markdown[2].value == "#### Resposta:"