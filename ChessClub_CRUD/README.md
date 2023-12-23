
# Chess Club Management System

This Flask application provides a simple web interface for managing chess club data. Users can view, insert, update, and delete chess club records. The application supports different output formats such as JSON, XML, and HTML.

## Features

- View a list of chess clubs
- Insert new chess club records
- Update existing chess club records
- Delete chess club records
- Search for a specific chess club by ID

## Prerequisites

Make sure you have the following installed:

- Python (3.6 or higher)
- Flask
- Flask-MySQLdb
- dicttoxml
- Flask-Testing

## Getting Started

1. Clone the repository:

```bash
   git clone https://github.com/Suzuya4/Flask.git
```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:

   - Create a MySQL database named `db`.
   - Update the database configuration in the Flask app (`chess_club.py`).

4. Run the application:

   ```bash
   python chess_club.py
   ```

   Access the application at [http://localhost:5000/](http://localhost:5000/).

## Running Tests

To run the tests, use the following command:

```bash
python test_chessclub.py
```

## Test Cases

- **test_index_route**: Checks if the index route returns a 200 status code and contains the term 'chess_club'.
- **test_insert_route**: Checks if the insert route returns a 302 status code after inserting a new chess club.
- **test_update_route**: Checks if the update route returns a 302 status code after updating an existing chess club.
- **test_delete_route**: Checks if the delete route returns a 302 status code after deleting a chess club.

