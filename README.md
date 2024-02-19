# Expense App

Full-stack web application using `Django REST`, `postgreSQL`, `ReactJS + Typescript @vite`, and `Docker`. Created for streamlining the expense reinbursement process for church members of various churches in the Neatherlands.

The project is deployed on `AWS Elastic Container Service (Fargate Spot)`, the Postgresql database on `AWS Relational Database Service (RDS)`. 
The backend and frontend are in separate containers: The backend is running on Gunicorn (linux-alpine) and the static files are served from Nginx (also linux-alpine). The images that are used by the containers are stored in `AWS Elastic Container Registry (ECR)`. The media files (church logos) are stored on `Cloudinary`. Emails are sent with Gmail's SMTP server.

---

# Local development

I used VSCode on MacOS to develop this project locally. For the backend, I used Python's venv package to create a virtual environment and utilised django's built in development server. For the database, I initially used SQLite3 then later moved on to the deployed postgresql database. For the frontend, I used @vite's built in development server to serve the React-Typescript code.


For the virtual environment, assuming `python3` is installed, run `python -m venv venv`, then activate the environment with either VSCode's prompt or with `source venv/bin/activate`. (venv) will appear in front of the prompt.

After cloning the project, navigate to the `backend` folder, install all dependencies with `pip install -r requirements.txt` and then run `python manage.py runserver`. 

Navigate to the `frontend` folder, install all dependencies with `npm install` and start @vite's dev server:  `npm run dev`. (assuming `node` is installed)



## Environment variables

    ```sh

    SECRET_KEY=my-secret-django-key

    # un-comment this if you want to use the local database (Sqlite3) as well as to set DEBUG to True.
    # DEVELOPMENT=1

    DATABASE_URL=postgres://<username>:<password>@<host>/<dbname>

    CLOUDINARY_URL=my-cloudinary-url

    EMAIL_HOST_USER=my-email-host-user
    EMAIL_HOST_PASS=my-email-host-users-password

    # un-comment these for local development, when not using Docker:
    # BACKEND_HOST=127.0.0.1  # this should match the port where the gunicorn server started. Could be 'localhost' too.
    # FRONTEND_URL=http://localhost:5173

    # un-comment these for docker settings
    # FRONTEND_URL=http://localhost
    # In the local Docker environment, the backend container is seen as "backend", its
    # container name, by the frontend container. In AWS, the containers are referred as
    # "localhost" by each other.
    # BACKEND_HOST=backend

    ```


In the local SQLite3 database, I created the superuser with django's CLI:

`python manage.py createsuperuser`.

For deployment, I created a custom command to be used by the Docker container to create the superuser. The credentials for the superuser therefore, also need to be specified as environment variables:


    ```sh

    DJANGO_SUPERUSER_USERNAME=my-superuser-username
    DJANGO_SUPERUSER_EMAIL=my-email
    DJANGO_SUPERUSER_PASSWORD=my-superuser-password

    ```

---

# Deployment for AWS Elastic Container Registry (ECR) and AWS Elastic Container Services (ECS)


## Docker Images

For deployment, I created `Dockerfiles` to containerize the project. The images that are used for deployment are created with `docker-compose`. The `docker-compose.local.yml` file allows to build the images and try out the running containers locally before uploading the images to AWS Elastic Container Registry.

    The backend image provides blueprint for the following:

        - Using Python on Linux-alpine as a base image
        - Installing all dependencies,
        - Connecting to the database,
        - Createing and running all migrations,
        - Createing a superuser if none exists,
        - Starting up the Gunicorn server serving the django project.

    The Nginx image is a blueprint for:

        1st stage:
        - Using node on Linux-alpine as a base image
        - Installing all dependencies
        - Building the React project for production

        2nd stage:
        - Using nginx on Linux-alpine as a base image
        - Copying the image from the 1st stage to serve them as static files
        - Copying the nginx config file to override its default.
        - Starting up the server


## Docker Compose

* To run the deployment version locally, I used the following command: 

`docker-compose -p local-expense-app -f docker-compose.aws_local.yml up --build`. 

    This buils all the necessary docker images and also runs the docker containers. 
    - The forntend being served on port 80 `http://localhost`.
    - The backend on port 8000 `http://localhost:8000`.

* To stop the containers: `CTRL + C`
* To destroy the containers: `docker-compose -p local-expense-app -f docker-compose.aws_local.yml down`
* To destroy all the volumes: `docker volume prune`.

* To build the images for AWS: `docker-compose -f docker-compose.aws.yml build`. This builds all the necessary docker images needed for AWS deployment.


## Connecting to the AWS RDS postgres database from the console

When using django as a backend framework, it's not recommended to make changes in the database in any other ways but through django's tools. That is because django tracks all changes to ensure consistency and integrity. However, if needed, it is possible to connect to the database from the console. If `psql` is installed you can connect to the database: 

`psql --host=your-rds-endpoint --port=5432 --username=your-username --password --dbname=your-dbname` 



* When I needed to re-create all the tables in a specific app, I followed the following steps:
    - connected to the database with the command above
    - listed tables: `\dt`
    - manually deleted the `__cache__` folders from both the app's route and also the `migrations` folder
    - deleted the migrations from the `migrations` folder, leaving the `__init__.py` file in place.
    - in the backend's Dockerfile, I added the `python manage.py migrate <app_name> zero` and commented out all other migration-related commands temporarily. The added command un-marks the `<app_name>`'s migrations so that django won't think it doesn't need to migrate the migrations we are about to recreate.
    - in a new terminal, I ran the `docker-compose -p local-expense-app -f docker-compose.aws_local.yml up --build` command, also making sure that `DEVELOPMENT` is commented out in the `.env` file, meaning the AWS database is being used, not the local SQLite3 database.
    - in the `psql` terminal, checked if the tables had been deleted.
    - deleted the previous command from the dockerfile and un-commented the previously out-commented lines.
    - ran the docker-compose again. This recreated the tables.
    - checked in the psql terminal if the new tables were present.
    - exit the psql console: `\q`


## Amazon ECR (Elastic Container Registry)

For deployment of the images, I took the following steps:

1. Logged in to Amazon AWS with an admin account. On the IAM board, I created an Access Key for CLI access.
2. In VS Code, I ran `aws configure`.
3. For the Access Key Id and Secret Access Key, entered the credentials I've created earlier. For default region name, I put `eu-west-2` and for output format, `json`.
4. Ran the docker-compose command detailed earlier.
5. Listing the images that were created can be done with: `docker ls`. There should be 2 of them:
    * expense-app-backend
    * expense-app-nginx
6. I connected to the AWS ECR service with the command: `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-amazon-account-number>.dkr.ecr.eu-west-2.amazonaws.com`.
7. I created an ECR repository for each image. This could have been done on the AWS ECR Console, but I used the CLI for this: 
    `aws ecr create-repository --repository-name expense-app-backend --region eu-west-2`
    `aws ecr create-repository --repository-name expense-app-nginx --region eu-west-2`
8. Tagged both of the docker images with the corresponding AWS ECR repos:
    `docker tag expense-app-backend:latest <the-repositoryUri-you-got-back-in-the-previous-step>`
    Repeated it with the nginx image.
9. Pushed the images one-by-one up to the AWS ECR repos:
    `docker push <the-repositoryUri>`


If an image needs to be updated:
1. Re-connect with the same command used earlier: `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-amazon-account-number>.dkr.ecr.eu-west-2.amazonaws.com`
2. Update the image locally with `docker-compose -f docker-compose.aws.yml build`
3. Re-tag the aws version with: `docker tag expense-app-backend:latest <your-amazon-account-number>.dkr.ecr.eu-west-2.amazonaws.com/expense-app-backend:latest` - Don't forget the latest tags!
4. Push it up to AWS ECR like earlier: `docker push <the-repositoryUri>`


## Amazon AWS Elastic Container Service (ECS)


1. Navigate to the ECS Dashboard and create a Cluster. Use the pre-selected `AWS Fargate (serverless)` option.


2. Click on `Task definitions` and on `Create new task definition`.


    * Create a Task Definition for running both containers:


        - Infrastructure requirements
            * Launch type: AWS FARGATE
            * Operating system/Architecture: Linux/X86_64 
            * Network Mode: awsvpc
            * Task size: 0.25 vCPU and 0.5GB memory. (The smallest possible option to keep costs at minimum)
            * Task Role: ecsTaskExecutionRole
            * Task execution role: ecsTaskExecutionRole (the default one)


        - Container 1
            * Name: backend
            * Image: The ECR URI of the backend image, the `:latest` tag appended at the end
            * Essential container: No
            * Port mappings: Container port 8000, Protocol TCP, Port name, backend-8000-tcp, App protocol HTTP
            * Read only root file system: don't check it
            * Resource allocation limits: left blank
            * Environment: The environment variables from the .env file, entered manually
            * Use log collection


        - Container 2
            * Name: nginx
            * Image: The ECR URI of the nginx image
            * Essential container: True
            * Port mappings: Host port 80 TCP, container port 80 HTTP
            * Read only root file system: don't check it
            * Startup dependency ordering: backend Start


        - Storage
            * Volume 1
            * Volume name: static_volume
            * Configuration type: Configure at task definition creation
            * Volume type: Bind mount
            * Container mount points:
                - Container: backend
                - Source volume: static_volume
                - Container path: /staticfiles/
            * Volumes from:
                - Container: nginx
                - Source container: backend


        Click Create



3. Create a Security Group for the service: Security groups are "stateful" meaning the response of a request is allowed in the same connection, without opening up the port in the backword direction. In this case, allow inbound request from port 80, outbound for 5432 (postgres AWS RDS), 443 (https), a Custom TCP for port 587 (gmail smtp port) and 80 (http).


4. Create a Security Group for the load balancer you'll create in the next step. Allow inbound traffic on port 80 and all traffic outbound.


5. Create an Application Load Balancer. Apply the security group described above, set the timeout to 120s.


6. Navigate back to the Cluster and create a new Service


    - Capacity provider strategy: Use Custom (Advanced)
    - Capacity provider: FARGATE_SPOT (This option is more cost-concious than FARGATE. It uses freely available resources instead of guaranteed ones for up to 90% less costs, in return for accepting some interruption to the service.)
    - Platform version: At the time of writing this, there is a glitch here. If I chose LATEST, the deployment fails. Hence I chose 1.4.0, which is currently the latest version.


    Deployment configuration
    
    - Application type: Service
    - Task definition family: choose the one you've just created
    - Service name: RunApp
    - Desired tasks: 1

    
    - Deployment options: Rolling update (default) 
    - Networking: The VPC and subnets should be already filled in. Adjust if necessary.
    - Use an existing security group: choose the security group you've created earlier for the service, delete the default
    - PublicIp: Turn on


    - Load Balancing: Application Load Balancer (ALB)
    - Use an existing load balancer: Choose the load balancer you've just created
    - Health check grace period: 120s
    - Container to load balance: nginx:80:80
    - Listener: Create a new listener: 80:HTTP
    - Target group: Create a New Target Group:
                    Name: expense-app-tg
                    Protocol (default): HTTP (port 80)
                    Health Check protocol: HTTP
                    Health check path: /


    **CREATE**


    Leave everythig else the default/blank


---

# Security

## Secure Hosting

## Secure Project Architecture

## Security measures by Django




# Vulnerabilities

1. Malicious users can send unwanted emails, with pictures included, to both the finance team and the email address given in the form.

2. Forms can be submitted without limits, resulting in possible service interruptions as well as increased hosting costs.

3. Steganographic attacks: While this involves advanced techniques and therefore this app is not a likely target, it's theoretically possible to upload an image which contains malicious code whithout being detected by the browser or the backend validation. The malicious code, in theory, could affect the backend server but also the computers of the recepients of the emails.