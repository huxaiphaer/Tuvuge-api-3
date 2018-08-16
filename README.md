# Tuvuge-api

[![Build Status](https://travis-ci.org/huxaiphaer/Tuvuge-api-3.svg?branch=master)](https://travis-ci.org/huxaiphaer/Tuvuge-api-3)
[![Coverage Status](https://coveralls.io/repos/github/huxaiphaer/Tuvuge-api-3/badge.svg?branch=master)](https://coveralls.io/github/huxaiphaer/Tuvuge-api-3?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/b67c22ffdc5eda369208/maintainability)](https://codeclimate.com/github/huxaiphaer/Tuvuge-api-3/maintainability)


Ride-my App is a carpooling application
that provides drivers with the ability to create ride offers and passengers  to join available ride offers.

To acces this API online visit [API Link ](https://tuvuge-app.herokuapp.com)

### Requirements Building blocks.
- ```Python3``` - A programming language that lets us work more quickly (The universe loves speed!).

- ```Flask``` - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.

- ```Virtualenv``` - A tool to create isolated virtual environment

-```Postgres``` - PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

### Installation on Windows

First clone this repository
```
 git clone @https://github.com/huxaiphaer/ride-my-way-api
 cd ride-my-way-api
 ```

Create virtual environment and install it on Windows

 ```
 virtualenv --python=python3 venv
 .\venv\bin\activate.bat
 ```

Then install all the necessary dependencies by
 ```
pip install -r requirements.txt
 ```

Then run the application
 ```
 python run.py
 ```
 Testing and knowing coverage run 
 ```
nosetests or python manage.py test
 ```

 #### Endpoints to create a user account and login into the application

| HTTP Method   | End Point             | Action          |
| ------------- | --------------------- |-----------------|
| POST          | api/v1/user/register  |Create an account|
| POST          | /api/v1/login         |Login user       |



#### Other Endpoints.

| HTTP Method   | End Point                                 | Action                         |
| ------------- | ------------------------------------------|--------------------------------|
| POST          | /api/v1/users/rides                       |Creates ride offers.            |
| GET           | /api/v1/users/rides                       |Login user.                     |
| GET           | /api/v1/rides/<rideId>                    |Get specific ride offer by ID.  | 
| POST          | /rides/<rideId>/requests                  |Makes a ride request.           |
| GET           |  /users/rides/<rideId>/requests           |Fetch all ride requests.        | 
| PUT           | /users/rides/<rideId>/requests/<requestId>|Accept or reject a ride request.|



### Authors
[Lutaaya Huzaifah Idris](https://github.com/huxaiphaer)

