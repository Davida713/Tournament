-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (playerid SERIAL PRIMARY KEY, name TEXT, wins INTEGER);

CREATE TABLE matches (matchid SERIAL, round INTEGER, p1 INTEGER REFERENCES players (playerid), p2 INTEGER REFERENCES players (playerid), winner INTEGER REFERENCES players (playerid));
