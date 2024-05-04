Pool Game Simulation
Overview
This project provides a web-based simulation of a pool game, allowing players to interact with a virtual pool table via a web interface. The simulation leverages a variety of technologies including SQL for database management, Python for backend processing, C for physics simulation, and front-end technologies like JavaScript, HTML, and CSS.

Technologies Used
SQL
SQL is utilized for managing all data persistence in the project. This includes tracking game states, player details, and ball positions through a custom schema in a SQLite database.

Key Features:

Database Schema: Tables for players, games, balls, and game states are defined.
Data Retrieval and Manipulation: SQL queries are executed to handle the creation of games, updating ball positions, and retrieving game history.
Python
Python serves as the backbone for the backend server, handling HTTP requests and integrating with the SQLite database.

Key Features:

HTTP Server: Utilizes the http.server module to listen for and respond to HTTP requests.
Game Logic: Manages the flow of the game, including processing shots, updating game states, and switching player turns.
C
C is used for the critical performance part of the project, particularly the physics engine responsible for simulating the movements of balls on the pool table.

Key Features:

Physics Simulation: Calculates ball trajectories, collisions, and rests using optimized C code for high-performance computation.
JavaScript
JavaScript is used to provide interactivity on the client side, handling user inputs, rendering frames, and communicating with the server.

Key Features:

User Interaction: Captures mouse events for cue stick control and shot execution.
Dynamic Content Loading: AJAX calls are made to the server to retrieve game state updates and dynamically update the game view without needing to reload the webpage.
HTML & CSS
HTML and CSS are employed to structure and style the web interface, providing a visually appealing and functional user experience.

Key Features:

Layout: HTML structures the game's visual components, including the game table and player information.
Styling: CSS is used to enhance the appearance, including the layout of the pool table, balls, and cue stick.
