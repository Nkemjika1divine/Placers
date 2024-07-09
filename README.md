<h1>Placers</h1>
<h3>See the world...</h3>

## Description
This is the backend for an application that allows a user to say what he/she thinks about a place he/she has visited. The user is requested to enter their rating of the place and their review of the place. This allows subsequent users to know about what a place does, and if the place is good enough. 

## Features
- **Role based access**: Regular users are onlr required to input information about places. Admins are the only ones required to add information or update information about a place. This ensures that the application is not littered with unverified information, as there's not yet a feature that enables verification of the places that are being added to the application
- **Search engine**: This search engine allows you to search for users and places differently. There's a route used to search for users while there's a route used to search for places. This ensures that the user gets the results the user desires
- **Authentication**: Only users who have accounts in the pplication will be allowed to access most routes in the application. As a new user, you will be required to create an account and log in before the rest of the routes will be available.


## Requirements
Please ensure that you have latest versions of Python and FastAPI installed on your computer.
Navigate to the root of the project directory and run `pip install -r requirements.txt`
Start the application by running `python start.py`


## API Routes
API routes include:

### Status:
- `GET /api/v1/status`: This returns the status and the version of the API.

### Authentication:
- `POST /api/v1/session/create_account`: This helps the user to create an account on the application
- `POST /api/v1/session/login`: This helps thte user to log into the application
- `DELETE /api/v1/session/logout`: This helps the user to logout of the application

### Stats:
- `GET /api/v1/number_of_users`: Retrieves the number of users in the application
- `GET /api/v1/number_of_places`: Retrieves the number of places in the application
- `GET /api/v1/number_of_reviews`: Retrieves the number of Reviews in the application

### Users:
- `GET /api/v1/users`: Returns a collection of all registered users in the application
- `GET /api/v1/users/{user_id}`: Returns a specific user
- `GET /api/v1/users/{keyword}`: Returns a collection of users whose username or name match the keyword specified
- `POST /api/v1/users`: This is used for creating a new user. This is reserved for admins and the superuser only
- `DELETE /api/v1/users/{user_id}`: This deletes an existing user in the application
- `PUT /api/v1/users/{user_id}`: This updates the information of a user. This is reserved for admins and the superuser only
- `PUT /api/v1/users/promote/{user_id}`: This is used to upgrade the role of a user to admin.
- `GET /api/v1/users/visit_history/{user_id}`: This retrieves the visit history of the user (places the user has visited and rated)
- `GET /api/v1/users/profile`: This returns the profile of the logged in user
- `GET /api/v1/users/demote/{user_id}`: This is used to demote an admin to a regular user. It can only be done by the superuser


## Contributing

Contributions are welcome! Please follow the guidelines.

## License

Licenced by MIT.