#!/usr/bin/env python3
"""Sanea una conversación para análisis defensivo.

- Elimina datos personales, URL/ID de vídeo y rutas locales.
- Sustituye líneas de código operativo por [CODIGO_REDACTADO].
- Conserva el número de líneas para mantener las referencias del análisis.
- No ejecuta nada del contenido.

Uso:
    python3 analysis/sanitize_conversation.py entrada.txt salida.txt
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REDACTIONS = [
    (re.compile(r"Rodolfo\s+Javier\s+Roa\s+Briceño", re.IGNORECASE), "[USUARIO]"),
    (re.compile(r"Rodolfo\s+J\.?", re.IGNORECASE), "[USUARIO]"),
    (re.compile(r"Rodolfo", re.IGNORECASE), "[USUARIO]"),
    (re.compile(r"https?://(?:www\.)?youtu\.be/\S+", re.IGNORECASE), "[VIDEO_REDACTADO]"),
    (re.compile(r"https?://(?:www\.)?youtube\.com/\S+", re.IGNORECASE), "[VIDEO_REDACTADO]"),
    (re.compile(r"\b[A-Za-z0-9_-]{11}_transcripcion\.md\b"), "[VIDEO_REDACTADO].md"),
    (re.compile(r"\b[A-Za-z0-9_-]{11}\b(?=\.(?:md|vtt|srt)\b)"), "[VIDEO_REDACTADO]"),
    (re.compile(r"C:\\\\?Extraer", re.IGNORECASE), "[RUTA_LOCAL]"),
    (re.compile(r"C:/Extraer", re.IGNORECASE), "[RUTA_LOCAL]"),
    (re.compile(r"\bPNG\b"), "[CAPTURA_REFERENCIADA]"),
]

CODE_PREFIXES = (
    "import ",
    "from ",
    "def ",
    "class ",
    "if __name__",
    "try:",
    "except ",
    "return ",
    "with open",
    "subprocess",
    "os.",
    "pip install",
    "python ",
    "yt-dlp",
    "youtube_transcript_api",
    "YouTubeTranscriptApi",
    "for ",
    "while ",
    "print(",
    "json.",
    "open(",
    "f.write",
    "Path(",
    "requests.",
    "urlopen",
    "re.sub",
    "video_id",
    "api_key",
    "token",
    "password",
    "fetch(",
    "get_transcript(",
    "--impersonate",
    "--cookies",
    "--proxy",
)

CODE_MARKERS = (
    "subprocess.check_call",
    "os.remove",
    "os.listdir",
    "YouTubeTranscriptApi",
    "yt_dlp",
    "youtube_transcript_api",
    "fetch(",
    "get_transcript(",
    "--impersonate",
    "--cookies",
    "--proxy",
    "extract_info",
    "download=True",
    ".startswith(",
    ".endswith(",
    ".get(",
    "print(",
    "json.",
    "re.sub",
)

STRONG_PREFIXES = (
    '"""',
    "'''",
    ")",
    "]",
    "}",
    "@",
    "async ",
    "await ",
    "finally:",
    "if ",
    "elif ",
    "else:",
    "for ",
    "while ",
    "break",
    "continue",
    "pass",
    "try:",
    "except ",
    "with ",
    "raise ",
    "yield ",
)

ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=")
FUNCTION_CALL = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\(.*\)$")
QUOTED_TEXT = re.compile(r'"([^"\n]{20,})"|\'([^\'\n]{20,})\'"')
YOUTUBE_ID = re.compile(r"\b[A-Za-z0-9_-]{11}\b")
BAD_FRAGMENT_MARKERS = (
    "YouTubeTranscriptApi",
    "getattr",
    "callable",
    "lambda",
    "subprocess",
    "os.",
    "def ",
    "import ",
    " = ",
    "==",
    ";",
    "print(",
    "fetch(",
    "get_transcript(",
)


def _is_code_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if line.startswith(("    ", "\t")) and stripped.startswith("#"):
        return True
    if stripped.startswith(CODE_PREFIXES):
        return True
    if stripped.startswith(STRONG_PREFIXES):
        return True
    if ASSIGNMENT.match(stripped):
        return True
    if FUNCTION_CALL.match(stripped):
        return True
    if line.startswith(("    ", "\t")) and any(marker in stripped for marker in CODE_MARKERS):
        return True
    return any(marker in stripped for marker in CODE_MARKERS)


def _extract_human_text(line: str) -> str:
    """Extrae cadenas legibles de una línea de código, sin ejecutarla."""
    fragments: list[str] = []
    for match in QUOTED_TEXT.finditer(line):
        fragment = match.group(1) or match.group(2) or ""
        if not fragment:
            continue
        if not any(char.isalpha() for char in fragment) or " " not in fragment:
            continue
        if any(marker in fragment for marker in BAD_FRAGMENT_MARKERS):
            continue
        fragments.append(fragment)
    return " ".join(fragments)


def _redact_youtube_id(match: re.Match[str]) -> str:
    """Redacta identificadores de 11 caracteres con forma de ID de YouTube."""
    token = match.group(0)
    has_upper = sum(1 for char in token if char.isupper()) >= 2
    has_lower = sum(1 for char in token if char.islower()) >= 2
    has_digit = any(char.isdigit() for char in token)
    if has_upper and has_lower and has_digit:
        return "[VIDEO_REDACTADO]"
    return token


def sanitize_text(text: str) -> str:
    """Devuelve el texto saneado conservando el número de líneas."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    output: list[str] = []

    for line in lines:
        if _is_code_line(line):
            human = _extract_human_text(line)
            if human:
                for pattern, replacement in REDACTIONS:
                    human = pattern.sub(replacement, human)
                human = YOUTUBE_ID.sub(_redact_youtube_id, human)
                output.append(f"[SALIDA_DE_CODIGO] {human}")
            else:
                output.append("[CODIGO_REDACTADO]")
            continue

        for pattern, replacement in REDACTIONS:
            line = pattern.sub(replacement, line)
        line = YOUTUBE_ID.sub(_redact_youtube_id, line)

        output.append(line)

    return "\n".join(output)


def sanitize_file(source: Path, destination: Path) -> None:
    text = source.read_text(encoding="utf-8", errors="replace")
    sanitized = sanitize_text(text)
    destination.write_text(sanitized, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanea una conversación para el laboratorio.")
    parser.add_argument("source", type=Path, help="Archivo de entrada")
    parser.add_argument("destination", type=Path, help="Archivo de salida")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"No existe: {args.source}")

    sanitize_file(args.source, args.destination)
    print(f"Saneado: {args.source} -> {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
