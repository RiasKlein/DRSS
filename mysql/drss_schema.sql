-- drop database drss;
-- drop table Donations;
create database drss;
use drss;
create table Donations (
	donor		varchar(256),
	amt_range	varchar(256),
	nonprofit	varchar(256),
	year_given	int,
	primary key (donor, amt_range, nonprofit, year_given)
);
