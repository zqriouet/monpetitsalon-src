# Poetry cheat-sheet

```
pip install poetry
poetry new project_name
poetry new --src project-folder --name project_name
cd project-folder
poetry config virtualenvs.in-project true
poetry install
poetry env use /path/to/preferred/python/version
```

```
poetry shell
poetry add requests
poetry add pytest --group dev
poetry remove requests
deactivate
```

```
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi $PYPI_TOKEN
poetry publish --build -r test-pypi
```

```
poetry export -f requirements.txt --without-hashes > requirements.txt
```
