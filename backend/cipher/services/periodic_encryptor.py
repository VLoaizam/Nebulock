"""Segunda capa de encriptación usando elementos de la tabla periódica."""

from __future__ import annotations

from typing import Iterable, List

PERIODIC_SYMBOLS = [
    (1, "H"),
    (2, "He"),
    (3, "Li"),
    (4, "Be"),
    (5, "B"),
    (6, "C"),
    (7, "N"),
    (8, "O"),
    (9, "F"),
    (10, "Ne"),
    (11, "Na"),
    (12, "Mg"),
    (13, "Al"),
    (14, "Si"),
    (15, "P"),
    (16, "S"),
    (17, "Cl"),
    (18, "Ar"),
    (19, "K"),
    (20, "Ca"),
    (21, "Sc"),
    (22, "Ti"),
    (23, "V"),
    (24, "Cr"),
    (25, "Mn"),
    (26, "Fe"),
    (27, "Co"),
    (28, "Ni"),
    (29, "Cu"),
    (30, "Zn"),
    (31, "Ga"),
    (32, "Ge"),
    (33, "As"),
    (34, "Se"),
    (35, "Br"),
    (36, "Kr"),
    (37, "Rb"),
    (38, "Sr"),
    (39, "Y"),
    (40, "Zr"),
    (41, "Nb"),
    (42, "Mo"),
    (43, "Tc"),
    (44, "Ru"),
    (45, "Rh"),
    (46, "Pd"),
    (47, "Ag"),
    (48, "Cd"),
    (49, "In"),
    (50, "Sn"),
    (51, "Sb"),
    (52, "Te"),
    (53, "I"),
    (54, "Xe"),
    (55, "Cs"),
    (56, "Ba"),
    (57, "La"),
    (58, "Ce"),
    (59, "Pr"),
    (60, "Nd"),
    (61, "Pm"),
    (62, "Sm"),
    (63, "Eu"),
    (64, "Gd"),
    (65, "Tb"),
    (66, "Dy"),
    (67, "Ho"),
    (68, "Er"),
    (69, "Tm"),
    (70, "Yb"),
    (71, "Lu"),
    (72, "Hf"),
]

NUMBER_TO_SYMBOL = {number: symbol for number, symbol in PERIODIC_SYMBOLS}
SYMBOL_TO_NUMBER = {symbol: number for number, symbol in PERIODIC_SYMBOLS}


def periodic_encrypt(codes: Iterable[str]) -> List[str]:
    """Convierte todos los códigos en el símbolo químico correspondiente."""
    transformed: List[str] = []
    for token in codes:
        token_str = str(token).strip()
        if not token_str:
            raise ValueError("Se encontró un código vacío en la capa periódica.")
        if not token_str.isdigit():
            raise ValueError(f"Código inválido para la capa periódica: {token_str!r}")
        numeric_value = int(token_str)
        if numeric_value not in NUMBER_TO_SYMBOL:
            raise ValueError(
                f"No existe elemento con número atómico {numeric_value}."
            )
        transformed.append(NUMBER_TO_SYMBOL[numeric_value])
    return transformed


def periodic_decrypt(tokens: Iterable[str]) -> List[str]:
    """Convierte símbolos químicos a códigos de dos dígitos."""
    result: List[str] = []
    for token in tokens:
        token_str = str(token).strip()
        if not token_str:
            raise ValueError("Se encontró un token vacío en la capa periódica.")
        if token_str.isdigit():
            result.append(f"{int(token_str):02d}")
        elif token_str in SYMBOL_TO_NUMBER:
            result.append(f"{SYMBOL_TO_NUMBER[token_str]:02d}")
        else:
            raise ValueError(f"Símbolo químico no reconocido: {token_str!r}")
    return result
