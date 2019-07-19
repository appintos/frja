import os
from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields


app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.String)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref=db.backref('tasks'))


db.create_all()


class PersonSchema(Schema):
    class Meta:
        type_ = 'person'
        self_view = 'person_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'person_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str(required=True, load_only=True)
    display_name = fields.Function(lambda obj: "{}".format(obj.name.upper()))
    tasks = Relationship(self_view='person_tasks',
                         self_view_kwargs={'id': '<id>'},
                         related_view='task_list',
                         related_view_kwargs={'id': '<id>'},
                         many=True,
                         schema='TaskSchema',
                         type_='task')


class TaskSchema(Schema):
    class Meta:
        type_ = 'task'
        self_view = 'task_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    what = fields.Str(required=True)
    owner = Relationship(attribute='person',
                         self_view='task_person',
                         self_view_kwargs={'id': '<id>'},
                         related_view='person_detail',
                         related_view_kwargs={'task_id': '<id>'},
                         schema='PersonSchema',
                         type_='person') 


class PersonList(ResourceList):
    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person}


class PersonDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('task_id') is not None:
            try:
                task = self.session.query(Task).filter_by(id=view_kwargs['task_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'task_id'},
                                     "Task: {} not found".format(view_kwargs['task_id']))
            else:
                if task.person is not None:
                    view_kwargs['id'] = task.person.id
                else:
                    view_kwargs['id'] = None

    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person,
                  'methods': {'before_get_object': before_get_object}}


class PersonRelationship(ResourceRelationship):
    schema = PersonSchema
    data_layer = {'session': db.session,
                  'model': Person}


class TaskList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Task)
        if view_kwargs.get('id') is not None:
            try:
                self.session.query(Person).filter_by(id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Person: {} not found".format(view_kwargs['id']))
            else:
                query_ = query_.join(Person).filter(Person.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get('id') is not None:
            person = self.session.query(Person).filter_by(id=view_kwargs['id']).one()
            data['person_id'] = person.id

    schema = TaskSchema
    data_layer = {'session': db.session,
                  'model': Task,
                  'methods': {'query': query,
                              'before_create_object': before_create_object}}


class TaskDetail(ResourceDetail):
    schema = TaskSchema
    data_layer = {'session': db.session,
                  'model': Task}


class TaskRelationship(ResourceRelationship):
    schema = TaskSchema
    data_layer = {'session': db.session,
                  'model': Task}


api = Api(app)
api.route(PersonList, 'person_list', '/persons')
api.route(PersonDetail, 'person_detail', '/persons/<int:id>', '/tasks/<int:task_id>/owner')
api.route(PersonRelationship, 'person_tasks', '/persons/<int:id>/relationships/tasks')
api.route(TaskList, 'task_list', '/tasks', '/persons/<int:id>/tasks')
api.route(TaskDetail, 'task_detail', '/tasks/<int:id>')
api.route(TaskRelationship, 'task_person', '/tasks/<int:id>/relationship/owner')
