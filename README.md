# Expense App

A full-stack web application using Django REST, postgreSQL, ReactJS + Typescript @vite, and Docker. Created for streamlining the expense reinbursement process for church members of Redeemer churches in the Neatherlands.

# How to use the project

To start up this full stack application locally, you need to take the followig steps:

1. You will need Docker to utilise the project's docker configuration. https://docs.docker.com/get-docker/
2. Clone the project into a local folder.
3. Create a `.env` file in the `full-stack/backend` folder and place in the following environment variables - filled in with your own (secret) details:
    - SECRET_KEY=your-secret-django-key
    - DEBUG=True
    - DEVELOPMENT=1

    - POSTGRES_DB=expense-app-db
    - POSTGRES_USER=db-username
    - POSTGRES_PASSWORD=db-password

    - DJANGO_SUPERUSER_USERNAME=superuser-username
    - DJANGO_SUPERUSER_EMAIL=superuser-email
    - DJANGO_SUPERUSER_PASSWORD=superuser-password

* For the first time, run `docker-compose up --build`. This will build all the necessary docker images and will also run the docker container. 
    - The full-stack app will be available locally on `0.0.0.0:80`.
    - The backend server will be available without the static files on `0.0.0.0:8000`.
* To stop and destroy the container, run `docker-compose down`.
* To destroy all the static files and database, run `docker volume prune`.
* To start up the project again, run `docker-compose up`.

## Docker resources

* https://docs.docker.com/
* https://www.youtube.com/watch?v=8VHheCkw-7k
* https://www.youtube.com/watch?v=oX5ElI-koww