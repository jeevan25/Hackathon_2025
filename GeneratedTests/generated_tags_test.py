Sure, I will generate the test cases for the given endpoints. 

Let's start with the helper file located in `apiLibrary/open_api/`. We'll call it `tag_api.py`.

```python
# apiLibrary/open_api/tag_api.py

from utilities.utils import Util
from base.api_requests import Request
from dataDirectory.common_data import config

class TagAPI:
    def create_tag_payload(self, tag_name):
        payload = {
            "tag_name": tag_name
        }
        return payload

    def create_tag(self, payload):
        response = Request.POST(
            config["API_ENDPOINTS"]["CREATE_TAG"], payload
        )
        response_json = response.json()
        return response

    def get_tags(self):
        response = Request.GET(
            config["API_ENDPOINTS"]["GET_TAGS"]
        )
        response_json = response.json()
        return response
```

Now, let's move on to the test file located in `tests/backend_tc/open_api/`. We'll call it `test_tag_api.py`.

```python
# tests/backend_tc/open_api/test_tag_api.py

import pytest
import allure
from apiLibrary.open_api.tag_api import TagAPI
from dataDirectory.api_status_codes import ApiStatusCodes

class TestTagAPI:
    tag_api = TagAPI()

    @pytest.mark.positive
    @allure.title("Test creating a new tag")
    def test_create_tag(self):
        tag_name = "TestTag" + Util.getUniqueName()
        payload = self.tag_api.create_tag_payload(tag_name)
        response = self.tag_api.create_tag(payload)
        assert response.status_code == ApiStatusCodes.OK, "Invalid status code"
        assert response.json()["tag_name"] == tag_name, "Tag name mismatch"

    @pytest.mark.positive
    @allure.title("Test getting all tags")
    def test_get_tags(self):
        response = self.tag_api.get_tags()
        assert response.status_code == ApiStatusCodes.OK, "Invalid status code"

    @pytest.mark.negative
    @allure.title("Test creating a tag without tag_name")
    def test_create_tag_without_name(self):
        payload = {}
        response = self.tag_api.create_tag(payload)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST, "Invalid status code"

    @pytest.mark.negative
    @allure.title("Test creating a tag with tag_name exceeding 100 characters")
    def test_create_tag_with_long_name(self):
        tag_name = "T" * 101
        payload = self.tag_api.create_tag_payload(tag_name)
        response = self.tag_api.create_tag(payload)
        assert response.status_code == ApiStatusCodes.BAD_REQUEST, "Invalid status code"

    @pytest.mark.edge
    @allure.title("Test creating a tag with tag_name of 100 characters")
    def test_create_tag_with_max_length_name(self):
        tag_name = "T" * 100
        payload = self.tag_api.create_tag_payload(tag_name)
        response = self.tag_api.create_tag(payload)
        assert response.status_code == ApiStatusCodes.OK, "Invalid status code"
        assert response.json()["tag_name"] == tag_name, "Tag name mismatch"

    @pytest.mark.edge
    @allure.title("Test creating a tag with tag_name of 1 character")
    def test_create_tag_with_min_length_name(self):
        tag_name = "T"
        payload = self.tag_api.create_tag_payload(tag_name)
        response = self.tag_api.create_tag(payload)
        assert response.status_code == ApiStatusCodes.OK, "Invalid status code"
        assert response.json()["tag_name"] == tag_name, "Tag name mismatch"

    @pytest.mark.edge
    @allure.title("Test getting tags when no tags exist")
    def test_get_tags_when_no_tags_exist(self):
        # Assuming there's a method to delete all tags
        self.tag_api.delete_all_tags()
        response = self.tag_api.get_tags()
        assert response.status_code == ApiStatusCodes.OK, "Invalid status code"
        assert response.json() == [], "Tag list is not empty"
```

Please note that you need to replace `ApiStatusCodes.OK` and `ApiStatusCodes.BAD_REQUEST` with the actual status codes in your application. Also, make sure to add the actual endpoints to `config["API_ENDPOINTS"]["CREATE_TAG"]` and `config["API_ENDPOINTS"]["GET_TAGS"]` in `common_data.py`.