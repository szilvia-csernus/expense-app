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


# Deployment

## Amazon ECR (Elastic Container Registry)

Deployment of the images:

0. Prerequisites: Amazon AWS and Docker accounts, install the AWS CLI.
1. Log in to your Amazon AWS account with an admin account. On the IAM board, create an Access Key for CLI access.
2. In VS Code, run `aws configure`.
3. For the Access Key Id and Secret Access Key, enter the credentials you've created earlier. For default region name, put `eu-west-2` and for output format, put `json`.
4. Run the docker-compose command detailed earlier.
5. List the images you created: `docker ls`. There should be 4 of them:
    * expense-app-backend
    * expense-app-frontend
    * expense-app-nginx
    * postgres
6. Connect to the AWS ECR service with the command: `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-amazon-account-number>.dkr.ecr.eu-west-2.amazonaws.com`.
7. Create an ECR repository for each image. Either on the AWS ECR Console or on the command line with: 
    `aws ecr create-repository --repository-name expense-app-backend --region eu-west-2`
    `aws ecr create-repository --repository-name expense-app-frontend --region eu-west-2`
    `aws ecr create-repository --repository-name expense-app-nginx --region eu-west-2`
    `aws ecr create-repository --repository-name postgres --region eu-west-2`
8. Tag all of your docker images with the corresponding AWS ECR repos:
    `docker tag expense-app-backend:latest <the-repositoryUri-you-got-back-in-the-previous-step>`
    Repeat it with the other 3.
9. Push the images one-by-one up to the AWS ECR repos:
    `docker push <the-repositoryUri>`


## Amazon AWS Elastic Container Service (ECS)

1. Navigate to the ECS Dashboard and create a Cluster. Use the pre-selected `AWS Fargate (serverless)` option.
2. Click on `Task definitions` and on `Create new task definition`.
    * Create a Task Definition for the db service:

        Name: db
        Network Mode: awsvpc
        Task size: Define according to your needs. For example, 0.5GB memory and 0.25 vCPU.
        Task Role: None (unless your container needs to access other AWS resources)
        Task execution role: ecsTaskExecutionRole (the default one)
        Container Definitions: Add a new container
            Image: postgres:15-alpine
            Port mappings: Host port 5432 TCP protocol, Port name 5432, App protocol: None.
            Environment: 
                POSTGRES_DB: your-db-name,
                POSTGRES_USER: your-db-username,
                POSTGRES_PASSWORD: your-db-password

            Storage / Volume-1: This is where you specify the path inside the container where you want to mount the volume.
            Volume name: db-data, Configure at task definition creation, volume type: Bind mount
            Add mount point: postgres:alpine-15, db-data, container path: /var/lib/postgresql/data


    * Create a Task Definition for the backend service:

        Network Mode: awsvpc
        Task size: Define according to your needs. For example, 1GB memory and 0.5 vCPU.
        Task Role: None (unless your container needs to access other AWS resources)
        Task execution role: ecsTaskExecutionRole (the default one)
        Container Definitions: Add a new container
            Image: The ECR URI of your backend image
            Port mappings: Host port 8000, container port 8000
            Environment: Define the environment variables from your .env file
        Storage / Volume-1: volume name: static_volume
        Add mount point: Source volume static_volume, container path /static/

    * Create a Task Definition for the frontend service:

        Task Role: None (unless your container needs to access other AWS resources)
        Network Mode: awsvpc
        Task size: Define according to your needs. For example, 1GB memory and 0.5 vCPU.
        Task execution role: ecsTaskExecutionRole (the default one)
        Container Definitions: Add a new container
        Image: The ECR URI of your frontend image
        Environment: VITE_DJANGO_HOST=http://localhost, VITE_DJANGO_PORT=8000
        Mount points: Source volume frontend, container path /app/dist

    * Create a Task Definition for the nginx service:

        Task Role: None (unless your container needs to access other AWS resources)
        Network Mode: awsvpc
        Task size: Define according to your needs. For example, 0.5GB memory and 0.25 vCPU.
        Container Definitions: Add a new container
        Image: The ECR URI of your nginx image
        Port mappings: Host port 80, container port 80
        Mount points: Source volume static_volume, container path /static/, and source volume frontend, container path /var/www/frontend
