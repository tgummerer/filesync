CREATE TABLE usertable
(
	userid serial NOT NULL,
	email text NOT NULL,
	"password" text NOT NULL,
	CONSTRAINT id PRIMARY KEY (userid),
	CONSTRAINT email UNIQUE (email)
)
WITH (
	OIDS=FALSE
);

CREATE TABLE client
(
	clientid serial NOT NULL,
	userid integer,
	CONSTRAINT primarykey PRIMARY KEY (clientid),
	CONSTRAINT userid FOREIGN KEY (userid)
	REFERENCES usertable (userid) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
	OIDS=FALSE
);

CREATE TABLE filetable
(
	fileid serial NOT NULL,
	userid integer NOT NULL,
	path text NOT NULL,
	lastchange timestamp without time zone DEFAULT now(),
	CONSTRAINT fileid PRIMARY KEY (fileid),
	CONSTRAINT userid FOREIGN KEY (userid)
	REFERENCES usertable (userid) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT path UNIQUE (path)
)
WITH (
	OIDS=FALSE
);

CREATE TABLE hasnewest
(
	clientid integer NOT NULL,
	fileid integer NOT NULL,
	CONSTRAINT hasnewest_pkey PRIMARY KEY (clientid, fileid),
	CONSTRAINT client FOREIGN KEY (clientid)
	REFERENCES client (clientid) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT file FOREIGN KEY (fileid)
	REFERENCES filetable (fileid) MATCH SIMPLE
	ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
	OIDS=FALSE
);

