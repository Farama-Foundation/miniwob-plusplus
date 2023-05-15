"""Environments for FlightWoB tasks."""

from miniwob.environment import MiniWoBEnvironment


class FlightAAEnv(MiniWoBEnvironment):
    """
    ## Description

    Search for flights on the American Airlines website.

    ## Utterance

    The utterance is the JSON serialization of the utterance fields.

    ## Utterance fields

    * Departure City
    * Departure Day
    * Departure Month
    * Destination City
    * One Way or Round Trip
    * Returning Day
    * Returning Month

    ## Custom settings

    None
    """

    subdomain = "flight.AA"


class FlightAlaskaEnv(MiniWoBEnvironment):
    """
    ## Description

    Search for flights on the Alaska Airlines website (original).

    ## Utterance

    The utterance is the JSON serialization of the utterance fields.

    ## Utterance fields

    * Departure City
    * Departure Day
    * Departure Month
    * Destination City
    * One Way or Round Trip
    * Returning Day
    * Returning Month
    """

    subdomain = "flight.Alaska"


class FlightAlaskaAutoEnv(MiniWoBEnvironment):
    """
    ## Description

    Search for flights on the Alaska Airlines website (harder).

    ## Utterance

    The utterance is the JSON serialization of the utterance fields.

    ## Utterance fields

    * Departure City
    * Departure Day
    * Destination City
    * Passengers
    * Returning Day
    * Seat type
    * Ticket Type
    """

    subdomain = "flight.Alaska-auto"
