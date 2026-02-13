# shopping_cart_fastAPI

Small version in python of the .NET simple shopping cart I have somewhere around here.

First of all, create the DB in the engine with these commands:
DROP DATABASE shopping_cart
CREATE DATABASE shopping_cart

The .env file should be set in the root folder and it should include the Database URL and its credentials. Naturally it should look something like this:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=shopping_cart

Upon .venv activation, next steps should be to install the requirements.txt dependencies.
Then the ideal would be to run the DB migrations by executing this command:

alembic upgrade head

If there's a need to apply a migration to the DB execute this:

alembic revision --autogenerate -m "message goes here!"
alembic upgrade head

http://127.0.0.1:8000/docs# is the url to use Swagger
