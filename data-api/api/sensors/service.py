"""Service layer for the API."""
from typing import Protocol

import pymongo
from api.query import MongoQueryFilter
from api.sensors.models import SensorData
from kink import inject
from pymongo.collection import Collection


class ISensorService(Protocol):
    def get_sensor_data(self, filters: dict) -> list[SensorData]:
        ...


@inject(alias=ISensorService)
class TemperatureService:
    def __init__(self, sensors_collection: Collection, mongo_query_filter: MongoQueryFilter = MongoQueryFilter()):
        self.__sensors_collection = sensors_collection
        self.__mongo_query_filter = mongo_query_filter

    def _run_query(self, mongo_query: dict, limit: int) -> list[SensorData]:
        cursor = self.__sensors_collection.find(mongo_query).limit(
            limit).sort("timestamp", pymongo.DESCENDING)
        return [SensorData(**doc) for doc in cursor]

    def get_sensor_data(self, filters: dict = None, limit: int = 100) -> list[SensorData]:
        """Queries the database for sensor data in a given time range or area.

        Args:
            filters (dict): The filters to be applied to the query.

        Returns:
            list[SensorData]: The list of sensor data to be serialized and sent to the client.
        """
        mongo_query_filters = {}
        if not filters:
            return self._run_query(mongo_query_filters, limit)

        if "limit" in filters:
            limit = int(filters["limit"])
            del filters["limit"]
        mongo_query_filters = self.__mongo_query_filter.build_from_filters(
            filters)
        return self._run_query(mongo_query_filters, limit)
