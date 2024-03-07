"""Module providing a class to retrieve car park data from an XML feed."""

from datetime import datetime
from traceback import format_tb

from .config import Config
from .helpers import XMLDataRetriever, XMLDataParser, CarParkTransformer
from .structures import CarPark

class LiveParkingNorwich():
    """Class to retrieve car park data from an XML feed.

    Properties:
        last_updated (datetime): The timestamp of the last data update.
        success (bool): A flag indicating the success of the data retrieval process.
        error_message (str): A message describing any error encountered during data retrieval.
        traceback (list[str]): A list containing the traceback information in case of an error.
    """

    def __init__(self) -> None:
        """Initialises an object with default attributes."""
        self.__data_retriever = XMLDataRetriever(Config.XML_URL)
        self.__data_parser = XMLDataParser(Config.XML_NAMESPACE, Config.DATE_FORMAT)
        self.__data_transformer = CarParkTransformer()

        self.__last_updated = None
        self.__success = None
        self.__error_message = None
        self.__traceback = None

    @property
    def last_updated(self) -> datetime:
        """Getter method for the last_updated attribute.

        Returns:
            datetime: The timestamp of the last data update.
        """
        return self.__last_updated

    @property
    def success(self) -> bool:
        """Getter method for the success attribute.

        Returns:
            bool: A flag indicating the success of the data retrieval process.
        """
        return self.__success

    @property
    def error_message(self) -> str:
        """Getter method for the error_message attribute.

        Returns:
            str: A message describing any error encountered during data retrieval.
        """
        return self.__error_message

    @property
    def traceback(self) -> list[str]:
        """Getter method for the traceback attribute.

        Returns:
            list[str]: A list containing the traceback information in case of an error.
        """
        return self.__traceback

    def refresh(self) -> list[CarPark]:
        """Refreshes the car park data from an XML feed.

        Returns:
            list[CarPark]: A list of CarPark objects representing the car park data.
        """
        try:

            # Get XML data
            xml = self.__data_retriever.retrieve_xml_data()

            # Parse XML data
            car_park_data, self.__last_updated = self.__data_parser.parse_xml_data(xml)

            # Transform car park data
            car_parks = self.__data_transformer.transform_data_to_car_parks(car_park_data)

            # Set success
            self.__success = True
            self.__error_message = ""
            self.__traceback = ""

            # Return list of CarPark objects
            return car_parks

        except Exception as e:

            # Set failure
            self.__success = False
            self.__error_message = f"{type(e).__name__}: {e}"
            self.__traceback = format_tb(e.__traceback__)

            # Return empty list
            return []
