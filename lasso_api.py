import requests
import os
import json
from typing import Any, Dict, Optional, Callable, List

from requests_aws4auth import AWS4Auth
from requests import Response

JSON_CONTENT_TYPE = "application/json"
AWS_SERVICE = "appsync"
DEFAULT_HOST = "y47qt5w6bzh3xpzmxosmv5x3re.appsync-api.us-west-2.amazonaws.com"
DEFAULT_REGION = "us-west-2"


class LassoAPI:
    def __init__(self, host: str = DEFAULT_HOST, region: str = DEFAULT_REGION):
        self.host = host
        self.region = region
        self.amz_target = ""
        self.lasso_api_url = f"https://{self.host}/graphql"

        # Retrieve access keys
        self.access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        self.secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        if self.access_key is None or self.secret_key is None:
            raise Exception("Must define access key and secret key")

        self.session = requests.Session()
        self.session.auth = AWS4Auth(self.access_key, self.secret_key, region, AWS_SERVICE)

    def _extract_json_response(self, raw_response: Response, data_key: str) -> dict:
        if raw_response.status_code == 200:
            json_response = json.loads(raw_response.content)
            if (data := json_response.get("data")) is not None and data.get(data_key) is not None:
                return {"status": "success", "data": json_response["data"][data_key]}

        return {
            "status": "error",
            "message": f"Problem loading response data for {data_key}",
            "response": raw_response.json(),
        }

    def get_asset(self, asset_id: str) -> Dict:
        query = """
        query getAsset($id: ID!) {
          getAsset(id: $id) {
            id
            identifier
            name
            details
            status
            deviceStatus
            coordinates {
              lat
              lon
            }
            depth
            volume    
            battery
            distanceToFluid
            ouPath      
            deviceESN
            lastLevelReport
            lastPositionReport
            lastReport
            geofences {
              id
              name
              type
            }
            createdAt
            updatedAt
          }
        }
        """
        variables = {"id": asset_id}

        return self._extract_json_response(
            self.query(query=query, variables=variables), "getAsset"
        )

    def query(self, query: str, variables: Optional[Dict] = None) -> Response:
        """ Generic GraphQL query method. Does an HTTP POST with the query and variables as parameters """
        if variables is None:
            variables = dict()
        response = self.session.request(
            url=self.lasso_api_url,
            method="POST",
            json={"query": query, "variables": variables},
        )
        return response
