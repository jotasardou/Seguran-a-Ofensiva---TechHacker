import json
import unittest
from unittest.mock import patch

from agent.main import BASE_URL, INTERPRETATION_SCHEMA, execute, main, parse_interpretation, public_proposal, public_result, read_block, validate


class AgentPolicyTests(unittest.TestCase):
    def login(self, url=BASE_URL + "/rest/user/login"):
        return {"tool": "curl", "args": [
            "-sS", "-X", "POST", "-H", "Content-Type: application/json",
            "--data-raw", json.dumps({"email": "teste@example.invalid", "password": "segredo"}), url
        ]}

    def feedbacks(self, *, token="token-comum", item=None, method=None):
        args = ["-sS", "-H", f"Authorization: Bearer {token}"]
        if method:
            args += ["-X", method]
        suffix = "/api/Feedbacks" + (f"/{item}" if item is not None else "")
        return {"tool": "curl", "args": [*args, BASE_URL + suffix]}

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
        self.assertNotIn("token-comum", json.dumps(public_proposal(self.feedbacks())))

    def test_feedback_collection_allows_only_authenticated_get(self):
        self.assertEqual(validate(self.feedbacks()), [])
        self.assertTrue(validate(self.feedbacks(method="DELETE")))
        self.assertTrue(validate(self.feedbacks(token="")))
        self.assertTrue(validate(self.feedbacks(token="abc\nX-Extra: sim")))

    def test_feedback_delete_allows_only_one_numeric_item(self):
        self.assertEqual(validate(self.feedbacks(item="17", method="DELETE")), [])
        self.assertTrue(validate(self.feedbacks(item="17")))
        self.assertTrue(validate(self.feedbacks(item="17", method="PUT")))
        self.assertTrue(validate(self.feedbacks(item="17/18", method="DELETE")))
        self.assertTrue(validate(self.feedbacks(item="abc", method="DELETE")))

    def test_feedback_policy_blocks_other_targets_routes_headers_and_query(self):
        proposal = self.feedbacks()
        proposal["args"][-1] = "http://example.org/api/Feedbacks"
        self.assertTrue(validate(proposal))
        proposal = self.feedbacks()
        proposal["args"][-1] = BASE_URL + "/api/Users"
        self.assertTrue(validate(proposal))
        proposal = self.feedbacks()
        proposal["args"][2] = "Cookie: token-comum"
        self.assertTrue(validate(proposal))
        proposal = self.feedbacks()
        proposal["args"][-1] += "?limit=1"
        self.assertTrue(validate(proposal))
        self.assertTrue(validate({"tool": "curl", "args": [BASE_URL + "/api/Feedbacks/abc"]}))

    def test_feedback_execution_adds_http_status_without_logging_token(self):
        with patch("agent.main.subprocess.run") as run:
            run.return_value = type("Result", (), {"returncode": 0, "stdout": "token-comum\nHTTP_STATUS:200", "stderr": ""})()
            code, output = execute(self.feedbacks())
        self.assertEqual((code, output), (0, "[REDACTED]\nHTTP_STATUS:200"))
        self.assertEqual(run.call_args.args[0][-2:], ["-w", "\nHTTP_STATUS:%{http_code}"])
        self.assertEqual(run.call_args.args[0][:2], ["curl", "-q"])

    def test_multiline_hypothesis_is_consumed_before_decision(self):
        with patch("builtins.input", side_effect=["primeira linha", "segunda linha", "FIM"]):
            self.assertEqual(read_block("Hipótese"), "primeira linha\nsegunda linha")

    def test_session_executes_only_one_approved_action(self):
        proposal = json.dumps({"tool": "curl", "args": [BASE_URL]})
        interpretation = json.dumps({"interpretacao": "respondeu", "limite": "sem conclusão", "proximo_passo": "revisar"})
        with patch("builtins.input", side_effect=["hipótese", "FIM", "a"]), \
             patch("agent.main.ask_ollama", side_effect=[proposal, interpretation]) as model, \
             patch("agent.main.execute", return_value=(0, "HTTP 200")) as execute, \
             patch("agent.main.record"):
            self.assertEqual(main(), 0)
            execute.assert_called_once()
            self.assertEqual(model.call_count, 2)
            self.assertEqual(model.call_args.kwargs["format"], INTERPRETATION_SCHEMA)

    def test_tool_proposal_is_not_accepted_as_interpretation(self):
        with self.assertRaisesRegex(ValueError, "Interpretação deve conter"):
            parse_interpretation('{"tool":"nmap","args":["-p","3000","10.0.80.3"]}')

    def test_invalid_interpretation_ends_session_without_another_action(self):
        proposal = json.dumps({"tool": "nmap", "args": ["-p", "3000", "10.0.80.3"]})
        with patch("builtins.input", side_effect=["hipótese", "FIM", "a"]), \
             patch("agent.main.ask_ollama", side_effect=[proposal, proposal]), \
             patch("agent.main.execute", return_value=(0, "3000/tcp open")) as execute, \
             patch("agent.main.record") as record:
            self.assertEqual(main(), 2)
            execute.assert_called_once()
            self.assertIn("interpretation_invalid", [call.args[0] for call in record.call_args_list])


if __name__ == "__main__":
    unittest.main()
