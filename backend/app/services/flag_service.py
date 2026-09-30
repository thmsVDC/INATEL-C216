from app.schemas.flag import Flag, FlagCreate, FlagPatch


class FlagNotFoundError(Exception):
    pass


class FlagService:
    def __init__(self) -> None:
        self._flags: dict[int, Flag] = {}
        self._next_id = 1

    def list_flags(self, limit: int) -> list[Flag]:
        return list(self._flags.values())[:limit]

    def get_flag(self, flag_id: int) -> Flag:
        try:
            return self._flags[flag_id]
        except KeyError as error:
            raise FlagNotFoundError(f"Flag {flag_id} not found") from error

    def create_flag(self, data: FlagCreate) -> Flag:
        flag = Flag(id=self._next_id, **data.model_dump())
        self._flags[flag.id] = flag
        self._next_id += 1
        return flag

    def replace_flag(self, flag_id: int, data: FlagCreate) -> Flag:
        self.get_flag(flag_id)
        flag = Flag(id=flag_id, **data.model_dump())
        self._flags[flag_id] = flag
        return flag

    def patch_flag(self, flag_id: int, data: FlagPatch) -> Flag:
        current_flag = self.get_flag(flag_id)
        updates = data.model_dump(exclude_unset=True, exclude_none=True)
        updated_flag = current_flag.model_copy(update=updates)
        self._flags[flag_id] = updated_flag
        return updated_flag

    def delete_flag(self, flag_id: int) -> None:
        self.get_flag(flag_id)
        del self._flags[flag_id]