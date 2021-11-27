# FastAPI Application with MongoDB and Redis Cache

This is a basis for an API application using the python framework FastAPI.
It contains a MongoDb for data storage und a Redis database for data caching as well.
To run this application [**Docker**](https://www.docker.com/products/docker-desktop) should be installed.


## Endpoint

http://localhost:8000/api

## OpenApi

http://localhost:8000/docs

## Preparation

Before running the application you should generate a new secret key using openssl.
Type in **"openssl rand -hex 32"** into your terminal. Copy the output and open the **.env** file.
Now replace the value of **ACCESS_TOKEN_SECRET_KEY**.

## Production

For starting the application run the **run<span/>.sh** script.

## Development

The development enviroment is designed for using [**VS Code**](https://code.visualstudio.com/download).
For development run the **runDev<span/>.sh** script. After the Containers are created run the ***Python: Docker***
debugger configuration. When the debugger is running the application will start immediately.

## Hint

If you want to test the api e.g. using the interactive openapi documentation start with creating a new User.
This User should have the role ***admin***. Afterwards you can login by the openapi password request from.
Now you are able to test the secured routes as well.