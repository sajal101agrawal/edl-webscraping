
## Prerequisites

Ensure you have the following installed:

- Python 3.6 or later
- pip (Python package installer)
- MongoDB
- Gunicorn

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/sajal101agrawal/edl-webscraping.git
    cd edl-webscraping
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up MongoDB:**

    Make sure MongoDB is running. You can start it using:

    ```bash
    sudo systemctl start mongod
    ```

4. **Create MongoDB collections:**

    ```javascript
    use edl_database
    db.createCollection("edl_collection")
    ```

## Running the Project

To start the project on an Azure server, use the following commands:

1. **Start the project initialization script this is api of websocket:**

    ```bash
    nohup ./start.sh > /home/DickiData/edl-webscraping/server.log 2>&1 &
    ```

2. **Start the Flask API using Gunicorn:**

    ```bash
    nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app > /home/DickiData/edl-webscraping/flask_api.log 2>&1 &
    ```

3. **Run the web scraping script:**

    ```bash
    cd websoket_fol
    nohup python scrape.py > /home/DickiData/edl-webscraping/scraping.log 2>&1 &
    ```

## Monitoring and Logs

Logs are generated for each component and can be found in the following locations:

- Server log: `/home/DickiData/edl-webscraping/server.log`
- Flask API log: `/home/DickiData/edl-webscraping/flask_api.log`
- Scraping log: `/home/DickiData/edl-webscraping/scraping.log`

You can monitor these logs using the `tail` command:

```bash
tail -f /home/DickiData/edl-webscraping/server.log
tail -f /home/DickiData/edl-webscraping/flask_api.log
tail -f /home/DickiData/edl-webscraping/scraping.log
```


## GET DATA FROM DATABASE

### API Endpoints

#### 1. **GET /data**

Fetch paginated data from the collection.

- **Request:** `GET /data?page=<page_number>`
  - `page` (optional): The page number to fetch, default is 1.
- **Response:**
  - Status: `200 OK`
  - Body: JSON object containing:
    - `data`: Array of documents
    - `page`: currunt page
    - `per_page`: number of entry per pages
    - `total`: Total number of entries
    - `total_pages`: Total number of pages

### Example Usage

Here's an example of how to use the API to fetch data from the database:

```python
import requests

url = "http://51.107.21.248:5000/data?page=1"

response = requests.get(url)

print(response.json())
```





