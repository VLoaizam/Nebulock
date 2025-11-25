from django.test import SimpleTestCase

from cipher.services import (
    EncryptionError,
    decrypt_string,
    encrypt_text,
    encrypt_to_string,
)


class BasicEncryptorTests(SimpleTestCase):
    def test_encrypt_single_values(self):
        self.assertEqual(encrypt_to_string("a"), "11")
        self.assertEqual(encrypt_to_string("B"), "14")
        self.assertEqual(encrypt_to_string("8"), "71")
        self.assertEqual(encrypt_to_string("9"), "72")

    def test_round_trip(self):
        original = "Hola01"
        encrypted = encrypt_to_string(original)
        self.assertEqual(encrypted, "26 41 33 11 63 64")
        self.assertEqual(decrypt_string(encrypted), original)

    def test_whitespace_handling(self):
        encrypted = encrypt_text("aZ9")
        self.assertEqual(encrypted, ["11", "62", "72"])
        self.assertEqual(decrypt_string("11\t62\n72"), "aZ9")

    def test_empty_inputs(self):
        self.assertEqual(encrypt_to_string(""), "")
        self.assertEqual(decrypt_string("   "), "")

    def test_invalid_characters_raise_error(self):
        with self.assertRaises(EncryptionError):
            encrypt_to_string("!")
        with self.assertRaises(EncryptionError):
            decrypt_string("99")
        with self.assertRaises(EncryptionError):
            decrypt_string("aa")
