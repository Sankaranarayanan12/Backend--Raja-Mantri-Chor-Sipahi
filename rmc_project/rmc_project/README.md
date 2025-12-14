# Raja-Mantri-Chor-Sipahi

A multiplayer online game where players take on roles: Raja, Mantri, Chor, and Sipahi. Built using Django for the backend, the game allows real-time role assignment, gameplay logic, and score tracking.  

## Project Workflow

The workflow of the Raja-Mantri-Chor-Sipahi project is divided into several stages:

### 1. **Player Registration and Room Creation**
- A player creates or joins a game room using a unique room code.
- The server stores room information and keeps track of connected players.
- Each player is registered in the system with their username and session data.

### 2. **Role Assignment**
- When the game starts, the server randomly assigns roles to each player: Raja, Mantri, Chor, and Sipahi.


### 3. **Gameplay Logic**
- The game proceeds in rounds.
- Players take actions based on their roles:
  - **Raja**: Judges or oversees the actions.
  - **Mantri**: Identifies the Chor.
  - **Chor**: Attempts to steal points without getting caught.
  - **Sipahi**: Protects the Raja and Mantri from the Chor’s theft.
- Each round, the server evaluates actions and updates the game state.

### 4. **Score Calculation and Updates**
- At the end of each round, the server calculates scores based on players’ actions.
- Scores are stored and updated in real-time, visible to all players in the game room.

### 5. **Real-Time Updates**
- Players’ game state, role information, and scores are synced across all clients.

### 6. **Game Completion**
- After the predetermined number of rounds, the game ends.
- Final scores are displayed, and the winner(s) are declared.
- Players can choose to start a new game.

## Features
- Real-time multiplayer gameplay
- Randomized role assignment
- Score tracking
- Clean and interactive UI


