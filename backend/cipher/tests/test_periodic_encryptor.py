from django.test import SimpleTestCase

from cipher.services import periodic_decrypt, periodic_encrypt


class PeriodicEncryptorTests(SimpleTestCase):
    def test_all_codes_map_to_elements(self):
        tokens = ["12", "13", "26", "27"]
        result = periodic_encrypt(tokens)
        self.assertEqual(result, ["Mg", "Al", "Fe", "Co"])

    def test_round_trip_periodic_layer(self):
        periodic = ["Mg", "Al", "Fe"]
        codes = periodic_decrypt(periodic)
        self.assertEqual(codes, ["12", "13", "26"])
        self.assertEqual(periodic_encrypt(codes), ["Mg", "Al", "Fe"])

    def test_digits_are_preserved_in_decrypt(self):
        tokens = ["Na", "15", "Xe", "72"]
        self.assertEqual(periodic_decrypt(tokens), ["11", "15", "54", "72"])

    def test_invalid_inputs_raise_errors(self):
        with self.assertRaises(ValueError):
            periodic_encrypt(["0"])
        with self.assertRaises(ValueError):
            periodic_decrypt(["??"])
