--Select Master DB:
USE master;

--create User and Passord for Database Server
CREATE LOGIN jazztrio
with password = 'YaLikeJazz!?123'

--Select your DB:
USE JazzTrio;

--Tie Account to Particular database:
CREATE USER rgamilo
FROM LOGIN rgamilo
WITH DEFAULT_SCHEMA=dbo;

create user denniskelly
from login denniskelly
with default_schema=dbo;

create user rstewart27
from login rstewart27
with default_schema=dbo;

create user jazztrio
from login jazztrio
with default_schema=dbo;

-- add user to database role(s) (i.e. db_owner)
ALTER ROLE db_owner ADD MEMBER rgamilo;
alter role db_owner add member denniskelly;
alter role db_owner add member rstewart27;
alter role db_owner add member jazztrio