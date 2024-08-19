# User-Registration-API
A REST API service for user registration and authentication using Flask and JWT tokens. Includes endpoints for user registration, login, token verification, revocation, and renewal.

## Description

A REST API service built using Flask for user registration and authentication. The API supports JWT tokens for secure access and includes endpoints for user registration, login, token management, and private resource access.

## Features

- **User Registration**: Register new users with name, email, and password.
- **Login**: Authenticate users and generate JWT tokens.
- **Private Resource Access**: Access restricted resources with valid JWT tokens.
- **Token Management**: Revoke and renew JWT tokens.

## Installation

To quickly set up and run the API service using Docker, follow these steps:

### Prerequisites

1. **Docker**: Ensure you have Docker installed on your machine. If not, download and install it from [Docker's official website](https://www.docker.com/products/docker-desktop).

### Running the API Service

1. **Pull the Docker Image**:
   
   Pull the Docker image from Docker Hub using the following command:

   ```sh
   docker pull tushartkm/user-registration-api

2. **Run the Docker Container**:
   
   Start a new container from the Docker image using the following command:

   ```sh
   docker run -p 5000:5000 tushartkm/user-registration-api

## Testing the API Endpoints using CURL commands

1. **Home Endpoint**
   
   ```sh
   curl -X GET http://127.0.0.1:5000/

2. **Register a New User**
   
   ```sh
   curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d "{\"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"password\": \"securepassword\"}"

3. **Login and Get JWT Token**
   
   ```sh
   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"email\": \"john.doe@example.com\", \"password\": \"securepassword\"}"

4. **Access Private Resource**
   
   ```sh
   curl -X POST http://127.0.0.1:5000/private-resource -H "Content-Type: application/json" -d "{\"email\": \"john.doe@example.com\", \"token\": \"<your_jwt_token>\"}"

5. **Revoke User Token**
   
   ```sh
   curl -X POST http://127.0.0.1:5000/revoke-token -H "Content-Type: application/json" -d "{\"email\": \"john.doe@example.com\"}"

6. **Renew Token**
   
   ```sh
   curl -X POST http://127.0.0.1:5000/renew-token -H "Content-Type: application/json" -d "{\"email\": \"john.doe@example.com\"}"

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or feedback, please contact tush.tkm@gmail.com
