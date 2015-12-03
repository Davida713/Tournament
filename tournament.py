#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.close()



def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("DELETE FROM matches")
    c.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("SELECT COUNT (*) FROM players")
    results = c.fetchall()
    for result in results:
        return result[0]
    db.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()





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

    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("CREATE VIEW wins as SELECT players.playerid, CASE WHEN count(matches.winner) is NULL THEN 0 ELSE count(matches.winner) END as wnum FROM matches right join players on matches.winner = players.playerid group by players.playerid")
    c.execute("CREATE VIEW loses as SELECT players.playerid, CASE WHEN count(matches.loser) is NULL THEN 0 ELSE count(matches.loser) END as lnum FROM matches right join players on matches.loser = players.playerid group by players.playerid")
    c.execute("SELECT players.playerid, players.name, wins.wnum as wins, (loses.lnum + wins.wnum) as matches FROM players left join matches on players.playerid = matches.winner left join wins on wins.playerid = players.playerid left join loses on loses.playerid = players.playerid")
    results = c.fetchall()
    print 
    return results
    db.close()




def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("INSERT INTO matches (winner) VALUES (%s)", (winner,))
    c.execute("INSERT INTO matches (loser) VALUES (%s)", (loser,))
    db.commit()
    db.close()

 
 
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
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("CREATE VIEW tmatch as SELECT players.playerid, players.name, CASE WHEN count(matches.winner) is NULL THEN 0 ELSE count(matches.winner) END as wnum FROM matches right join players on matches.winner = players.playerid group by players.playerid ORDER BY wnum DESC")
    
    c.execute("SELECT a.playerid, a.name, b.playerid, b.name FROM tmatch as a, tmatch as b WHERE a.wnum = b.wnum and a.playerid > b.playerid")
    #c.execute("SELECT count(*) FROM tmatch")
    #tplayers = c.fetchall()
    #pairs = []
    #for row in rows:
        #pair = (playerid1, name)
    rows = c.fetchall()
    print rows
    for row in rows:
        return row[0]
        return row[1]
    #results = c.fetchall()
    #return results
    db.close()


