import json
import unittest

from agent.main import BASE_URL, public_proposal, public_result, validate


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


if __name__ == "__main__":
    unittest.main()
