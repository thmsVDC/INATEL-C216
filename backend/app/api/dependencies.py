from app.services.flag_provider import FlagProvider, RestCountriesFlagProvider

_flag_provider = RestCountriesFlagProvider()


def get_flag_provider() -> FlagProvider:
    return _flag_provider
