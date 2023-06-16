# Introduction to the Lasso API

The Lasso API understands [GraphQL](https://graphql.org/). GraphQL is a query language for APIs that provides a complete
and understandable description of the data in the API, and gives clients the power to ask for exactly what they need and
nothing more. There are several popular Python libraries for GraphQL, however the included example relies on directly
POSTing GraphQL queries to the endpoint. For demonstration purposes, each of the supported queries are included in
the `LassoAPI` class contained in the `lasso_api.py` file. The `get_asset_example.py`
file demonstrates basic usage of the example class, and you are free to experiment using the provided documentation as a
guide.

# Endpoint

The endpoint for Lasso's API is:

https://y47qt5w6bzh3xpzmxosmv5x3re.appsync-api.us-west-2.amazonaws.com/graphql

Calls to the endpoint must be signed with an AWS SIG V4 signature. The signature process is the same as that used by
AWS when authenticating users using IAM. The appropriate Access Key ID and Secret Access Key will be provided to you by Lasso.
The `lasso_api.py` script included with these docs details the procedure needed to call the API. This script leverages
the `requests` and `AWS4Auth` libraries. A sample `requirements.txt` file is included as well.

# Schema

Please refer to the `schema.graphql` file for a complete schema definition of available endpoints in the Lasso API.

## Model Types

### Asset
```graphql
type Asset {
  id: String!
  name: String!
  identifier: String!
  details: String
  status: String
  deviceStatus: String    
  coordinates: Coordinates
  depth: Float
  volume: Float
  battery: Float
  distanceToFluid: Float
  ouPath: String!
  deviceESN: String
  lastReport: String
  lastPositionReport: String
  lastLevelReport: String
  geofences: [LightweightGeofence]
  createdAt: String!
  updatedAt: String!
}
```
The Asset type is the central data element on the Lasso platform.  It represents a unique piece of equipment that a
tracking device is attached to at any given time.

### Asset Elements
- id – System-generated ID for the asset, used internally as the key for all item level operations.
- name – Name of the asset.
- identifier - Customer identifier for the asset
- ouPath – String representation of the assigned “Path” of the asset within a customer organization.
- deviceESN – Electronic Serial Number (ESN) of the tracking device attached to the asset.  An asset can exist without an assigned tracking device.
- status - "OK", "Warning", "Issue", or "None".  This value depends on the asset configuration.  Contact your Lasso representative for details
- deviceStatus - A textual description of the device health, indicating when there is missing or out-of-date telemetry or position data.
- details – additional textual data supplied by the customer.
- coordinates – Latitude / Longitude coordinates most recently recorded
- geofences – Names and type information about any geofences that the asset is within based on most recent position data
- depth – Most recent depth value for the asset according to the most recent device telemetry
- volume – Most recent volume value for the asset according to the most recent device telemetry.  Expressed in the unit of measure (i.e. Gallons) according to the device configuration.
- battery – Most recent battery voltage sent from the device 
- distanceToFluid – Most recent “distance to fluid” sent from the asset according to the most recent device telemetry
- lastReport – UTC Time last received data of any kind from the device associated with the asset
- lastPositionReport –  UTC Time last received GPS position data from the device associated with the asset
- lastLevelReport – UTC Time last received level telemetry data from the device associated with the asset


## Queries

### getAsset

**Description:**
The getAsset query takes a single parameter representing the system-generated ID for the asset and will return full 
details about the asset.

**Request:**

```graphql
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
```

**Response:**
The Lasso API getAsset endpoint will return a JSON string in the manner requested by the client that will resemble the
following:

```json
{
    "data": {
        "getAsset": {
            "id": "e695f67c-d3b8-46f9-a6e3-8dcd19fb34ba",
            "identifier": "lso-6fh-4wx-bx4",
            "name": "Offshore Tank #1",
            "details": null,
            "status": "None",
            "deviceStatus": "OK",
            "coordinates": {
                "lat": 28.6496,
                "lon": -92.0701
            },
            "depth": 60.1,
            "volume": 481.0,
            "battery": 7.300000000000001,
            "distanceToFluid": 9.8,
            "ouPath": "OU-SAMPLE",
            "deviceESN": "0-4246000",
            "lastLevelReport": "2023-04-19T16:13:29.000Z",
            "lastPositionReport": "2023-04-19T09:25:41.000Z",
            "lastReport": "2023-04-19T16:13:29.000Z",
            "geofences": [
                {
                    "id": 33938,
                    "name": "2533-E",
                    "type": "GOM Platform"
                },
                {
                    "id": 1643,
                    "name": "SM69",
                    "type": "GOM Lease Block"
                }
            ],
            "createdAt": "2023-02-04T00:41:03.064Z",
            "updatedAt": "2023-04-19T16:18:45.962Z"
        }
    }
}
```


