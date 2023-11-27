class BaseConstant:
    _ids = {}
    _names = {}

    @classmethod
    def get_id(cls, name: str) -> str:
        return cls._ids[name]

    @classmethod
    def get_name_dict(cls, name: str):
        if name in cls._names:
            return {"English": cls._names[name][0], "Korean": cls._names[name][1]}
        else:
            raise ValueError(f"{name} not found in {cls.__name__}")

    @classmethod
    def from_string(cls, string_id: str):
        for name, id in cls._ids.items():
            if id == string_id:
                return getattr(cls, name)
        raise ValueError(f"String ID {string_id} not found in {cls.__name__}")
