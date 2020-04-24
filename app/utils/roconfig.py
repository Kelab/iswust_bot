from collections import abc
from typing import Any, Dict, Mapping, Optional

__all__ = ["Configuration", "ConfigurationError", "ConfigurationOverrideError"]


class ConfigurationError(Exception):
    """An exception risen for invalid configuration."""


class ConfigurationOverrideError(ConfigurationError):
    """An exception risen for invalid configuration override."""


def apply_key_value(obj, key, value):
    key = key.strip("_:")  # remove special characters from both ends
    for token in (":", "__"):
        if token in key:
            parts = key.split(token)

            sub_property = obj
            last_part = parts[-1]
            for part in parts[:-1]:
                if isinstance(sub_property, abc.MutableSequence):
                    try:
                        index = int(part)
                    except ValueError:
                        raise ConfigurationOverrideError(
                            f"{part} was supposed to be a numeric index in {key}"
                        )

                    sub_property = sub_property[index]
                    continue

                try:
                    sub_property = sub_property[part]
                except KeyError:
                    sub_property[part] = {}
                    sub_property = sub_property[part]
                else:
                    if not isinstance(sub_property, abc.Mapping) and not isinstance(
                        sub_property, abc.MutableSequence
                    ):
                        raise ConfigurationOverrideError(
                            f"The key `{key}` cannot be used "
                            f"because it overrides another "
                            f"variable with shorter key! ({part}, {sub_property})"
                        )

            if isinstance(sub_property, abc.MutableSequence):
                try:
                    index = int(last_part)
                except ValueError:
                    raise ConfigurationOverrideError(
                        f"{last_part} was supposed to be a numeric index in {key}, "
                        f"because the affected property is a mutable sequence."
                    )

                try:
                    sub_property[index] = value
                except IndexError:
                    raise ConfigurationOverrideError(
                        f"Invalid override for mutable sequence {key}; "
                        f"assignment index out of range"
                    )
            else:
                try:
                    sub_property[last_part] = value
                except TypeError as te:
                    raise ConfigurationOverrideError(
                        f"Invalid assignment {key} -> {value}; {str(te)}"
                    )

            return obj

    obj[key] = value
    return obj


class Configuration:
    """
    Provides methods to handle configuration objects.
    A read-only façade for navigating configuration objects using attribute notation.
    Thanks to Fluent Python, book by Luciano Ramalho; this class is inspired by his
    example of JSON structure explorer.
    """

    __slots__ = ("__data",)

    def __new__(cls, arg=None):
        if not arg:
            return super().__new__(cls)
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        if isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        return arg

    def __init__(self, mapping: Optional[Mapping[str, Any]] = None):
        self.__data: Dict[str, Any] = {}
        if mapping:
            self.add_map(mapping)

    def __contains__(self, item: str) -> bool:
        return item in self.__data

    def __getitem__(self, name):
        value = self.__getattr__(name)
        if value is None:
            raise KeyError(name)
        return value

    def __getattr__(self, name, default=None) -> Any:
        if name in self.__data:
            value = self.__data.get(name)
            if isinstance(value, abc.Mapping) or isinstance(value, abc.MutableSequence):
                return Configuration(value)  # type: ignore
            return value
        return default

    def __repr__(self) -> str:
        return repr(self.values)

    @property
    def values(self) -> Dict[str, Any]:
        """
        Returns a copy of the dictionary of current settings.
        """
        return self.__data.copy()

    def to_dict(self):
        return self.values

    def add_value(self, name: str, value: Any):
        """
        Adds a configuration value by name. The name can contain
        paths to nested objects and list indices.
        :param name: name of property to set
        :param value: the value to set
        """
        apply_key_value(self.__data, name, value)

    def add_object(self, obj):
        config = {
            k: v
            for k, v in obj.__dict__.items()
            if k.isupper() and not k.startswith("_")
        }
        self.__data.update(config)

    def add_map(self, value: Mapping[str, Any]):
        """
        Merges a mapping object such as a dictionary,
        inside this configuration,
        :param value: instance of mapping object
        """
        for key, value in value.items():
            self.__data[key] = value

    def to_config(self):
        class Config:
            pass

        for k, v in self.values.items():
            if k.isupper() and not k.startswith("_"):
                setattr(Config, k, v)
        return Config
