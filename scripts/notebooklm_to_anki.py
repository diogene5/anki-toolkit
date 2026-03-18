#!/usr/bin/env python3
"""
🔄 notebooklm_to_anki.py — Converte flashcards do NotebookLM para .apkg do Anki

PIPELINE: NotebookLM → JSON → genanki → .apkg → Anki
────────────────────────────────────────────────────────

O NotebookLM gera flashcards a partir de qualquer fonte (PDFs, URLs, vídeos).
Este script converte o JSON exportado para um .apkg pronto para importar no Anki.

COMO FUNCIONA:
  1. No NotebookLM, gere flashcards para um notebook
  2. Baixe com: notebooklm download flashcards cards.json
  3. Rode este script para converter em .apkg
  4. Importe no Anki: File > Import

O JSON do NotebookLM tem formato simples:
  {"title": "...", "cards": [{"front": "...", "back": "..."}, ...]}

MODOS DE USO:
  # Converter um arquivo JSON específico
  python3 notebooklm_to_anki.py dados/nlm_git_flashcards.json

  # Converter e especificar deck destino
  python3 notebooklm_to_anki.py dados/nlm_git_flashcards.json --deck "NLM::Git"

  # Converter TODOS os JSONs de flashcards na pasta dados/
  python3 notebooklm_to_anki.py --all

  # Pipeline completo: baixar + converter
  python3 notebooklm_to_anki.py --download --notebook <id>

DEPENDÊNCIAS:
  pip install genanki
  pip install notebooklm-py  # para --download
"""
import json
import hashlib
import os
import re
import subprocess
import argparse
from pathlib import Path

import genanki
import random

random.seed(77)  # seed diferente dos outros geradores para evitar colisão de GUIDs

# CSS, modelo e funções de texto centralizados em shared.py
from shared import CARD_CSS, create_model, enriquecer_html, safe_name

MODEL = create_model()


def converter_json_para_apkg(
    json_path: str,
    deck_name: str = None,
    output_dir: str = None,
) -> str:
    """
    Converte JSON de flashcards do NotebookLM para .apkg.

    Args:
        json_path: caminho para o JSON baixado
        deck_name: nome do deck (default: "NLM::<título do notebook>")
        output_dir: diretório de saída (default: output/)

    Returns:
        Caminho do .apkg gerado
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get('title', 'NotebookLM Import')
    cards = data.get('cards', [])

    if not cards:
        print(f"⚠️  Nenhum card encontrado em {json_path}")
        return ""

    # Gerar nome de deck a partir do título
    if not deck_name:
        clean_title = re.sub(r'[^\w\s-]', '', title).strip()
        deck_name = f"NLM::{clean_title}"

    # Criar deck com ID baseado no nome (determinístico)
    deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16) % (10**9) + 3000000000
    deck = genanki.Deck(deck_id, deck_name)

    for card in cards:
        front = enriquecer_html(card.get('front', ''))
        back = enriquecer_html(card.get('back', ''))

        if front and back:
            note = genanki.Note(
                model=MODEL,
                fields=[front, back],
                tags=['notebooklm', title.lower().replace(' ', '_')[:30]],
            )
            deck.add_note(note)

    # Exportar
    if not output_dir:
        output_dir = str(Path(__file__).parent.parent / "output")
    os.makedirs(output_dir, exist_ok=True)

    fname = safe_name(title)
    output_path = os.path.join(output_dir, f"NLM_{fname}.apkg")

    package = genanki.Package([deck])
    package.write_to_file(output_path)

    print(f"✅ {output_path}")
    print(f"   {len(deck.notes)} cards → deck '{deck_name}'")
    return output_path


def converter_todos(dados_dir: str = None) -> list[str]:
    """Converte todos os JSONs de flashcards na pasta dados/."""
    if not dados_dir:
        dados_dir = str(Path(__file__).parent.parent / "dados")

    resultados = []
    for f in sorted(Path(dados_dir).glob("nlm_*.json")):
        print(f"\n📥 {f.name}")
        result = converter_json_para_apkg(str(f))
        if result:
            resultados.append(result)
    return resultados


def baixar_e_converter(notebook_id: str, deck_name: str = None) -> str:
    """
    Pipeline completo: baixa flashcards do NotebookLM e converte.

    Requer notebooklm-py instalado e autenticado.
    """
    dados_dir = str(Path(__file__).parent.parent / "dados")
    os.makedirs(dados_dir, exist_ok=True)

    # Definir contexto
    subprocess.run(["notebooklm", "use", notebook_id], check=True)

    # Verificar se já tem flashcards
    result = subprocess.run(
        ["notebooklm", "artifact", "list", "--json"],
        capture_output=True, text=True
    )
    artifacts = json.loads(result.stdout)

    has_flashcards = any(
        a['type_id'] == 'flashcards' and a['status'] == 'completed'
        for a in artifacts.get('artifacts', [])
    )

    if not has_flashcards:
        print("📝 Gerando flashcards (pode levar 5-15 min)...")
        subprocess.run(["notebooklm", "generate", "flashcards"], check=True)
        print("⏳ Aguardando...")
        # Pegar o ID do artifact recém-criado
        result = subprocess.run(
            ["notebooklm", "artifact", "list", "--json"],
            capture_output=True, text=True
        )
        artifacts = json.loads(result.stdout)
        fc = [a for a in artifacts['artifacts'] if a['type_id'] == 'flashcards'][-1]
        subprocess.run(["notebooklm", "artifact", "wait", fc['id']], check=True)

    # Baixar
    title = artifacts.get('notebook_title', 'notebook')
    safe = re.sub(r'[^\w-]', '_', title)[:40]
    json_path = os.path.join(dados_dir, f"nlm_{safe}.json")

    subprocess.run(
        ["notebooklm", "download", "flashcards", json_path],
        check=True
    )

    return converter_json_para_apkg(json_path, deck_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converter flashcards NotebookLM → Anki .apkg"
    )
    parser.add_argument("json_file", nargs="?", help="JSON de flashcards para converter")
    parser.add_argument("--deck", help="Nome do deck destino")
    parser.add_argument("--all", action="store_true", help="Converter todos os JSONs em dados/")
    parser.add_argument("--download", action="store_true", help="Baixar do NotebookLM primeiro")
    parser.add_argument("--notebook", help="ID do notebook (para --download)")
    args = parser.parse_args()

    if args.download and args.notebook:
        baixar_e_converter(args.notebook, args.deck)
    elif args.all:
        converter_todos()
    elif args.json_file:
        converter_json_para_apkg(args.json_file, args.deck)
    else:
        parser.print_help()
        print("\nExemplo:")
        print("  python3 scripts/notebooklm_to_anki.py dados/nlm_git_flashcards.json")
        print("  python3 scripts/notebooklm_to_anki.py --all")
        print("  python3 scripts/notebooklm_to_anki.py --download --notebook abc123")
