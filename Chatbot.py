from os import getenv
import json
from utils import load_cookies
import requests

class Chatbot:
    """
    Chatbot class for RMIT Val
    """

    def __init__(self, settings: dict) -> None:
        """
        Args:
            settings(dict):
            {
                "response_length": str, <- response_length: short (1365), medium (2730), long (4096)
                "temperature": float,
                "system_prompt": str,
                "precaution": str,
                "stream": bool,
            }
        """
        self.settings = settings

        # Get response length
        response_length_mapping = {
            "short": 1365,
            "medium": 2730,
            "long": 4096,
        }
        response_length = response_length_mapping.get(
            self.settings.get("response_length"), 1365
        )

        # Init the payload headers
        self.payload = {
            "context": {
                "overrides": {
                    "temperature": self.settings.get("temperature", 0.5),
                    "data_selection": "general",
                    "system_prompt": self.settings.get("system_prompt", ""),
                    "response_length": response_length,
                }
            },
        }

        self.session = requests.Session()
        self.url = "https://val.rmit.edu.au"

        cookies = load_cookies()
        self.session.cookies.update(cookies)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "*/*",
            "Accept-Language": "en,en-US;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://val.rmit.edu.au/",
            "Content-Type": "application/json",
            "Origin": "https://val.rmit.edu.au",
            "Dnt": "1",
            "Sec-Gpc": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
            "Te": "trailers",
        }

    def get_response(self, messages: list) -> dict:
        """Get the response from Val's API endpoint

        Args:
            message (list):
            [{"role": str, "content": str}]

        Returns:
            dict: Response from the API, includes title, role, and content
        """
        api_endpoint = "/history/generate"

        # Populate the message list before appending to payload
        if type(messages) != list:
            return None

        ordered_messages = []
        for message in messages:
            ordered_message = {
                "id": "",
                "role": message.get("role"),
                "content": message.get("content"),
                "date": "",
            }
            ordered_messages.append(ordered_message)

        self.payload["messages"] = ordered_messages

        print(self.payload)
        # Make the POST request
        is_streaming = self.settings.get("stream", False)
        api_response = self.session.post(
            self.url + api_endpoint,
            headers=self.headers,
            json=self.payload,
            stream=is_streaming,
        )

        if api_response.status_code != 200:
            response = {"status": "error", "data": api_response.text}
        else:
            # Parse the response
            data = [
                json.loads(line)
                for line in api_response.text.strip().split("\n")
                if line.strip()
            ]

            # Filter out empty dictionaries
            filtered_data = [entry for entry in data if entry]

            # Extract title, role, and concatenate content
            title = filtered_data[0]["history_metadata"]["title"]
            role = filtered_data[0]["choices"][0]["messages"][0]["role"]
            content = " ".join(
                message["content"]
                for entry in filtered_data
                for choice in entry["choices"]
                for message in choice["messages"]
            )

            # Initialize the final dictionary
            result = {"title": title, "role": role, "content": content}

            response = {"status": "success", "data": result}

        return response
