import pytest

from app.schemas.flag import FlagCreate, FlagPatch
from app.services.flag_service import FlagNotFoundError, FlagService


def make_flag(country: str = "Brasil") -> FlagCreate:
    return FlagCreate(
        country=country,
        country_code="BR",
        flag_url="https://example.com/br.png",
    )


def test_create_flag_assigns_id() -> None:
    service = FlagService()

    flag = service.create_flag(make_flag())

    assert flag.id == 1
    assert flag.country == "Brasil"


def test_list_flags_respects_limit() -> None:
    service = FlagService()
    service.create_flag(make_flag("Brasil"))
    service.create_flag(make_flag("Canadá"))

    flags = service.list_flags(limit=1)

    assert len(flags) == 1
    assert flags[0].country == "Brasil"


def test_replace_flag_replaces_all_fields() -> None:
    service = FlagService()
    flag = service.create_flag(make_flag())

    updated = service.replace_flag(
        flag.id,
        FlagCreate(
            country="Argentina",
            country_code="AR",
            flag_url="https://example.com/ar.png",
        ),
    )

    assert updated.id == flag.id
    assert updated.country == "Argentina"
    assert updated.country_code == "AR"


def test_patch_flag_changes_only_requested_field() -> None:
    service = FlagService()
    flag = service.create_flag(make_flag())

    updated = service.patch_flag(flag.id, FlagPatch(country="Portugal"))

    assert updated.country == "Portugal"
    assert updated.country_code == "BR"
    assert updated.flag_url == flag.flag_url


def test_delete_flag_removes_it() -> None:
    service = FlagService()
    flag = service.create_flag(make_flag())

    service.delete_flag(flag.id)

    with pytest.raises(FlagNotFoundError):
        service.get_flag(flag.id)


@pytest.mark.parametrize("flag_id", [0, 10])
def test_get_missing_flag_raises_error(flag_id: int) -> None:
    service = FlagService()

    with pytest.raises(FlagNotFoundError):
        service.get_flag(flag_id)