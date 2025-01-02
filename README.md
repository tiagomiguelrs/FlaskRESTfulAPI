# Cafe API Application

## Description
This project is a web application built using the Flask framework. It provides a RESTful API for managing a database of cafes. The application allows users to add, update, delete, and retrieve information about cafes. It uses SQLAlchemy for database management and supports various HTTP methods for interacting with the data.

## Features
Add Cafes: Allows users to add new cafes to the database via a POST request.

Update Cafe Prices: Allows users to update the coffee price of a specific cafe via a PATCH request.

Delete Cafes: Allows users to delete a cafe from the database via a DELETE request.

Retrieve Cafes: Provides endpoints to retrieve all cafes, search for cafes by location, and get a random cafe.

Data Storage: Stores cafe data in a SQLite database.

JSON Responses: Returns data in JSON format for easy integration with other applications.

## How It Works
Home Page: The home page renders a simple HTML template.

Search Cafes: The /search endpoint allows users to search for cafes by location. It returns a list of cafes that match the specified location.

Get All Cafes: The /all endpoint returns a list of all cafes in the database.

Get Random Cafe: The /random endpoint returns a random cafe from the database.

Add Cafe: The /add endpoint allows users to add a new cafe to the database by sending a POST request with the cafe details.

Update Cafe Price: The /update-price/<cafe_id> endpoint allows users to update the coffee price of a specific cafe by sending a PATCH request with the new price.

Delete Cafe: The /report-closed/<cafe_id> endpoint allows users to delete a cafe from the database by sending a DELETE request with the cafe ID and an API key.
