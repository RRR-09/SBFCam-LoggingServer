from os import getenv

from dotenv import dotenv_values


def check_dotenv():
    dotenv_key = ""
    try:
        for dotenv_key in list(dotenv_values(".env.default").keys()):
            if getenv(dotenv_key) is None:
                raise IndexError
    except IndexError:
        exception_message = (
            "Could not validate .env file! Does it exist/is it properly formatted?"
        )
        if dotenv_key:
            exception_message = (
                f"Failed when validating '{dotenv_key}' key in .env file! "
                "Does it exist/is it properly formatted?"
            )

        raise Exception(exception_message)
