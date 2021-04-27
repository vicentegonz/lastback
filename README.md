# Backend

This repository contains the code for the base backend application.

## Requirements

The requirements are simple! You just need:

- [Docker](https://docs.docker.com/engine/install/)
- [Compose](https://docs.docker.com/compose/install/)

## Starting the server

To start the server, first create a `.env` file with all the environmental variables:

```sh
cp .env.example .env
nano .env  # Or use your favorite text editor
```

Then, build the Docker image:

```sh
docker-compose build
```

Now, just start the server!

```sh
docker-compose up
```

The API can be reached at `http://localhost:8000/`.

## Running commands inside the container

From now on, every command that should be run on the console will be run inside the container. This means that, for example, the command `python manage.py shell` will now be run through Docker using `docker-compose run web python manage.py shell`. The gist is that any command `[COMMAND]` will now be run as:

```sh
docker-compose run <service> [COMMAND]
```

Where `<service>` corresponds to the name of the service in which you want to run the command (the services get defined inside the `docker-compose.yml` file).

## Environmental variables

There are some environmental variables that need to be added to the repository:

- `DJANGO_SECRET_KEY`: **Required on production**. This random string variable is used by Django as a seed for all of its random stuff, so **it is essential to be random, unique and unknown**.
- `SOCIAL_SECRET`: **Required on production**. A secret random string used as a password for all the users created with the social workflow.
- `DJANGO_ENV`: **Required on production**. This string (should be in `["production", "development"]`) dictates the environment in which Django will run.
- `DEBUG`: This overwrites the `DJANGO_ENV` regarding the debug mode. If `DJANGO_ENV` is set to something other than `production`, the app will run by default on debug mode. If `DJANGO_ENV` is on `production`, however, you can still run the app on debug mode, by setting the `DEBUG` variable to `True`.
- `GOOGLE_CLIENT_ID`: **Required on production**. This is the client ID of the Google project that allows logins of the users through Google.
- `JWT_LIFETIME`: The duration of the JWT, in minutes. Defaults to `60`.
- `JWT_REFRESH_LIFETIME`: The duration of the refresh token, in hours. Defaults to `24`.
- `ALLOWED_ORIGINS`: A list of allowed tokens for CORS, separated by spaces (for instance, `https://production.com https://development.com http://localhost:8000`). Note that the application will always allow `http://localhost:3000`.
- `DEFAULT_DATABASE_URL`: **Required on production**. The URL for the default database. This variable overwrites the following variables:
  - `DEFAULT_DATABASE_NAME`: **Required on production** (unless `DEFAULT_DATABASE_URL` is set). Defines the name of the database to access. Defaults to `postgres`.
  - `DEFAULT_DATABASE_USER`: **Required on production** (unless `DEFAULT_DATABASE_URL` is set). Defines the username of the database engine to use. Defaults to `postgres`.
  - `DEFAULT_DATABASE_PASSWORD`: **Required on production** (unless `DEFAULT_DATABASE_URL` is set). Defines the password to use with the database user.
  - `DEFAULT_DATABASE_HOST`: **Required on production** (unless `DEFAULT_DATABASE_URL` is set). Defines the machine hosting the database engine. Defaults to `default_db`.
  - `DEFAULT_DATABASE_PORT`: **Required on production** (unless `DEFAULT_DATABASE_URL` is set). Defines the port of the host machine to query for the database. Defaults to `5432`.
- `EXTERNAL_DATABASE_URL`: **Required on production**. The URL for the external (read-only access) database. This variable overwrites the following variables:
  - `EXTERNAL_DATABASE_NAME`: **Required on production** (unless `EXTERNAL_DATABASE_URL` is set). Defines the name of the external database to access. Defaults to `postgres`.
  - `EXTERNAL_DATABASE_USER`: **Required on production** (unless `EXTERNAL_DATABASE_URL` is set). Defines the username of the external database engine to use. Defaults to `postgres`.
  - `EXTERNAL_DATABASE_PASSWORD`: **Required on production** (unless `EXTERNAL_DATABASE_URL` is set). Defines the password to use with the external database user.
  - `EXTERNAL_DATABASE_HOST`: **Required on production** (unless `EXTERNAL_DATABASE_URL` is set). Defines the machine hosting the external database engine. Defaults to `external_db`.
  - `EXTERNAL_DATABASE_PORT`: **Required on production** (unless `EXTERNAL_DATABASE_URL` is set). Defines the port of the host machine to query for the external database. Defaults to `5432`.

## Adding new apps

You will notice that, inside the `backend` folder, there are two sub-folders. Each of these folders corresponds to a specific app, and probably more will be added. The `docs` app corresponds to the app that starts the interactive documentation (more of this in a bit). The example app is just an application that serves as an example of how to set up a new application. The steps are as follow:

1. Create the application using `django-admin startapp new-app-name` **while your console is inside the `backend` folder**. This will create a new folder named `new-app-name` with some pre-configured stuff.
2. Add the application to the `.dockerignore` file with a _bang_. This means that, on the "_applications file_" section, you should add, at the bottom, `!backend/new-app-name`. This will indicate Docker to add that app to the Docker build context for the production image (on development everything will work OK, though, so **be careful**).
3. Modify the `apps.py` file inside the newly created app. Change the `name` property of the `NewAppNameConfig` object from `"new-app-name"` to `"backend.new-app-name"`.
4. Modify the `settings.py` file located inside `backend`. Add the application just added to the bottom of the `INSTALLED_APPS` variable, using the following syntax: `"backend.new-app-name.apps.NewAppNameConfig"`.
5. After creating some URLs on the new app (on a `urlpatterns` variable inside the `urls.py` file of that app), add the whole app router to the project's URLs. To do this, just add the following line to the `urls.py` file located inside `backend`: `path("new-app-name/", include("backend.new-app-name.urls"))`. This will make every URL added to the new app be reachable through `/new-app-name/url-defined-on-app`.

## Interactive documentation

This application comes loaded with interactive documentation. You will find a file named `openapi.json` inside the `docs` file. This file corresponds to the [OpenAPI](https://swagger.io/specification/) spec of the API, and will get rendered by [SwaggerUI](https://swagger.io/tools/swagger-ui/) at `/docs` and by [ReDoc](https://redoc.ly/redoc) at `/docs/redoc` (enter through the browser). Also, you can get the JSON spec at `/docs/openapi.json` (this will return the spec located at `docs/openapi.json`).

## Running the linters

This project includes quite some linters. `black`, `flake8`, `isort` and `pylint` are our Python linters. These linters will need to be passing throughout the whole development, and will be enforced by the CI _pipeline_. You will first need to install a virtual environment with all the dependencies to run the tests. To achieve this, run:

```sh
make get-poetry  # Download poetry, our package manager
make build-env  # Install dependencies on virtual env
```

Notice that this will create a `.venv` folder, containing all the installed dependencies. Finally, you can run the linters using the `make` commands included:

```sh
make black
make flake8
make isort
make pylint
```

You can also format your code _automagically_ using `black` and `isort`. To do this, just run:

```sh
make black!
make isort!
```
