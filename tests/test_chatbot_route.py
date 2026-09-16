import unittest

from app import app
import routes.chatbot_routes as chatbot_routes


class ChatbotRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_returns_friendly_message_when_ai_service_fails(self):
        original = chatbot_routes.ask_chatbot

        try:
            def boom(*args, **kwargs):
                raise RuntimeError("Gemini unavailable")

            chatbot_routes.ask_chatbot = boom

            response = self.client.post(
                "/chatbot/ask",
                json={"question": "hello"}
            )

            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("Sorry", data["answer"])
            self.assertIn("AI", data["answer"])
        finally:
            chatbot_routes.ask_chatbot = original


if __name__ == "__main__":
    unittest.main()
