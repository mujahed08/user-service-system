User and user role services are exposed here.
Follwing are end points:
1. create user
2. assign role
3. remove role
4. add password
5. suspend user
6. enable user

Tortoise Database migration with aerich
Follwing are steps to create database schema
1. navigate to project root directory i.e. user-service-system
2. >aerich init -t USER_SERVICE_SYSTEM.tortoise_orm.settings.TORTOISE_ORM
Success create migrate location ./migrations
Success generate config file aerich.ini
3. aerich init-db
aerich init-db
Success create app migrate location migrations\models
Success generate schema for app "models"
4. aerich migrate (If latter changes to data models)
5. aerich upgrade (after migrate changes)
6. aerich downgrade (if require to downgrade)


.pylintrc has been created with following command
pylint --generate-rcfile > .pylintrc

pytest.ini is a configuration file for pytest having higest configuration precedence. -s argument says python print() function 
prints to the console.


To Start applicationuse the following command
user-service-system>uvicorn USER_SERVICE_SYSTEM.main:app --port 8000 --log-config log4py.yaml --reload --reload-dir USER_SERVICE_SYSTEM