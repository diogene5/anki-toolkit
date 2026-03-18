#!/usr/bin/env python3
"""
📦 batch_nlm_download.py — Baixa e converte flashcards de TODOS os notebooks NotebookLM

Usa a lista gerada pelo scan (notebooks_com_flashcards.json) para
baixar cada set de flashcards e converter para .apkg individual.

USO:
  python3 scripts/batch_nlm_download.py           # baixa todos
  python3 scripts/batch_nlm_download.py --limit 10 # apenas os 10 primeiros
  python3 scripts/batch_nlm_download.py --merge    # gera 1 .apkg com tudo
"""
import json
import hashlib
import os
import re
import subprocess
import argparse
import time
from pathlib import Path

import genanki
import random

random.seed(78)

# CSS, modelo e funções de texto centralizados em shared.py
from shared import CARD_CSS, create_model, enriquecer_html, safe_name

MODEL = create_model()


def baixar_flashcards(notebook_id, title, output_dir):
    """Baixa flashcards de um notebook específico."""
    json_path = os.path.join(output_dir, f"nlm_{safe_name(title)}.json")

    if os.path.exists(json_path):
        return json_path  # já baixado

    # Set context
    r = subprocess.run(["notebooklm", "use", notebook_id], capture_output=True)
    if r.returncode != 0:
        return None

    # Download
    r = subprocess.run(
        ["notebooklm", "download", "flashcards", json_path],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        return None

    return json_path


def converter_json(json_path, deck_name):
    """Converte JSON para lista de notas genanki."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"⚠️  Erro ao ler {json_path}: {e}")
        return []

    notas = []
    for card in data.get('cards', []):
        front = enriquecer_html(card.get('front', ''))
        back = enriquecer_html(card.get('back', ''))
        if front and back:
            tag = safe_name(deck_name).lower()[:30]
            notas.append(genanki.Note(
                model=MODEL, fields=[front, back],
                tags=['notebooklm', tag]
            ))
    return notas


def main():
    parser = argparse.ArgumentParser(description="Batch download NotebookLM → Anki")
    parser.add_argument("--limit", type=int, help="Máximo de notebooks a processar")
    parser.add_argument("--merge", action="store_true", help="Gerar 1 .apkg com tudo")
    args = parser.parse_args()

    base = Path(__file__).parent.parent
    dados_dir = str(base / "dados" / "nlm_batch")
    output_dir = str(base / "output")
    os.makedirs(dados_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Carregar lista de notebooks com flashcards
    with open(base / "dados" / "notebooks_com_flashcards.json") as f:
        notebooks = json.load(f)

    if args.limit:
        notebooks = notebooks[:args.limit]

    print(f"📦 Batch download: {len(notebooks)} notebooks")
    print(f"{'=' * 60}\n")

    all_decks = []
    total_cards = 0
    errors = 0

    for i, (nid, title, _count) in enumerate(notebooks):
        print(f"  [{i+1:3d}/{len(notebooks)}] {title[:55]}...", end=" ", flush=True)

        json_path = baixar_flashcards(nid, title, dados_dir)
        if not json_path:
            print("❌ falhou")
            errors += 1
            continue

        # Converter
        deck_name = f"NLM::{title[:60]}"
        notas = converter_json(json_path, title)

        if not notas:
            print("⚠️  0 cards")
            continue

        deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16) % (10**9) + 3000000000
        deck = genanki.Deck(deck_id, deck_name)
        for n in notas:
            deck.add_note(n)

        all_decks.append(deck)
        total_cards += len(notas)
        print(f"✅ {len(notas)} cards")

        # Rate limiting gentil
        time.sleep(0.5)

    # Exportar
    print(f"\n{'=' * 60}")
    print(f"Total: {total_cards} cards de {len(all_decks)} notebooks ({errors} erros)")

    if args.merge and all_decks:
        merged_path = os.path.join(output_dir, "NLM_TODOS.apkg")
        package = genanki.Package(all_decks)
        package.write_to_file(merged_path)
        print(f"\n✅ Arquivo único: {merged_path}")
    elif all_decks:
        # Gerar .apkg individual por notebook
        for deck in all_decks:
            name = safe_name(deck.name.replace('NLM::', ''))
            path = os.path.join(output_dir, f"NLM_{name}.apkg")
            genanki.Package([deck]).write_to_file(path)
        print(f"\n✅ {len(all_decks)} arquivos .apkg em {output_dir}/")

    # Relatório
    report = {
        'total_notebooks': len(notebooks),
        'downloaded': len(all_decks),
        'total_cards': total_cards,
        'errors': errors,
        'decks': [{'name': d.name, 'cards': len(d.notes)} for d in all_decks]
    }
    report_path = os.path.join(str(base / "dados"), "batch_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"📊 Relatório: {report_path}")


if __name__ == "__main__":
    main()
