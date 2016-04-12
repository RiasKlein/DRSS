-- drop database drss;
-- drop table Donations;
create database drss;
use drss;
create table Donations (
	donor		varchar(256),
	amt_range	varchar(256),
	nonprofit	varchar(256),
	year_given	int,
	primary key (donor, nonprofit, year_given)
);

insert into Donations (donor, amt_range, nonprofit, year_given) values ("a", "5 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("b", "5 and up", "AMERICAN NATIONAL RED CROSS", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("c", "5 and up", "UNITED NEGRO COLLEGE FUND", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("d", "5 and up", "SMITHSONIAN INSTITUTION OFFICE OF THE COMPTROLLER", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("e", "10 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("f", "10 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("g", "10 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("h", "10 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("i", "15 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("j", "15 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("k", "15 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("l", "15 and up", "National Geographic", 1994);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("a", "5 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("b", "5 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("c", "5 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("d", "5 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("e", "10 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("f", "10 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("g", "10 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("h", "10 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("i", "15 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("j", "15 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("k", "15 and up", "National Geographic", 2004);
insert into Donations (donor, amt_range, nonprofit, year_given) values ("l", "15 and up", "National Geographic", 2004);

