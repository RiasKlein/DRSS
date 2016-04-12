// header file
#include "credentials.hpp"

// STL
#include <string> 				// string, .append(), .back(), .pop_back(), .substr(), .find(), .end()

// other
#include <unistd.h>				// read(), exit()
#include <stdio.h>       		// perror(),

Credentials::Credentials(int connfd){
	std::string read_string;
	char read_buf[MAX_LINE];
	ssize_t read_bytes;

	// keep reading into string until nothing left
	while( (read_bytes = read(connfd, read_buf, MAX_LINE)) > 0){
		// cast to size_t okay, guaranteed to be > 0
		read_string.append(read_buf, (size_t)read_bytes);
		if(read_string.back() == '\n'){ break; }
	} 
	while((read_string.back() == '\r') || (read_string.back() == '\n')) { 
		read_string.pop_back();
	}
	// if critical error, perror() and exit()
	if( read_bytes == -1){
		perror("Read from connection failed.");
		exit(ERR_READ);
	}

	// pull username and password fields from string into object
	size_t delimiter_index = read_string.find(DELIMITER);
	// if delimiter not found, output error, reply error, and mark invalid object
	if( delimiter_index == std::string::npos ){
		username = INVALID_VALUE;
		password = INVALID_VALUE;
	}
	else {
		username = read_string.substr(0, delimiter_index);
		password = read_string.substr(delimiter_index + 1);
	}
}

bool Credentials::user_exists(std::map<std::string, std::string> user_map){
	return (user_map.find(username) != user_map.end());
}

bool Credentials::password_matches(std::map<std::string, std::string> user_map){
	return (user_map[username] == password);
}

bool Credentials::invalid(){
	return ((username == INVALID_VALUE) && (password == INVALID_VALUE));
}
