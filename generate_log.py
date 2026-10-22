from datetime import datetime
import requests

URL = "https://jsonplaceholder.typicode.com/posts/1"


def generate_log(data):
    """Write each item in the list to a dated log file and return the filename."""
    # STEP 1: Validate input
    if not isinstance(data, list):
        raise ValueError("Input data must be a list.")

    # STEP 2: Generate a filename with today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"log_{today}.txt"

    # STEP 3: Write the log entries to the file
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for entry in data:
                file.write(f"{entry}\n")
    except OSError as error:
        print(f"Error writing to file: {error}")
        return None

    # STEP 4: Print a confirmation message
    print(f"Log written to {filename}")
    return filename


def fetch_data(url=URL):
    """Fetch JSON data from the API. Returns an empty dict if the request fails."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Request failed: {error}")
        return {}


if __name__ == "__main__":
    post = fetch_data()
    print("Fetched Post Title:", post.get("title", "No title found"))