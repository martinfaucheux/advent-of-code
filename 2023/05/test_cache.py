from dataclasses import dataclass
from functools import lru_cache


@dataclass
class MyClass:
    mult: int

    @lru_cache(maxsize=128)
    def calculate(self, value: int) -> int:
        return value * self.mult

    def __hash__(self):
        return hash(self.mult)


inst1 = MyClass(2)
inst2 = MyClass(3)

print(inst1.calculate(3))
print(inst2.calculate(3))
