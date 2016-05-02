Python Requirements:
NOTE: On first invocation, server creates default account with values:
	#define ADMIN_PASSWORD		"password"
	#define ADMIN_USER		"admin"
	(located in: include/auth_server.hpp)

0) Connect to server at appropriate port:
	#define AUTH_PORT		13370
	(located in: include/auth_server.hpp)

1) Precede every request with the appropriate request code:
	#define REQUEST_LOGIN		"LOGIN"
	#define REQUEST_CHANGE		"CHANGE PASSWORD"
	#define REQUEST_REGISTER	"REGISTER"
	(located in: include/auth_server.hpp)

2) Terminate every request with a newline ("\r\n")

3) Separate every set of credentials with the appropriate delimiter
	#define DELIMITER 		'\t'
	(located in: include/auth_server.hpp)



