#include "auth_server.hpp"		// validate_credentials(), listen_socket()
#include <stdlib.h>				// atoi(), exit()
#include <sys/types.h>			// struct sockaddr, socklen_t
#include <sys/socket.h>			// accept()
#include <stdio.h>       		// perror(), fprintf()
#include <unistd.h>				// close()
#include <map>					// map
#include <string>				// string

// Global map of usernames and passwords, backed up on every modification.
std::map<std::string, std::string> users;

int main(int argc, char **argv){
	int listenfd, connfd;
	int auth_port = (argc == 2) ? atoi(argv[1]) : AUTH_PORT;
	listenfd = listen_socket(auth_port);

	// if server is being brought back up, reload prior user credentials
	load_existing_users(users);
	// if first invocation ever, have an admin account so can logon
	if(users.empty()) { 
		users[ADMIN_USER] = ADMIN_PASSWORD;
		save_existing_users(users);
	}
	
	for ( ; ; ) {
        // Block until someone connects.
		fprintf(stderr, "Ready to connect.\n");
		if ((connfd = accept(listenfd, (struct sockaddr *) NULL, NULL)) == -1) {
			perror("Accept failed.");
			exit(ERR_ACCEPT);
		}
		fprintf(stderr, "Connected\n");

		// determine type of request and handle accordingly
		handle_request(connfd);

        // Close connection. Loop forever.
		close(connfd);
	}
}

