"""Vistas para exponer el encriptador vía JSON."""

from __future__ import annotations

import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services import (
    EncryptionError,
    decrypt_string,
    encrypt_to_string,
    periodic_decrypt,
    periodic_encrypt,
)


def _parse_payload(request) -> dict:
    """Lee el body del request y lo transforma en dict."""
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise EncryptionError(f"JSON inválido: {exc.msg}") from exc


def _normalize_tokens(value, empty_error: str) -> list[str]:
    if value is None:
        raise EncryptionError(empty_error)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise EncryptionError(empty_error)
        return stripped.split()
    if isinstance(value, (list, tuple)):
        tokens = [str(item).strip() for item in value if str(item).strip()]
        if not tokens:
            raise EncryptionError(empty_error)
        return tokens
    raise TypeError("Formato de entrada no soportado. Usa string o lista.")


@csrf_exempt
@require_http_methods(["POST"])
def encrypt_view(request):
    """Recibe el texto plano y responde con los códigos generados."""
    try:
        payload = _parse_payload(request)
        text = payload.get("text", "")
        encoded = encrypt_to_string(text)
        return JsonResponse({"text": text, "codes": encoded})
    except (EncryptionError, TypeError) as exc:
        return JsonResponse({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
@require_http_methods(["POST"])
def decrypt_view(request):
    """Recibe códigos numéricos y reconstruye el texto original."""
    try:
        payload = _parse_payload(request)
        tokens = _normalize_tokens(
            payload.get("codes"),
            "Debes enviar los códigos generados por el primer encriptador.",
        )
        code_string = " ".join(tokens)
        text = decrypt_string(code_string)
        return JsonResponse({"codes": code_string, "text": text})
    except (EncryptionError, TypeError) as exc:
        return JsonResponse({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
@require_http_methods(["POST"])
def periodic_encrypt_view(request):
    """Transforma códigos pares en elementos químicos."""
    try:
        payload = _parse_payload(request)
        tokens = _normalize_tokens(
            payload.get("codes"),
            "Debes enviar los códigos del primer encriptador para aplicar la capa periódica.",
        )
        periodic_tokens = periodic_encrypt(tokens)
        return JsonResponse(
            {
                "codes": " ".join(tokens),
                "periodic": periodic_tokens,
            }
        )
    except (EncryptionError, TypeError, ValueError) as exc:
        return JsonResponse({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
@require_http_methods(["POST"])
def periodic_decrypt_view(request):
    """Convierte símbolos químicos de regreso a códigos numéricos."""
    try:
        payload = _parse_payload(request)
        tokens = _normalize_tokens(
            payload.get("periodic"),
            "Debes enviar los símbolos generados por la capa periódica.",
        )
        codes_list = periodic_decrypt(tokens)
        code_string = " ".join(codes_list)
        return JsonResponse(
            {
                "periodic": tokens,
                "codes": code_string,
            }
        )
    except (EncryptionError, TypeError, ValueError) as exc:
        return JsonResponse({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
