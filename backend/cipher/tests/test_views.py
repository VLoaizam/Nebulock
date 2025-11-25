import json

from django.test import TestCase
from django.urls import reverse

from cipher.services import encrypt_to_string, periodic_encrypt


class CipherViewsTests(TestCase):
    def post_json(self, url_name, payload):
        return self.client.post(
            reverse(url_name),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_encrypt_endpoint_returns_codes(self):
        response = self.post_json("cipher:encrypt", {"text": "Hola"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["codes"], encrypt_to_string("Hola"))

    def test_decrypt_endpoint_returns_text(self):
        codes = encrypt_to_string("HolaMundo")
        response = self.post_json("cipher:decrypt", {"codes": codes})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "HolaMundo")

    def test_periodic_encrypt_endpoint(self):
        codes = encrypt_to_string("Hola")
        response = self.post_json("cipher:periodic-encrypt", {"codes": codes})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["periodic"], periodic_encrypt(codes.split()))

    def test_periodic_decrypt_endpoint(self):
        codes = encrypt_to_string("Hola")
        periodic_tokens = periodic_encrypt(codes.split())
        response = self.post_json(
            "cipher:periodic-decrypt",
            {"periodic": periodic_tokens},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["codes"], codes)
