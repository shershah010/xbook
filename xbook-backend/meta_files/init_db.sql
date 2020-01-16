DROP DATABASE xbook;

CREATE DATABASE xbook;

USE xbook;

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Friends;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Comments;

CREATE TABLE IF NOT EXISTS Users(
  token VARCHAR(64) NOT NULL,
  username VARCHAR(50) NOT NULL,
  firstname VARCHAR(50) NOT NULL,
  lastname VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS Friends(
  origin VARCHAR(50) NOT NULL,
  destination VARCHAR(50) NOT NULL,
  FOREIGN KEY (origin) REFERENCES Users(username),
  FOREIGN KEY (destination) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Messages(
  id INT NOT NULL AUTO_INCREMENT,
  origin VARCHAR(50) NOT NULL,
  destination VARCHAR(50) NOT NULL,
  message VARCHAR(4000) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (origin) REFERENCES Users(username),
  FOREIGN KEY (destination) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Posts(
  id INT NOT NULL AUTO_INCREMENT,
  origin VARCHAR(50) NOT NULL,
  message VARCHAR(4000) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (origin) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Comments(
  id INT NOT NULL AUTO_INCREMENT,
  origin VARCHAR(50) NOT NULL,
  post_id INT NOT NULL,
  message VARCHAR(4000) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (origin) REFERENCES Users(username),
  FOREIGN KEY (post_id) REFERENCES Posts(id)
);
