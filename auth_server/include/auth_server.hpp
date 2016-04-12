#ifndef AUTH_SERVER_HPP
#define AUTH_SERVER_HPP

#define INVALID_VALUE		"\t\t" 	// double delimiter
#define DELIMITER 			'\t'	// credential text delimiter
#define MAX_LINE			512		// default buffer size
#define AUTH_PORT			13370 	// port for this server
#define	LISTENQ				1024	// 2nd argument to listen()
#define ERR_SOCKET 			255
#define ERR_LISTEN 			254
#define ERR_BIND 			253
#define ERR_ACCEPT 			252
#define ERR_READ			251
#define ERR_WRITE 			250
#define ERR_WRITE_PARTIAL	249

#include 	<string>		// string

void reply(int connfd, std::string msg);
int listen_socket(int port);
void validate_credentials(int connfd);

#endif