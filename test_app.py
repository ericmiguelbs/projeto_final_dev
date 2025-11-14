import unittest
from app import app
import werkzeug

# Patch temporário para werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class CriticalTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    # 1 — Token inválido → deve recusar
    def test_protected_invalid_token(self):
        headers = {"Authorization": "Bearer token_invalido_123"}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 422)

    # 2 — Método incorreto → 405
    def test_items_wrong_method(self):
        response = self.client.post('/items')
        self.assertEqual(response.status_code, 405)

    # 3 — Estrutura do token no login
    def test_login_token_structure(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertIn("access_token", data)
        self.assertIsInstance(data["access_token"], str)
        self.assertGreater(len(data["access_token"]), 10)

if __name__ == '__main__':
    unittest.main()
