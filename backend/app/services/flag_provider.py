import random
from typing import Protocol

import httpx

from app.schemas.game import FlagQuestion


class FlagProvider(Protocol):
    async def get_random_flag(self) -> FlagQuestion: ...


class RestCountriesFlagProvider:
    url = "https://restcountries.com/v3.1/all?fields=name,flags"

    async def get_random_flag(self) -> FlagQuestion:
        async with httpx.AsyncClient(
            timeout=10,
            follow_redirects=True,
        ) as client:
            response = await client.get(self.url)
            response.raise_for_status()
            countries = response.json()

        available = [
            country
            for country in countries
            if country.get("name", {}).get("common")
            and country.get("flags", {}).get("png")
        ]

        if not available:
            raise RuntimeError("A API não retornou bandeiras disponíveis")

        selected = random.choice(available)

        return FlagQuestion(
            correct_country=selected["name"]["common"],
            flag_url=selected["flags"]["png"],
        )
