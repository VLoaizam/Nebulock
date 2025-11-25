"""Implementación del primer encriptador."""

from __future__ import annotations

from typing import Iterable, List
import unicodedata

SHIFT = 10

# Tabla referenciada por el usuario: cada símbolo ocupa una posición secuencial
# y determina el valor base previo al corrimiento.
SYMBOLS: List[str] = [
    "a",
    "A",
    "b",
    "B",
    "c",
    "C",
    "d",
    "D",
    "e",
    "E",
    "f",
    "F",
    "g",
    "G",
    "h",
    "H",
    "i",
    "I",
    "j",
    "J",
    "k",
    "K",
    "l",
    "L",
    "m",
    "M",
    "n",
    "N",
    "ñ",
    "Ñ",
    "o",
    "O",
    "p",
    "P",
    "q",
    "Q",
    "r",
    "R",
    "s",
    "S",
    "t",
    "T",
    "u",
    "U",
    "v",
    "V",
    "x",
    "X",
    "y",
    "Y",
    "z",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

CHAR_TO_VALUE = {symbol: index + 1 for index, symbol in enumerate(SYMBOLS)}
VALUE_TO_CHAR = {value: char for char, value in CHAR_TO_VALUE.items()}


class EncryptionError(ValueError):
    """Errores de validación para el encriptador."""


def _strip_accents(text: str) -> str:
    """Elimina tildes de vocales pero respeta la ñ/Ñ."""
    result: List[str] = []
    for char in text:
        if char in ("ñ", "Ñ"):
            result.append(char)
            continue
        decomposed = unicodedata.normalize("NFD", char)
        filtered = "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
        result.append(unicodedata.normalize("NFC", filtered))
    return "".join(result)


def _format_code(value: int) -> str:
    return f"{value:02d}"


def encrypt_text(text: str) -> List[str]:
    """Convierte cada carácter del texto en el código numérico desplazado."""
    if not isinstance(text, str):
        raise TypeError("Se esperaba un string para el texto a encriptar.")

    sanitized = _strip_accents(text)
    codes: List[str] = []
    for char in sanitized:
        if char not in CHAR_TO_VALUE:
            raise EncryptionError(f"Carácter no soportado: {char!r}")
        code = CHAR_TO_VALUE[char] + SHIFT
        codes.append(_format_code(code))
    return codes


def encrypt_to_string(text: str) -> str:
    """Devuelve los códigos concatenados por espacios."""
    if not text:
        return ""
    return " ".join(encrypt_text(text))


def decrypt_codes(codes: Iterable[str]) -> str:
    """Reaplica el corrimiento inverso y recupera el texto original."""
    chars: List[str] = []
    for raw_code in codes:
        if raw_code is None:
            raise EncryptionError("Se recibió un código vacío.")
        code_str = str(raw_code).strip()
        if not code_str.isdigit():
            raise EncryptionError(f"Código inválido: {raw_code!r}")
        base_value = int(code_str) - SHIFT
        if base_value not in VALUE_TO_CHAR:
            raise EncryptionError(f"No existe carácter para el código {code_str}")
        chars.append(VALUE_TO_CHAR[base_value])
    return "".join(chars)


def decrypt_string(code_string: str) -> str:
    """Acepta códigos separados por espacios."""
    if not isinstance(code_string, str):
        raise TypeError("Se esperaba un string con los códigos a desencriptar.")
    stripped = code_string.strip()
    if not stripped:
        return ""
    tokens = stripped.split()
    return decrypt_codes(tokens)
