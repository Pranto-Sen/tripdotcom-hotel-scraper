
## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Pranto-Sen/tripdotcom-hotel-scraper.git
    cd tripdotcom-hotel-scraper
    ```

2. **Create a virtual environment:**

    - On Windows, create and activate the virtual environment:
      ```bash
       py -3 -m venv .venv
      .venv\Scripts\activate
      ```

    - On Linux/Mac, create and activate the virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```


3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
   

4. **Set up environment variables:**
   
    - Create a `.env` file in the same directory as `.env_sample` and add the following environment variables

     
       ```env
         DATABASE_URL=postgresql://{username}:{password}@{Host Address}:{Port}/{Database Name}
        ```


5. **Run the application:**
    ```bash
    cd trip_scraper
    scrapy crawl trip_spider
    ```

    
