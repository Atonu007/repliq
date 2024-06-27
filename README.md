
# Asset Management System 

This project is a Asset Management System developed using Django and Django Rest Framework.SQLite3 is used as the database. The system provides several features to users for managing their employee and asset.


## Features

User Related Features

    User Registration: Allows new users to register by providing their email, password, first name, and last name.

    User Login: Enables users to log in using their email and password.

    User Profile: Allows authenticated users to retrieve their profile information, including the total number of employees and devices associated with them.

    Update User Profile: Permits authenticated users to update their profile information.


Employee Related Features

    Create Employee: Allows authenticated users to create a new employee with details such as name and position.

    List Employees: Enables authenticated users to list all employees associated with them.

    Employee Details: Provides authenticated users with the ability to retrieve detailed information about a specific employee.

    Update Employee: Allows authenticated users to update the information of a specific employee.

    Delete Employee: Permits authenticated users to delete a specific employee.

Device Related Features 
    Add Device: Allows authenticated users to add a new device with details such as name and type.

    List Devices: Enables authenticated users to list all devices associated with them.

    Device Details: Provides authenticated users with the ability to retrieve detailed information about a specific device.

    Update Device: Allows authenticated users to update the information of a specific device.

    Delete Device: Permits authenticated users to delete a specific device.

Device Assignment Related Features

    Assign Device: Allows authenticated users to assign a device to an employee, specifying details such as checkout date and checkout note.

    Mark Device as Returned: Enables authenticated users to mark a device as returned, providing a return note.

Device Log Related Features

    List Device Logs: Allows authenticated users to list all device logs.
    
    Device Log Details: Provides users with the ability to retrieve detailed information about a specific device log.

## Technologies Used

1.Django: A high-level Python web framework for rapid development and clean, pragmatic design.

2.Django Rest Framework: A powerful and flexible toolkit for building Web APIs in Django.

3.SQLITE: Relational database system.






## Installation

Step 1 : Clone the repository
```bash
  git clone <repository_url>


```
step 2 : Install dependencies.
```bash
  pip install -r requirements.txt

```


Step 3 : Run migrations.
```bash
  python manage.py migrate


```
Step 4 : Start the development server.
```bash
  python manage.py runserver



```
    
## API Testing with Postman 
This collection of Postman requests allows users to test the endpoints of the Asset Management System API. By importing the provided asset_management_api_colllection.json file into Postman, users can quickly and efficiently evaluate the functionality and performance of the API.



Instructions   
1.Download Collection: Download the asset_management_api_colllection.json.file from the api_collection folder.

2.Import into Postman: Open Postman and import the downloaded collection by clicking on "Import" in the top left corner, then selecting the JSON file. This will load all the requests and configurations into your Postman workspace.

4.Setup Environment (Optional): If required, set up environment variables such as base URL, authentication tokens, etc., for easier testing across different environments.

5.Run Requests: Run individual requests or entire folders to test various endpoints of the Movie Management System API. Ensure to provide required parameters and payloads according to the API documentation.

6.Analyze Responses: Evaluate the responses received from the API for correctness, completeness, and adherence to specifications. Check for status codes, response bodies, and headers to ensure proper functioning.

7.Monitor Performance: Use Postman's features to monitor API performance, including response times, latency, and error rates. Analyze performance metrics to identify bottlenecks and areas for optimization.




## Acknowledgments
Special thanks to the Django and Django Rest Framework communities for their excellent documentation and support.
