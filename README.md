Test task for parsing "publishDTInEIS" data from tenders on first two pages of EIS portal.

To start func's based case:
```
celery -A parser.tasks_class worker
```

To start class based case:
```
celery -A parser.tasks_class worker
```