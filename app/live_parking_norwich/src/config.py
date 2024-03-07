class Config():
    """A class containing configuration constants for the application.

    Attributes:
        XML_URL (str): The URL from which to retrieve the XML data.
        XML_NAMESPACE (dict): The namespace for parsing the XML data.
        DATE_FORMAT (str): The format string for parsing and formatting dates.
    """
    XML_URL = "https://datex.norfolk.cdmf.info/carparks/content.xml"
    XML_NAMESPACE = { "d2lm": "http://datex2.eu/schema/1_0/1_0" }
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
