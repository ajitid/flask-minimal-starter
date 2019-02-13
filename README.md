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
CORS_API_ORIGINS=<https://somehost.com>
```

> Apart from `FLASK_*` configs in dotenv, configs are loaded using src/config.py

- Expiry time for both cookie-session and JWT is set to 365 days. To change JWT expiry time, [set expiry time dynamically](https://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior.html#dynamic-token-expires-time). For cookie-session, refer to Flask Login docs. Both changes are needed to be done in `login` method of src/routes/auth.py.
- Create tables using migrations `pipenv run flask db upgrade` (do `pipenv run flask db migrate` if needed)
- Run using `pipenv run flask run`

---

For production:

- Use different random generated keys than development environment
- Drop `FLASK_ENV` from dotenv so that it defaults to `production`
- Add `DB_URI` to dotenv having database production URI (uses SQLite when no `DB_URI` is provided)
- Change `CORS_API_ORIGINS` if needed (don't set it to `*` as CSRF ain't used for cookie-session and so it is relying on CORS instead)
- Add error logging at src/handlers/error_handlers.py for 500 HTTP status
- Add GZip, rate-limiting
- Use Redis or other performant backend for JWT token blacklisting. For this, refer to bottom of the page [Blacklist And Token Revoking](https://flask-jwt-extended.readthedocs.io/en/latest/blacklist_and_token_revoking.html) and modify code at src/handlers/jwt.py accordingly

> Functionality of revoking JWT tokens is achieved by adding them to blacklist

## TODO

_If you are seeing this, probably readme is not completely done yet, so raise an issue about incomplete `README.md` at its repo_

- https://flask-login.readthedocs.io/en/latest/#disabling-session-cookie-for-apis
- haven't checked whether black and `exclude=` from pyproject.toml works or not
- SSE (server sent event) for notification
- flask konch - konch - bpython-curses
- flask hot reload
- flask channels
- flask storages
- fix poetry bug - removes common dependencies when a package is removed (if 2 packages are present and both have x as dependency, poetry has a bug by which when one package is removed it'll remove x too)
