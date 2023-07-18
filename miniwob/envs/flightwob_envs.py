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

    ## Additional notes

    * **Partial reward:** If all required fields are filled, the partial reward is the fraction of correct fields.
    * The instructions come from a fixed set from the original FlightWoB dataset. Use the `set_data_mode` method of the environment to switch between the train and test scenarios.
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

    ## Additional notes

    * **Partial reward:** If all required fields are filled, the partial reward is the fraction of correct fields.
    * The instructions come from a fixed set from the original FlightWoB dataset. Use the `set_data_mode` method of the environment to switch between the train and test scenarios.
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

    ## Additional notes

    * **Partial reward:** If all required fields are filled, the partial reward is the fraction of correct fields.
    * The instructions are automatically generated.
    """

    subdomain = "flight.Alaska-auto"
