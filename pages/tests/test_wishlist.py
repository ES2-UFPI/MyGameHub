from streamlit.testing.v1 import AppTest
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_wishlist():
    try:
        at = AppTest.from_file("../✨ Wishlist.py").run(timeout=50)
        assert not at.error, f"Erro encontrado durante a execução inicial: {at.error}"
        logger.info("Teste inicial passado sem erros.")
        
# Adicione qualquer verificação adicional que possa ser necessária aqui

    except Exception as e:
        logger.error(f"Exceção durante o teste: {e}")
        assert False, f"Exceção durante o teste: {e}"

if __name__ == "__main__":
    test_reviews()
