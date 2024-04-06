install:
	poetry shell
	poetry install

start-func:
	celery -A parser.tasks_func worker

start-class:
	celery -A parser.tasks_class worker