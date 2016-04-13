// header file
#include "credentials.hpp"

// STL
#include <string> 				// string, .append(), .back(), .pop_back(), .substr(), .find(), .end()

// other
#include <unistd.h>				// read(), exit()
#include <stdio.h>       		// perror(),

Credentials::Credentials(const std::string& message){
	// pull username and password fields from string into object
	size_t delimiter_index = message.find(DELIMITER);
	// if delimiter not found, output error, reply error, and mark invalid object
	if( delimiter_index == std::string::npos ){
		username = INVALID_VALUE;
		password = INVALID_VALUE;
	}
	else {
		username = message.substr(0, delimiter_index);
		password = message.substr(delimiter_index + 1);
	}
}

bool Credentials::user_exists(std::map<std::string, std::string>& user_map){
	return (user_map.find(username) != user_map.end());
}

bool Credentials::password_matches(std::map<std::string, std::string>& user_map){
	return (user_map[username] == password);
}

bool Credentials::invalid(){
	return ((username == INVALID_VALUE) && (password == INVALID_VALUE));
}

const std::string& Credentials::get_username(){
	return username;
}

const std::string& Credentials::get_password(){
	return password;
}
