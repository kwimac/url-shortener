# url-shortener

This repo contains simple Django app allowing to create shorten URL.

## Instalation

1. Install [uv]
2. Open project root folder in console
3. Create virtual environment - run in console: `uv venv`
4. Install project dependencies (including dev dependencies): `uv sync`
5. Create `src/.env` file from template `src/.env.template` and fill required values: `cp src/env.template src/.env`
6. Run migrations for local DB: `uv run python ./manage.py migrate`
7. To check if all apackages are installed properly run tests - `uv run python ./manage.py test`

## Local development

To run local command one can either:

1. Enter the venv by runing in console: `source .venv/bin/activate`
2. Runing by uv - runing Django command with `uv run python ./manage.py ...`

Dev server is started by runing `.manage.py runserver`

## Admin panel

Admin panel is available at http://localhost:8000/admin (with dev server active).

To create superuser to log in run `./manage.py createsuperuser` and folow CLI request.

## Documentation

Beside this doc there is OpenAPI documentation available at `http://localhost:8000/swagger/` (with dev server active).

<!-- Links -->
[uv]: https://docs.astral.sh/uv/getting-started/installation/