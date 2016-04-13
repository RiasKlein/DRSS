#ifndef CREDENTIALS_HPP
#define CREDENTIALS_HPP

// defines
#include "auth_server.hpp"

// STL
#include <map>			//map
#include <string>		//string

class Credentials {
public:
	Credentials(const std::string& message);
	bool user_exists(std::map<std::string, std::string>& user_map);
	bool password_matches(std::map<std::string, std::string>& user_map);
	bool invalid();
	const std::string& get_username();
	const std::string& get_password();
private:
	std::string username;
	std::string password;
};

#endif