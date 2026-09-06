import unittest
from fastapi.testclient import TestClient
from server.main import app
from server.command_engine import JasperVoiceCommandEngine

class TestJasperVoiceCopilot(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.engine = JasperVoiceCommandEngine()

    def test_root_status(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "active")
        self.assertIn("Jasper AI", data["service"])

    def test_system_status_api(self):
        res = self.client.get("/api/system/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("disks", data)
        self.assertIn("total_projects", data)

    def test_calculator_intent(self):
        res = self.engine.parse_and_execute("Kalkulyatorni och")
        self.assertEqual(res["intent"], "OPEN_APP")
        self.assertEqual(res["action"], "calc")
        self.assertIn("Kalkulyator", res["speech_response"])

    def test_github_website_intent(self):
        res = self.engine.parse_and_execute("GitHub profilimni och")
        self.assertEqual(res["intent"], "OPEN_WEBSITE")
        self.assertEqual(res["action"], "github")
        self.assertIn("GitHub", res["speech_response"])

    def test_disk_audit_intent(self):
        res = self.engine.parse_and_execute("C diskda qancha joy qoldi?")
        self.assertEqual(res["intent"], "SYSTEM_AUDIT")
        self.assertEqual(res["action"], "disk_status")
        self.assertIn("gigabayt", res["speech_response"])

    def test_projects_list_intent(self):
        res = self.engine.parse_and_execute("Qanday loyihalar bor?")
        self.assertEqual(res["intent"], "PROJECTS_LIST")
        self.assertIn("loyihalar", res["speech_response"].lower())

    def test_voice_process_api_endpoint(self):
        payload = {"text": "Salom ishlar qalay?"}
        res = self.client.post("/api/voice/process", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["intent"], "GREETING")

if __name__ == "__main__":
    unittest.main()
