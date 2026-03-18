#!/usr/bin/env python3
"""
📦 batch_por_categoria.py — Organiza flashcards NotebookLM por categoria temática

Lê os JSONs já baixados (dados/nlm_batch/) e gera 1 .apkg por categoria,
cada um com sub-decks por notebook.

Resultado:
  output/NLM-Programação.apkg     → NLM::Programação::CS50, Git, Python...
  output/NLM-Medicina.apkg        → NLM::Medicina::Via Aérea, ACLS, ECG...
  output/NLM-Data.apkg            → NLM::Data::P2P, DAX, SQL...
  output/NLM-Ferramentas.apkg     → NLM::Ferramentas::Obsidian, Zotero...
  output/NLM-Gestão.apkg          → NLM::Gestão::Lean, SBIS...
  output/NLM-Finanças.apkg        → NLM::Finanças::Investimentos, Tesouro...
  output/NLM-Outros.apkg          → NLM::Outros::Salsa, Johnny Decimal...

USO:
  python3 scripts/batch_por_categoria.py              # gera todos
  python3 scripts/batch_por_categoria.py --categoria Programação  # só 1
"""
import json
import hashlib
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict

import genanki
import random

random.seed(79)

# CSS, modelo e funções de texto centralizados em shared.py
from shared import CARD_CSS, create_model, enriquecer_html, safe_name, limpar_titulo, categorizar

MODEL = create_model()


# Categorização agora vem de shared.py (CATEGORIAS + categorizar)


def main():
    parser = argparse.ArgumentParser(description="Organizar flashcards por categoria")
    parser.add_argument("--categoria", help="Gerar só uma categoria")
    args = parser.parse_args()

    base = Path(__file__).parent.parent
    batch_dir = base / "dados" / "nlm_batch"
    output_dir = base / "output"
    output_dir.mkdir(exist_ok=True)

    # Carregar lista de notebooks
    with open(base / "dados" / "notebooks_com_flashcards.json") as f:
        notebooks = json.load(f)

    # Mapear ID → título
    id_to_title = {nid: title for nid, title, _ in notebooks}

    # Agrupar JSONs por categoria
    por_categoria = defaultdict(list)

    json_files = sorted(batch_dir.glob("nlm_*.json")) if batch_dir.exists() else []
    # Também incluir JSONs na pasta dados/ raiz (como nlm_git_flashcards.json)
    json_files += sorted((base / "dados").glob("nlm_*.json"))

    # Deduplicate
    seen = set()
    unique_files = []
    for f in json_files:
        if f.name not in seen:
            seen.add(f.name)
            unique_files.append(f)

    print(f"📂 {len(unique_files)} JSONs de flashcards encontrados\n")

    for json_path in unique_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError, OSError) as e:
            print(f"⚠️  Erro ao ler {json_path}: {e}")
            continue

        title = data.get('title', json_path.stem)
        # Tentar encontrar o título original do notebook
        for nid, orig_title, _ in notebooks:
            if safe_name(orig_title) in json_path.stem or safe_name(title) in json_path.stem:
                title = orig_title
                break

        cat = categorizar(title, json_path.name)
        cards = data.get('cards', [])
        if cards:
            por_categoria[cat].append((title, cards))

    # Stats
    print("📊 Distribuição por categoria:")
    for cat in sorted(por_categoria.keys()):
        items = por_categoria[cat]
        total_cards = sum(len(cards) for _, cards in items)
        print(f"  {cat}: {len(items)} notebooks, {total_cards} cards")

    print()

    # Filtrar se pediu só uma categoria
    if args.categoria:
        if args.categoria not in por_categoria:
            print(f"❌ Categoria '{args.categoria}' não encontrada")
            print(f"   Disponíveis: {', '.join(sorted(por_categoria.keys()))}")
            return
        por_categoria = {args.categoria: por_categoria[args.categoria]}

    # Gerar .apkg por categoria
    for cat, items in sorted(por_categoria.items()):
        decks = []
        total_cards = 0

        for title, cards in items:
            clean = limpar_titulo(title)
            deck_name = f"NLM::{cat}::{clean}"
            deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16) % (10**9) + 3000000000
            deck = genanki.Deck(deck_id, deck_name)

            for card in cards:
                front = enriquecer_html(card.get('front', ''))
                back = enriquecer_html(card.get('back', ''))
                if front and back:
                    tag = f"nlm_{cat.lower()}"
                    deck.add_note(genanki.Note(
                        model=MODEL, fields=[front, back],
                        tags=['notebooklm', tag]
                    ))

            if deck.notes:
                decks.append(deck)
                total_cards += len(deck.notes)

        if decks:
            apkg_path = output_dir / f"NLM-{cat}.apkg"
            genanki.Package(decks).write_to_file(str(apkg_path))
            print(f"✅ {apkg_path.name}: {len(decks)} decks, {total_cards} cards")

    print(f"\n💡 Para importar: Anki > File > Import > selecionar o .apkg da categoria desejada")


if __name__ == "__main__":
    main()
