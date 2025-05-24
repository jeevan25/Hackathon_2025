import os
import git
import requests
from datetime import datetime
from dotenv import load_dotenv

# === CONFIG ===
load_dotenv(override=True)

def create_branch_with_file_changes(new_branch_name, file_changes):
    repo = git.Repo(os.getenv("LOCAL_REPO_PATH"))
    origin = repo.remote(name='origin')

    new_branch = repo.create_head(new_branch_name)
    new_branch.checkout()

    # Apply file changes
    for filename, content in file_changes.items():
        file_path = os.path.join(os.getenv("LOCAL_REPO_PATH"), filename)
        with open(file_path, 'w') as f:
            f.write(content)

    # Commit and push
    repo.git.add(A=True)
    repo.index.commit(f"Automated commit to {new_branch_name}")
    origin.push(new_branch_name)
    
    print(f"Branch {new_branch_name} created and pushed successfully.")
    
NEW_BRANCH_NAME = f'auto-test-branch-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
FILE_CHANGES = {
    'README2.md': '# Updated by Python script\nThis is an automated update.\n',
    'tests/backend_tc/open_api/test_allowed_indicators_api.py' : '''import pytest
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
        assert response.status_code == ApiStatusCodes.OK''',
    'apiLibrary/open_api/allowed_indicators_api.py': '''class AllowedIndicatorsAPI:
    def create_payload(self, threat_indicators):
        payload = {
            "threat_indicators": threat_indicators
        }
        return payload'''
}

# create_branch_with_file_changes(NEW_BRANCH_NAME, FILE_CHANGES)
