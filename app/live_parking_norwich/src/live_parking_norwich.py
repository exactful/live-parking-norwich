"""Module providing a function to retrieve car park data from an XML feed."""

from urllib.request import urlopen
from xml.etree import ElementTree
from datetime import datetime
from traceback import format_tb
from re import sub

from .config import Config
from .carpark import CarPark

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

    def refresh(self) -> list[CarPark]:
        """
        Refreshes the car park data from an XML feed.

        Returns:
        - list[CarPark]: A list of CarPark objects representing the car park data.
        """

        try:

            # Open URL
            with urlopen(self.__url) as response:

                # Read XML document and convert to XML tree
                xml = response.read()
                root = ElementTree.fromstring(xml)

                # Get the publication time and convert to datetime
                publication_time = root.find(".//d2lm:publicationTime", self.__namespace).text # E.g. 2024-02-10T12:19:24
                self.__last_updated = datetime.strptime(publication_time, Config.DATE_FORMAT) # 2024-02-10 12:19:24

                # Define data structure hold CarPark() objects
                car_parks = []

                # Iterate through each car park
                for situation in root.findall(".//d2lm:payloadPublication/d2lm:situation", self.__namespace):

                    for situation_record in situation.findall("d2lm:situationRecord", self.__namespace):

                        # Extract details
                        identity = situation_record.find("d2lm:carParkIdentity", self.__namespace).text # E.g. "Harford, Ipswich Road, Norwich:CPN0015"
                        status = situation_record.find("d2lm:carParkStatus", self.__namespace).text # E.g. "enoughSpacesAvailable"
                        occupied_spaces = int(situation_record.find("d2lm:occupiedSpaces", self.__namespace).text) # E.g. 128
                        total_capacity = int(situation_record.find("d2lm:totalCapacity", self.__namespace).text) # E.g. 798
                        occupancy = float(situation_record.find("d2lm:carParkOccupancy", self.__namespace).text) # E.g. 16.0

                        # Split the identity to capture the code and name
                        identity_parts = identity.split(":")
                        code = identity_parts[1] # "CPN0015"
                        name = identity_parts[0] # "Harford, Ipswich Road, Norwich"

                        # Fix truncated names with "Nor", "NORW" and "Norwic"
                        name = sub(r'Nor(?:wic)?\b', 'Norwich', name)
                        name = sub(r'NORW\b', 'NORWICH', name)

                        # Calc remaining spaces
                        remaining_spaces = total_capacity - occupied_spaces # 670

                        # Add CarPark object to list
                        car_parks.append(CarPark(code, name, status, occupied_spaces, remaining_spaces, total_capacity, occupancy))

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
