import re

sample_output = '''Sure, I will generate the test file and helper file as per your request.

Test File: test_allowed_indicators_api.py
```python
import pytest
import allure
from apiLibrary.open_api.generate_credentials import GenerateCredentials
from apiLibrary.open_api.allowed_indicators_api import AllowedIndicatorsAPI
from dataDirectory.common_data import DataClass
from dataDirectory.api_status_codes import ApiStatusCodes
from utilities.utils import Util
from apiLibrary.open_api.api_endpoint import OpenAPIendpoint
from apiLibrary.open_api.genrate_custom_param import CSAPAPI

class TestAllowedIndicatorsAPI:
    @pytest.fixture(scope="class", autouse=True)
    def classSetup(self, init_api_db):
        self.__class__.analyst = GenerateCredentials(self.dashboard_token)
        genrate_response = self.analyst.genrate_open_api_credentials(self.analyst.payload_for_analyst_role())
        self.__class__.csap_open_api = CSAPAPI(self.base_url, self.access_id, self.secret_key)
        self.__class__.allowed_indicators_api = AllowedIndicatorsAPI()

    # Positive Test Cases
    @pytest.mark.apiTestCase
    @allure.title("Add Single Indicator")
    def test_add_single_indicator(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="exampledomain.com")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.OK

    @pytest.mark.apiTestCase
    @allure.title("Add Multiple Indicators")
    def test_add_multiple_indicators(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="exampledomain.com,1.1.1.1")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.OK

    # Negative Test Cases
    @pytest.mark.apiTestCase
    @allure.title("Missing Threat Indicators")
    def test_missing_threat_indicators(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST

    @pytest.mark.apiTestCase
    @allure.title("Add Duplicate Indicator")
    def test_add_duplicate_indicator(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="exampledomain.com")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert "exampledomain.com" in response.json()["duplicate_indicators"]

    # Edge Test Cases
    @pytest.mark.apiTestCase
    @allure.title("Add Indicator with Special Characters")
    def test_add_indicator_with_special_characters(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="example$domain.com")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.OK

    @pytest.mark.apiTestCase
    @allure.title("Add Indicator with Long String")
    def test_add_indicator_with_long_string(self):
        long_string = "a" * 256
        payload = self.allowed_indicators_api.create_payload(threat_indicators=long_string)
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.OK

    @pytest.mark.apiTestCase
    @allure.title("Add Indicator with Numbers")
    def test_add_indicator_with_numbers(self):
        payload = self.allowed_indicators_api.create_payload(threat_indicators="123456")
        response = self.csap_open_api.query("POST", self.base_url + OpenAPIendpoint.allowed_indicators, data=payload)
        assert response.status_code == ApiStatusCodes.OK
```

Helper File: allowed_indicators_api.py
```python
class AllowedIndicatorsAPI:
    def create_payload(self, threat_indicators):
        payload = {
            "threat_indicators": threat_indicators
        }
        return payload
```

Please note that these test cases are written based on the information provided and may need to be adjusted based on the actual behavior of the API.
'''

# FILE_CHANGES = {
#     'README2.md': '# Updated by Python script\nThis is an automated update.\n'
# }

def extract_files_and_contents(sample_output: str) -> dict:
    file_dict = {}
    
    # Regular expression to find file blocks like: Test File: filename.py or Helper File: filename.py
    pattern = r"(?:Test File|Helper File):\s*(\S+)\n```python\n(.*?)```"
    
    matches = re.findall(pattern, sample_output, re.DOTALL)
    
    for file_name, code_content in matches:
        file_dict[file_name] = code_content.strip()
    
    return file_dict

# test_file_pattern = r'^test_.*\.py$'
# files_data = extract_files_and_contents(sample_output)

# def basic_file_change_logic(files_data):
#     for file_name, content in files_data.items():
#         if re.match(test_file_pattern, file_name):
#             FILE_CHANGES[f"tests/backend_tc/open_api/{file_name}"] = content
#         else:
#             FILE_CHANGES[f"apiLibrary/open_api/{file_name}"] = content
#     return FILE_CHANGES

# basic_file_change_logic(files_data)