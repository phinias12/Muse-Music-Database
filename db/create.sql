/* user(userID, first_name, last_name, email, password, dob) */
CREATE TABLE users (
    userID          INT NOT NULL AUTO_INCREMENT,
    first_name      VARCHAR(25) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password        VARCHAR(255) NOT NULL,
    dob             DATE NOT NULL,
    PRIMARY KEY (userID)
);

/* artist(artistID, name, dob, location, bio) */
CREATE TABLE artist (
    artistID        INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    dob             INT(4) NOT NULL,
    location        VARCHAR(150) NOT NULL,
    bio             VARCHAR(5000) NOT NULL,
    PRIMARY KEY (artistID)
);

/* album(albumID, name, release_year) */
CREATE TABLE album (
    albumID         INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    genre           VARCHAR(100) NOT NULL,
    release_year    INT(4) NOT NULL,
    PRIMARY KEY (albumID)
);

/* song(songID, artistID, albumID, name, genre, track_num, length) */
CREATE TABLE song (
    songID          INT NOT NULL AUTO_INCREMENT,
    artistID        INT NOT NULL,
    albumID         INT NOT NULL,
    name            VARCHAR(100) NOT NULL,
    track_num       INT NOT NULL,
    length          VARCHAR(20) NOT NULL,
    PRIMARY KEY (songID),
    CONSTRAINT
        FOREIGN KEY (artistID)
            REFERENCES artist(artistID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT
        FOREIGN KEY (albumID)
            REFERENCES album(albumID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

/* listens(userID, songID, day_time) */
CREATE TABLE listens (
    userID      INT NOT NULL,
    songID      INT NOT NULL,
    date_time   TIMESTAMP NOT NULL,
    CONSTRAINT
        FOREIGN KEY (userID)
            REFERENCES users(userID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT
        FOREIGN KEY (songID)
            REFERENCES song(songID)
            ON DELETE CASCADE
            ON UPDATE CASCADE      
);

/* likes(userID, songID) */
CREATE TABLE likes (
    userID      INT NOT NULL,
    songID      INT NOT NULL,
    PRIMARY KEY (userID, songID),
    CONSTRAINT
        FOREIGN KEY (userID)
            REFERENCES users(userID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT
        FOREIGN KEY (songID)
            REFERENCES song(songID)
            ON DELETE CASCADE
            ON UPDATE CASCADE      
);

