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
import os
import re
import subprocess
import argparse
import time
from pathlib import Path

import genanki
import random

random.seed(77)

# Reutilizar CSS e Model do notebooklm_to_anki.py
CARD_CSS = '''
.card { font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; font-size: 15px; line-height: 1.6; text-align: left; color: #bac2de; background-color: #181825; padding: 28px 24px; max-width: 65ch; margin: 0 auto; }
.front { font-size: 17px; font-weight: 600; line-height: 1.45; color: #cdd6f4; }
.back { font-size: 15px; line-height: 1.65; color: #a6adc8; }
.back b, .back strong { color: #cdd6f4; font-weight: 600; }
code { font-family: "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace; font-size: 0.88em; color: #94e2d5; background: rgba(49,50,68,0.7); padding: 2px 7px; border-radius: 4px; border: 1px solid rgba(69,71,90,0.5); }
pre { background: #11111b; padding: 16px 18px; border-radius: 8px; border: 1px solid rgba(49,50,68,0.8); overflow-x: auto; margin: 12px 0; }
pre code { padding: 0; background: none; border: none; color: #a6e3a1; font-size: 13px; line-height: 1.7; }
hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #45475a 15%, #585b70 50%, #45475a 85%, transparent 100%); margin: 20px 0; }
.nightMode .card { background-color: #181825; }
'''

MODEL = genanki.Model(
    1607392077, 'NotebookLM Import',
    fields=[{'name': 'Frente'}, {'name': 'Verso'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="front">{{Frente}}</div>',
        'afmt': '<div class="front">{{Frente}}</div><hr id="answer"><div class="back">{{Verso}}</div>',
    }],
    css=CARD_CSS,
)


def enriquecer_html(texto):
    texto = re.sub(r'`([^`]+)`', r'<code>\1</code>', texto)
    cmd_patterns = [r'\b(git\s+\w+(?:\s+--?\w+)*)', r'\b(ssh-keygen\b)',
                    r'\b(pip\s+install\s+\S+)', r'\b(python3?\s+\S+)']
    for p in cmd_patterns:
        texto = re.sub(p, r'<code>\1</code>', texto)
    texto = texto.replace('<code><code>', '<code>').replace('</code></code>', '</code>')
    return texto


def safe_name(title):
    return re.sub(r'[^\w-]', '_', title)[:50].strip('_')


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
    except:
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

        deck_id = abs(hash(deck_name)) % (10**9) + 3000000000
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
