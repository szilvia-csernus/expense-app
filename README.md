# Expense App

Full-stack web application using Django REST, postgreSQL, ReactJS + Typescript @vite, and Docker. Created for streamlining the expense reinbursement process for church members of Redeemer churches in the Neatherlands.

# How to use the project

You will need Docker to utilise the project's docker configuration, more info: https://docs.docker.com/get-docker/.
Dockerfiles and docker-compose files are provided to run this project both in development or production modes.

## Set up the necessary files and accounts

1. Clone the project into a local folder.
2. Create a Cloudinary and a GMAIL account.
3. Create an `.env.dev` file in the `full-stack/backend` folder and place in the following environment variables - filled in with your own (secret) details:
    ```
    - SECRET_KEY=your-secret-django-key
    - DEBUG=True
    - DEVELOPMENT=1

    - POSTGRES_DB=db
    - POSTGRES_USER=your-db-username
    - POSTGRES_PASSWORD=your-db-password

    - CLOUDINARY_URL=your-cloudinary-url
    ```
4. Create an `.env.prod` file in the same folder placing next to `.env.dev`. For production, all database migrations as well as the superuser creation is part of the build process so we have to specify them in the `.env.prod` file:
    ```
    - SECRET_KEY=your-secret-django-key
    - DEBUG=False

    - POSTGRES_DB=db
    - POSTGRES_USER=db-username
    - POSTGRES_PASSWORD=db-password

    - DJANGO_SUPERUSER_USERNAME=your-superuser-name
    - DJANGO_SUPERUSER_EMAIL=your-superuser-email
    - DJANGO_SUPERUSER_PASSWORD=your-superuser-password

    - CLOUDINARY_URL=your-cloudinary-url
    ```

## Run the project in DEV mode

* For the first time, run the project with `docker-compose -p dev_expense_app -f docker-compose.dev.yml up --build`. This will build all the necessary docker images and will also run the docker container. 
    - The forntend will be available on `http://localhost:5173`.
    - The backend server will be running on `http://localhost:8000`.
    Both servers refresh whenever the source code gets changed.
* To set up the database, you first need to apply the migrations: `docker exec -it backend python manage.py migrate`
* Then, create a superuser: `docker exec -it backend python manage.py createsuperuser`
* If you need to install a new package (Pillow in this case), run: `docker exec -it backend pip install Pillow`
* After each install, you have to update the requirements.txt: `docker exec -it backend pip freeze > requirements.txt.` This will overwrite your existing `requirements.txt` file with the current state of installed packages in the container.
* After each install, you also have to rebuild the Docker image using this command: `docker-compose -p dev_expense_app -f docker-compose.dev.yml up --build && docker image prune -f`. The second, `docker image prune -f` command is used to remove the old image which otherwise would stay there, dangling. Please note however, that this command will remove all other dangling images in case there was any (although this is not a bad thing :)
* Whenever you modify the database models, don't forget to migrate the changes with the `docker exec -it backend python manage.py makemigrations` and the `docker exec -it backend python manage.py migrate` commands.

* To stop the container: `CTRL + C`.
* To start up the container again, run `docker-compose -p dev_expense_app -f docker-compose.dev.yml up`.

* To destroy the container: `docker-compose -p dev_expense_app -f docker-compose.dev.yml down`
* To destroy all the static files and database, run `docker volume prune`.

## Run the project in PRODUCTION mode

* For the first time, run the project with `docker-compose -p prod_expense_app -f docker-compose.prod.yml up --build`. This will build all the necessary docker images, create and run all the migrations, create a superuser and will also start up the docker container. 
    - The full-stack app will be available locally on `http://localhost:80`.
    - The backend server will be available without the static files on `http://localhost:8000`.
* To stop the container: `CTRL + C`.
* To start up the container again, run `docker-compose -p prod_expense_app -f docker-compose.prod.yml up`.
* To destroy the container: `docker-compose -p prod_expense_app -f docker-compose.prod.yml down`
* To destroy all the static files and database, run `docker volume prune`.