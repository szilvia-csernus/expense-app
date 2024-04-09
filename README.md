# Expense App

[![DeepScan grade](https://deepscan.io/api/teams/23376/projects/26640/branches/850430/badge/grade.svg)](https://deepscan.io/dashboard#view=project&tid=23376&pid=26640&bid=850430)

Full-stack web application using `Django REST` framework for backend, `postgreSQL` for database and `ReactJS + Typescript @vite` for frontend. Created for streamlining the expense reinbursement process for church members of Redeemer Churches and connected organisations in the Neatherlands.

Church members frequently pay for goods and services for the church's benefit which they can later submit for reimbursement. In the past, this process involved lots of administration from both members and admins, which church leaders wished to reduce. An earlier solution to this problem, implemented by Redeemer International Church Rotterdam, was a WordPress website, which allowed users to upload the receipts alongside their details into a form to be sent to the finance team via email. While this solution helped the end users, the finance team had more work with converting the incoming image files, many times in different file formats into one pdf document. Other churches faced similar problems, so a universal solution was needed.

This app allows the end-users to submit their expense forms to any of the subscribed churches / organisations, attaching the receipts in various image or pdf formats. The incoming forms and the receipts are converted to one multi-page pdf document, and sent to the respective finance teams.

Admins can register new churches or organisations. In addition to the church's name and finance teams' contact details, they can upload the organisation's logo which makes the forms more recognisable by end users.

The project is currently deployed on `Heroku`. The backend and frontend are in separate dynos and the PostgreSQL database is running in a managed postgresql database. Emails are sent with Gmail's SMTP server, the images (church logos) are stored on `Cloudinary`. 

Originally, the app was deployed on `AWS Elastic Container Service (Fargate Spot)`, the Postgresql database on `AWS Relational Database Service (RDS)`, but later on it was migrated over to Heroku mainly for cost reasons. The documentation for AWS ECS deployment alongside with the dockerfiles can be found on the `docker-aws` branch.


---

# Local development

I used VSCode on MacOS to develop this project locally. For the backend, I used Python's venv package to create a virtual environment and utilised django's built in development server. For the database, I initially used SQLite3 then later moved on to AWS RDS postgresql database. For the frontend, I used @vite's built in development server to serve the React-Typescript code.


For the virtual environment, assuming `python3` is installed, run `python -m venv venv`, then activate the environment with either VSCode's prompt or with `source venv/bin/activate`. (venv) will appear in front of the prompt.

After cloning the project, navigate to the `backend` folder, install all dependencies with `pip install -r requirements.txt` and then run `python manage.py runserver`. 

Navigate to the `frontend` folder, install all dependencies with `npm install` and start @vite's dev server:  `npm run dev`. (assuming `node` is installed)

As this app is a `Progressive Web App`, all frontend content is cached in the browser so `empty cache and hard reload` is needed whenever update is made.

---

# Environment variables

    ```sh

    SECRET_KEY=my-secret-django-key
    DEBUG=True  # Don't set this setting in production
    NO_HTTPS=1  # Don't set this setting in production

    # un-comment this if you want to use the the local Sqlite3 database.
    # SQLITE3=True

    # This setting is used if SQLITE3=True is commented out
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

    # For AWS deployment, I created a custom command to be used by the Docker container to create the superuser 
    # for the first time after the database was created. The credentials for the superuser therefore, 
    # also need to be specified as environment variables:

    # DJANGO_SUPERUSER_USERNAME=my-superuser-username
    # DJANGO_SUPERUSER_EMAIL=my-email
    # DJANGO_SUPERUSER_PASSWORD=my-superuser-password

    ```


In the local SQLite3 database, I created the superuser with django's CLI:

`python manage.py createsuperuser`.



# Deployment with Heroku


## Backend

1. Create an app on Heroku: Click on `Create App`

2. App name: `expense-app--backend`, Region: `Europe`

3. Log in to Heroku in the terminal: `heroku login`

4. Add a postgres database: `heroku addons:create heroku-postgresql --app expense-app--backend`
    This should have added `DATABASE_URL` to the config vars in Heroku Settings.

5. Add all other config vars at Settins / Reveal Config Vars / Add Config Vars

6. As we are going to push from one git repo to two remote heroku repos (one for backend and one for frontend), name the remote repositoriy to heroku-backend for clarity:

    `heroku git:remote -a expense-app--backend -r heroku-backend`

7. Push the content of the backend folder to this remote repo:

    `git subtree push --prefix full-stack/backend heroku-backend main`

8. Create a superuser for the new database:

    `heroku run python manage.py createsuperuser --app expense-app--backend`

9. To re-deploy any previously committed code, run:

    `git subtree push --prefix full-stack/backend heroku-backend main`

    from the root (expense-app) directory.



## Frontend


1. Create an app on Heroku: Click on `Create App`

2. App name: `expense-app`, Region: `Europe`

3. Name the remote repo:

    `heroku git:remote -a expense-app -r heroku-frontend`

4. Set the nodejs buildpack to be used to build the `dist` folder (with the heroku-postbuild script)
    `heroku buildpacks:add heroku/nodejs --index 1 --app expense-app`

5. Set the nginx buildback to static serving:
    `heroku buildpacks:add heroku-community/nginx --index 2 --app expense-app`

6. The `config/nginx.conf.erb` file and the `Procfile` provides the nginx configuration and start script.
    I also added `"heroku-postbuild": "npm run build"` to the `scripts` in `package.json` which heroku will run when the project is being built.

7. If needed, a `bash` container can be run to interact with the remote container:
    `heroku run bash --app expense-app`

8. To push only the frontend folder into this heroku repo (which will start up the build & deployment process):

    `git subtree push --prefix full-stack/frontend heroku-frontend main`

---

## Deployment of the Test Environment on Heroku

1. Create an app for testing the backend: `test-expense-app-backend`
2. Add the Config Vars, including the test database's url, under the `DATABASE_URL` url environment variable
3. Label the new app: `heroku git:remote -a test-expense-app-backend -r heroku-backend-test`
4. Deploy the test backend: `git subtree push --prefix full-stack/backend heroku-backend-test main`

5. Create an app for testing the frontend: `test-expense-app-frontend`
6. Add the `BACKEND_URL` url as a Config Var
7. Label the new app: `heroku git:remote -a test-expense-app-frontend -r heroku-frontend-test`
8. Deploy the test backend: `git subtree push --prefix full-stack/frontend heroku-frontend-test main`
9. Add the Node.js buildback as the 1st step for deployment: `heroku buildpacks:add heroku/nodejs --index 1 --app test-expense-app-frontend`
10. Add the 2nd step for nginx: `heroku buildpacks:add heroku-community/nginx --index 2 --app test-expense-app-frontend`
11. Push: `git subtree push --prefix full-stack/frontend heroku-frontend-test main`


## Accessing the Logfiles

Heroku retains logs for a period of 1 week, however, this is not guarantied. 
Currently, there is no log service set up for this application. 
Access the logfiles through the Heroku CLI with:

`heroku logs --app test-expense-app-backend`

# Deployment for AWS Elastic Container Registry (ECR) and AWS Elastic Container Services (ECS)


For deployment to AWS ECS, `Docker` was needed to run the backend and frontend in separate containers: The backend container uses Gunicorn (linux-alpine), the static files are served from Nginx (also linux-alpine). The images that are used by the containers are stored in `AWS Elastic Container Registry (ECR)`.

---

## Docker Images

For deployment, I created `Dockerfiles` to containerize the project. The images that are used for deployment are created with `docker-compose`. The `docker-compose.aws_local.yml` file allows to build the images and try out the running containers locally before uploading the images to AWS Elastic Container Registry.

    The backend image provides blueprint for the followings:

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
    - The forntend will be served on port 80 `http://localhost`.
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
    - Platform version: At the time of writing this, there is a glitch here. When I chose LATEST, the deployment failed. Hence I chose 1.4.0, which is currently the latest version.


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

# Migrating the database from AWS RDS to Heroku postgres

For this operation it's essential that the postgres version is the same in all 3 places: AWS RDS, local psql, Heroku postgres

Dump the aws records locally into a file called `db.dump`:

`pg_dump -Fc --no-acl --no-owner -h aws-rds-endpoint -U aws-rds-username -d aws-rds-database > db.dump`

-Fc: This stands for "custom format". This option outputs a custom-format archive suitable for input into pg_restore. The custom format allows for easy loading of the dump into a new database. It's also a compressed format, which can significantly reduce the size of the dump.

--no-acl: This prevents any access privilege (grant/revoke) commands from being included in the dump. This is useful when you're moving data to a different database where the same roles or users may not exist.

--no-owner: This prevents commands that would set ownership of objects to be included in the dump. This is useful when you're moving data to a different database where the same roles or users may not exist.

Retrieve the Heroku Postgres database url:
`heroku config:get DATABASE_URL --app expense-app--backend`

Upload the data to the Heroku Postgres database:
`pg_restore --verbose --clean --no-acl --no-owner -h my-heroku-host -U my-heroku-user -d my-heroku-database -W < db.dump`

Clean up the local file:
`rm db.dump`

---


# Security


## Secure Hosting

Heroku provides several security measures to ensure secure hosting for applications. 

* Infrastructure: Heroku's infrastructure is hosted and managed within Amazon's data centers which continually manages risks and compliance. 

* Data Encription: Heroku provides SSL encription for data in transit and rest. This applies to the database too.

* Security Updates: Heroku automatically applies security patches to the platform's underlying technologies.


## Secure Django Application


* Environment variables and secrets have never been committed to version control and they are registered as `Config Vars` on Heroku.

* Database Security: Django's Object Relational Model takes care of the integrity and security for all interactions with the database to avoid SQL injection attacks. The database is also protected with a strong password.

* Django's built-in auth and session framework securely handles user authentication and sessions.

* Input Validation: In addition to frontend validations, all inputs are sanitised again in the backend to protect against cross-site scripting (XSS) and other injection attacks.

* CSRF Protection: Django has a built-in protection against Cross Site Request Forgery (CSRF) attacks in the form of CSRF tokens which are used in this app to validate the origins of any "unsafe" requests, such as POST requests.

* `python manage.py check --deploy` command identifies no issues.

* Django has several settings as defaults to increase site security such as  
    - X_CONTENT_TYPE_OPTIONS = 'nosniff' to protect against as Cross-Site Scripting (XSS) and MIME type confusion attacks
    - X_FRAME_OPTIONS = 'DENY' to protect against clickjacking attacks by denying the site to be framed.
    - SESSION_COOKIE_HTTPONLY = True so that client-side JavaScript will not be able to access the session cookie.

---

# Vulnerabilities

1. Malicious users can send unwanted emails, with pictures included, to the finance team and the email address given in the form.

2. Forms can be submitted without limits, resulting in possible service interruptions as well as increased hosting costs.

3. Steganographic attacks: While this involves advanced techniques and therefore this app is not a likely target, it's theoretically possible to upload an image which contains malicious code whithout being detected by the browser or the backend validation. The malicious code, in theory, could affect the backend server but also the computers of the recepients of the emails.