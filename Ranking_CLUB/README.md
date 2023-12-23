# Flask Ranking Application

This is a simple Flask web application for managing ranking codes. The application allows you to perform CRUD operations (Create, Read, Update, Delete) on ranking codes, and it supports different output formats such as JSON, XML, and HTML.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Suzuya4/flask.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database. Update the `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DB` configurations in the `app.py` file to match your MySQL server settings.

4. Run the Flask application:

   ```bash
   python app.py
   ```

   The application will be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage

### 1. View Ranking Codes

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the list of ranking codes. The default format is JSON, but you can specify the format in the URL parameters (`format=json` or `format=xml`).

### 2. Insert Ranking Code

- To insert a new ranking code, go to [http://127.0.0.1:5000/insert](http://127.0.0.1:5000/insert) and fill out the form.

### 3. Update Ranking Code

- To update a ranking code, go to [http://127.0.0.1:5000/update](http://127.0.0.1:5000/update) and fill out the form.

### 4. Delete Ranking Code

- To delete a ranking code, go to [http://127.0.0.1:5000/delete/6](http://127.0.0.1:5000/delete/6) (replace '6' with the actual ranking code to be deleted).

### 5. Search for Ranking Code

- To search for a specific ranking code, go to [http://127.0.0.1:5000/search/6](http://127.0.0.1:5000/search/6) (replace '6' with the actual ranking code to be searched).

## Testing

The project includes unit tests to ensure the functionality of the application. Run the tests using the following command:

```bash
python test_ranking.py
```