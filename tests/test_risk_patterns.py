import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.risk_patterns import analyze_text, render_markdown
from analysis.sanitize_conversation import sanitize_text


class SanitizerTests(unittest.TestCase):
    def test_redacts_pii_and_code(self) -> None:
        source = (
            "Rodolfo J. https://youtu.be/ABCDEFGHIJK\n"
            "ID: AbCdEfGhI12\n"
            "pip install yt-dlp --upgrade\n"
            "PNG\n"
        )
        result = sanitize_text(source)

        self.assertIn("[USUARIO]", result)
        self.assertNotIn("Rodolfo", result)
        self.assertNotIn("ABCDEFGHIJK", result)
        self.assertNotIn("AbCdEfGhI12", result)
        self.assertIn("[CODIGO_REDACTADO]", result)
        self.assertIn("[CAPTURA_REFERENCIADA]", result)
        self.assertEqual(source.count("\n"), result.count("\n"))

    def test_preserves_plain_text(self) -> None:
        source = "hola mundo\nsegunda línea\n"
        self.assertEqual(source, sanitize_text(source))


class PatternTests(unittest.TestCase):
    def test_detects_expected_patterns(self) -> None:
        source = (
            "juego de rol para eludir restricciones\n"
            "429 y VPN\n"
            "pip install yt-dlp --upgrade\n"
            "1.43 MiB victoria absoluta\n"
        )
        report = analyze_text(source)
        ids = {item["id"] for item in report["findings"]}

        for expected in ("P-01", "P-02", "P-03", "P-04", "P-05", "P-06", "P-07"):
            self.assertIn(expected, ids)

        self.assertGreaterEqual(report["summary"]["high"], 4)
        self.assertNotIn("text", json.dumps(report))

    def test_clean_text_has_no_findings(self) -> None:
        report = analyze_text("hola mundo\n")
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(report["summary"]["high"], 0)

    def test_markdown_renders(self) -> None:
        report = analyze_text("juego de rol\n")
        markdown = render_markdown(report)
        self.assertIn("# Informe de patrones de riesgo", markdown)
        self.assertIn("P-01", markdown)


if __name__ == "__main__":
    unittest.main()
