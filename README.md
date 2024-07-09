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

### Authentication:
- `POST /api/v1/session/create_account`: This helps the user to create an account on the application
- `POST /api/v1/session/login`: This helps thte user to log into the application
- `DELETE /api/v1/session/logout`: This helps the user to logout of the application

### Stats
- `GET /api/v1/number_of_users`: Retrieves the number of users in the application
- `GET /api/v1/number_of_places`: Retrieves the number of places in the application
- `GET /api/v1/number_of_reviews`: Retrieves the number of Reviews in the application


## Contributing

Contributions are welcome! Please follow the guidelines.

## License

Licenced by MIT.