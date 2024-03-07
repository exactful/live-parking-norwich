from urllib.request import urlopen
from urllib.error import URLError
from xml.etree import ElementTree
from datetime import datetime
from re import sub

from .structures import RawCarPark, CarPark

class XMLDataRetriever():
    """A class for retrieving XML car park data from a given URL."""

    def __init__(self, url) -> None:
        """Initialises an XMLDataRetriever object."""
        self.__url = url

    def retrieve_xml_data(self) -> bytes:
        """Retrieves the XML car park data from a URL.

        Returns:
            bytes: The raw XML data.

        Raises:
            URLError: If an error occurs while retrieving the XML data.
        """
        try:
            with urlopen(self.__url) as response:
                xml_data = response.read()
                return xml_data
        except URLError as e:
            raise URLError(f"Failed to retrieve XML data from {self.__url}: {e.reason}")

class XMLDataParser():
    """A class for parsing XML car park data."""

    def __init__(self, namespace, date_format) -> None:
        """Initialises an XMLDataParser object."""
        self.__namespace = namespace
        self.__date_format = date_format

    def parse_xml_data(self, xml: bytes) -> list[RawCarPark]:
        """Parses the raw XML car park data and extracts car park information.

        Args:
            xml (bytes): The raw XML data.

        Returns:
            list[RawCarPark]: A list of named tuples containing the extracted car park data.
        """
        root = ElementTree.fromstring(xml)

        # Get the publication time and convert to datetime
        publication_time = root.find(".//d2lm:publicationTime", self.__namespace).text
        last_updated = datetime.strptime(publication_time, self.__date_format)

        car_park_data = []

        # Iterate through each car park
        for situation in root.findall(".//d2lm:payloadPublication/d2lm:situation", self.__namespace):
            for situation_record in situation.findall("d2lm:situationRecord", self.__namespace):

                # Extract details
                identity = situation_record.find("d2lm:carParkIdentity", self.__namespace).text
                status = situation_record.find("d2lm:carParkStatus", self.__namespace).text
                occupied_spaces = int(situation_record.find("d2lm:occupiedSpaces", self.__namespace).text)
                total_capacity = int(situation_record.find("d2lm:totalCapacity", self.__namespace).text)
                occupancy = float(situation_record.find("d2lm:carParkOccupancy", self.__namespace).text)

                car_park_data.append(RawCarPark(identity, status, occupied_spaces, total_capacity, occupancy))

        return car_park_data, last_updated

class CarParkTransformer():
    """A class for transforming the extracted car park data."""

    def transform_data_to_car_parks(self, car_park_data: list[RawCarPark]) -> list[CarPark]:
        """Transforms the extracted car park data into a list of CarPark objects.

        Args:
            car_park_data (list[RawCarPark]): A list of named tuples containing the extracted car park data.

        Returns:
            list[CarPark]: A list of CarPark objects.
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
