
alter table users add password varchar(255);

update users
set password=display_name;




/*display_name VARCHAR(255) NOT NULL,there the where not exists(display_name) fails   i think some other reason   as not exists is not an aggregate function works on relations not the 
/* display_name and DisplayNmae are the same dont confuse on the viva