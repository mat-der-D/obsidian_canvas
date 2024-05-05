class Color:
    def __init__(self, key_phrase: str):
        self._key_phrase = key_phrase

    @property
    def key_phrase(self) -> str:
        return self._key_phrase

    @classmethod
    def red(cls) -> "Color":
        return cls("1")

    @classmethod
    def orange(cls) -> "Color":
        return cls("2")

    @classmethod
    def yellow(cls) -> "Color":
        return cls("3")

    @classmethod
    def green(cls) -> "Color":
        return cls("4")

    @classmethod
    def cyan(cls) -> "Color":
        return cls("5")

    @classmethod
    def purple(cls) -> "Color":
        return cls("6")

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int):
        def _is_valid(n: int) -> bool:
            return n in range(256)

        if not all(map(_is_valid, [r, g, b])):
            raise ValueError("Invalid RGB value: {r}, {g}, {b}")

        def _to_hex(n: int) -> str:
            return f"{n:02x}"[:2].upper()

        return cls(f"#{_to_hex(r)}{_to_hex(g)}{_to_hex(b)}")

    def to_json(self) -> dict:
        return {
            "color": self._key_phrase,
        }
