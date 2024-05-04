import os
import math
import Physics
import urllib.parse
import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Global variables for player names
global_player1Name = None
global_player2Name = None
global_currentPlayer = None


class MyHTTPServer(BaseHTTPRequestHandler):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def do_GET(self):
        if self.path == '/':
            # Serve the index.html page for the root path (/)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/game.html':
            # Serve the game.html page for the /game.html path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('game.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/styles.css':
            # Serve the styles.css file
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('styles.css', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/script.js':
            # Serve the script.js file
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('script.js', 'rb') as file:
                self.wfile.write(file.read())
    
    def do_POST(self):
        global global_player1Name, global_player2Name, global_currentPlayer
        if self.path == '/shoot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            dx = data.get('dx')
            dy = data.get('dy')
            
            # Simulate the shot and generate all frames here
            db = Physics.Database()
            beforeShotID = db.getLastTableID()-1  # Get the latest table ID
           
            game = Physics.Game(gameID=0)
            # Get player names for the given game ID
            # Access global player names
            print("Player 1 Name:", global_player1Name)
            print("Player 2 Name:", global_player2Name)
            if(global_currentPlayer == None):
                global_currentPlayer = global_player1Name
            elif(global_currentPlayer == global_player1Name):
                global_currentPlayer = global_player2Name
            elif(global_currentPlayer == global_player2Name):
                global_currentPlayer = global_player1Name
            

            game.shoot("Game01", global_currentPlayer, db.readTable(beforeShotID), dx, dy)
            afterShotID = db.getLastTableID() -1
        
            frames_data = {
            "frames": []
            }

            i=beforeShotID
            while (i <= afterShotID): 
                table = db.readTable(i)
                frame_info = {
                    "svg": table.svg().strip(),  # Strip to remove any potential whitespace
                    "time": table.time  
                }
                frames_data["frames"].append(frame_info)
                i+=1

            print("Number of frames:", len(frames_data["frames"]))
            lastTable = db.readTable(afterShotID)
            print(lastTable)
            # Package the frames data along with player names and the current player into the response
            response_data = {
                "message": "Shot processed successfully",
                "frames": frames_data["frames"],
                "player1Name": global_player1Name,
                "player2Name": global_player2Name,
                "currentPlayer": global_currentPlayer
            }
            
            jsonResponse = json.dumps(response_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', str(len(jsonResponse)))
            self.end_headers()
            self.wfile.write(jsonResponse.encode('utf-8'))
        
        elif self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Here, set the global variables with player names
            
            global_player1Name = form_data.get('player1Name', [None])[0]
            global_player2Name = form_data.get('player2Name', [None])[0]

            
            db = Physics.Database()
            game = Physics.Game(gameName="Game01", player1Name=global_player1Name, player2Name=global_player2Name)
    
            firstTable = game.initialize_game_table()
            db.writeTable(firstTable)

            # Generate the SVG content of the table
            svg_content = firstTable.svg()

            # Serve game.html with the SVG content embedded in it
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('game.html', 'rb') as file:
                content = file.read().decode('utf-8').replace('{svg_content}', svg_content)
                self.wfile.write(content.encode('utf-8'))
        else:
            # Handle other POST requests as necessary
            pass





def main():
    db = Physics.Database()
    db.createDB()  # Ensures the database schema is set up at server start
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web server configuration')
    parser.add_argument('port', type=int, help='Port number for the web server')
    args = parser.parse_args()

    # Get the port number from command line arguments
    port = args.port

    # Create an instance of the HTTPServer class
    server = HTTPServer(('', port), MyHTTPServer)
    print(f'Server started on port {port}')

    # Start the server
    server.serve_forever()

if __name__ == '__main__':
    main()
