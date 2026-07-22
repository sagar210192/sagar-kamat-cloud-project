# E-Commerce Flask Application


## Project Overview 

This project is a basic ecommerce application. It is implemented using Python and Flask. Application was developed using the learnings from different modules listed in the course. The app contains different features such as user authentication, order management, basic monitoring, health check, product catalog. 


## Application Features

### User Authentication

Application supports basic account functionality.
Users can:
* Register with an email address and password
* Log in / log out


### Product Management

Application stores product information in a database.
Each product contains:
* Name
* Description
* Price
* Stock quantity
* Creation date
Application provides CRUD operation support for products.


### Product Catalog

Products can be listed using '/products' endpoint
Each product card shows:
* Product name
* Description
* Price
* Available stock
* Add to Cart button
User friendly page to show product details to the user


### Shopping Cart

Application includes a simple shopping cart feature similar to e-commmerce websites like Amazon
Users can:
* Add products to the cart
* See selected products
* Remove products
* Review total cost
Cart stores product IDs temporarily in the user session.


### Order Management

Products added to cart can be ordered by clicking the place an order button.
Each order stores:
* Order ID
* User ID
* Total amount
* Order status
* Creation date
Cart becomes empty once the order is placed


### Basic Monitoring

Application provides basic monitoring feature.
'/health' endpoint shows the status/health of the applciation
Example response:
json
{
  "application": "ecommerce",
  "status": "healthy"
}


Similarly '/metrics' endpoint displays the number of requests handled by the application. It resets when the app is restarted.

## Different Endpoints
* "health": "GET /health",
* "login": "POST /auth/login",
* "logout": "POST /auth/logout",
* "metrics": "GET /metrics",
* "orders": "GET /orders",
* "product_catalog": "GET /products",
* "products_api": "GET /api/products",
* "register": "POST /auth/register",
* "shopping_cart": "GET /cart"
 

Once the app is started, different endpoints can be very easily tested through the Codio browser and with `curl`.

We have added tests covering functionality such as:
* User registration
* Duplicate registration
* Login
* Product listing
* Authentication requirements
* Product creation


## Challenges Encountered

### GitHub Auth

Github has stopped accepting account credentials (username/password) for git operations over https. Github personal access token was generated to push the changes to git.


### Docker in Codio
Codio does not support Docker. Flask application was run on local computer to make it run in docker.

### Database Configuration
Used SQLitefor the main Flask application because it required less setup in Codio than PostgreSQL.

### MySQL Authentication
For the MySQL lab, the root account was not accessible through code. A separate database user was created to use in the application.

## Future Enhancements
This application developed is basic and can be enhanced in the future

Future enhancements:
* HTTPS
* Rate limit
* Stronger password support
* Admin only product management
* Validations for CRUD


## GitHub Repository

https://github.com/sagar210192/sagar-kamat-cloud-project
