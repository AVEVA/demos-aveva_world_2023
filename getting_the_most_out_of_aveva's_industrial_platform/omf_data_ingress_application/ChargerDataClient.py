from dataclasses import dataclass
import datetime
import random
from typing import Any

types = [
    {
        "id": "TimeIndexed.Double",
        "name": "Double",
        "classification": "dynamic",
        "type": "object",
        "properties": {
            "TimeIndexed.Double.Timestamp": {
                "format": "date-time",
                "type": "string",
                "isindex": True
            },
            "TimeIndexed.Double.Value": {
                "type": "float64"
            }
        }
    },
    {
        "id": "TimeIndexed.String",
        "name": "String",
        "classification": "dynamic",
        "type": "object",
        "properties": {
            "TimeIndexed.String.Timestamp": {
                "format": "date-time",
                "type": "string",
                "isindex": True
            },
            "TimeIndexed.String.Value": {
                "type": "string"
            }
        }
    },
    {
        "id": "TimeIndexed.Int64",
        "name": "Int64",
        "classification": "dynamic",
        "type": "object",
        "properties": {
            "TimeIndexed.Int64.Timestamp": {
                "format": "date-time",
                "type": "string",
                "isindex": True
            },
            "TimeIndexed.Int64.Value": {
                "type": "int64"
            }
        }
    }
]

chargers = [
    {
        "Id": "0061-02-02-17-C22-Webasto DX-AvgKwhDelivered",
        "Name": "0061-02-02-17-C22-Webasto DX-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.9145607Z",
                "ModifiedDate": "2023-07-17T21:34:24.9145607Z"
    },
    {
        "Id": "0061-02-02-19-C24-Webasto DX-AvgSessionIdleMin",
        "Name": "0061-02-02-19-C24-Webasto DX-AvgSessionIdleMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.9848323Z",
                "ModifiedDate": "2023-07-17T21:34:24.9848323Z"
    },
    {
        "Id": "0061-02-02-19-C24-Webasto DX-PilotSignalAmps",
        "Name": "0061-02-02-19-C24-Webasto DX-PilotSignalAmps",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.9681874Z",
                "ModifiedDate": "2023-07-17T21:34:24.9681874Z"
    },
    {
        "Id": "0061-02-02-19-C24-Webasto DX-Status",
        "Name": "0061-02-02-19-C24-Webasto DX-Status",
                "Description": "",
                "TypeId": "TimeIndexed.String",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:56:44.8347218Z",
                "ModifiedDate": "2023-07-17T21:56:44.8347218Z"
    },
    {
        "Id": "0061-02-02-19-C24-Webasto DX-GhgAvoidedLbs",
        "Name": "0061-02-02-19-C24-Webasto DX-GhgAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.9926903Z",
                "ModifiedDate": "2023-07-17T21:34:24.9926903Z"
    },
    {
        "Id": "0061-02-02-20-C29-Webasto DX-TotalCostActual",
        "Name": "0061-02-02-20-C29-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.0309014Z",
                "ModifiedDate": "2023-07-17T21:34:25.0309014Z"
    },
    {
        "Id": "0061-02-03-01-C01-Tesla-AvgKwhDelivered",
        "Name": "0061-02-03-01-C01-Tesla-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.0522019Z",
                "ModifiedDate": "2023-07-17T21:34:25.0522019Z"
    },
    {
        "Id": "0061-02-03-02-C02-Tesla-AvgChargeDurationMin",
        "Name": "0061-02-03-02-C02-Tesla-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.1103546Z",
                "ModifiedDate": "2023-07-17T21:34:25.1103546Z"
    },
    {
        "Id": "0061-02-03-02-C02-Tesla-StartedSessionCount",
        "Name": "0061-02-03-02-C02-Tesla-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.1009759Z",
        "ModifiedDate": "2023-07-18T14:41:52.2252014Z"
    },
    {
        "Id": "0061-02-03-02-C02-Tesla-TotalReturningUsers",
        "Name": "0061-02-03-02-C02-Tesla-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.1274213Z",
        "ModifiedDate": "2023-07-18T14:41:50.9217727Z"
    },
    {
        "Id": "0061-02-03-03-C03-Tesla-GhgAvoidedLbs",
        "Name": "0061-02-03-03-C03-Tesla-GhgAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.1481947Z",
                "ModifiedDate": "2023-07-17T21:34:25.1481947Z"
    },
    {
        "Id": "0061-02-03-03-C03-Tesla-PilotSignalAmps",
        "Name": "0061-02-03-03-C03-Tesla-PilotSignalAmps",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.1342765Z",
                "ModifiedDate": "2023-07-17T21:34:25.1342765Z"
    },
    {
        "Id": "0061-02-03-03-C03-Tesla-Status",
        "Name": "0061-02-03-03-C03-Tesla-Status",
                "Description": "",
                "TypeId": "TimeIndexed.String",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:56:44.8734054Z",
                "ModifiedDate": "2023-07-17T21:56:44.8734054Z"
    },
    {
        "Id": "0061-02-03-04-C04-Tesla-Status",
        "Name": "0061-02-03-04-C04-Tesla-Status",
                "Description": "",
                "TypeId": "TimeIndexed.String",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:56:44.8811166Z",
                "ModifiedDate": "2023-07-17T21:56:44.8811166Z"
    },
    {
        "Id": "0061-02-03-05-C05-Tesla-AvgKwhDelivered",
        "Name": "0061-02-03-05-C05-Tesla-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.2075671Z",
                "ModifiedDate": "2023-07-17T21:34:25.2075671Z"
    },
    {
        "Id": "0061-02-03-05-C05-Tesla-TotalUniqueUsers",
        "Name": "0061-02-03-05-C05-Tesla-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.228408Z",
        "ModifiedDate": "2023-07-18T14:41:50.7701048Z"
    },
    {
        "Id": "0061-02-03-06-C26-Webasto DX-AvgSessionDurationMin",
        "Name": "0061-02-03-06-C26-Webasto DX-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.2496364Z",
                "ModifiedDate": "2023-07-17T21:34:25.2496364Z"
    },
    {
        "Id": "0061-02-03-06-C26-Webasto DX-TotalReturningUsers",
        "Name": "0061-02-03-06-C26-Webasto DX-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.2685759Z",
        "ModifiedDate": "2023-07-18T14:41:51.6109485Z"
    },
    {
        "Id": "0061-02-03-07-C27-Tesla-AvgKwhDelivered",
        "Name": "0061-02-03-07-C27-Tesla-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.2904935Z",
                "ModifiedDate": "2023-07-17T21:34:25.2904935Z"
    },
    {
        "Id": "0061-02-03-07-C27-Tesla-StartedSessionCount",
        "Name": "0061-02-03-07-C27-Tesla-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.2809023Z",
        "ModifiedDate": "2023-07-18T14:41:50.6822823Z"
    },
    {
        "Id": "0061-02-03-08-C28-Webasto DX-TotalUniqueUsers",
        "Name": "0061-02-03-08-C28-Webasto DX-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.3596836Z",
        "ModifiedDate": "2023-07-18T14:41:51.3860054Z"
    },
    {
        "Id": "0061-02-03-08-C28-Webasto DX-PilotSignalAmps",
        "Name": "0061-02-03-08-C28-Webasto DX-PilotSignalAmps",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.3205757Z",
                "ModifiedDate": "2023-07-17T21:34:25.3205757Z"
    },
    {
        "Id": "0061-02-03-08-C28-Webasto DX-GasolineAvoidedLbs",
        "Name": "0061-02-03-08-C28-Webasto DX-GasolineAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.3413074Z",
                "ModifiedDate": "2023-07-17T21:34:25.3413074Z"
    },
    {
        "Id": "0061-02-03-08-C28-Webasto DX-MaxKwhDelivered",
        "Name": "0061-02-03-08-C28-Webasto DX-MaxKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.3322848Z",
                "ModifiedDate": "2023-07-17T21:34:25.3322848Z"
    },
    {
        "Id": "0061-02-03-09-C29-Tesla-AvgSessionIdleMin",
        "Name": "0061-02-03-09-C29-Tesla-AvgSessionIdleMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.3760584Z",
                "ModifiedDate": "2023-07-17T21:34:25.3760584Z"
    },
    {
        "Id": "0061-02-03-10-C30-Webasto DX-TotalCostActual",
        "Name": "0061-02-03-10-C30-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.4235757Z",
                "ModifiedDate": "2023-07-17T21:34:25.4235757Z"
    },
    {
        "Id": "0061-02-03-10-C30-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-02-03-10-C30-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.4171819Z",
                "ModifiedDate": "2023-07-17T21:34:25.4171819Z"
    },
    {
        "Id": "0061-02-03-11-C31-Tesla-AvgSessionDurationMin",
        "Name": "0061-02-03-11-C31-Tesla-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.4488354Z",
                "ModifiedDate": "2023-07-17T21:34:25.4488354Z"
    },
    {
        "Id": "0061-02-03-12-C32-Webasto DX-Status",
        "Name": "0061-02-03-12-C32-Webasto DX-Status",
                "Description": "",
                "TypeId": "TimeIndexed.String",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:56:44.9587746Z",
                "ModifiedDate": "2023-07-17T21:56:44.9587746Z"
    },
    {
        "Id": "0061-02-03-13-C33-Tesla-AvgSessionDurationMin",
        "Name": "0061-02-03-13-C33-Tesla-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.5210983Z",
                "ModifiedDate": "2023-07-17T21:34:25.5210983Z"
    },
    {
        "Id": "0061-02-03-13-C33-Tesla-CommutedMilesAvoided",
        "Name": "0061-02-03-13-C33-Tesla-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:25.5352728Z",
                "ModifiedDate": "2023-07-17T21:34:25.5352728Z"
    },
    {
        "Id": "0061-02-03-13-C33-Tesla-CompletedSessionCount",
        "Name": "0061-02-03-13-C33-Tesla-CompletedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:25.5118336Z",
        "ModifiedDate": "2023-07-18T14:41:52.1469406Z"
    },
    {
        "Id": "0061-02-02-16-C21-Webasto DX-TotalSiteCost",
        "Name": "0061-02-02-16-C21-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.9000354Z",
                "ModifiedDate": "2023-07-17T21:34:24.9000354Z"
    },
    {
        "Id": "0061-02-02-16-C21-Webasto DX-TotalReturningUsers",
        "Name": "0061-02-02-16-C21-Webasto DX-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.9072816Z",
        "ModifiedDate": "2023-07-18T14:41:50.3910205Z"
    },
    {
        "Id": "0061-02-02-16-C21-Webasto DX-AvgChargeDurationMin",
        "Name": "0061-02-02-16-C21-Webasto DX-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.8837766Z",
                "ModifiedDate": "2023-07-17T21:34:24.8837766Z"
    },
    {
        "Id": "0061-02-02-16-C21-Webasto DX-GasolineAvoidedLbs",
        "Name": "0061-02-02-16-C21-Webasto DX-GasolineAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.8924285Z",
                "ModifiedDate": "2023-07-17T21:34:24.8924285Z"
    },
    {
        "Id": "0061-02-02-15-C20-Webasto DX-StartedSessionCount",
        "Name": "0061-02-02-15-C20-Webasto DX-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.8417448Z",
        "ModifiedDate": "2023-07-18T14:41:50.0277533Z"
    },
    {
        "Id": "0061-02-02-15-C20-Webasto DX-TotalSiteCost",
        "Name": "0061-02-02-15-C20-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.8626865Z",
                "ModifiedDate": "2023-07-17T21:34:24.8626865Z"
    },
    {
        "Id": "0061-02-02-15-C20-Webasto DX-TotalMicrosessions",
        "Name": "0061-02-02-15-C20-Webasto DX-TotalMicrosessions",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.8696802Z",
        "ModifiedDate": "2023-07-18T14:41:50.3133586Z"
    },
    {
        "Id": "0061-02-02-15-C20-Webasto DX-AvgChargeDurationMin",
        "Name": "0061-02-02-15-C20-Webasto DX-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.8507838Z",
                "ModifiedDate": "2023-07-17T21:34:24.8507838Z"
    },
    {
        "Id": "0061-02-02-14-C19-Tesla-CommutedMilesAvoided",
        "Name": "0061-02-02-14-C19-Tesla-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.8278253Z",
                "ModifiedDate": "2023-07-17T21:34:24.8278253Z"
    },
    {
        "Id": "0061-02-02-12-C17-Webasto DX-PilotSignalAmps",
        "Name": "0061-02-02-12-C17-Webasto DX-PilotSignalAmps",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.7294772Z",
                "ModifiedDate": "2023-07-17T21:34:24.7294772Z"
    },
    {
        "Id": "0061-02-02-12-C17-Webasto DX-TotalCostActual",
        "Name": "0061-02-02-12-C17-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.7576363Z",
                "ModifiedDate": "2023-07-17T21:34:24.7576363Z"
    },
    {
        "Id": "0061-02-02-12-C17-Webasto DX-AvgSessionDurationMin",
        "Name": "0061-02-02-12-C17-Webasto DX-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.7427442Z",
                "ModifiedDate": "2023-07-17T21:34:24.7427442Z"
    },
    {
        "Id": "0061-02-02-12-C17-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-02-02-12-C17-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.7508995Z",
                "ModifiedDate": "2023-07-17T21:34:24.7508995Z"
    },
    {
        "Id": "0061-02-02-10-C15-Tesla-Status",
        "Name": "0061-02-02-10-C15-Tesla-Status",
                "Description": "",
                "TypeId": "TimeIndexed.String",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:56:44.7460179Z",
                "ModifiedDate": "2023-07-17T21:56:44.7460179Z"
    },
    {
        "Id": "0061-02-02-10-C15-Tesla-AvgChargeDurationMin",
        "Name": "0061-02-02-10-C15-Tesla-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.6671254Z",
                "ModifiedDate": "2023-07-17T21:34:24.6671254Z"
    },
    {
        "Id": "0061-02-02-08-C13-Webasto DX-TotalSiteCost",
        "Name": "0061-02-02-08-C13-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.6127248Z",
                "ModifiedDate": "2023-07-17T21:34:24.6127248Z"
    },
    {
        "Id": "0061-02-02-08-C13-Webasto DX-TotalKwhDelivered",
        "Name": "0061-02-02-08-C13-Webasto DX-TotalKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.5899453Z",
                "ModifiedDate": "2023-07-17T21:34:24.5899453Z"
    },
    {
        "Id": "0061-02-02-08-C13-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-02-02-08-C13-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.6062181Z",
                "ModifiedDate": "2023-07-17T21:34:24.6062181Z"
    },
    {
        "Id": "0061-02-02-06-C11-Tesla-TotalCostActual",
        "Name": "0061-02-02-06-C11-Tesla-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.5253526Z",
                "ModifiedDate": "2023-07-17T21:34:24.5253526Z"
    },
    {
        "Id": "0061-02-02-06-C11-Tesla-CompletedSessionCount",
        "Name": "0061-02-02-06-C11-Tesla-CompletedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.5062436Z",
        "ModifiedDate": "2023-07-18T14:41:51.6742458Z"
    },
    {
        "Id": "0061-02-02-06-C11-Tesla-AvgChargeDurationMin",
        "Name": "0061-02-02-06-C11-Tesla-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.5155042Z",
                "ModifiedDate": "2023-07-17T21:34:24.5155042Z"
    },
    {
        "Id": "0061-02-02-05-C10-Webasto DX-AvgKwhDelivered",
        "Name": "0061-02-02-05-C10-Webasto DX-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.4754939Z",
                "ModifiedDate": "2023-07-17T21:34:24.4754939Z"
    },
    {
        "Id": "0061-02-02-04-C09-Webasto DX-TotalUniqueUsers",
        "Name": "0061-02-02-04-C09-Webasto DX-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.4690108Z",
        "ModifiedDate": "2023-07-18T14:41:51.1872288Z"
    },
    {
        "Id": "0061-02-02-04-C09-Webasto DX-TotalMicrosessions",
        "Name": "0061-02-02-04-C09-Webasto DX-TotalMicrosessions",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.4600572Z",
        "ModifiedDate": "2023-07-18T14:41:52.5456865Z"
    },
    {
        "Id": "0061-02-02-04-C09-Webasto DX-AvgSessionIdleMin",
        "Name": "0061-02-02-04-C09-Webasto DX-AvgSessionIdleMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.4468963Z",
                "ModifiedDate": "2023-07-17T21:34:24.4468963Z"
    },
    {
        "Id": "0061-02-02-04-C09-Webasto DX-TotalCostActual",
        "Name": "0061-02-02-04-C09-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.4535288Z",
                "ModifiedDate": "2023-07-17T21:34:24.4535288Z"
    },
    {
        "Id": "0061-02-02-03-C08-Tesla-CompletedSessionCount",
        "Name": "0061-02-02-03-C08-Tesla-CompletedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.387037Z",
        "ModifiedDate": "2023-07-18T14:41:52.4693122Z"
    },
    {
        "Id": "0061-02-02-02-C07-Webasto DX-AvgKwhDelivered",
        "Name": "0061-02-02-02-C07-Webasto DX-AvgKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:34:24.3620694Z",
                "ModifiedDate": "2023-07-17T21:34:24.3620694Z"
    },
    {
        "Id": "0061-02-02-02-C07-Webasto DX-StartedSessionCount",
        "Name": "0061-02-02-02-C07-Webasto DX-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.3552476Z",
        "ModifiedDate": "2023-07-18T14:41:51.0428684Z"
    },
    {
        "Id": "0061-02-02-01-C06-Tesla-TotalMicrosessions",
        "Name": "0061-02-02-01-C06-Tesla-TotalMicrosessions",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:34:24.3446382Z",
        "ModifiedDate": "2023-07-18T14:41:51.2654474Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-TotalSiteCost",
        "Name": "0061-01-04-15-T12-Tesla-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5964352Z",
                "ModifiedDate": "2023-07-17T21:12:42.5964352Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-TotalReturningUsers",
        "Name": "0061-01-04-15-T12-Tesla-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.6022984Z",
        "ModifiedDate": "2023-07-18T14:41:53.0213926Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-StartedSessionCount",
        "Name": "0061-01-04-15-T12-Tesla-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.5691776Z",
        "ModifiedDate": "2023-07-18T14:41:52.6101527Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-MaxKwhDelivered",
        "Name": "0061-01-04-15-T12-Tesla-MaxKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5747615Z",
                "ModifiedDate": "2023-07-17T21:12:42.5747615Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-GasolineAvoidedLbs",
        "Name": "0061-01-04-15-T12-Tesla-GasolineAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5851715Z",
                "ModifiedDate": "2023-07-17T21:12:42.5851715Z"
    },
    {
        "Id": "0061-01-04-15-T12-Tesla-CommutedMilesAvoided",
        "Name": "0061-01-04-15-T12-Tesla-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5909553Z",
                "ModifiedDate": "2023-07-17T21:12:42.5909553Z"
    },
    {
        "Id": "0061-01-04-14-T11-Tesla-TotalUniqueUsers",
        "Name": "0061-01-04-14-T11-Tesla-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.5633619Z",
        "ModifiedDate": "2023-07-18T14:41:51.9966959Z"
    },
    {
        "Id": "0061-01-04-14-T11-Tesla-MaxKwhDelivered",
        "Name": "0061-01-04-14-T11-Tesla-MaxKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5428289Z",
                "ModifiedDate": "2023-07-17T21:12:42.5428289Z"
    },
    {
        "Id": "0061-01-04-14-T11-Tesla-AvgSessionDurationMin",
        "Name": "0061-01-04-14-T11-Tesla-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5484227Z",
                "ModifiedDate": "2023-07-17T21:12:42.5484227Z"
    },
    {
        "Id": "0061-01-04-13-T10-Tesla-TotalUniqueUsers",
        "Name": "0061-01-04-13-T10-Tesla-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.5311063Z",
        "ModifiedDate": "2023-07-18T14:41:50.6081464Z"
    },
    {
        "Id": "0061-01-04-13-T10-Tesla-StartedSessionCount",
        "Name": "0061-01-04-13-T10-Tesla-StartedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.5052646Z",
        "ModifiedDate": "2023-07-18T14:41:51.5274604Z"
    },
    {
        "Id": "0061-01-04-13-T10-Tesla-GasolineAvoidedLbs",
        "Name": "0061-01-04-13-T10-Tesla-GasolineAvoidedLbs",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5224123Z",
                "ModifiedDate": "2023-07-17T21:12:42.5224123Z"
    },
    {
        "Id": "0061-01-04-13-T10-Tesla-AvgSessionDurationMin",
        "Name": "0061-01-04-13-T10-Tesla-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5167258Z",
                "ModifiedDate": "2023-07-17T21:12:42.5167258Z"
    },
    {
        "Id": "0061-01-04-13-T10-Tesla-AvgChargeDurationMin",
        "Name": "0061-01-04-13-T10-Tesla-AvgChargeDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.5108566Z",
                "ModifiedDate": "2023-07-17T21:12:42.5108566Z"
    },
    {
        "Id": "0061-01-04-12-T9-Tesla-TotalUniqueUsers",
        "Name": "0061-01-04-12-T9-Tesla-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.4932528Z",
        "ModifiedDate": "2023-07-18T14:41:49.9705512Z"
    },
    {
        "Id": "0061-01-04-12-T9-Tesla-TotalReturningUsers",
        "Name": "0061-01-04-12-T9-Tesla-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.499721Z",
        "ModifiedDate": "2023-07-18T14:41:52.691078Z"
    },
    {
        "Id": "0061-01-04-03-H3-Webasto DX-AvgSessionIdleMin",
        "Name": "0061-01-04-03-H3-Webasto DX-AvgSessionIdleMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.4479537Z",
                "ModifiedDate": "2023-07-17T21:12:42.4479537Z"
    },
    {
        "Id": "0061-01-04-03-H3-Webasto DX-TotalCostActual",
        "Name": "0061-01-04-03-H3-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.454313Z",
                "ModifiedDate": "2023-07-17T21:12:42.454313Z"
    },
    {
        "Id": "0061-01-04-03-H3-Webasto DX-AvgSessionDurationMin",
        "Name": "0061-01-04-03-H3-Webasto DX-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.4407564Z",
                "ModifiedDate": "2023-07-17T21:12:42.4407564Z"
    },
    {
        "Id": "0061-01-04-03-H3-Webasto DX-TotalReturningUsers",
        "Name": "0061-01-04-03-H3-Webasto DX-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.4600351Z",
        "ModifiedDate": "2023-07-18T14:41:50.4674189Z"
    },
    {
        "Id": "0061-01-04-03-H3-Webasto DX-TotalKwhDelivered",
        "Name": "0061-01-04-03-H3-Webasto DX-TotalKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.4319204Z",
                "ModifiedDate": "2023-07-17T21:12:42.4319204Z"
    },
    {
        "Id": "0061-01-04-02-H2-Webasto DX-AvgSessionDurationMin",
        "Name": "0061-01-04-02-H2-Webasto DX-AvgSessionDurationMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.4023577Z",
                "ModifiedDate": "2023-07-17T21:12:42.4023577Z"
    },
    {
        "Id": "0061-01-04-02-H2-Webasto DX-TotalReturningUsers",
        "Name": "0061-01-04-02-H2-Webasto DX-TotalReturningUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.4241445Z",
        "ModifiedDate": "2023-07-18T14:41:53.0950319Z"
    },
    {
        "Id": "0061-01-04-01-H1-Webasto DX-TotalSiteCost",
        "Name": "0061-01-04-01-H1-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.3745431Z",
                "ModifiedDate": "2023-07-17T21:12:42.3745431Z"
    },
    {
        "Id": "0061-01-04-01-H1-Webasto DX-AvgSessionIdleMin",
        "Name": "0061-01-04-01-H1-Webasto DX-AvgSessionIdleMin",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.3662611Z",
                "ModifiedDate": "2023-07-17T21:12:42.3662611Z"
    },
    {
        "Id": "0061-01-03-39-W24-Webasto DX-TotalKwhDelivered",
        "Name": "0061-01-03-39-W24-Webasto DX-TotalKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.3089485Z",
                "ModifiedDate": "2023-07-17T21:12:42.3089485Z"
    },
    {
        "Id": "0061-01-03-39-W24-Webasto DX-TotalSiteCost",
        "Name": "0061-01-03-39-W24-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.3347416Z",
                "ModifiedDate": "2023-07-17T21:12:42.3347416Z"
    },
    {
        "Id": "0061-01-03-38-W23-Webasto DX-TotalKwhDelivered",
        "Name": "0061-01-03-38-W23-Webasto DX-TotalKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2714715Z",
                "ModifiedDate": "2023-07-17T21:12:42.2714715Z"
    },
    {
        "Id": "0061-01-03-37-W22-Webasto DX-TotalSiteCost",
        "Name": "0061-01-03-37-W22-Webasto DX-TotalSiteCost",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2628774Z",
                "ModifiedDate": "2023-07-17T21:12:42.2628774Z"
    },
    {
        "Id": "0061-01-03-37-W22-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-01-03-37-W22-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2566647Z",
                "ModifiedDate": "2023-07-17T21:12:42.2566647Z"
    },
    {
        "Id": "0061-01-03-37-W22-Webasto DX-MaxKwhDelivered",
        "Name": "0061-01-03-37-W22-Webasto DX-MaxKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2466481Z",
                "ModifiedDate": "2023-07-17T21:12:42.2466481Z"
    },
    {
        "Id": "0061-01-03-37-W22-Webasto DX-TotalKwhDelivered",
        "Name": "0061-01-03-37-W22-Webasto DX-TotalKwhDelivered",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2397028Z",
                "ModifiedDate": "2023-07-17T21:12:42.2397028Z"
    },
    {
        "Id": "0061-01-03-36-W21-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-01-03-36-W21-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.2183053Z",
                "ModifiedDate": "2023-07-17T21:12:42.2183053Z"
    },
    {
        "Id": "0061-01-03-35-W20-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-01-03-35-W20-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.1807267Z",
                "ModifiedDate": "2023-07-17T21:12:42.1807267Z"
    },
    {
        "Id": "0061-01-03-35-W20-Webasto DX-TotalUniqueUsers",
        "Name": "0061-01-03-35-W20-Webasto DX-TotalUniqueUsers",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.1930777Z",
        "ModifiedDate": "2023-07-18T14:41:52.39351Z"
    },
    {
        "Id": "0061-01-03-35-W20-Webasto DX-TotalCostActual",
        "Name": "0061-01-03-35-W20-Webasto DX-TotalCostActual",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.1871862Z",
                "ModifiedDate": "2023-07-17T21:12:42.1871862Z"
    },
    {
        "Id": "0061-01-03-34-W19-Webasto DX-CompletedSessionCount",
        "Name": "0061-01-03-34-W19-Webasto DX-CompletedSessionCount",
                "Description": "",
                "TypeId": "TimeIndexed.Int64",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": [
                    {
                        "SdsTypePropertyId": "Value",
                        "Uom": None,
                        "InterpolationMode": 1
                    }
                ],
        "CreatedDate": "2023-07-17T21:12:42.1284914Z",
        "ModifiedDate": "2023-07-18T14:41:50.9839321Z"
    },
    {
        "Id": "0061-01-03-34-W19-Webasto DX-CommutedMilesAvoided",
        "Name": "0061-01-03-34-W19-Webasto DX-CommutedMilesAvoided",
                "Description": "",
                "TypeId": "TimeIndexed.Double",
                "Indexes": None,
                "InterpolationMode": None,
                "ExtrapolationMode": None,
                "PropertyOverrides": None,
                "CreatedDate": "2023-07-17T21:12:42.1472247Z",
                "ModifiedDate": "2023-07-17T21:12:42.1472247Z"
    }
]

to_send = {charger.get('Id'): datetime.datetime.utcnow().replace(
    second=0, microsecond=0) for charger in chargers}

statuses = ['UNPLUGGED', 'IDLE', 'NOT CHARGING',
            'ADAPTIVE', 'DISABLED_CHARGER']


@dataclass
class ChargerData(object):
    Id: str
    Timestamp: str
    Value: float | str


class ChargerDataClient(object):
    """Example client to simulate communication with Charger Data source"""

    def getStreams(self) -> list[dict[str, str]]:
        return [self.__getStreamFromId(charger) for charger in chargers]

    def getTypes(self) -> list[dict[str, str]]:
        return types

    def getData(self, id: str) -> list[ChargerData]:
        queue = []
        type_id = next(charger.get('TypeId')
                       for charger in chargers if charger.get('Id') == id)
        while to_send[id] < datetime.datetime.utcnow():
            value = None
            if type_id == 'TimeIndexed.Double':
                value = 100 * random.random()
            elif type_id == 'TimeIndexed.Int64':
                value = int(100 * random.random())
            else:
                value = statuses[random.randint(0, 4)]
            queue.append(ChargerData(id, to_send[id].isoformat() + 'Z', value))
            to_send[id] += datetime.timedelta(milliseconds=250)
        return queue

    def __getStreamFromId(self, charger: dict) -> dict[str, str]:
        return {'id': charger.get('Id'), 'typeid': charger.get('TypeId'), 'name': charger.get('Name')}
