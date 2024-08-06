from streamlit.testing.v1 import AppTest

def test_login():
    at = AppTest.from_file("../../login.py").run(timeout=50)
    assert not at.error, "Erro encontrado durante a execução inicial"

    at.text_input[0].input("luishmq").run(timeout=50)
    at.text_input[1].input("1234").run(timeout=50)
    at.button[0].click().run(timeout=20)

    assert at.error[0].value == "Nome de usuário ou senha incorretos"