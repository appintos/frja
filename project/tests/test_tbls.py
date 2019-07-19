import json
import unittest
from project.tests.base import BaseTestCase


class TestService(BaseTestCase):
    def test_persons_get(self):
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
            response = self.client.get(f'/persons')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('person', data['data'][0]['type'])
            self.assertIn('REN HOEK', data['data'][0]['attributes']['display_name'])
            self.assertIn('1', data['data'][0]['id'])

    def test_persons_post(self):
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

    def test_persons_get_id(self):
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
            response = self.client.get(f'/persons/1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('person', data['data']['type'])
            self.assertIn('REN HOEK', data['data']['attributes']['display_name'])
            self.assertIn('1', data['data']['id'])

    def test_persons_patch_id(self):
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
            response = self.client.patch(
                '/persons/1',
                data=json.dumps({
                    'data': {
                        'type': 'person',
                        'id': '1',
                        'attributes': {
                            'name': 'Marland Hoek'
                        }
                    }
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('person', data['data']['type'])
            self.assertIn('MARLAND HOEK', data['data']['attributes']['display_name'])
            self.assertIn('1', data['data']['id'])

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
