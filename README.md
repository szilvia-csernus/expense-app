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

I used VSCode on MacOS to develop this project locally. For the backend, I used Python's venv package to create a virtual environment and utilised django's built in development server. For the database, I initially used SQLite3 then later moved on to managed, cloud-based database. For the frontend, I used @vite's built in development server to serve the React-Typescript code.

## Backend

For the virtual environment, assuming `python3` is installed, create a virtual environment in the root folder by running `python -m venv venv`. Activate the environment in the workspace in VSCode by selecting this newly created environment with either VSCode's prompt or the 'Python: Select Environment' command. (shift+cmd+P). If this is not an option, activate venv with the `source venv/bin/activate` command. (venv) should appear in front of the prompt.

After cloning the project, navigate to the `backend` folder, install all dependencies with `pip install -r requirements.txt` and then run `python manage.py runserver` to start the development server.

## Frontend

Navigate to the `frontend` folder, install all dependencies with `npm install` and start @vite's dev server: `npm run dev`. (assuming `node` is installed)

As this app is a `Progressive Web App`, you need to adjust the settings in DevTools/Application to see updates during development.

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

    # BACKEND_HOST should match the port where the gunicorn server started.
    # Could be 'localhost' too.
    BACKEND_HOST=127.0.0.1  
    FRONTEND_URL=http://localhost:5173

    ```


In the local SQLite3 database, I created the superuser with django's CLI:

`python manage.py createsuperuser`.



# Deployment with Heroku

I first deployed the project manually, later created CI/CD workflows with Github Actions. (See )


## Backend

0. Prerequisite: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) needs to be installed.

1. Create an app on Heroku: Click on `Create App`

2. App name: `expense-app--backend`, Region: `Europe`

3. Log in to Heroku in the terminal: `heroku login`

4. Add a postgres database: `heroku addons:create heroku-postgresql --app expense-app--backend`
    This should have added `DATABASE_URL` to the config vars in Heroku Settings.

5. Add all other config vars at Settins / Reveal Config Vars / Add Config Vars

6. As we are going to push from one git repo to two remote heroku repos (one for backend and one for frontend), name the remote repositoriy to heroku-backend for clarity:

    `heroku git:remote -a expense-app--backend -r heroku-backend`

7. Push the content of the backend folder to this remote repo:

    `git subtree push --prefix backend heroku-backend main`

8. Create a superuser for the new database:

    `heroku run python manage.py createsuperuser --app expense-app--backend`

9. To re-deploy any previously committed code, run:

    `git subtree push --prefix backend heroku-backend main`

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

    `git subtree push --prefix frontend heroku-frontend main`



# CI/CD with Github Actions

I created two workflows to automate the deployment process. One for the test environment (`test` branch) and one for production (`main` branch). Every 'push' to the these branches initiate the deployment processes respectively. The details of these actions can be found in the `.github/worflows` folder.
