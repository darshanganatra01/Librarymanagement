from celery import Celery, Task
from main import make_app


app, _ = make_app()

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

