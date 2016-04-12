// header file
#include "auth_server.hpp"
#include "credentials.hpp" 

// networking
#include <stdio.h>       // perror, snprintf
#include <stdlib.h>      // exit
#include <unistd.h>      // close, write
#include <string.h>      // strlen
#include <strings.h>     // bzero
#include <time.h>        // time, ctime
#include <sys/socket.h>  // socket, AF_INET, SOCK_STREAM,
                         // bind, listen, accept
#include <netinet/in.h>  // servaddr, INADDR_ANY, htons

// STL
#include <iostream>		// cerr
#include <string> 		// string
#include <map>			// map
#include <sstream> 		// stringstream

extern std::map<std::string, std::string> users;

// sends a given msg over a given connfd, first appending a C++ "endl" to it. 
// exit()s and perror()s on any critical error.
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

// listen_socket() creates and returns a listening socket at the specified port.
// exit()s and perror()s on any critical error.
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

// reads credentials over network and sends appropriate authentication reply.
void validate_credentials(int connfd){
	Credentials attempt = Credentials(connfd);
	if( attempt.invalid() ) {
		reply(connfd, "Invalid credentials format. Missing delimiter.");
	}
	else if(!attempt.user_exists(users)){ 
		reply(connfd, "User does not exist."); 
	}
	else if(!attempt.password_matches(users)){ 
		reply(connfd, "Password does not match username."); 
	}
	else {
		reply(connfd, "Success.");
	}
}
