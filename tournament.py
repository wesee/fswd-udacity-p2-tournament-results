#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pg = connect();
    c = pg.cursor();
    c.execute("delete from matches")
    pg.commit();
    pg.close()



def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect();
    c = pg.cursor();
    c.execute("delete from players")
    pg.commit();
    pg.close()


def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect();
    c = pg.cursor();
    c.execute("select count(*) from players");
    r = c.fetchone();
    pg.close()
    return r[0];


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg = connect()
    c = pg.cursor()
    c.execute("insert into players(name) values (%s)", (name,));
    pg.commit()
    pg.close()


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
    pg = connect()
    c = pg.cursor()
    c.execute("select id, name, wins, matches from players order by wins desc");
    r = c.fetchall()
    pg.close()
    return r


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg = connect()
    c = pg.cursor()
    c.execute("insert into matches(winner, loser) values (%s, %s)", (winner, loser,));
    c.execute("update players set wins = wins+1, matches = matches+1 where id = %s", (winner,));
    c.execute("update players set matches = matches+1 where id = %s", (loser,));
    pg.commit()
    pg.close()
 
 
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

    """Get current standings
    """
    standings = playerStandings()


    """Construct pairing tuples
    """
    pairings = []
    for i in range(0, len(standings), 2):
        standing1 = standings[i]
        standing2 = standings[i+1]
        pairings.append([standing1[0], standing1[1], standing2[0], standing2[1]])

    return pairings




