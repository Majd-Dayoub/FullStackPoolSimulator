import phylib;
import sqlite3
import os
import math


################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_BALL_DIAMETER 
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH 
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH 
SIM_RATE = phylib.PHYLIB_SIM_RATE 
VEL_EPSILON =phylib.PHYLIB_VEL_EPSILON 
DRAG = phylib.PHYLIB_DRAG 
MAX_TIME = phylib.PHYLIB_MAX_TIME 
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS 

# A3 constant FRAME_RATE
FRAME_RATE = 0.01  

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################

class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall

    def svg(self):
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.still_ball.pos.x,
            self.obj.still_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.still_ball.number]
        )

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall
    
    def svg(self):
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.rolling_ball.pos.x,
            self.obj.rolling_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.rolling_ball.number]
        )

class Hole(phylib.phylib_object):
    def __init__(self, pos):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_HOLE, 
                                      0, 
                                      pos, 
                                      None, None, 
                                      pos.x, pos.y)
        self.__class__ = Hole
    
    def svg(self):
        return """<circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (
            self.obj.hole.pos.x,
            self.obj.hole.pos.y,
            HOLE_RADIUS
        )

class HCushion(phylib.phylib_object):

    def __init__(self, y):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_HCUSHION, 
                                      0, None, None, None, 
                                      0.0, y)
        self.__class__ = HCushion

    def svg(self):
        return """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (
            -25 if self.obj.hcushion.y == 0 else 2700
        )


class VCushion(phylib.phylib_object):
    def __init__(self, x):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_VCUSHION, 
                                      0, None, None, None, 
                                      x, 0.0)
        self.__class__ = VCushion

    def svg(self):
        return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (
            -25 if self.obj.vcushion.x == 0 else 1350
        )

    


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self )
        self.current = -1
    
    # add svg method here
    def svg(self):
        svg_string = HEADER
        for obj in self:
            if obj is not None:  # Check if the object is not None
                svg_string += obj.svg()
        svg_string += FOOTER
        return svg_string

    # A3 Roll Method
    def roll( self, t ):
        new = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                    Coordinate(0,0),
                    Coordinate(0,0),
                    Coordinate(0,0) )
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )
                # add ball to table
                new += new_ball

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                    Coordinate( ball.obj.still_ball.pos.x,
                    ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
        # return table
        return new
    
    def cueBall(self, table):
        # Find the object representing the cue ball (number 0)
        
        cue_ball = None
        table_copy = table
        table_copy = [ball for ball in table]  
    
        for ball in table_copy:
            if isinstance(ball, StillBall):
                if ball.obj.still_ball.number == 0:
                    cue_ball = ball
                    break             
        if cue_ball is None:
            raise ValueError("Cue ball (number 0) not found on the table")
        
        return cue_ball
        


    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other )
        return self

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self )
        if result:
            result.__class__ = Table
            result.current = -1
        return result
    
################################################################################
class Database:
    def __init__(self, reset=False):
        self.conn = None
        if reset:
            # Delete existing database file if reset is True
            try:
                os.remove("phylib.db")
                print("Deleted existing database file.")
            except FileNotFoundError:
                pass  # File does not exist, nothing to delete

        self.conn = sqlite3.connect('phylib.db')
        
    
    def createDB(self):
        if self.conn:
            cursor = self.conn.cursor()
            # SQL commands to create tables

            #Ball
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO INTEGER NOT NULL,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT,
                YVEL FLOAT
            )""")

            #TTable
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS TTable (
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            )""")

            #BallTable
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS BallTable (
                BALLID INTEGER NOT NULL, 
                TABLEID INTEGER NOT NULL, 
                FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
            )""")

            #Shot
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Shot (
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            )""")


            #TableShot
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS TableShot (
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            )""")


            #Game
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game (
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            )""")

            #Player
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Player (
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            )""")


            # Commit changes and close cursor
            self.conn.commit()
            cursor.close()
            print("Database tables created successfully.")
        else:
            print("Database connection not established.")

    # Reads data from database and stores it into table object
    # I think its broken because i am not getting the time 
    def readTable(self, tableID):
        
        if self.conn:
            cursor = self.conn.cursor()
        
            # Execute SQL query with JOIN clause
            cursor.execute("""
                SELECT TTable.TIME, Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                FROM Ball
                JOIN BallTable 
                    ON Ball.BALLID = BallTable.BALLID
                JOIN TTable 
                    ON BallTable.TABLEID = TTable.TABLEID
                WHERE BallTable.TABLEID = ?
            """, (tableID +1,))

            #Fetch all rows from cursor
            rows = cursor.fetchall() 
        
            if not rows:
                return None #TABLEID is not in BallTable table
            
            table = Table() # Create Table object

            for row in rows:
                # Extract ball attributes from the row
                time,ball_id, ball_number, xpos, ypos, xvel, yvel = row
                
                # Instantiate StillBall or RollingBall based on velocity
                if xvel is None or yvel is None:
                    # Ball has no velocity, instantiate as StillBall
                    pos = Coordinate(xpos, ypos)
                    ball = StillBall(ball_number, pos)
                    table += ball  # Add ball to the table
                else:
                    # Ball has velocity, calculate acceleration and instantiate as RollingBall
                    speed = math.sqrt(xvel ** 2 + yvel ** 2)
                    if speed > VEL_EPSILON:
                        acc_x = -(xvel / speed) * DRAG
                        acc_y = -(yvel / speed) * DRAG
                    else:
                        acc_x = acc_y = 0  # No acceleration if below threshold

                    acceleration = Coordinate(acc_x, acc_y)
                    pos = Coordinate(xpos, ypos)
                    vel = Coordinate(xvel, yvel)
                    ball = RollingBall(ball_number, pos, vel, acceleration)
                    table += ball  # Add ball to the table
            table.time = time           
                
                 
            # Close cursor and commit changes
            cursor.close()
            self.conn.commit()
            return table
        else:
            print("Database not connected")
            return None


    
    # Writes data to database from table object 
    def writeTable(self, table):
        if self.conn:
            cursor = self.conn.cursor()

            # Create a placeholder for TABLEID
            table_id = None

            try:
                # Insert a new row into TTable to get a new TABLEID
                cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
                table_id = cursor.lastrowid  # Retrieve the autoincremented TABLEID
                table_id -= 1  # Adjusting to start numbering from zero

                # Loop through balls in the table and insert them into Ball and BallTable tables
                for ball in table: #CHECK IF YOU SHOULD CHANGEEEE
                    if isinstance(ball, (StillBall, RollingBall)):
                        if isinstance(ball, StillBall):
                            xvel = yvel = None  # StillBall has no velocity
                            
                            # Insert ball data into Ball table
                            cursor.execute("""
                                INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                VALUES (?, ?, ?, ?, ?)
                            """, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, xvel, yvel))
                            
                            # Retrieve the autoincremented BALLID
                            ball_id = cursor.lastrowid
                        elif isinstance(ball, RollingBall):
                            xvel = ball.obj.rolling_ball.vel.x
                            yvel = ball.obj.rolling_ball.vel.y
                            
                            # Insert ball data into Ball table
                            cursor.execute("""
                                INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                VALUES (?, ?, ?, ?, ?)
                            """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, xvel, yvel))
                            # Retrieve the autoincremented BALLID
                            ball_id = cursor.lastrowid

                        

                        # Insert mapping between BALLID and TABLEID into BallTable table
                        cursor.execute("""
                            INSERT INTO BallTable (BALLID, TABLEID) 
                            VALUES (?, ?)
                        """, (ball_id, table_id+1))

                # Commit changes and close cursor
                self.conn.commit()
                cursor.close()

                # Return the autoincremented TABLEID minus 1
                return table_id

            except Exception as e:
                print("Error writing table:", e)
                # Rollback changes if an error occurs
                self.conn.rollback()
                cursor.close()
                return None

        else:
            print("Database not connected")
            return None
    
    def getGame(self, gameID):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT Game.GAMENAME, Player1.PLAYERNAME AS PLAYER1NAME, Player2.PLAYERNAME AS PLAYER2NAME
                FROM Game
                JOIN Player AS Player1 ON Game.GAMEID = Player1.GAMEID AND Player1.PLAYERID = (SELECT MIN(PLAYERID) FROM Player WHERE Game.GAMEID = Player.GAMEID)
                LEFT JOIN Player AS Player2 ON Game.GAMEID = Player2.GAMEID AND Player1.PLAYERID != Player2.PLAYERID
                WHERE Game.GAMEID = ?
            """, (gameID,))
            game_data = cursor.fetchone()
            cursor.close()
            if game_data:
                return {
                    'gameName': game_data[0],
                    'player1Name': game_data[1],
                    'player2Name': game_data[2] if game_data[2] else None
                }
            else:
                return None
        else:
            print("Database connection not established.")
            return None
        
    def setGame(self, gameName, player1Name, player2Name):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
            gameID = cursor.lastrowid
            cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
            player1ID = cursor.lastrowid
            if player2Name:
                cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))
                player2ID = cursor.lastrowid
            else:
                player2ID = None
            cursor.close()
            self.conn.commit()
            print("Game added successfully.")
        else:
            print("Database connection not established.")

    def newShot(self, gameName, playerName):
        cursor = self.conn.cursor()

        # First, retrieve the playerID associated with the given playerName
        cursor.execute("""
            SELECT Player.PLAYERID 
            FROM Player 
            JOIN Game ON Player.GAMEID = Game.GAMEID
            WHERE Player.PLAYERNAME = ? AND Game.GAMENAME = ?
        """, (playerName, gameName))
        player_data = cursor.fetchone()

        if player_data is None:
            raise ValueError(f"No player found with name '{playerName}' in game '{gameName}'")

        playerID = player_data[0]

         # Next, insert a new row into the Shot table to record the shot
        cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, (SELECT GAMEID FROM Game WHERE GAMENAME = ?))", (playerID, gameName))
        shot_id = cursor.lastrowid  # Retrieve the auto-incremented shotID
        self.conn.commit()
        cursor.close()

        return shot_id

    def recordTableShot(self, table_id, shot_id):
        if self.conn:
            cursor = self.conn.cursor()

            try:
                cursor.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (table_id, shot_id))
                self.conn.commit()
                cursor.close()
            except Exception as e:
                print("Error recording table shot:", e)
                self.conn.rollback()
                cursor.close()
        else:
            print("Database connection not established.")
            
    def getLastTableID(self):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(TABLEID) FROM TTable")
            max_id = cursor.fetchone()[0]
            cursor.close()
            if max_id is not None:
                return max_id
            else:
                return 0  # Default to 0 if no tables are found
        else:
            print("Database not connected")
            return None

    def getPlayerNamesByGameID(self, gameID):
        """
        Retrieves player names for a given game ID.
        """
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT PLAYERNAME 
                FROM Player
                WHERE GAMEID = ?
            """, (gameID,))
            players = cursor.fetchall()
            # Assuming there are always two players per game for simplicity
            if players and len(players) >= 2:
                return players[0][0], players[1][0]  # Return the names of the first two players
            else:
                return None, None  # No players found or not enough players

    
    def close(self):
        if self.conn:
            self.conn.commit()  # Commit any pending changes
            self.conn.close()   # Close the connection




################################################################################
            


class Game:
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        # Check for valid combinations of arguments
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("Invalid combination of arguments")

        db = Database()
        self.table = None
        # If gameID is provided, retrieve game details from the database
        if gameID is not None:
            # Increment gameID by 1 to match SQL numbering
            gameID += 1
            game_data = db.getGame(gameID)
            if game_data is not None:
                self.gameName = game_data['gameName']
                self.player1Name = game_data['player1Name']
                self.player2Name = game_data['player2Name']


        # If gameID is None and other arguments are provided
        else:
            db.setGame(gameName, player1Name, player2Name)
            # Add rows to the Game and Player tables to record game details
            # Call a helper method (e.g. setGame) in the Database class
            # One new row shall be added to the Game table
            # Two new rows shall be added to the Player table to record gameName, player1Name, and player2Name
            # Player1Name shall be added to the Player table first to get the lower PLAYERID

    def shoot( self, gameName, playerName, table, xvel, yvel ): 
        
        db = Database()

        # Retrieve the shotID for later use
        
        shot_id = db.newShot(gameName, playerName)
        
        # Find the object representing the cue ball (number 0)
        cue_ball = table.cueBall(table)

         # Retrieve the x and y values of the cue ball's position
        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y

        # Set the type attribute of the cue ball to phylib.ROLLING_BALL
        
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
    
        # Set the rolling ball attributes
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        # calculate Acceleration
        speed_rb = math.sqrt(xvel**2 + yvel**2)
        if speed_rb > VEL_EPSILON:
            acc_x = -(xvel / speed_rb) * DRAG
            acc_y = -(yvel / speed_rb) * DRAG
        else:
            acc_x = acc_y = 0

        # Set acceleration attributes
        cue_ball.obj.rolling_ball.acc.x = acc_x
        cue_ball.obj.rolling_ball.acc.y = acc_y

        # Set the number of the cue ball to 0
        cue_ball.obj.rolling_ball.number = 0
        
        
        # Determine the length of the segment in seconds
        segment_length = 0
        preSegTable = table


        while table is not None:
            before_seg = table.time
            new_table = table.segment()
            if new_table is None:
                break
            else:
                after_seg = new_table.time
                num_frames = math.floor((after_seg - before_seg) / FRAME_RATE)

                for i in range(num_frames):
                    frame_time = i * FRAME_RATE
                    next_table = table.roll(frame_time)
                    next_table.time = before_seg + frame_time
                    table_id = db.writeTable(next_table)
                    db.recordTableShot(table_id, shot_id)
            table = new_table
            

    
    def initialize_game_table(self):
        table = Table()

        # Position for the cue ball
        cue_ball_pos = Coordinate(675, 2025)
        cue_ball = StillBall(0, cue_ball_pos)  # Assuming 0 is the cue ball's number
        table += cue_ball

        # Ball1 - Yellow
        ball1_pos = Coordinate(675,675)
        ball1 = StillBall(1, ball1_pos)  
        table += ball1

        # Ball2 - Blue
        ball2_pos = Coordinate(645,622)
        ball2 = StillBall(2, ball2_pos)  
        table += ball2

        # Ball 3 - Red
        ball3_pos = Coordinate(614, 569)
        ball3 = StillBall(3, ball3_pos)
        table += ball3

        # Ball 4 - Purple
        ball4_pos = Coordinate(584, 516)
        ball4 = StillBall(4, ball4_pos)
        table += ball4

        # Ball 5 - Orange
        ball5_pos = Coordinate(797, 463)
        ball5 = StillBall(5, ball5_pos)
        table += ball5

        # Ball 6 - Green
        ball6_pos = Coordinate(614, 463)
        ball6 = StillBall(6, ball6_pos)
        table += ball6

        # Ball 7 - Brown
        ball7_pos = Coordinate(706, 516)
        ball7 = StillBall(7, ball7_pos)
        table += ball7

        # Ball 8 - Black
        ball8_pos = Coordinate(675, 569)
        ball8 = StillBall(8, ball8_pos)
        table += ball8

        # Ball 9 - Light Yellow
        ball9_pos = Coordinate(706, 622)
        ball9 = StillBall(9, ball9_pos)
        table += ball9

        # Ball 10 - Light Blue
        ball10_pos = Coordinate(736, 569)
        ball10 = StillBall(10, ball10_pos)
        table += ball10

        # Ball 11 - Pink
        ball11_pos = Coordinate(767, 516)
        ball11 = StillBall(11, ball11_pos)
        table += ball11

        # Ball 12 - Medium Purple
        ball12_pos = Coordinate(553, 463)
        ball12 = StillBall(12, ball12_pos)
        table += ball12

        # Ball 13 - Light Salmon
        ball13_pos = Coordinate(736, 463)
        ball13 = StillBall(13, ball13_pos)
        table += ball13

        # Ball 14 - Light Green
        ball14_pos = Coordinate(645, 516)
        ball14 = StillBall(14, ball14_pos)
        table += ball14

        # Ball 15 - Sandy Brown
        ball15_pos = Coordinate(675, 463)
        ball15 = StillBall(15, ball15_pos)
        table += ball15



        self.table = table
        return table


    
            
                    





       


        








