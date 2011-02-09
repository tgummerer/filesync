CREATE TABLE usertable
(
  userid integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  email text NOT NULL,
  "password" text NOT NULL,
  CONSTRAINT id PRIMARY KEY (userid),
  CONSTRAINT email UNIQUE (email)
)
WITH (
  OIDS=FALSE
);

CREATE TABLE file
(
  fileid serial NOT NULL,
  userid integer NOT NULL,
  path text NOT NULL,
  lastchange timestamp without time zone,
  CONSTRAINT fileid PRIMARY KEY (fileid),
  CONSTRAINT userid FOREIGN KEY (userid)
      REFERENCES "user" (userid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT path UNIQUE (path)
)
WITH (
  OIDS=FALSE
);

