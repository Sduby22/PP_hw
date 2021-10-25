create table if not exists users (
	name varchar(30) not null,
	number char(11) not null primary key check(length(number) == 11),
	balance int default 0
)
