import socket
from config import *

'''
auth_server functions:
- valid_credentials()	-->		verifies if valid credentials provided
- auth_server()			-->		generic API for handling all requests	

'''


# Returns response from auth_server API for "LOGIN" call
def valid_credentials(username, password):
	return auth_server("LOGIN", credentials)


	
# Returns response from auth_server API for any request call
def auth_server(request_type, credentials, new_password=""):
	# connect to server, send request
	connfd = socket.socket()
	connfd.connect((AUTH_SERVER,AUTH_PORT)) 
	connfd.send(request_type + "\r\n")

	# get response, handle errors
	response = connfd.recv(1024)
	if response.strip() != "VALID REQUEST":
		connfd.close()
		return response
	# to login, verify credentials
	if request_type == "LOGIN" or request_type == "REGISTER":
		connfd.send(credentials + "\r\n")
		response = connfd.recv(1024)
		connfd.close()
		return response
	# to change password, first validate credentials
	elif request_type == "CHANGE PASSWORD":
		if new_password == "":
			connfd.close()
			return "Please enter in a new password."
		connfd.send(credentials + "\r\n")
		response = connfd.recv(1024)
		# if validated, change password
		if response.strip() != "SUCCESS":
			connfd.close()
			return response
		connfd.send(new_password + "\r\n")
		response = connfd.recv(1024)
		connfd.close()
		return response
	else:
		return "Invalid request specified."
 