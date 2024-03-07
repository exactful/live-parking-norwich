"""Module providing a class to retrieve car park data from an XML feed."""

from urllib.request import urlopen
from urllib.error import URLError
from xml.etree import ElementTree
from datetime import datetime
from traceback import format_tb
from re import sub

from .config import Config
from .structures import RawCarPark, CarPark

class LiveParkingNorwich():
    """
    Class to retrieve car park data from an XML feed.

    Attributes:
    - last_updated (datetime): The timestamp of the last data update.
    - success (bool): A flag indicating the success of the data retrieval process.
    - error_message (str): A message describing any error encountered during data retrieval.
    - traceback (list[str]): A list containing the traceback information in case of an error.
    """

    def __init__(self) -> None:
        """
        Initializes a Usage object with default attributes.
        """
        self.__url = Config.XML_URL
        self.__namespace = Config.XML_NAMESPACE
        self.__last_updated = None
        self.__success = None
        self.__error_message = None
        self.__traceback = None

    @property
    def last_updated(self) -> datetime:
        """
        Getter method for the last_updated attribute.

        Returns:
        - datetime: The timestamp of the last data update.
        """
        return self.__last_updated

    @property
    def success(self) -> bool:
        """
        Getter method for the success attribute.

        Returns:
        - bool: A flag indicating the success of the data retrieval process.
        """
        return self.__success

    @property
    def error_message(self) -> str:
        """
        Getter method for the error_message attribute.

        Returns:
        - str: A message describing any error encountered during data retrieval.
        """
        return self.__error_message

    @property
    def traceback(self) -> list[str]:
        """
        Getter method for the traceback attribute.

        Returns:
        - list[str]: A list containing the traceback information in case of an error.
        """
        return self.__traceback

    @staticmethod
    def _retrieve_xml_data(url) -> bytes:
        """
        Retrieves the XML data from the given URL; internal method.

        Args:
        - url (str): The URL of the XML feed.

        Returns:
        - bytes: The raw XML data.

        Raises:
        - URLError: If an error occurs while retrieving the XML data.
        """
        try:
            with urlopen(url) as response:
                xml_data = response.read()
                return xml_data
        except URLError as e:
            raise URLError(f"Failed to retrieve XML data from {url}: {e.reason}")

    @staticmethod
    def _parse_xml_data(xml_data: bytes, namespace: str) -> list[RawCarPark]:
        """
        Parses the raw XML data and extracts car park information; internal method.

        Args:
        - xml_data (bytes): The raw XML data.
        - namespace (str): The XML namespace mapping.

        Returns:
        - list[RawCarPark]: A list of named tuples containing the extracted car park data.
        """
        root = ElementTree.fromstring(xml_data)

        # Get the publication time and convert to datetime
        publication_time = root.find(".//d2lm:publicationTime", namespace).text
        last_updated = datetime.strptime(publication_time, Config.DATE_FORMAT)

        car_park_data = []

        # Iterate through each car park
        for situation in root.findall(".//d2lm:payloadPublication/d2lm:situation", namespace):
            for situation_record in situation.findall("d2lm:situationRecord", namespace):

                # Extract details
                identity = situation_record.find("d2lm:carParkIdentity", namespace).text
                status = situation_record.find("d2lm:carParkStatus", namespace).text
                occupied_spaces = int(situation_record.find("d2lm:occupiedSpaces", namespace).text)
                total_capacity = int(situation_record.find("d2lm:totalCapacity", namespace).text)
                occupancy = float(situation_record.find("d2lm:carParkOccupancy", namespace).text)

                car_park_data.append(RawCarPark(identity, status, occupied_spaces, total_capacity, occupancy))

        return car_park_data, last_updated

    @staticmethod
    def _transform_data_to_car_parks(car_park_data: list[RawCarPark]) -> list[CarPark]:
        """
        Transforms the extracted car park data into a list of CarPark objects; internal method.

        Args:
        - car_park_data (list[RawCarPark]): A list of named tuples containing the extracted car park data.

        Returns:
        - list[CarPark]: A list of CarPark objects.
        """
        car_parks = []

        for data in car_park_data:

            # Split the identity to capture the code and name
            identity_parts = data.identity.split(":")
            code = identity_parts[1] # "CPN0015"
            name = identity_parts[0] # "Harford, Ipswich Road, Norwich"

            # Fix truncated names with "Nor", "NORW" and "Norwic"
            name = sub(r'Nor(?:wic)?\b', 'Norwich', name)
            name = sub(r'NORW\b', 'NORWICH', name)

            # Calc remaining spaces
            remaining_spaces = data.total_capacity - data.occupied_spaces

            # Create CarPark object and add to list
            car_parks.append(CarPark(code, name, data.status, data.occupied_spaces, remaining_spaces, data.total_capacity, data.occupancy))

        return car_parks

    def refresh(self) -> list[CarPark]:
        """
        Refreshes the car park data from an XML feed.

        Returns:
        - list[CarPark]: A list of CarPark objects representing the car park data.
        """

        try:

            # Get XML data
            xml = LiveParkingNorwich._retrieve_xml_data(self.__url)

            # Parse XML data
            car_park_data, self.__last_updated = LiveParkingNorwich._parse_xml_data(xml, self.__namespace)

            # Transform car park data
            car_parks = LiveParkingNorwich._transform_data_to_car_parks(car_park_data)

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
