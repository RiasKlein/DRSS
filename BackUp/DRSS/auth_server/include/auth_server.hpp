#ifndef AUTH_SERVER_HPP
#define AUTH_SERVER_HPP

#define ADMIN_PASSWORD		"password" // default password on first run
#define ADMIN_USER			"admin" // default account on first run
#define FILE_MASK			0666	// default permissions, rw-rw-rw-
#define	STORAGE_PATH		"./storage/map.dump"
#define REQUEST_LOGIN		"LOGIN"
#define REQUEST_CHANGE		"CHANGE PASSWORD"
#define REQUEST_REGISTER	"REGISTER"
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
#define ERR_OPEN			248
#define ERR_FOPEN			247


#include 	<string>		// string
#include	<map>			// map

// networking
int listen_socket(int port);
std::string get_message(int connfd);
void reply(int connfd, std::string msg);
void handle_request(int connfd);

// functionality
void load_existing_users(std::map<std::string, std::string>& user_map);
void save_existing_users(const std::map<std::string, std::string>& user_map);
void validate_credentials(int connfd);
bool valid_credentials(int connfd, const std::string& message);
void change_password(int connfd);
void register_user(int connfd);

#endif