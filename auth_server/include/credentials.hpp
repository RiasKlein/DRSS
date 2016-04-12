#ifndef CREDENTIALS_HPP
#define CREDENTIALS_HPP

// defines
#include "auth_server.hpp"

// STL
#include <map>			//map
#include <string>		//string

class Credentials {
public:
	Credentials(int connfd);
	bool user_exists(std::map<std::string, std::string> user_map);
	bool password_matches(std::map<std::string, std::string> user_map);
	bool invalid();
private:
	std::string username;
	std::string password;
};

#endif