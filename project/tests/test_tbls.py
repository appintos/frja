import json
import unittest
from project.tests.base import BaseTestCase


class TestService(BaseTestCase):
    def test_add_person(self):
        with self.client:
            response = self.client.post(
                '/persons',
                data=json.dumps({
                    'data': {
                        'type': 'person',
                        'attributes': {
                            'name': 'Ren Hoek'
                        }
                    }
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('REN HOEK', data['data']['attributes']['display_name'])

    def test_add_task(self):
        with self.client:
            response = self.client.post(
                '/tasks',
                data=json.dumps({
                    'data': {
                        'type': 'task',
                        'attributes': {
                            'what': 'do nothing'
                        }
                    }
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('do nothing', data['data']['attributes']['what'])


    def test_add_person_rel_task(self):
        with self.client:
            response = self.client.post(
                '/persons/1/relationships/tasks',
                data=json.dumps({
                    'data': [{
                        'type': 'task',
                        'id': '1'
                    }]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Relationship successfully created', data['meta']['message'])


if __name__ == '__main__':
    unittest.main()
