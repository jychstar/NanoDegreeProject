-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create table players (id serial, name text, points integer);
-- create table players (id serial unique, name text );
create table players (id serial, name text, wins integer, matches integer);

create table matches (winner integer, loser integer);
