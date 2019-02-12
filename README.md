# Flask minimal starter

Uses Pipenv

## Init

Setup `.env` (dotenv) at root of project. For example, development environment will need:

```
FLASK_APP=src/app.py
FLASK_ENV=development
FLASK_SKIP_DOTENV=1
SECRET_KEY=<ncb.vJ$k*ILr-RANDOM_GENERATED_KEY-l13/y48te>
JWT_SECRET_KEY=<cnfdPl-RANDOM_GENERATED_KEY-4nq0dk@E^n>
```

For production:

- Change random generated keys
- Drop `FLASK_ENV` so that it defaults to `production`
- Add `DB_URI` to dotenv having database production URI (uses SQLite when no DB_URI is provided)
- Use Redis or other performant backend for JWT token blacklisting (refer to [Flask JWT Extended docs](https://flask-jwt-extended.readthedocs.io/en/latest/blacklist_and_token_revoking.html) and modify code at src/handlers/jwt.py)

> Functionality of revoking JWT tokens is achieved by adding them to blacklist

Apart from `FLASK_*` configs in dotenv, configs are loaded using src/config.py

## TODO

_If you are seeing this, raise an issue about incomplete `README.md`_

- check static files serving
- expire time of JWT and cookie-session, provide refresh token in JWT?
- haven't checked whether black and `exclude=` from pyproject.toml works or not
- SSE (server sent event) for notification
