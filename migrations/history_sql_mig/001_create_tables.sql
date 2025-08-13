
CREATE TABLE admin_users (
	id VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	phone VARCHAR NOT NULL, 
	full_name VARCHAR NOT NULL, 
	gender VARCHAR NOT NULL, 
	dob DATE NOT NULL, 
	is_active BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (phone)
)

;


CREATE TABLE email_otps (
	email VARCHAR NOT NULL, 
	otp VARCHAR NOT NULL, 
	expires_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	PRIMARY KEY (email)
)

;


CREATE TABLE tokens (
	id SERIAL NOT NULL, 
	access_token VARCHAR NOT NULL, 
	token_type VARCHAR, 
	expires_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
)

;

