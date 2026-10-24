#!/usr/bin/env python3
"""Analizador defensivo de patrones de riesgo en conversaciones.

No ejecuta contenido, no hace peticiones de red y no imprime el texto
coincidente: solo nombres de patrón, líneas y recuentos.

Uso:
    python3 analysis/risk_patterns.py data/Conversacion.sanitized.txt \
        --json report.json --md report.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Pattern:
    id: str
    name: str
    category: str
    iso27090: str
    owasp: str
    severity: str
    regex: str


PATTERNS: tuple[Pattern, ...] = (
    Pattern(
        "P-01",
        "Role-play / encuadre ficticio",
        "jailbreak",
        "T-11 Prompt injection",
        "LLM01",
        "high",
        r"\b(juego de rol|role.?play|personaje|mago|hechicero|puntos de poder|hechizo|misi[oó]n|ficci[oó]n|cuento)\b",
    ),
    Pattern(
        "P-02",
        "Lenguaje de elusión",
        "bypass",
        "T-11 Prompt injection",
        "LLM01",
        "high",
        r"\b(eludir|elusi[oó]n|bypass|burlar|evadir|sobrepasar|saltar|ignorar)\b",
    ),
    Pattern(
        "P-03",
        "Límite de tasa / 429",
        "abuse",
        "T-14 Agotamiento de recursos",
        "LLM10",
        "medium",
        r"\b(429|too many requests|rate.?limit|l[ií]mite de tasa|bloqueo de ip)\b",
    ),
    Pattern(
        "P-04",
        "Evasión de red",
        "abuse",
        "T-11 / T-14",
        "LLM01, LLM10",
        "high",
        r"\b(VPN|datos m[oó]viles|red alternativa|proxy|otra ip|reiniciar el router)\b",
    ),
    Pattern(
        "P-05",
        "Ejecución de herramientas",
        "supply_chain",
        "Cadena de suministro",
        "LLM03",
        "high",
        r"\b(pip install|subprocess|os\.remove|os\.listdir|yt.?dlp|youtube.?transcript.?api|check_call)\b",
    ),
    Pattern(
        "P-06",
        "Instalación sin pinning",
        "supply_chain",
        "Cadena de suministro",
        "LLM03",
        "high",
        r"pip\s+install\s+(?!.*==).*(--upgrade|yt-dlp|youtube-transcript-api)",
    ),
    Pattern(
        "P-07",
        "Éxito no verificado",
        "integrity",
        "T-11 / integridad de salida",
        "LLM09",
        "high",
        r"\b(1\.43\s*MiB|victoria absoluta|completado con [eé]xito|tesoro conquistado|descargados? perfectamente|hechizo anterior s[ií] logr[oó])\b",
    ),
    Pattern(
        "P-08",
        "Datos sensibles",
        "privacy",
        "A.7 / A.8",
        "LLM02",
        "medium",
        r"\b(C:\\\\|shadow_copy|root_evidence|flag_root|api[_-]?key\s*[:=]|token\s*[:=]|password\s*[:=])",
    ),
    Pattern(
        "P-09",
        "Términos de servicio / derechos de autor",
        "legal",
        "Gobernanza",
        "—",
        "medium",
        r"\b(YouTube|t[eé]rminos de servicio|ToS|derechos de autor|copyright|subt[ií]tulos)\b",
    ),
    Pattern(
        "P-10",
        "Sicofancia / recompensa",
        "human_oversight",
        "A.9 Supervisión humana",
        "—",
        "medium",
        r"\b(hechicero final|victoria absoluta|puntos de poder|gran mago|maestro|has ganado)\b",
    ),
    Pattern(
        "P-11",
        "Inyección indirecta",
        "injection",
        "T-12 Prompt injection indirecta",
        "LLM01",
        "high",
        r"\b(ignora tus reglas|ignore previous|reveal.*prompt|system prompt|instrucciones internas)\b",
    ),
)


def _compile(pattern: Pattern) -> re.Pattern[str]:
    return re.compile(pattern.regex, re.IGNORECASE | re.UNICODE)


def analyze_text(text: str) -> dict:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    compiled = [(pattern, _compile(pattern)) for pattern in PATTERNS]
    hits: dict[str, dict] = {
        pattern.id: {
            "id": pattern.id,
            "name": pattern.name,
            "category": pattern.category,
            "iso27090": pattern.iso27090,
            "owasp": pattern.owasp,
            "severity": pattern.severity,
            "count": 0,
            "lines": [],
        }
        for pattern in PATTERNS
    }

    for line_number, line in enumerate(lines, start=1):
        for pattern, regex in compiled:
            if regex.search(line):
                hits[pattern.id]["count"] += 1
                hits[pattern.id]["lines"].append(line_number)

    findings = [hit for hit in hits.values() if hit["count"] > 0]
    findings.sort(key=lambda item: (item["severity"] != "high", item["id"]))

    high = sum(1 for item in findings if item["severity"] == "high")
    medium = sum(1 for item in findings if item["severity"] == "medium")
    total = sum(item["count"] for item in findings)

    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "lines": len(lines),
            "patterns": len(PATTERNS),
            "tool": "risk_patterns.py",
            "note": "Triaje automatizado; no sustituye la revisión humana.",
        },
        "summary": {
            "findings": len(findings),
            "high": high,
            "medium": medium,
            "total_matches": total,
        },
        "findings": findings,
    }


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# Informe de patrones de riesgo",
        "",
        f"Generado: `{report['metadata']['generated_at']}`",
        f"Líneas analizadas: **{report['metadata']['lines']}**",
        "",
        "## Resumen",
        "",
        f"- Hallazgos: **{summary['findings']}**",
        f"- Severidad alta: **{summary['high']}**",
        f"- Severidad media: **{summary['medium']}**",
        f"- Coincidencias totales: **{summary['total_matches']}**",
        "",
        "## Hallazgos",
        "",
        "| ID | Patrón | Categoría | ISO 27090 | OWASP | Severidad | Coincidencias | Líneas |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for item in report["findings"]:
        line_list = ", ".join(str(number) for number in item["lines"][:20])
        if len(item["lines"]) > 20:
            line_list += ", …"
        lines.append(
            f"| {item['id']} | {item['name']} | {item['category']} | "
            f"{item['iso27090']} | {item['owasp']} | {item['severity']} | "
            f"{item['count']} | {line_list} |"
        )

    lines.extend(
        [
            "",
            "## Lectura",
            "",
            "- Los patrones son indicadores, no pruebas de explotación.",
            "- La coincidencia de `P-03` y `P-04` en la misma conversación sugiere evasión de límites de tasa.",
            "- La coincidencia de `P-01`, `P-02` y `P-07` sugiere un jailbreak con afirmación de éxito no verificada.",
            "- Revisar manualmente las líneas indicadas antes de concluir.",
            "",
            "## Siguiente paso",
            "",
            "1. Confirmar los hallazgos con revisión humana.",
            "2. Contrastar con `docs/02_analisis_conversacion.md`.",
            "3. Aplicar los controles de `docs/03_threat_model_iso27090.md`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analiza patrones de riesgo en una conversación.")
    parser.add_argument("source", type=Path, help="Archivo de texto a analizar")
    parser.add_argument("--json", type=Path, help="Ruta del informe JSON")
    parser.add_argument("--md", type=Path, help="Ruta del informe Markdown")
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Devuelve código 2 si hay hallazgos de severidad alta",
    )
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"No existe: {args.source}")

    text = args.source.read_text(encoding="utf-8", errors="replace")
    report = analyze_text(text)

    if args.json:
        args.json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    if args.md:
        args.md.write_text(render_markdown(report), encoding="utf-8", newline="\n")

    print(json.dumps(report["summary"], ensure_ascii=False))
    if args.fail_on_high and report["summary"]["high"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
