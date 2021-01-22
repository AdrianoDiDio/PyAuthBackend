# PyAuthBackend
A simple implementation of the OAuth2.0 protocol to handle user sessions.  

A demo is available at [adrianodd.pythonanywhere.com](https:://adrianodd.pythonanywhere.com/)  

Table of contents
=================

   * [PyAuthBackend](#PyAuthBackend)
   * [Table of contents](#table-of-contents)
   * [Requirements](#requirements)
   * [Installation](#installation)
   * [Architecture](#architecture)
      * [Endpoints](#endpoints)

Requirements
============
This guide assumes that a Linux distribution is used, commands for Windows are similar but requires some steps to get the required files.
In order to setup this package we need to install python3,pip,mysql using a simple bash command (Note that sudo may be required in order to install it):
```bash
$ apt-install python3,pip,mysql-server
```
After installing the required packages the installation can proceed.

Installation
============
After unzipping the package, we need to create a new virtual enviroment.
Virtual Enviroment let us create a separate enviroment from the system to install local dependencies required by this package.
In order to create a new enviroment, open up the shell in the folder where the project was unzipped and run:
```bash
$ python3 -m venv env
```
This will create an hidden folder called .env that will contains all the required files to run the project.
Next, we need to activate it by running:
```bash
$ source .env/bin/activate
```
Now, we need to download all the required files by running:
```bash
$ pip install -r requirements.txt
```
After pip is done installing, we need to setup our database using django utilities.  
Before running the commands, modify the section DATABASES inside the file PyAuthBackend/settings.py by inserting the  
MySQL Username,Password,DBName and Host.  
If any of the parameters is wrong or missing DJango will display an error asking to fix it.  
Next, we need to prepare our query needed to create the Database structure by running the command:
```bash
$ python manage.py makemigrations
```
and then:
```bash
$ python manage.py migrate
```
If all the commands completed without error, we can now start the local development server by running:
```bash
$ python manage.py runserver <OptionalIPAddress:Port>
```
If IP address is not specified, server will be available at localhost:8000, API can be reached at localhost:8000/api.
By opening localhost:8000 in a browser user should see the API documentation made using swagger.  

Finally, after checking that everything is working, we can create a SuperUser that will manage the User's registration  
by running the command:  

```bash
$ python manage.py createsuperuser
```
This user can now login at localhost:8000/admin (or a custom IP address) to manage all the registered users.  
When deploying to a real server we also need to set-up a cron job that blacklists all the expired tokens by running  
the following command in a shell:
```bash
$ source /path/to/project/.env/bin/activate && python /path/to/project/PyAuthBackend/manage.py flushexpiredtokens
```
API can be tested using built-in ui available at localhost:8000, however due to the model that the API uses (OAuth2.0)  
not being supported by OpenAPI 2.0, it is recommended to use an external tool like Postman that makes   
easy adding the Bearer token to each protected request.  

Architecture
============
  
Database
--------
In order to store user information PyAuthBackend uses the default Django user model that  
contains several fields like username,password,email etc...   
This model has been extended by declaring a new field called biometricToken, used to login without
specifying a password.

```
CREATE TABLE `AuthRESTAPI_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `biometricToken` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 |
```
SimpleJWT Tokens
----------------
This library simplify the implementation of the OAuth 2.0 protocol  
by generating and managing the JWT tokens.  
There are only two tokens generated by the backend: Refresh and Access token.  

Access token is a short-lived JWT token that is used as a Bearer token inside each request's authorization header  
while the Refresh token, which has a longer lifespan, is used to let the user refresh the expired access token.  

Tokens lifespan can be set in the settings.py file, and the main paramters that have been changed were:  

```
ACCESS_TOKEN_LIFETIME => Set to 5 minutes
REFRESH_TOKEN_LIFETIME => Set to 6 days
```  

This makes sure that the access token gets renewed every 5 minutes and can be refreshed using  
the endpoint [Refresh](#refresh-tokens).  
When the refresh token expires, users are forced to login again in order to generate a new pair.  
If the user logout then the refresh token is blacklisted and the access token won't be renewed.  

Inside each JWT token there is only one information about the user which is the Id field  
needed to personalize all the protected endpoints to show information only for the current user.  

SimpleJWT contains an app that can be installed that adds a command to the django manage interface  
that flushes all the expired tokens as seen in the [installation process](#installation) when setting up a new cron job.  

Endpoints
---------
All the endpoints are available at <serverIporAddress:Port>/api/<EndpointName>.  

Login
-----
This endpoint,available at <serverIporAddress:Port>/api/login, let the user authenticate in order to  
obtain the access and refresh token.  
It is implemented using SimpleJWT library that exposes a POST only endpoint taking the username and password  
and returning a TokenPair containing the Access and Refresh Token.  
It uses DJango builtin authentication schema to verify that the user exists and the password is valid.  
It requires two parameters that are passed as JSON object inside the POST body request:  
```javascript
{
	“username": “foo",
	“password": “foobarpassword"
}
```
If the Username/Password are valid it returns the token pair as seen below:  
```javascript
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMDM4MjA0Nyw
              ianRpIjoiYmIzNWNhYmQ0NjQxNGY5ZGE1ZjJiM2Q0MTIxNGZhYzUiLCJVc2VySWQiOjF9.bqGGPM70jkF6b3KfoFqciwDrUOCcYwOk1_Njl1fSG",
	"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwMjk1OTQ3LCJqdGkiO	
             iJhYWNmZjExMmM0MzE0ZTJmYTU4OTA0YzlkMzQ2MmMzMSIsIlVzZXJJZCI6MX0.7C9k6ud1xcSqoYUcN70OqY5X-LVXrMqLJcoiiDRkZ50"
}
```
Otherwise a response containing the error is returned:  
```javascript
{
	"detail": "Invalid Username/Password"
}
```
Biometric Login
---------------
This endpoint, available at <serverIporAddress:Port>/api/biometricLogin, let the user authenticate  
by using a biometricToken and the userId.  
It is implemented by adding a new authentication method to DJango and implementing our own TokenObtainPair.    
In particular, every time a request is made to this endpoint, a query to the database is done to  
check if the userId and biometricToken matches the one stored inside the database.  
It requires two parameters that are passed as JSON object inside the POST body request,  
and the biometricToken must be encoded in Base64 as seen below:    
```javascript
{
	“userId": 1,
	“biometricToken": “YmlvbWV0cmljVG9rZW4"
}
```
If the userId/biometricToken are valid it returns the token pair as seen below:  
```javascript
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMDM4MjA0Nyw
              ianRpIjoiYmIzNWNhYmQ0NjQxNGY5ZGE1ZjJiM2Q0MTIxNGZhYzUiLCJVc2VySWQiOjF9.bqGGPM70jkF6b3KfoFqciwDrUOCcYwOk1_Njl1fSG",
	"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwMjk1OTQ3LCJqdGkiO	
             iJhYWNmZjExMmM0MzE0ZTJmYTU4OTA0YzlkMzQ2MmMzMSIsIlVzZXJJZCI6MX0.7C9k6ud1xcSqoYUcN70OqY5X-LVXrMqLJcoiiDRkZ50"
}
```
Otherwise a response containing the error is returned:  
```javascript
{
	"detail": "Invalid Biometric Token"
}
```
Refresh
-------
This endpoint, available at <serverIporAddress:Port>/api/login/refresh, let the user refresh his access token.  
It takes one parameter, the refresh token and doesn't require the user to be authenticated since the access token  
is no longer valid.  
The refresh token is passed in the body of the POST request as a JSON string as seen below:  
```javascript
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.	eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMDM4MjA0Nyw	
              ianRpIjoiYmIzNWNhYmQ0NjQxNGY5ZGE1ZjJiM2Q0MTIxNGZhYzUiLCJVc2VySWQiOjF9.bqGGPM70jkF6b3KfoFqciwDrUOCcYwOk1_Njl1fSG",
}
```
Returns a new access token if the Refresh token was valid:  
```javascript
{
	“access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMDM4MjA0Nyw
             ianRpIjoiYmIzNWNhYmQ0NjQxNGY5ZGE1ZjJiM2Q0MTIxNGZhYzUiLCJVc2VySWQiOjF9.bqGGPM70jkF6b3KfoFqciwDrUOCcYwOk1_Njl1fSG",
}
```
Or 401 (unauthorized) if refresh token is not valid or blacklisted.  

Registration
------------
This endpoint is available at <serverIporAddress:Port>/api/registration and requires three parameters   
that are passed in the body of the POST request as a JSON String as seen below:   
```javascript
{
	“username": “foo",
	“email":  "foo@bar.com",
	“password": “foobarpassword"
}
```
The server will then verify if all the fields are present and valid and will return a JSON response containing   
the details of the new user if valid:   
```javascript
{
  “id": 1,
	“username": “foo",
	“email":  "foo@bar.com",
}
```
Or a response containing the error messages:   
```javascript
{
	“email":  [
		“Enter a valid email address.”
	],
	“password”: [
		“Ensure this field has at least 8 characters”
	]
}
```
User Info
---------
This endpoint, available at <serverIporAddress:Port>/api/userDetails, let the user view his own data by accepting a GET request.  
Since server needs to be sure that only authenticated user can see their own data, this endpoint requires  
an authorization header called Bearer Token containing the Access Token that can be obtained after LogIn.  
If the user is authorized then the server will return the following JSON object:   
```javascript
{
	“id": 1,
	“username":  foobar,
	“email”: “foo@bar.com"
}
```
If user is not authenticated or the access token is no longer valid then a 401 (unauthorized) response is returned.  

Get Biometric Challenge
-----------------------
This endpoint, available at <serverIporAddress:Port>/api/getBiometricChallenge, let the user start the enrollment process by generating  
an UUID4 and sending it back to the client as a JSON object.  
It requires the user to be authenticated, by setting the access token in the authorization header, and it doesn't  
requires any additional parameters.  
Response can be either the biometricChallenge encoded using base64:
```javascript
  "biometricChallenge": "MDZiMmVmYWYtYTc1Ni00OTBkLTk1NmQtMTA1YjA3OWI2OWUx"
```
or 401 (unauthorized) if the access token was not valid or missing.  

Generate Biometric Token
------------------------
This endpoint, available at <serverIporAddress:Port>/api/generateBiometricToken, let the user complete  
the enrollment process by generating a new biometric token.  
It requires the user to be authenticated, by setting the access token in the authorization header, and takes  
four parameters: Public Key (encoded using base64),Original Challenge (encoded using base64), Signed Challenge (encoded using base64) and a  
nonce (a random number added to the challenge).
These parameters are passed in the POST request body as a JSON string:  
```javascript
  "signedChallenge" : "c2lnbmVkQ2hhbGxlbmdl",
  "originalChallenge" : "b3JpZ2luYWxDaGFsbGVuZ2U=",
  "nonce" : 10201,
  "publicKey" : "cHVibGljS2V5"
```  
The server uses the PyCrypto library to verify if the challenge was signed correctly, by using the public key,  and  
if the signature is valid it generates a random string of 32 bytes using the python's library secrets that it is then encrypted    
with PyCrypto using the public key,encoded using base64,stored inside the database and returned to the user as a JSON object:
```
  "biometricToken" : "ZW5jcnlwdGVkQmlvbWV0cmljVG9rZW4="
```
If the signature was not valid then 400 (Bad request) is returned.  

Logout
------
This endpoint, available at api/logout, handles user's logout.  
Since this REST API uses Oauth2.0 and it is stateless, the logout flow simply blacklist the refresh token  
forcing the user to login again after the access token is expired.  
It takes only one parameter, the refresh token, but in order to call it, the user must be logged in and thus  
it must pass the access token inside the authorization header of the request.  
Sample request can be seen below:  
```javascript
{
	“refresh": 	“eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsIm
               V4cCI6MTYxMDQ2NDAxNiwianRpIjoiZDFiODE2Y2JiOTUzNDkxMDhhOWRkOW	
               MzMmM4YjdhYWIiLCJVc2VySWQiOjF9.P3cpclE_BlNue7tWoZ7Ayr6lwirsFMzBrE4TgNMyhuk",
}
```
If the request was successful then the server will return 205 ( Reset Content ) if the refresh token was valid,   
401 if user was not authorized or 400 (Bad request) if refresh token was invalid or blacklisted.  

