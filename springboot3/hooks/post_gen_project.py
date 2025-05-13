import os
import shutil

REMOVE_PATHS = [
    '{% if cookiecutter.use_liquibase != "yes" %}src/main/resources/migracoes{% endif %}'
]
for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        # os.unlink(path) if os.path.isfile(path) else os.rmdir(path)
