-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop database if exists tournament;
create database tournament;
\c tournament
-- create table players (id serial primary key, name text, wins integer, matches integer);
create table players (id serial primary key, name text);
create table matches (matchid serial primary key, winner integer references players(id), loser integer references players(id));
