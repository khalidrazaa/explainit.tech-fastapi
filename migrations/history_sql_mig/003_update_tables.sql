
CREATE TABLE articles (
	id SERIAL NOT NULL, 
	title VARCHAR NOT NULL, 
	seo_title VARCHAR, 
	slug VARCHAR NOT NULL, 
	category VARCHAR, 
	subcategory VARCHAR, 
	tags VARCHAR[], 
	status VARCHAR, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	updated_at TIMESTAMP WITH TIME ZONE, 
	published_at TIMESTAMP WITH TIME ZONE, 
	author_id INTEGER, 
	content TEXT, 
	excerpt TEXT, 
	reading_time INTEGER, 
	keywords VARCHAR[], 
	featured_image_url VARCHAR, 
	image_alt_text VARCHAR, 
	language VARCHAR, 
	canonical_url VARCHAR, 
	open_graph_title VARCHAR, 
	open_graph_description VARCHAR, 
	open_graph_image VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE keywords (
	id SERIAL NOT NULL, 
	keyword VARCHAR NOT NULL, 
	source VARCHAR, 
	monthly_searches INTEGER, 
	cpc FLOAT, 
	seo_difficulty FLOAT, 
	suggestions JSON, 
	processed BOOLEAN, 
	article_id INTEGER, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id)
)

;