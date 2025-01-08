# Homeward API Service

This repository contains the Homeward API service, built using Django and Django Rest Framework. Follow the steps below to clone the repository, set up the environment, and run the tests.

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.8+
- pip (Python package manager)
- Virtualenv
- Git

## Cloning the Repository

1. Open your terminal or command prompt.
2. Clone the repository:
    ```sh
    git clone git@github.com:marcellhenrique/homeward.git
    ```
3. Navigate to the project directory:
    ```sh
    cd homeward
    ```

## Setting Up the Environment

1. Create a virtual environment:
    ```sh
    python -m venv env
    ```
2. Activate the virtual environment:
    - On macOS/Linux:
        ```sh
        source env/bin/activate
        ```
    - On Windows:
        ```sh
        .\env\Scripts\activate
        ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Tests

1. Ensure the virtual environment is activated.
2. Run the tests using the Django test runner:
    ```sh
    python manage.py test
    ```
3. All tests should pass if the setup was successful.


# Design Pattern Documentation

## Design Pattern: Service Pattern

In this project, the **Service Pattern** is utilized to manage the application's business logic. The pattern is designed to decouple complex business logic from views and models, making the code more modular, testable, and maintainable.

### Why Service Pattern?
The **Service Pattern** is appropriate for this project due to the following reasons:
1. **Separation of Concerns**: It isolates business logic from Django views and models, making it easier to manage, test, and modify.
2. **Single Responsibility**: Each service has a single responsibility and does not need to manage how the data is presented or stored.
3. **Reusability**: Services can be reused across different views and projects, promoting code reuse and reducing duplication.
4. **Testability**: By isolating the business logic into services, the code is easier to unit test without being tightly coupled to other layers like the database or web framework.

### Structure of the Project

In the Service Pattern, the logic of the application is split between **views**, **models**, and **services**. The service layer handles the core business logic, including interactions with external APIs and other services.

#### File Structure
The service pattern is implemented with the following structure:

# AgentService Documentation

The `AgentService` is responsible for managing the business logic related to real estate agents. It provides methods to fetch agent details associated with a specific customer and to retrieve a list of agents based on their location.

## Methods

### 1. `get_agent_details(customer_id)`
This method retrieves the details of an agent associated with a given customer ID.

#### Parameters:
- `customer_id` (int): The ID of the customer whose associated agent information needs to be fetched.

#### Returns:
- A dictionary containing the customer and agent details if found, or `None` if the customer or agent is not found.

#### Example Response:
```json
{
    "customer": {
        "id": 1,
    "name": "Cynthia Hart",
    "email": "c.hart@sample.com",
    "phone": "111-123-1234",
    "current_address": "908 Test St. Austin, TX 78749"
  },
  "agent": {
      "name": "Dana Agent",
    "contact_info": "dana.agent@example.com",
    "brokerage_name": "Super Realty",
    "location": "Austin, TX"
  }
}
```


# Agent Model Documentation

The `Agent` model represents a real estate agent in the system. It stores essential details about the agent, such as their name, contact information, brokerage name, and location.

## Fields

### 1. `name`
- **Type**: `CharField`
- **Max Length**: 255 characters
- **Description**: The full name of the real estate agent.
- **Example**: `"Dana Agent"`

### 2. `contact_info`
- **Type**: `CharField`
- **Max Length**: 255 characters
- **Nullable**: Yes
- **Blank**: Yes
- **Description**: The contact information of the real estate agent (e.g., phone number, email). This field is optional.
- **Example**: `"dana.agent@example.com"`

### 3. `brokerage_name`
- **Type**: `CharField`
- **Max Length**: 255 characters
- **Nullable**: Yes
- **Blank**: Yes
- **Description**: The name of the brokerage that the agent is associated with. This field is optional.
- **Example**: `"Super Realty"`

### 4. `location`
- **Type**: `CharField`
- **Max Length**: 255 characters
- **Nullable**: Yes
- **Blank**: Yes
- **Description**: The location (city, state) where the agent operates. This field is optional.
- **Example**: `"Austin, TX"`

## Methods

### 1. `__str__(self)`
This method defines how the `Agent` object will be represented as a string. It returns a string combining the agent's name and brokerage name.


# Views Documentation

This section provides the documentation for the views in the project. These views interact with the `AgentService` to provide data related to customers and agents.

## 1. CustomerAgentView

### Endpoint:
- **URL**: `/customer-agent/<customer_id>/`
- **Method**: `GET`
- **Description**: Fetches the details of the real estate agent associated with a specific customer, based on the `customer_id`.
- **Parameters**:
  - `customer_id`: The ID of the customer. This is a required URL parameter.

### Response:
- **200 OK**: If the customer and agent are found, returns a JSON object with the customer and agent details.
- **404 Not Found**: If either the customer or agent is not found, returns a "Customer or agent not found." error message.

#### Example Request:
```http
GET /customer-agent/1/
```

## 2. AgentsByLocationView

### Endpoint:
- **URL**: `/agents/`
- **Method**: `GET`
- **Description**: Fetches a list of real estate agents filtered by location (city or state). This view expects a query parameter to specify the location.
- **Parameters**:
  - **queryparams**:
    - `location`: The location (city or state) to filter the agents by. This is a required query parameter.

### Response:
- **200 OK**: Returns a list of agents matching the provided location.
- **400 Bad Request**: If the location query parameter is not provided, returns an error message indicating that the location parameter is required.

#### Example Request:
```http
GET /agents-by-location/?location=Austin
```



