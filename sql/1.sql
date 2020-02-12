create user ttlAdmin with password 'oracle9i';
alter role ttlAdmin set client_encoding to 'utf8';
alter role ttlAdmin set default_transaction_isolation to 'read committed';
alter role ttlAdmin set timezone to 'UTC+5';
grant all privileges on database "Merchant" to ttlAdmin;