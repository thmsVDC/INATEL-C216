import asyncio
import os
import random
import time
from typing import Protocol

import httpx

from app.schemas.game import FlagQuestion, FlagQuizQuestion


class FlagProviderError(Exception):
    pass


class FlagProvider(Protocol):
    async def get_random_flag(self) -> FlagQuestion: ...

    async def get_quiz_questions(self, count: int) -> list[FlagQuizQuestion]: ...


class RestCountriesFlagProvider:
    url = "https://api.restcountries.com/countries/v5"
    cache_seconds = 60 * 60

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("REST_COUNTRIES_API_KEY")
        self._countries: list[dict[str, str]] = []
        self._countries_loaded_at = 0.0
        self._cache_lock = asyncio.Lock()

    async def _fetch_countries(self) -> list[dict[str, str]]:
        if not self.api_key:
            raise FlagProviderError("Configure REST_COUNTRIES_API_KEY no arquivo .env.")

        countries: list[dict[str, str]] = []
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                offset = 0
                total = 1
                while offset < total:
                    response = await client.get(
                        self.url,
                        params={
                            "limit": 100,
                            "offset": offset,
                            "response_fields": "names.common,flag.url_png",
                        },
                        headers={"Authorization": f"Bearer {self.api_key}"},
                    )
                    response.raise_for_status()
                    payload = response.json().get("data", {})
                    countries.extend(payload.get("objects", []))
                    total = payload.get("meta", {}).get("total", len(countries))
                    offset += 100
        except (httpx.HTTPError, ValueError) as error:
            raise FlagProviderError(
                "Não foi possível carregar os países da REST Countries."
            ) from error

        available = [
            {
                "name": country.get("names", {}).get("common", ""),
                "flag": country.get("flag", {}).get("url_png", ""),
            }
            for country in countries
            if country.get("names", {}).get("common")
            and country.get("flag", {}).get("url_png")
        ]
        if len(available) < 4:
            raise FlagProviderError(
                "A REST Countries retornou poucos países para montar o quiz."
            )
        return available

    async def _get_countries(self) -> list[dict[str, str]]:
        if (
            self._countries
            and time.monotonic() - self._countries_loaded_at < self.cache_seconds
        ):
            return self._countries

        async with self._cache_lock:
            if (
                not self._countries
                or time.monotonic() - self._countries_loaded_at >= self.cache_seconds
            ):
                self._countries = await self._fetch_countries()
                self._countries_loaded_at = time.monotonic()
        return self._countries

    async def get_random_flag(self) -> FlagQuestion:
        selected = random.choice(await self._get_countries())

        return FlagQuestion(
            correct_country=selected["name"],
            flag_url=selected["flag"],
        )

    async def get_quiz_questions(self, count: int) -> list[FlagQuizQuestion]:
        countries = await self._get_countries()
        selected_countries = random.sample(countries, min(count, len(countries)))
        questions = []

        for country in selected_countries:
            distractors = random.sample(
                [item["name"] for item in countries if item["name"] != country["name"]],
                3,
            )
            choices = [country["name"], *distractors]
            random.shuffle(choices)
            questions.append(
                FlagQuizQuestion(
                    country=country["name"],
                    flag_url=country["flag"],
                    choices=choices,
                )
            )
        return questions
