// header file
#include "auth_server.hpp"
#include "credentials.hpp" 

// networking
#include <stdio.h>       // perror, snprintf
#include <stdlib.h>      // exit
#include <unistd.h>      // close, write, access
#include <string.h>      // strlen
#include <strings.h>     // bzero
#include <time.h>        // time, ctime
#include <sys/socket.h>  // socket, AF_INET, SOCK_STREAM,
                         // bind, listen, accept
#include <netinet/in.h>  // servaddr, INADDR_ANY, htons
#include <sys/types.h> 	 // open()
#include <sys/stat.h>	 // open()
#include <fcntl.h>		 // open()

// STL
#include <iostream>		// cerr
#include <string> 		// string
#include <map>			// map
#include <sstream> 		// stringstream
#include <fstream>		// ofstream, ifstream

extern std::map<std::string, std::string> users;

/* NETWORKING */

// listen_socket() creates and returns a listening socket at the specified port.
int listen_socket(int port){  
	struct sockaddr_in	servaddr;
	int listenfd;
    // Create the socket
	if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		close(listenfd);
		perror("Unable to create a socket");
		exit(ERR_SOCKET); 
	}

    // Set up the sockaddr_in
    memset(&servaddr, 0, sizeof(servaddr)); // zero it. 
    servaddr.sin_family      = AF_INET; // Specify the family
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); // use any network card present
    servaddr.sin_port        = htons(port);	

    // Bind that address object to our listening file descriptor
    if (bind(listenfd, (struct sockaddr *) &servaddr, sizeof(servaddr)) == -1) {		
    	close(listenfd);
    	perror("Unable to bind port");
    	exit(ERR_BIND);
    }

    // Mark socket for listening and request queue length.
    if (listen(listenfd, LISTENQ) == -1) {		
    	close(listenfd);
    	perror("Unable to listen on file descriptor.");
    	exit(ERR_LISTEN); 
    } 
    return listenfd;
}

// Gets a newline delimited message from a connected socket file descriptor.
std::string get_message(int connfd){
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
	return read_string;
}

// sends a given msg over a given connfd, first appending a C++ "endl" to it. 
void reply(int connfd, std::string msg){
	// stringstream to append endl to message
	std::stringstream reply_ss; 
	reply_ss << msg << std::endl; 
	std::cerr << std::endl << "Sending reply: " << reply_ss.str() << std::endl; // local output
	
	// convert stringstream -> string -> dynamic c string
	std::string reply_s(reply_ss.str());
	char *reply_c=new char[reply_s.size()]; 
	reply_s.copy(reply_c, reply_s.size() ); 
	// reply_ss.str() returns temporary object, .str().c_str() would be garbage

	// write message, deallocate dynamic c string, handle errors
	ssize_t written_bytes = write(connfd, reply_c, reply_s.size()); // write that char* with that size out to the network
	delete[] reply_c;
	// cast to size_t okay, guaranteed to be > 0
	if( (written_bytes > 0) && ((size_t)written_bytes < reply_s.size()) ){
		perror("Write to connection only partially succeeded.");
		exit(ERR_WRITE_PARTIAL);
	}
	else if( written_bytes < 0 ){
		perror("Write to connection totally failed.");
		exit(ERR_WRITE);
	}
}

// Gets request type from connected socket, executes appropriate operation.
void handle_request(int connfd){
	std::string message = get_message(connfd);
	if( message == REQUEST_REGISTER ){
		reply(connfd, "VALID REQUEST");
		register_user(connfd);
	}
	else if ( message == REQUEST_CHANGE ){
		reply(connfd, "VALID REQUEST");
		change_password(connfd);
	}
	else if (message == REQUEST_LOGIN ){
		reply(connfd, "VALID REQUEST");
		validate_credentials(connfd);
	}
	else {
		reply(connfd, "INVALID REQUEST");
		perror(message.c_str());
	}
}


/* FUNCTIONALITY */

// loads in-memory map of user credentials from a file
void load_existing_users(std::map<std::string, std::string>& user_map){
	if( access(STORAGE_PATH, F_OK) == -1){
		std::fstream create;
		create.open(STORAGE_PATH, std::fstream::out);
		create.close();
	}

	std::ifstream input;
	input.open(STORAGE_PATH, std::fstream::in);
	std::string first, second;
	while( 	input >> first >> second ){
		if((first != "") && (second != "")){
			user_map[first] = second; 
		}
	}
    input.close();
}

// stores in-memory map of user credentials to a file
void save_existing_users(const std::map<std::string, std::string>& user_map){
	std::ofstream output;
	output.open(STORAGE_PATH, std::ofstream::out | std::ofstream::trunc);
	std::map<std::string, std::string>::const_iterator it;
    for(it = user_map.begin(); it != user_map.end(); ++it) {
        output << it->first << "\t" << it->second << "\n";
    }
    output.close();
}

// gets credentials in a message and validates them
void validate_credentials(int connfd){
	std::string message = get_message(connfd);
	valid_credentials(connfd, message);
}

// sends appropriate response based on credential validation
bool valid_credentials(int connfd, const std::string& message){
	Credentials attempt = Credentials(message);
	if( attempt.invalid() ) {
		reply(connfd, "Invalid credentials format. Missing delimiter.");
		return false;
	}
	else if(!attempt.user_exists(users)){ 
		reply(connfd, "User does not exist."); 
		return false;
	}
	else if(!attempt.password_matches(users)){ 
		reply(connfd, "Password does not match username."); 
		return false;
	}
	else {
		reply(connfd, "SUCCESS");
	}
	return true;
}

// Changes password after first validating credentials.
void change_password(int connfd){
	// get current credentials to validate
	std::string message = get_message(connfd);
	size_t delimiter_index = message.find(DELIMITER);
	std::string username = message.substr(0, delimiter_index);
	if( valid_credentials(connfd, message) ){
		// no real verification of password requirements
		message = get_message(connfd);
		users[username] = message;
		save_existing_users(users);
		reply(connfd, "SUCCESS");
	}
}

// registers a new user if their username is not already taken.
void register_user(int connfd){
	std::string message = get_message(connfd);
	Credentials attempt = Credentials(message);
	if( attempt.invalid() ) {
		reply(connfd, "Invalid credentials format. Missing delimiter.");
	}
	else if(attempt.user_exists(users)){ 
		reply(connfd, "Username already taken."); 
	}
	else {
		users[attempt.get_username()] = attempt.get_password();
		save_existing_users(users);
		reply(connfd, "SUCCESS");
	}
}
