# ncsportal
Portal for Name Certifying Service

Prerequisites: `python`, `oscrypto`, `certbuilder`, `flask` , `mysql`

Get the latest version of source using git.

``````
git clone https://github.com/ramtejatadishetti/ncsportal.git

cd ncsportal

``````

Create certificate for root_ca, directories for string certificates, private keys:

``````
python certs.py

./startup_script.sh

``````

Build schema using mysql:

Login into mysql server using cmdline.

Create a database with name ncs.

Create a table with name name_data with following fields.

``````

CREATE TABLE name_data(
    user_id BIGINT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(50),
    mobile VARCHAR(15),
    address vARCHAR(150),
    identifier VARCHAR(64) NOT NULL,
    gns_provider VARCHAR(130) NOT NULL,
    certificate_file_name VARCHAR(150) NOT NULL,
    verified TINYINT,
    time_stamp TIMESTAMP,
    PRIMARY KEY ( user_id ),
    UNIQUE KEY (identifier)
);
``````

Update mysql username, password, port by changing MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD, MYSQL_DATABASE_PORT in final_app.py

Starting the server:

``````
sudo python final_app.py

``````
