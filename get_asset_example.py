import argparse
import json
from lasso_api import LassoAPI, DEFAULT_HOST


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
    # Interact with the Lasso GraphQL API
    # To use this tool you must define 2 environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY).
    # You can get these values from your Lasso technical contact.
    # """
    )

    parser.add_argument("asset_id", type=str, help="Required Asset ID")
    parser.add_argument(
        "--endpoint", type=str, help="Optional endpoint value to override the default", default=DEFAULT_HOST
    )
    args = parser.parse_args()

    api = LassoAPI(host=args.endpoint)
    # Use JSON format string for the query. It does not need reformatting.

    get_asset_result = api.get_asset(args.asset_id)
    if get_asset_result["status"] != "success":
        print(f"Error calling getAsset: {get_asset_result['message']}.\n"
              "Ensure proper AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set and "
              "configured properly in the Lasso portal")
        return

    # Print the output to the console.
    print(json.dumps(get_asset_result["data"], indent=3))


if __name__ == "__main__":
    main()
