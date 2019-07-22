import json
import unittest
from project.tests.base import BaseTestCase


def person_post(self):
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
    return response

def task_post(self):
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
    return response

class TestService(BaseTestCase):
    def test_persons_get(self):
            response = person_post(self)
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
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('REN HOEK', data['data']['attributes']['display_name'])

    def test_persons_tasks_post(self):
        with self.client:
            response = task_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = self.client.post(
                '/persons',
                data=json.dumps({
                    'data': {
                        'type': 'person',
                        'attributes': {
                            'name': 'Ren Hoek'
                        },
                        'relationships': {
                            'tasks': {
                                'data': [
                                    {
                                        'type': 'task',
                                        'id': '1'
                                    }
                                ]
                            }
                        }
                    }
                }), 
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 201)

    def test_persons_id_get(self):
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = self.client.get(f'/persons/1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('person', data['data']['type'])
            self.assertIn('REN HOEK', data['data']['attributes']['display_name'])
            self.assertIn('1', data['data']['id'])

    def test_persons_id_patch(self):
            response = person_post(self)
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

    def test_persons_id_tasks_patch(self):
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = task_post(self)
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
                        },
                        'relationships': {
                            'tasks': {
                                'data': [
                                    {
                                        'type': 'task',
                                        'id': '1'
                                    }
                                ]
                            }
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

    def test_persons_id_delete(self):
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = self.client.delete(f'/persons/1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Object successfully deleted', data['meta']['message'])

    def test_persons_id_tasks_get(self):
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = task_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = self.client.post(
                '/persons/1/relationships/tasks',
                data=json.dumps({
                    'data': [
                        {
                            'type': 'task',
                            'id': '1'
                        }
                    ]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            response = self.client.get(f'/persons/1/tasks')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('task', data['data'][0]['type'])
            self.assertIn('1', data['data'][0]['id'])

    def test_persons_id_tasks_post(self):
        with self.client:
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('REN HOEK', data['data']['attributes']['display_name'])
            response = self.client.post(
                '/persons/1/tasks',
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

    def test_persons_id_rel_tasks_get(self):
        with self.client:
            response = person_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = task_post(self)
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
            response = self.client.get(f'/persons/1/relationships/tasks')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('task', data['data'][0]['type'])
            self.assertEqual(1, data['data'][0]['id'])

    def test_tasks_get(self):
        with self.client:
            response = task_post(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('do nothing', data['data']['attributes']['what'])

if __name__ == '__main__':
    unittest.main()
