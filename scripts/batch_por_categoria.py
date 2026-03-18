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
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict

import genanki
import random

random.seed(77)

# ─── CSS ──────────────────────────────────────────────────────
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
@media (max-width: 480px) { .card { padding: 22px 18px; } .front { font-size: 16px; } }
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


# ─── Regras de categorização ─────────────────────────────────
# Cada regra: (padrões no título, categoria)

CATEGORIAS = [
    # Programação / CS / CLI
    (["CS50", "ASIMOV", "Python", "Git", "SQL", "DS-CLI", "DS_CLI",
      "CLI", "Shell", "Bash", "Script", "Missing Semester",
      "Vim", "IDE", "Ambiente de Desenvolvimento", "Doc-as-code",
      "Ciência de Dados", "Linha de Comando", "Lógica de Programação",
      "Fundamentos do Desenvolvimento", "Ferramenta", "MCP", "Agno",
      "LangChain", "Streamlit", "Machine Learning",
      "Manipulação Correta de Nomes", "Automação de Tarefas com Cron",
      "Symlinks", "Matplotlib", "Plotly", "Seaborn", "OpenPyEx",
      "LM Studio", "API"], "Programação"),

    # Medicina / Emergência
    (["EM", "Pediatr", "Via Aérea", "Intub", "ACLS", "PALS",
      "Ressuscit", "Trauma", "ECG", "cardio", "Dispneia",
      "Emergênci", "Cetoacidose", "Sepse", "BVM", "Ventil",
      "Bolsa-Válvula", "Manejo", "MBE", "Cuidados Paliativos",
      "Lesão Renal", "Hipertensão", "Coronária", "Dor Torácica",
      "Probabilidade Pré-Teste", "Epidemiologia",
      "Emergência Pediátrica", "PEM", "Abordagem Prática",
      "Malpractice", "Suporte Básico", "Suporte Avançado",
      "Gemini TextBlaze", "estatística na prática médica",
      "análise bayesiana"], "Medicina"),

    # Data / P2P / Análise
    (["P2P", "Dados", "Data", "Modelagem", "DAX", "Power",
      "Planilha", "Dashboard", "Indicadores", "KNIME",
      "Warehouse", "Estatística", "Regressão", "Amostragem",
      "Hipótese", "Inferência", "EDA", "Visualização",
      "Narrativas de Dados", "Pareto", "Governança"], "Data"),

    # Obsidian / Ferramentas de produtividade
    (["Obsidian", "Zotero", "Hazel", "Keyboard Maestro",
      "SiteSucker", "Downie", "Text Blaze", "NotebookLM",
      "Dotfiles", "Backup", "SSH", "Navegador", "iPhone",
      "Máquinas Virtuais", "Contêiner"], "Ferramentas"),

    # Lean / Gestão / Saúde pública
    (["Lean", "Gestão", "UPA", "Jornada do Paciente",
      "SBIS", "Prontuário", "FRAM", "Regulação",
      "Superlotação", "Protocolo de Londres", "Workshop",
      "Operações", "Liderança", "Qualidade", "Serviço",
      "SAMU", "Excelência", "Certificação", "Rede Atenção",
      "GRADE"], "Gestão"),

    # Finanças
    (["Investimento", "Renda Fixa", "Tesouro", "Dólar",
      "Finanças", "FIN"], "Finanças"),
]


def categorizar(titulo: str) -> str:
    """Determina a categoria de um notebook pelo título."""
    for patterns, cat in CATEGORIAS:
        for p in patterns:
            if p.lower() in titulo.lower():
                return cat
    return "Outros"


def enriquecer_html(texto: str) -> str:
    texto = re.sub(r'`([^`]+)`', r'<code>\1</code>', texto)
    cmd_patterns = [r'\b(git\s+\w+(?:\s+--?\w+)*)', r'\b(ssh-keygen\b)',
                    r'\b(pip\s+install\s+\S+)', r'\b(python3?\s+\S+)',
                    r'\b(SELECT\s+\w+)', r'\b(CREATE\s+\w+)', r'\b(INSERT\s+\w+)']
    for p in cmd_patterns:
        texto = re.sub(p, r'<code>\1</code>', texto)
    texto = texto.replace('<code><code>', '<code>').replace('</code></code>', '</code>')
    return texto


def safe_name(title: str) -> str:
    return re.sub(r'[^\w-]', '_', title)[:50].strip('_')


def limpar_titulo(titulo: str) -> str:
    """Remove prefixos como [EM], [ASIMOV], P2P_ment_pro_6: etc."""
    # Remove [tags]
    titulo = re.sub(r'\[.*?\]\s*', '', titulo)
    # Remove prefixos P2P_ment_xxx_NN:
    titulo = re.sub(r'P2P_\w+_\d+:\s*', '', titulo)
    # Remove DS-CLI N / DS_CLI_N
    titulo = re.sub(r'DS[-_]CLI[-_]?\d+:?\s*', 'DS-CLI: ', titulo)
    # Remove MBE_NN:
    titulo = re.sub(r'MBE_\d+:\s*', 'MBE: ', titulo)
    return titulo.strip()


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
        except:
            continue

        title = data.get('title', json_path.stem)
        # Tentar encontrar o título original do notebook
        for nid, orig_title, _ in notebooks:
            if safe_name(orig_title) in json_path.stem or safe_name(title) in json_path.stem:
                title = orig_title
                break

        cat = categorizar(title)
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
            deck_id = abs(hash(deck_name)) % (10**9) + 3000000000
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
