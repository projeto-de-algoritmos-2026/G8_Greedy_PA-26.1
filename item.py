from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    nome: str
    peso: int
    valor: int
