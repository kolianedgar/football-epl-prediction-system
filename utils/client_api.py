import requests
import time

class APIClient:
    def __init__(
        self,
        headers = None,
        connect_timeout = 10,
        read_timeout = 30,
        max_retries = 3
    ):
        self.session = requests.Session()

        self.session.headers = headers or {
            "User-Agent": "Mozilla/5.0"
        }

        self.session.headers.update(self.session.headers)

        self.timeout = (
            connect_timeout,
            read_timeout
        )

        self.max_retries = max_retries

    def get(self, url):

        for attempt in range(self.max_retries+1):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout
                )

                response.raise_for_status()

                return response.json()
            
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code

                if status_code in [500, 502, 503, 504]:
                    if attempt == self.max_retries:
                        raise

                    wait_time = 2 ** attempt

                    print(
                        f"HTTP {status_code}. "
                        f"Retrying in {wait_time} seconds"
                        f"({attempt + 1}/{self.max_retries})"
                    )

                    time.sleep(wait_time)

                else:
                    raise

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout
            ):

                if attempt == self.max_retries:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Connection error. "
                    f"Retrying in {wait_time}s "
                    f"({attempt + 1}/{self.max_retries})"
                )

    def close(self):
        self.session.close()