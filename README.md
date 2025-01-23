
# TastyTales - A Django Rest Framework API

TastyTales is a full-stack web application designed for sharing and managing recipes, and user interactions. It uses Django Rest Framework for the backend and provides functionality for users to create and explore recipes, interact with other users through comments and likes, and manage their profiles. The application incorporates user authentication and recipe management to deliver a seamless experience.


The TastyTales API serves as the backend service for the TastyTales React application, enabling efficient data management and interaction.


![TastyTales - website](docs/images/startpage_3_card_user_loggedin.webp)

### Table of Contents

1. [TastyTales - A Django Rest Framework API](#tastytales---a-django-rest-framework-api)
2. [General Details](#general-details)
   - [Frontend Repository](#frontend-repository)
   - [Live Frontend Site](#live-frontend-site)
   - [Live API](#live-api)
3. [Agile Development](#agile-development)
   - [Kanban Workflow](#kanban-workflow)
   - [User Stories](#user-stories)
   - [Retrospectives](#retrospectives)
4. [Database Design](#database-design)
   - [Database Model](#database-model)
   - [ERD](#erd)
   - [Custom Models](#custom-models)
   - [CRUD Functionality](#crud-functionality)
   - [Database and Models](#database-and-models)
5. [API Endpoints](#api-endpoints)
   - [Recipe Endpoints](#recipe-endpoints)
   - [Recipe Ingredient Endpoints](#recipe-ingredient-endpoints)
   - [Comment Endpoints](#comment-endpoints)
   - [Like Endpoints](#like-endpoints)
   - [Profile Endpoints](#profile-endpoints)
   - [Follower Endpoints](#follower-endpoints)
6. [Technologies](#technologies)
   - [Language](#language)
   - [Tools](#tools)
   - [Frameworks and Libraries](#frameworks-and-libraries)
   - [Libraries Used](#libraries-used)
     - [Python Libraries](#python-libraries)
     - [Django Libraries](#django-libraries)
     - [External Libraries and Applications](#external-libraries-and-applications)
   - [Database](#database)
7. [Testing and Issues](#testing-and-issues)
8. [Deployment](#deployment)
   - [Cloning the Repository](#cloning-the-repository)
   - [Forking the Repository](#forking-the-repository)
   - [Deployment at Heroku](#deployment-at-heroku)
   - [Setting Config Vars](#setting-config-vars)
9. [Credits](#credits)
   - [Content](#content)
   - [Acknowledgements](#acknowledgements)

## General Details

This is the API for the TastyTales backend application. It manages user authentication, recipe management, and user interactions such as comments, likes, and followers.

- [Frontend repository](#https://github.com/behemot-biz/tastytales).

- [Live frontend site](#https://tastytales-83bed5f61a06.herokuapp.com).

- [Live API](#https://tastytales-api-56d55ea68c61.herokuapp.com).


## Agile Development

**TastyTales** was developed using agile methodologies, focusing on iterative progress and flexibility. 

[Kanban main board](https://github.com/users/behemot-biz/projects/5/views/1)

[Kanban sprint planning](https://github.com/users/behemot-biz/projects/5/views/3)

[Milestones](https://github.com/behemot-biz/tt-drf/milestones)

### Kanban Workflow
A **Kanban board** was used to track tasks with the following columns:
- **Backlog**: Planned tasks and features.
- **To Do**: Tasks ready to begin.
- **In Progress**: Tasks being worked on.
- **Test**: Completed tasks pending review.
- **Done**: Finished tasks ready for deployment.

### User Stories
Features were planned as user stories to prioritize the end-user perspective. Each story included functionality, acceptance criteria, and priority.


 [See User Stories in TEST.md](https://github.com/behemot-biz/tastytales/blob/main/TEST.md#user-stories)


### Retrospectives

At the end of each sprint, time was dedicated to reviewing successes, identifying challenges, and discussing areas for improvement. This iterative feedback loop was essential in continuously refining both the development process and the final product.

## Database Design
### Database Model

The database for `TastyTales` is structured to be scalable and efficient, adhering to the DRY (Don't Repeat Yourself) principle. The **Recipe** table is central to this design, linking multiple models and efficiently storing recipe details, ingredients, and user interactions without duplication of data.

The initial design of the entity-relationship diagram (ERD) captures the core models of the system, including the relationships between recipes, ingredients, comments, likes, and followers. Every part of the model is carefully constructed to ensure maximum reuse and minimal redundancy.


### ERD

Below is a visual representation of the database model for the `TastyTales` project:
<details>
<summary>ERD, image of</summary>

![ERD](docs/images/erd/tt-drf-erd.webp)

</details>

### Custom Models

The database includes several custom models tailored specifically to the needs of `TastyTales`.

These models make use of foreign key relationships to keep the data model clean and flexible. For example, instead of duplicating ingredient data across multiple recipe entries, the `Recipe` and `Ingredient` models are connected via a many-to-many relationship through the `RecipeIngredient` model. This approach reduces redundancy and keeps the database optimized.

<details>
<summary>Custom Models</summary>

- **Profile**: Extends the user profile with additional details such as bio, image, and content.

- **Recipe**: Tracks user-created recipes, linking each entry to the user who created it. Recipes also include metadata such as images, instructions, and introduction text.

- **RecipeIngredient**: Connects recipes with ingredients, storing additional data such as quantity and measurement. It ensures efficient many-to-many relationships between recipes and ingredients.

- **Ingredient**: Manages ingredients for recipes, ensuring unique and reusable entries.

- **Measurement**: Defines units of measurement (e.g., grams, cups) for ingredient quantities.

- **Comment**: Enables users to add comments to recipes, fostering engagement and interaction among users.

- **Like**: Tracks likes on recipes, allowing users to express appreciation for shared content.

- **Follower**: Manages relationships between users, allowing one user to follow another and stay updated on their activities.


</details>


### CRUD Functionality

The CRUD (Create, Read, Update, Delete) principle is foundational to the design of the database and the entire application:

- **Create**: Authenticated users can create recipes, adding ingredients and descriptions. Users can also leave comments, likes/, and follow other users.

- **Read**: Users both authenticated and unauthenticaded,  can view recipes, their ingredient lists, user profiles, and interactions such as comments, likes, and followers.

- **Update**: Users can update their recipes, modifying recipe details, ingredients, and quantities as needed.

- **Delete**: Users can delete their recipes, ingredients or comments if they are no longer relevant as well as unfollow profiles and unlike recipes. 

### Database and Models

TastyTales uses SQLite for development and PostgreSQL for production, ensuring a scalable and reliable database for live deployment.

#### User Model (from `django.contrib.auth.models.User`)

- **Table Name**: `auth_user`
- **Fields**: `id`, `username`, `email`, `password`, `first_name`, `last_name`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`
- **Functionality**: Manages user authentication and basic user details.

#### Profile Model

- **Table Name**: `profile_profile`
- **Fields**: `id`, `owner`, `name`, `content`, `image`, `created_at`, `updated_at`
- **Functionality**: Extends the user profile with additional details such as bio and avatar.

#### Recipe Model

- **Table Name**: `recipes_recipe`
- **Fields**: `id`, `owner`, `recipe_name`, `intro`, `instruction`, `image`, `created_at`, `updated_at`
- **Functionality**: Stores user-created recipes with descriptions and images.

#### Ingredient Model

- **Table Name**: `recipes_ingredient`
- **Fields**: `id`, `name`
- **Functionality**: Manages ingredients for recipes.

#### Measurement Model

- **Table Name**: `recipes_measurement`
- **Fields**: `id`, `measure`
- **Functionality**: Defines units for ingredient quantities (e.g., grams, liters).

#### RecipeIngredient Model (Intermediate Table)

- **Table Name**: `recipes_recipeingredient`
- **Fields**: `id`, `recipe`, `ingredient`, `quantity`, `measure`
- **Functionality**: Manages many-to-many relationships between recipes and ingredients with additional data like quantity and measurement.

#### Comment Model

- **Table Name**: `recipes_comment`
- **Fields**: `id`, `owner`, `recipe`, `content`, `created_at`, `updated_at`
- **Functionality**: Allows users to comment on recipes.

#### Like Model

- **Table Name**: `recipes_like`
- **Fields**: `id`, `owner`, `recipe`, `created_at`
- **Functionality**: Enables users to like recipes.

#### Follower Model

- **Table Name**: `followers_follower`
- **Fields**: `id`, `owner`, `followed`, `created_at`
- **Functionality**: Tracks user-to-user following relationships, ensuring unique and meaningful connections.


## API Endpoints
The TastyTales platform uses a **React frontend** and a **Django REST Framework (DRF) backend** to work together through API endpoints. 

The **DRF backend** provides endpoints for managing recipes, ingredients, profiles, likes, and comments. For example:
- `/recipes/` lets the frontend create and fetch recipes.
- `/likes/` allows liking or unliking recipes.
- `/comments/` handles adding, updating, or deleting comments.

The **React frontend** interacts with these endpoints to display data and handle user actions. For instance, when a user views a recipe, the frontend gets its details from `/recipes/<id>/`. When a user likes a recipe, it sends a request to `/likes/`.

This structure keeps the frontend and backend connected, making the app interactive and user-friendly.


### Recipe Endpoints
| HTTP Method | Endpoint            | Description                                                 | Authentication Required |
|-------------|---------------------|-------------------------------------------------------------|-------------------------|
| GET         | `/recipes/`         | Retrieve a list of recipes. Recipes with `pre_delete` or `pending_publish` status are visible only to the owner. | **Yes** for private statuses |
| POST        | `/recipes/`         | Create a new recipe.                                        | Yes                     |
| GET         | `/recipes/<int:pk>/`| Retrieve a single recipe by ID. Recipes with private statuses are visible only to the owner. | **Yes** for private statuses |
| PUT         | `/recipes/<int:pk>/`| Update a recipe if the user is the owner.                   | Yes                     |
| DELETE      | `/recipes/<int:pk>/`| Delete a recipe if the user is the owner.                   | Yes                     |




### Recipe Ingredient Endpoints
| HTTP Method | Endpoint                   | Description                                             | Authentication Required |
|-------------|----------------------------|---------------------------------------------------------|--------------------------|
| GET         | /ingredients/              | Retrieve a list of recipe ingredients.                 | No                       |
| POST        | /ingredients/              | Add a new ingredient to a recipe.                      | Yes                      |
| GET         | /ingredients/<int:pk>/     | Retrieve a specific recipe ingredient by ID.           | No                       |
| PUT         | /ingredients/<int:pk>/     | Update a recipe ingredient if the user is the owner.   | Yes                      |
| DELETE      | /ingredients/<int:pk>/     | Delete a recipe ingredient if the user is the owner.   | Yes                      |



### Comment Endpoints
| HTTP Method | Endpoint            | Description                                            | Authentication Required |
|-------------|---------------------|--------------------------------------------------------|--------------------------|
| GET         | /comments/          | Retrieve a list of comments.                          | No                       |
| POST        | /comments/          | Create a new comment.                                 | Yes                      |
| GET         | /comments/<int:pk>/ | Retrieve a single comment by ID.                      | No                       |
| PUT         | /comments/<int:pk>/ | Update a comment if the user is the owner.            | Yes                      |
| DELETE      | /comments/<int:pk>/ | Delete a comment if the user is the owner.            | Yes                      |



### Like Endpoints
| HTTP Method | Endpoint        | Description                     | Authentication Required |
|-------------|-----------------|---------------------------------|--------------------------|
| GET         | /likes/         | Retrieve a list of likes.       | No                       |
| POST        | /likes/         | Like a recipe.                  | Yes                      |
| GET         | /likes/<int:pk>/| Retrieve a single like by ID.   | No                       |
| DELETE      | /likes/<int:pk>/| Unlike a recipe.                | Yes                      |



### Profile Endpoints
| HTTP Method | Endpoint              | Description                                             | Authentication Required |
|-------------|-----------------------|---------------------------------------------------------|--------------------------|
| GET         | /profiles/            | Retrieve a list of user profiles.                      | No                       |
| GET         | /profiles/<int:pk>/   | Retrieve a single user profile by ID.                  | No                       |
| PUT         | /profiles/<int:pk>/   | Update a profile if the user is the owner.             | Yes                      |



### Follower Endpoints
| HTTP Method | Endpoint              | Description                                             | Authentication Required |
|-------------|-----------------------|---------------------------------------------------------|--------------------------|
| GET         | /followers/           | Retrieve a list of followers.                          | No                       |
| POST        | /followers/           | Follow a user.                                         | Yes                      |
| GET         | /followers/<int:pk>/  | Retrieve a specific follower by ID.                    | No                       |
| DELETE      | /followers/<int:pk>/  | Unfollow a user.                                       | Yes                      |



*<span style="color: blue;">[Back to top](#table-of-contents)</span>*

## Technologies


**Language:**
- [Python](https://www.python.org/)


**Tools:**
- VsCode (IDE)
- [GitHub](https://github.com) (Repository)
- [Heroku platform](https://www.heroku.com/) (Deployment and hosting platform)
- [CI Python Linter](https://pep8ci.herokuapp.com/#) (Python code validation)
- [Dbdiagram.io](https://dbdiagram.io/) (Draw Entity-Relationship Diagrams)


**Frameworks and Libraries:**
- [Django](https://www.djangoproject.com/) (Web framework for Python)
- [Django REST Framework](https://www.django-rest-framework.org/) (Simplified API development for Django)
- [PostgreSQL](https://www.postgresql.org/)
- [Cloudinary](https://cloudinary.com/) (Cloud storage for all images)
- [Dillinger](https://dillinger.io) (Readme editor)
- [Postman](https://www.postman.com) (API testing and debugging made simple)


### Libraries Used
The TastyTales application uses several external libraries. Below is a list of these libraries along with a breif description and instructions on how to install them.

### Python Libraries
<details>
<summary>List of libraries</summary>

- **asgiref**  
  - **Description**: ASGI is a standard for Python asynchronous web apps and servers to communicate.  
  - **Installation**: `pip install asgiref==3.8.1`  

- **certifi**  
  - **Description**: Mozilla’s curated collection of Root Certificates for SSL.  
  - **Installation**: `pip install certifi==2024.8.30`  

- **cffi**  
  - **Description**: Foreign Function Interface for Python calling C code.  
  - **Installation**: `pip install cffi==1.17.1`  

- **charset-normalizer**  
  - **Description**: Library for reading text from unknown charset encoding.  
  - **Installation**: `pip install charset-normalizer==3.4.0`  

- **cloudinary**  
  - **Description**: Integration with Cloudinary for managing images and files.  
  - **Installation**: `pip install cloudinary==1.41.0`  

- **coverage**  
  - **Description**: Code coverage measurement for Python.  
  - **Installation**: `pip install coverage==7.6.8`  

- **cryptography**  
  - **Description**: Provides cryptographic recipes and primitives to Python developers.  
  - **Installation**: `pip install cryptography==44.0.0`  

- **gunicorn**  
  - **Description**: Python WSGI HTTP Server for UNIX.  
  - **Installation**: `pip install gunicorn==23.0.0`  

- **idna**  
  - **Description**: Support for the Internationalized Domain Names in Applications protocol.  
  - **Installation**: `pip install idna==3.10`  

- **oauthlib**  
  - **Description**: Thorough implementation of the OAuth request-signing logic.  
  - **Installation**: `pip install oauthlib==3.2.2`  

- **packaging**  
  - **Description**: Core utilities for Python packages.  
  - **Installation**: `pip install packaging==24.2`  

- **Pillow**  
  - **Description**: Python Imaging Library for image processing.  
  - **Installation**: `pip install Pillow==8.2.0`  

- **psycopg2-binary**  
  - **Description**: PostgreSQL database adapter for Python.  
  - **Installation**: `pip install psycopg2-binary==2.9.10`  

- **PyJWT**  
  - **Description**: JSON Web Token implementation in Python.  
  - **Installation**: `pip install PyJWT==2.10.1`  

- **python3-openid**  
  - **Description**: OpenID support for modern servers and consumers.  
  - **Installation**: `pip install python3-openid==3.2.0`  

- **pytz**  
  - **Description**: Cross-platform timezone calculations.  
  - **Installation**: `pip install pytz==2024.2`  

- **requests**  
  - **Description**: Simple HTTP library for sending requests.  
  - **Installation**: `pip install requests==2.32.3`  

- **sqlparse**  
  - **Description**: Non-validating SQL parser for Python.  
  - **Installation**: `pip install sqlparse==0.5.2`  

- **typing_extensions**  
  - **Description**: Backported and experimental type hints.  
  - **Installation**: `pip install typing_extensions==4.12.2`  

- **urllib3**  
  - **Description**: HTTP library with thread-safe connection pooling.  
  - **Installation**: `pip install urllib3==2.2.3`  

</details>

### Django Libraries
<details>
<summary>List of libraries</summary>

- **Django**  
  - **Description**: High-level Python web framework.  
  - **Installation**: `pip install Django==4.2.16`  

- **django-allauth**  
  - **Description**: Integrated set of applications for authentication and account management.  
  - **Installation**: `pip install django-allauth==0.50.0`  

- **django-cloudinary-storage**  
  - **Description**: Facilitates integration with Cloudinary.  
  - **Installation**: `pip install django-cloudinary-storage==0.3.0`  

- **django-cors-headers**  
  - **Description**: Handles server headers for Cross-Origin Resource Sharing (CORS).  
  - **Installation**: `pip install django-cors-headers==4.6.0`  

- **django-filter**  
  - **Description**: Allows users to filter querysets dynamically.  
  - **Installation**: `pip install django-filter==24.3`  

- **djangorestframework**  
  - **Description**: Toolkit for building Web APIs.  
  - **Installation**: `pip install djangorestframework==3.15.2`  

- **djangorestframework-simplejwt**  
  - **Description**: Minimal JSON Web Token authentication plugin.  
  - **Installation**: `pip install djangorestframework-simplejwt==5.3.1`  

- **dj-database-url**  
  - **Description**: Utility for configuring the database using environment variables.  
  - **Installation**: `pip install dj-database-url==0.5.0`  

- **dj-rest-auth**  
  - **Description**: Set of API endpoints for User Registration and Authentication.  
  - **Installation**: `pip install dj-rest-auth==2.1.9`  

</details>

### External Libraries and Applications

<details>
<summary>List of libraries</summary>

- **Cloudinary**  
  - **Description**: Cloud-based image management and delivery solution.  
  - **Installation**: `pip install cloudinary==1.41.0`  

- **Coverage**  
  - **Description**: Code coverage measurement for Python.  
  - **Installation**: `pip install coverage==7.6.8`  

</details>

## Database

<details>
<summary>List of databases</summary>

- **PostgreSQL**: Used as the production database backend for scalability and robustness.  
- **SQLite**: Used as the development database backend for simplicity and ease of setup during the development process.

</details>

*<span style="color: blue;">[Back to top](#table-of-contents)</span>*

## Testing and Issues

Testing information and issues encountered during development are tracked and documented in the respective repositories.

[See User Stories in TEST.md](https://github.com/behemot-biz/tastytales/blob/main/TEST.md#tastytales-api)


## Deployment

### Cloning the Repository
To clone the repository to your local machine:

1. Visit the [TastyTales - API GitHub repository](https://github.com/behemot-biz/tt-drf).
2. Click the green **"Code"** button.
3. Copy the HTTPS, SSH, or GitHub CLI link provided.
4. Open your terminal and navigate to the desired folder location.
5. Run the following command:
   ```bash
   git clone <repository-link>
   ```
   Replace `<repository-link>` with the copied link.
6. Navigate into the cloned repository:
   ```bash
   cd tastytales
   ```

### Forking the Repository
To fork the repository to your GitHub account:

1. Visit the [TastyTales - API GitHub repository](https://github.com/behemot-biz/tt-drf).
2. Click the **"Fork"** button at the top-right corner of the page.
3. Select your GitHub account as the destination.
4. A forked copy of the repository will appear in your account.

You can now make changes to the forked repository independently. To update your fork with changes from the original repository, use a pull request or the GitHub sync feature.

### Deployment at Heroku
The application is deployed form and hosted on the Heroku platform, enabling seamless deployment and hosting. Below is an overview of the process used:

#### Creating a Heroku Account
1. Visit [Heroku's website](https://www.heroku.com/) and create a free account.
2. Verify your email to activate the account.

#### Creating the App
1. Log in to the Heroku dashboard.
2. Click **"New"** > **"Create New App"**.
3. Choose a unique app name.
4. Select **Europe** as the region to optimize latency for users in the region.
5. Navigate to **settings** and select Add buildpack **python** 

#### Setting Up Deployment
1. Link the app to the GitHub repository:
   - Navigate to the **"Deploy"** tab in the Heroku dashboard.
   - Under **Deployment method**, select **GitHub**.
   - Authorize Heroku to access your GitHub account, if prompted.
   - Search for and connect the appropriate repository.

2. Enable Automatic Deploys (optional):
   - Under **Automatic deploys**, select the branch (e.g., `main`) to deploy changes automatically after every push.

3. Deploy the App:
   - Under **Manual deploy**, select the branch and click **"Deploy Branch"** to build and deploy the app.

### Setting Config Vars

Config vars are essential for the secure and smooth functioning of the app. To set up config vars:

1. Navigate to the **"Settings"** tab of your app in the Heroku dashboard.
2. Click **"Reveal Config Vars"** under the **Config Vars** section.
3. Add the following key-value pairs:

| Key               | Description                                                                                                                                          | Example Value                         |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| `ALLOWED_HOSTS`    | Specify the domains that can access your app. Include `herokuapp.com` and your custom domains if any.                                                | `your-app-name.herokuapp.com`         |
| `CLIENT_ORIGIN`    | Specify the URL of your frontend application in production.                                                                                         | `https://your-frontend-domain.com`    |
| `CLIENT_ORIGIN_DEV`| Specify the URL of your frontend application in development (useful for local testing).                                                             | `http://localhost:3000`               |
| `CLOUDINARY_URL`   | Cloudinary URL for storing and retrieving media assets. This should match the URL provided by your Cloudinary account.                               | `cloudinary://API_KEY:API_SECRET@CLOUD_NAME` |
| `DATABASE_URL`     | The database connection string, can set up automatically by Heroku when using Heroku Postgres.                                                |   `URL to your Postgres DB`                  |
| `SECRET_KEY`       | A random and secure secret key used for cryptographic operations. Keep this value confidential.                                                      | `a-very-secret-key`                   |

4. Save each key-value pair after entering them in the respective fields.

## Credits

<details>
<summary>Content</summary>

Resources that inspired and guided development:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [Code Institute Walkthrough Project](https://codeinstitute.net/)
</details>

<details>
<summary>Acknowledgements</summary>

### Thank You
- A Big thank to CI's cohort facilitator Kay Welfare and to mentor Rohit Sharma for the support and help along the way
- My friends and family for the tests, patience and support
- The slack community and mainly the Swedish Channel.

</details>

*<span style="color: blue;">[Back to top](#table-of-contents)</span>*