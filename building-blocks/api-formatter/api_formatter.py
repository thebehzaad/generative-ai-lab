import logging
import requests

class APIFormatter:
    def __init__(self, llm, base_url):
        """
        Initialize the API formatter with a fine-tuned language model and a base URL.
        :param llm: The fine-tuned language model to be used for parsing prompts
        :param base_url: The base URL for the API calls
        """
        self.llm = llm
        self.base_url = base_url
        logging.basicConfig(level=logging.INFO)

    def parse_prompt(self, prompt):
        """
        Use the fine-tuned LLM to parse the prompt and extract API call details.
        :param prompt: The prompt to be parsed
        :return: A dictionary with tool name, action, and parameters
        """
        try:
            api_details = self.llm.parse_prompt(prompt)
            logging.info(f"API details extracted from prompt '{prompt}': {api_details}")
            return api_details
        except Exception as e:
            logging.error(f"Error parsing prompt '{prompt}': {e}")
            return None

    def format_api_call(self, api_details):
        """
        Format the extracted API details into an API call.
        :param api_details: The extracted API details
        :return: The response from the API call
        """
        if not api_details:
            return None

        tool_name = api_details.get('tool')
        action = api_details.get('action')
        params = api_details.get('params', {})

        url = f"{self.base_url}/{tool_name}/{action}"
        try:
            response = requests.post(url, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API call to {url} failed: {e}")
            return None

# Example usage
class MockLLM:
    def parse_prompt(self, prompt):
        # Mocked prompt parsing
        return {'tool': 'search_tool', 'action': 'search', 'params': {'query': prompt}}

llm = MockLLM()
api_formatter = APIFormatter(llm, base_url="http://api.example.com")

prompts = ["find information on AI", "summarize recent news"]
for prompt in prompts:
    api_details = api_formatter.parse_prompt(prompt)
    result = api_formatter.format_api_call(api_details)
    print(f"Result for prompt '{prompt}': {result}")