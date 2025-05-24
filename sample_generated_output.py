import re
from typing import Dict


sample_output = ''' Generated Test Cases:

Sure, I will generate the test cases for the endpoint `/csap/v1/allowed_indicators/` as per your instructions.

Test File: `test_allowed_indicators_api.py`

```python
import pytest
import allure
from apiLibrary.open_api.allowed_indicators_api import AllowedIndicatorsAPI
from utilities.utils import Util
from dataDirectory.common_data import DataClass
from dataDirectory.api_status_codes import ApiStatusCodes

class TestAllowedIndicatorsAPI:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, init_api_db):
        self.allowed_indicators_api = AllowedIndicatorsAPI(init_api_db)

    @allure.title("Test Allowed Indicators POST API with valid data")
    def test_post_allowed_indicators_valid_data(self):
        indicators = Util.generate_random_indicators()
        response = self.allowed_indicators_api.post_allowed_indicators(indicators)
        assert response.status_code == ApiStatusCodes.OK
        self.allowed_indicators_api.verify_indicators_in_response(indicators, response.json())

    @allure.title("Test Allowed Indicators POST API with duplicate data")
    def test_post_allowed_indicators_duplicate_data(self):
        indicators = Util.generate_random_indicators()
        response = self.allowed_indicators_api.post_allowed_indicators(indicators)
        assert response.status_code == ApiStatusCodes.OK
        response = self.allowed_indicators_api.post_allowed_indicators(indicators)
        assert 'duplicate_indicators' in response.json()

    @allure.title("Test Allowed Indicators POST API with missing threat_indicators field")
    def test_post_allowed_indicators_missing_field(self):
        response = self.allowed_indicators_api.post_allowed_indicators(None)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST

    @allure.title("Test Allowed Indicators GET API with valid data")
    def test_get_allowed_indicators_valid_data(self):
        response = self.allowed_indicators_api.get_allowed_indicators()
        assert response.status_code == ApiStatusCodes.OK

    @allure.title("Test Allowed Indicators GET API with invalid type parameter")
    def test_get_allowed_indicators_invalid_type(self):
        response = self.allowed_indicators_api.get_allowed_indicators(type='invalid')
        assert response.status_code == ApiStatusCodes.OK
        assert response.json()['count'] == 0

    @allure.title("Test Allowed Indicators GET API with no results")
    def test_get_allowed_indicators_no_results(self):
        response = self.allowed_indicators_api.get_allowed_indicators(value='nonexistent')
        assert response.status_code == ApiStatusCodes.OK
        assert response.json()['count'] == 0

    @allure.title("Test Allowed Indicators GET API with large page size")
    def test_get_allowed_indicators_large_page_size(self):
        response = self.allowed_indicators_api.get_allowed_indicators(page_size=1000)
        assert response.status_code == ApiStatusCodes.OK

    @allure.title("Test Allowed Indicators GET API with negative page number")
    def test_get_allowed_indicators_negative_page(self):
        response = self.allowed_indicators_api.get_allowed_indicators(page=-1)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST

    @allure.title("Test Allowed Indicators GET API with zero page size")
    def test_get_allowed_indicators_zero_page_size(self):
        response = self.allowed_indicators_api.get_allowed_indicators(page_size=0)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST
```

Helper File: `allowed_indicators_api.py`

```python
from base.api_requests import Request
from utilities.utils import Util

class AllowedIndicatorsAPI:

    def __init__(self, token):
        self.headers = {'Authorization': f'Bearer {token}'}
        self.endpoint = '/csap/v1/allowed_indicators/'

    def post_allowed_indicators(self, indicators):
        payload = {'threat_indicators': indicators}
        response = Request.POST(self.endpoint, payload, headers=self.headers)
        return response

    def get_allowed_indicators(self, page=1, page_size=10, type=None, value=None):
        params = {'page': page, 'page_size': page_size, 'type': type, 'value': value}
        response = Request.GET(self.endpoint, params=params, headers=self.headers)
        return response

    def verify_indicators_in_response(self, indicators, response):
        for indicator in indicators.split(','):
            assert indicator in response
```

Please note that the helper file `allowed_indicators_api.py` should be placed in `apiLibrary/open_api/` and the test file `test_allowed_indicators_api.py` should be placed in `tests/backend_tc/open_api/` as per the repository structure.
'''

FILE_CHANGES = {
    'README2.md': '# Updated by Python script\nThis is an automated update.\n'
}

def extract_files_and_contents(sample_output: str) -> Dict[str, str]:
    """
    Extracts Python code blocks labeled with 'Test File:' or 'Helper File:'.

    Args:
        sample_output (str): A string containing labeled code blocks.

    Returns:
        Dict[str, str]: Mapping of file names to code strings.
    """
    file_dict = {}

    # Match either "Test File:" or "Helper File:" followed by filename and a Python code block
    pattern = r"(?:Test File|Helper File):\s*`?([^`\n]+?)`?\s*```python\s*(.*?)```"

    matches = re.findall(pattern, sample_output, re.DOTALL | re.IGNORECASE)

    for file_name, code in matches:
        file_name = file_name.strip()
        code = code.strip()
        if file_name and code:
            file_dict[file_name] = code

    return file_dict



test_file_pattern = r'^test_.*\.py$'
files_data = extract_files_and_contents(sample_output)

def basic_file_change_logic(files_data):
    for file_name, content in files_data.items():
        if re.match(test_file_pattern, file_name):
            FILE_CHANGES[f"tests/backend_tc/open_api/{file_name}"] = content
        else:
            FILE_CHANGES[f"apiLibrary/open_api/{file_name}"] = content
    return FILE_CHANGES

basic_file_change_logic(files_data)