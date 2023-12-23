
# Flask Player Management App

This is a simple Flask application for managing player records. The application allows users to perform CRUD operations (Create, Read, Update, Delete) on player information stored in a MySQL database.

## Features

- **View Players:** Browse through the list of players.
- **Insert Player:** Add a new player to the database.
- **Update Player:** Modify details of an existing player.
- **Delete Player:** Remove a player from the database.
- **Search Player:** Search for a player by their unique ID.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-MySQLdb
- Flask-Testing

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Suzuya4/flask.git
   ```

2. Navigate to the project directory:

   ```bash
   cd flask-player-app
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python player.py
   ```

   The app should now be running at `http://localhost:5000`.

### Testing

To run the tests, use the following command:

```bash
python test_player.py
```

## Usage

1. **View Players:** Open your browser and go to `http://localhost:5000/`. Players will be displayed in JSON format by default.

2. **Insert Player:** Submit the player details using the insertion form at `http://localhost:5000/insert`.

3. **Update Player:** Click on a player's ID at `http://localhost:5000/` to view details and update them using the update form.

4. **Delete Player:** Click on a player's ID at `http://localhost:5000/` and then go to `http://localhost:5000/delete/<player_id>` to delete the player.

5. **Search Player:** Visit `http://localhost:5000/search/<player_id>` to search for a player by their ID.


---

