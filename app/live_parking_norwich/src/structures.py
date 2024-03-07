"""Module containing the CarPark class for representing car park details."""

from typing import NamedTuple

class RawCarPark(NamedTuple):
    """A named tuple representing the raw data of a car park.

    Attributes:
        identity (str): The identity string of the car park, typically containing the name and code.
        status (str): The status of the car park, e.g., "enoughSpacesAvailable".
        occupied_spaces (int): The number of occupied spaces in the car park.
        total_capacity (int): The total capacity of the car park.
        occupancy (float): The occupancy rate of the car park, expressed as a percentage.
    """

    identity: str
    status: str
    occupied_spaces: int
    total_capacity: int
    occupancy: float

class CarPark:
    """A class representing a car park with its details.

    Properties:
        code (str): The code identifying the car park.
        name (str): The name of the car park.
        status (str): The status of the car park.
        occupied_spaces (int): The number of occupied spaces in the car park.
        remaining_spaces (int): The number of remaining spaces in the car park.
        total_capacity (int): The total capacity of the car park.
        occupancy (float): The occupancy rate of the car park, expressed as a percentage.
    """

    def __init__(self, code:str, name:str, status:str, \
                 occupied_spaces:int, remaining_spaces:int, \
                    total_capacity:int, occupancy:float) -> None:
        """Initialises a CarPark object with the provided attributes.

        Args:
            code (str): The code identifying the car park.
            name (str): The name of the car park.
            status (str): The status of the car park.
            occupied_spaces (int): The number of occupied spaces in the car park.
            remaining_spaces (int): The number of remaining spaces in the car park.
            total_capacity (int): The total capacity of the car park.
            occupancy (float): The occupancy rate of the car park.
        """
        self.__code = code
        self.__name = name
        self.__status = status
        self.__occupied_spaces = occupied_spaces
        self.__remaining_spaces = remaining_spaces
        self.__total_capacity = total_capacity
        self.__occupancy = occupancy

    @property
    def code(self) -> str:
        """Getter method for the code attribute.

        Returns:
            str: The code identifying the car park.
        """
        return self.__code

    @property
    def name(self) -> str:
        """Getter method for the name attribute.

        Returns:
            str: The name of the car park.
        """
        return self.__name

    @property
    def status(self) -> str:
        """Getter method for the status attribute.

        Returns:
            str: The status of the car park.
        """
        return self.__status

    @property
    def occupied_spaces(self) -> int:
        """Getter method for the occupied_spaces attribute.

        Returns:
            int: The number of occupied spaces in the car park.
        """
        return self.__occupied_spaces

    @property
    def remaining_spaces(self) -> int:
        """Getter method for the remaining_spaces attribute.

        Returns:
            int: The number of remaining spaces in the car park.
        """
        return self.__remaining_spaces

    @property
    def total_capacity(self) -> int:
        """Getter method for the total_capacity attribute.

        Returns:
            int: The total capacity of the car park.
        """
        return self.__total_capacity

    @property
    def occupancy(self) -> float:
        """Getter method for the occupancy attribute.

        Returns:
            float: The occupancy rate of the car park.
        """
        return self.__occupancy
