# Flask minimal starter

Uses Pipenv

## Setup for usage

- `pipenv install` to install dependencies

- Create and setup `.env` (dotenv) file at root of the project. For example, dotenv for development environment will look like:

```
FLASK_APP=src/app.py
FLASK_ENV=development
FLASK_SKIP_DOTENV=1
SECRET_KEY=<ncb.vJ$k*ILr-RANDOM_GENERATED_KEY-l13/y48te>
JWT_SECRET_KEY=<cnfdPl-RANDOM_GENERATED_KEY-4nq0dk@E^n>
```

> Apart from `FLASK_*` configs in dotenv, configs are loaded using src/config.py

- Run using `pipenv run flask run`

---

For production:

- Use different random generated keys than development environment
- Drop `FLASK_ENV` from dotenv so that it defaults to `production`
- Add `DB_URI` to dotenv having database production URI (uses SQLite when no `DB_URI` is provided)
- Add error logging at src/handlers/error_handlers.py for 500 HTTP status
- Use Redis or other performant backend for JWT token blacklisting (refer to [Flask JWT Extended docs](https://flask-jwt-extended.readthedocs.io/en/latest/blacklist_and_token_revoking.html) and modify code at src/handlers/jwt.py)

> Functionality of revoking JWT tokens is achieved by adding them to blacklist

## TODO

_If you are seeing this, probably readme is not completely done yet, so raise an issue about incomplete `README.md` at its repo_

- check static files serving
- expire time of JWT and cookie-session, provide refresh token in JWT?
- haven't checked whether black and `exclude=` from pyproject.toml works or not
- SSE (server sent event) for notification
