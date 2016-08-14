#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")  # different from sqlite3
    except:
        print ("connection failed")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches;")
    # c.execute("update players set matches=0;")
    # c.execute("update players set wins=0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players;")
    conn.commit()
    conn.close()
    return None

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(id) from players;")
    results = c.fetchone()
    conn.close()
    return results[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # c.execute("insert into players(name,wins, matche) values (%s,0,0)", (name,))
    c.execute("insert into players(name) values (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # c.execute("select id,name, wins,matches from players order by wins;")
    c.execute("select id,name, coalesce(sum(point),0) as wins, count(matches) as num from players left join matches on id=playerid group by id order by wins DESC;")
    results= c.fetchall()
    # print results
    conn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # c.execute("insert into matches values (%s,%s)", (winner,loser,))
    # c.execute("update players set matches=matches+1 where id=(%s) or id=(%s)", (winner,loser,))
    # c.execute("update players set wins=wins+1 where id=(%s) ", (winner,))
    c.execute("insert into matches(playerid, point) values (%s,1)", (winner,))
    c.execute("insert into matches(playerid, point) values (%s, 0)", (loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("create view subque as select  id, name, row_number() over (order by coalesce(sum(point),0) DESC) as row from players left join matches on id=playerid group by id;")
    c.execute("select a.id, a.name, b.id, b.name from subque as a, subque  as b where a.row=b.row-1 and (b.row %2)=0;")
    results= c.fetchall()
    # print results
    conn.close()
    return results
