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
- `GET /api/v1/session/send_verification_token`: This sends the verification token to the user's email
- `POST /api/v1/session/verify_token`: This takes the user's input and checks if it matches with the token.


### Stats:
- `GET /api/v1/number_of_users`: Retrieves the number of users in the application
- `GET /api/v1/number_of_places`: Retrieves the number of places in the application
- `GET /api/v1/number_of_reviews`: Retrieves the number of Reviews in the application
- `GET /api/v1/number_of_categories`: Retrieves the number of Categories in the application
- `GET /api/v1/number_of_replies`: Retrieves the number of Replies in the application

### Users:
- `GET /api/v1/users`: Returns a collection of all registered users in the application
- `GET /api/v1/users/{user_id}`: Returns a specific user
- `GET /api/v1/users/{keyword}`: Returns a collection of users whose username or name match the keyword specified
- `POST /api/v1/users`: This is used for creating a new user. This is reserved for the superuser only
- `DELETE /api/v1/users/{user_id}`: This deletes an existing user in the application
- `PUT /api/v1/users/{user_id}`: This updates the information of a user. This is reserved for the superuser only
- `PUT /api/v1/users/promote/{user_id}`: This is used to upgrade the role of a user to admin.
- `GET /api/v1/users/visit_history/{user_id}`: This retrieves the visit history of the user (places the user has visited and rated)
- `GET /api/v1/users/profile`: This returns the profile of the logged in user
- `PUT /api/v1/profile/update`: This updates the profile of the user himself
- `GET /api/v1/users/demote/{user_id}`: This is used to demote an admin to a regular user. It can only be done by the superuser
- `GET /api/v1/users/best_places_nearby`: This finds the best places in the city a user currently resides in

### Places
- `GET /api/v1/places`: Returns all places in the database
- `GET /api/v1/places/{place_id}`: Returns a particular place in the database
- `GET /api/v1/places/{keyword}`: Returns a collection of places whose names, category, city, state, or country matches the keyword.
- `DELETE /api/v1/places/{place_id}`: Deletes a place from the database. This can only be done by the admins and the superuser
- `POST /api/v1/places`: Adds a new place to the database. This can only be done by the admins and the superuser only.
- `PUT /api/v1/places/{place_id}`: Edits the information about a place. This can only be done by the admins and the superuser only
- `GET /api/v1/places/average_rating/{place_id}`: Gets the average rating of a place.
- `GET /api/v1/places/all_reviews/{place_id}`: Returns all the reviews given to a place
- `GET /api/v1/places/{place_id}/like_details`: Returns the likes count of a place and the percentage of likes
- `GET /api/v1/places/places_by_category`: Returns all places that match a certain category

### Reviews
- `GET /api/v1/reviews`: Returns all the reviews in the application
- `GET /api/v1/reviews/{review_id}`: Returns a particular review
- `POST /api/v1/reviews`: Adds a new review
- `PUT /api/v1/reviews/{review_id}`: Edits a review. This can only be done by the reviewer.
- `DELETE /api/v1/reviews/{review_id}`: This deletes a review. It can only be done by the reviewer, an admin or the superuser
- `GET /api/v1/{review_id}/replies`: This returns all the replies to a review

### Categories
- `GET /api/v1/categories`: Returns all the categories in the application. This can only be done by the admins and the superuser
- `POST /api/v1/categories`: Adds a new category. This can only be done by the admins and the superuser
- `GET /api/v1/categories/names`: Returns just the names of the categories in the database
- `PUT /api/v1/categories/{category_id}`: Edits a category. This can only be done by the admins and the superuser
- `DELETE /api/v1/categories/{category_id}`: Deletes a category. This can only be done by the admins and the superuser

### Replies
- `GET /api/v1/replies`: Returns all the replies in the database
- `GET /api/v1/replies/{reply_id}`: Return a particular reply from the database
- `DELETE /api/v1/replies/{reply_id}`: Deletes a reply from the database
- `POST /api/v1/replies/{review_id}`: adds a new reply to a review

## Role Description:

### Superuser:
He manages the whole application and is in charge of deciding who the admins are. He has access to all routes except for minor functions like changing a user's email or password.

### Admins:
They are the second tier. They are in charge of creating places, managing user activities, regulating activities on the application. they have restrictions when it comes to altering a user's information

### Users:
They are the regular users. They are not allowed to perform operations like creating places, creating users, but they can add reviews and give a rating to a place.



## Contributing

Contributions are welcome! Please follow the guidelines.

## License

Licenced by MIT.