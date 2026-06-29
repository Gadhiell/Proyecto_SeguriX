import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.auth_service import validar_acceso


class StrategyAccesoTests(unittest.TestCase):
    def test_qr_permite_acceso_para_usuario_activo_con_qr(self):
        usuarios = {
            "1": {"id": 1, "activo": True, "metodo": "Código QR"}
        }

        permitido, estado = validar_acceso("1", usuarios, "Código QR")

        self.assertTrue(permitido)
        self.assertEqual(estado, "activo")

    def test_rfid_rechaza_si_el_metodo_no_coincide(self):
        usuarios = {
            "2": {"id": 2, "activo": True, "metodo": "Tarjeta RFID"}
        }

        permitido, estado = validar_acceso("2", usuarios, "Código QR")

        self.assertFalse(permitido)
        self.assertEqual(estado, "metodo_no_autorizado")


if __name__ == "__main__":
    unittest.main()
