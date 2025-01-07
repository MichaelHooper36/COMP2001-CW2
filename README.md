# COMP2001-CW2

## Project description:
The "TrailService" is a micro-service that has the ability to perform the CRUD operations on any data relating to trails and allows a user to view any trails with a limitation, depending on their role and ownership.

## Installation instructions:
To run the code, follow the instructions based on whether you are using docker or python.
Make sure you are connected to the University of Plymouth using either the campus Wi-Fi or the university VPN.

### __Using Docker__:
 - Install Docker
 - Start Docker
 - In the terminal:
   - docker pull mhooper36/comp2001_image
   - docker run -p 8000:8000 mhooper36/comp2001_image
 - Access the API:
   - Open your web browser and navigate to localhost:8000 and select the link on the screen
   - Or use Postman, Curl, or similar tools to interact with the endpoints

### __Using Python:__
 - Install Python
 - Run app.py
 - Open your web browser and navigate to localhost:8000 and select the link on the screen
   - Or use Postman, Curl, or similar tools to interact with the endpoints


The following accounts have been used in the application:
1. Grace Hopper
   - email: grace@plymouth.ac.uk
   - password: ISAD123!
2. Tim Berners-Lee
   - email: tim@plymouth.ac.uk
   - password: COMP2001!
3. Ada Lovelace
   - email: ada@plymouth.ac.uk
   - password: insecurePassword
