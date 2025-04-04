## Nutrition domain (microservice)
Rendering the nutrition screen, which is the main screen on the customer side, 
the frontend should request these endpoints to work with nutrition domain.

### Table of Contents
- [API](#api)
- [Getting Daily Diet Endpoint Flow](#getting-daily-diet-endpoint-flow)
- [Data Storage Structure](#data-storage-structure)

### API
* ```GET nutrition/diets/${specific_day}```:
    * endpoint_info: to get the meal fact day for the client by date
    * example_request_uri: nutrition/diets/2024-07-11
    * response_json: ./extras/get_daily_diet_for_customer_by_date_out.json

* ```POST nutrition/diets```:
    * endpoint_info: to put product into the customer meal inside diet day fact
    * example_request_uri: nutrition/diets
    * request_json: ./extras/post_add_product_to_diet_in.json
    * response_json: ./extras/post_add_product_to_diet_out.json

/* not implemented in first feature iteration */ 
* ```GET nutrition/products/history```:
    * endpoint_info: to list last consumed customer products
    * example_request_uri: nutrition/products/history
    * response_json: ./extras/get_products_lookup_out.json

/* not implemented in first feature iteration */ 
* ```GET nutrition/products/lookup/${query_text}```:
    * endpoint_info: to get products with their info by some relative product word
    * example_request_uri1: nutrition/products/lookup/молоко
    * example_request_uri2: nutrition/products/lookup/молоко-простоквашино
    * example_request_uri3: nutrition/products/lookup/простоквашино-молоко-2%
    * response_json: ./extras/get_products_lookup_out.json

* ```POST nutrition/products```:
    * endpoint_info: to put product to AsCoach database
    * example_request_uri: nutrition/products
    * request_json: ./extras/post_create_product.json
    * response_json: ./extras/get_receive_product_out.json

* ```GET nutrition/products/${product_id}```:
    * endpoint_info: to get product data by their id for product detail card
    * example_request_uri: nutrition/products/d7182bb0-9a03-4e48-86ca-8b20d4a9bcba
    * response_json: ./extras/get_receive_product_out.json

/* not implemented in first feature iteration */ 
* ```DELETE nutrition/products/${product_id}```:
    * endpoint_info: to delete product by product id, user can delete only their products
    * example_request_uri: nutrition/products/d7182bb0-9a03-4e48-86ca-8b20d4a9bcba
    * response_json: {"id": "d7182bb0-9a03-4e48-86ca-8b20d4a9bcba"}

/* not implemented in first feature iteration */ 
* ```PUT nutrition/products/${product_id}```:
    * endpoint_info: to update product data by product id, user can modify only their products
    * example_request_uri: nutrition/products/d7182bb0-9a03-4e48-86ca-8b20d4a9bcba
    * request_json: ./extras/post_create_product.json
    * response_json: ./extras/get_receive_product.json

### Getting Daily Diet Endpoint Flow
![get_daily_diet_flow_diagram](4_get_daily_diet_flow_diagram.drawio.svg)

### Data Storage Structure
Command Query Responsibility Segregation (CQRS) pattern, separating the write operations (commands) 
from the read operations (queries).

* AWS DynamoDB: Used for storing product data and handling insert/update operations.
* AWS OpenSearch Service: Used for indexing and full-text search of product data.
* AWS Lambda: Used to synchronize data between DynamoDB and OpenSearch.

