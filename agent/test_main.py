import json
import unittest
from unittest.mock import patch

from agent.main import BASE_URL, main, public_proposal, public_result, read_block, validate


class AgentPolicyTests(unittest.TestCase):
    def login(self, url=BASE_URL + "/rest/user/login"):
        return {"tool": "curl", "args": [
            "-sS", "-X", "POST", "-H", "Content-Type: application/json",
            "--data-raw", json.dumps({"email": "teste@example.invalid", "password": "segredo"}), url
        ]}

    def test_login_is_limited_to_authorized_endpoint(self):
        self.assertEqual(validate(self.login()), [])
        self.assertTrue(validate(self.login("http://example.org/rest/user/login")))
        self.assertTrue(validate(self.login(BASE_URL + "/api/Users")))

    def test_extra_targets_and_options_are_blocked(self):
        self.assertTrue(validate({"tool": "curl", "args": [BASE_URL, "http://example.org"]}))
        self.assertTrue(validate({"tool": "curl", "args": ["-L", BASE_URL]}))
        self.assertTrue(validate({"tool": "nmap", "args": ["-p", "3000", "10.0.80.3", "3000"]}))

    def test_credentials_and_token_are_redacted(self):
        self.assertNotIn("segredo", json.dumps(public_proposal(self.login())))
        response = '{"authentication":{"token":"abc123","umail":"admin@example.invalid"}}\nHTTP_STATUS:200'
        self.assertNotIn("abc123", public_result(response))
        self.assertIn("HTTP_STATUS:200", public_result(response))

    def test_multiline_hypothesis_is_consumed_before_decision(self):
        with patch("builtins.input", side_effect=["primeira linha", "segunda linha", "FIM"]):
            self.assertEqual(read_block("Hipótese"), "primeira linha\nsegunda linha")

    def test_session_executes_only_one_approved_action(self):
        proposal = json.dumps({"tool": "curl", "args": [BASE_URL]})
        with patch("builtins.input", side_effect=["hipótese", "FIM", "a"]), \
             patch("agent.main.ask_ollama", side_effect=[proposal, '{"interpretacao":"ok"}']) as model, \
             patch("agent.main.execute", return_value=(0, "HTTP 200")) as execute, \
             patch("agent.main.record"):
            self.assertEqual(main(), 0)
            execute.assert_called_once()
            self.assertEqual(model.call_count, 2)


if __name__ == "__main__":
    unittest.main()
