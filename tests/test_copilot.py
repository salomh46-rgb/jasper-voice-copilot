import unittest
from fastapi.testclient import TestClient
from server.main import app
from server.command_engine import JasperVoiceCommandEngine
from server.system_actions import SystemActionExecutor

class TestJasperVoiceCopilot(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.engine = JasperVoiceCommandEngine()
        self.executor = SystemActionExecutor()

    def test_root_endpoint_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<!DOCTYPE html>', response.text)

    def test_calculator_intent(self):
        res = self.engine.parse_and_execute('Kalkulyatorni och')
        self.assertEqual(res['intent'], 'OPEN_APP')
        self.assertEqual(res['action'], 'calc')

    def test_notepad_intent(self):
        res = self.engine.parse_and_execute('Bloknotni och')
        self.assertEqual(res['intent'], 'OPEN_APP')
        self.assertEqual(res['action'], 'notepad')

    def test_telegram_intent(self):
        res = self.engine.parse_and_execute('Telegramni och')
        self.assertEqual(res['intent'], 'OPEN_APP')
        self.assertEqual(res['action'], 'telegram')
        self.assertTrue(res['details']['success'])

    def test_disk_audit_intent(self):
        res = self.engine.parse_and_execute('C diskda qancha joy qoldi?')
        self.assertEqual(res['intent'], 'SYSTEM_AUDIT')
        self.assertEqual(res['action'], 'disk_status')

    def test_projects_list_intent(self):
        res = self.engine.parse_and_execute('Loyihalarimni ko\'rsat')
        self.assertEqual(res['intent'], 'PROJECTS_LIST')
        self.assertEqual(res['action'], 'list_projects')

    def test_api_system_status(self):
        response = self.client.get('/api/system/status')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('disks', data)

    def test_api_voice_process_with_tts(self):
        response = self.client.post('/api/voice/process', json={'text': 'Salom', 'voice': 'uz-UZ-SardorNeural'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('audio_base64', data)

if __name__ == '__main__':
    unittest.main()
