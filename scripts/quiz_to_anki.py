#!/usr/bin/env python3
"""
🧩 quiz_to_anki.py — Converte quizzes do NotebookLM para Anki (.apkg)

FORMATO DO QUIZ DO NOTEBOOKLM:
──────────────────────────────
{
  "title": "...",
  "questions": [{
    "question": "Pergunta aqui",
    "answerOptions": [
      {"text": "Opção A", "isCorrect": false, "rationale": "Por que está errada"},
      {"text": "Opção B", "isCorrect": true,  "rationale": "Por que está certa"},
      ...
    ],
    "hint": "Dica opcional"
  }]
}

COMO CONVERTE PARA ANKI:
─────────────────────────
Cada questão vira 1 card com:
  - Frente: pergunta + opções embaralhadas (A, B, C, D)
  - Verso: resposta correta destacada + rationale de TODAS as opções

Isso é melhor que Cloze para múltipla escolha porque:
  1. Você vê as opções na frente (simula prova real)
  2. A rationale ensina POR QUE cada alternativa está certa/errada
  3. O hint aparece como callout na frente (ajuda sem dar a resposta)

USO:
  python3 scripts/quiz_to_anki.py dados/nlm_git_quiz.json
  python3 scripts/quiz_to_anki.py dados/nlm_git_quiz.json --deck "NLM::Quiz::Git"
  python3 scripts/quiz_to_anki.py --scan          # baixar quizzes de todos os notebooks
  python3 scripts/quiz_to_anki.py --categorize     # organizar por categoria (como batch_por_categoria)
"""
import json
import hashlib
import os
import re
import subprocess
import argparse
from pathlib import Path
from collections import defaultdict

import genanki
import random

random.seed(88)  # Seed única para quizzes (diferente de flashcards: 77-79)

# Importar módulo compartilhado
import sys
sys.path.insert(0, str(Path(__file__).parent))
from shared import CARD_CSS, enriquecer_html, safe_name, limpar_titulo

# ─── CSS estendido para quizzes ───────────────────────────────
# Herda o CARD_CSS base e adiciona estilos para opções de múltipla escolha
QUIZ_CSS = CARD_CSS + '''
.options { margin: 16px 0 0; }
.opt {
  padding: 8px 12px; margin: 6px 0;
  border-radius: 6px; font-size: 14px; line-height: 1.5;
  border: 1px solid rgba(69,71,90,0.4);
  background: rgba(49,50,68,0.3);
}
.opt-label {
  font-weight: 600; color: #89b4fa;
  margin-right: 8px;
}
.opt-correct {
  border-color: rgba(166,227,161,0.6);
  background: rgba(166,227,161,0.08);
}
.opt-wrong {
  border-color: rgba(243,139,168,0.3);
  background: rgba(243,139,168,0.04);
  opacity: 0.8;
}
.rationale {
  font-size: 12.5px; color: #7f849c;
  margin-top: 4px; padding-left: 24px;
  line-height: 1.4;
}
.hint {
  background: rgba(137,180,250,0.06);
  border-left: 2px solid rgba(137,180,250,0.4);
  padding: 8px 12px; margin: 12px 0 0;
  border-radius: 0 6px 6px 0;
  font-size: 13px; color: #a6adc8;
}
.correct-banner {
  background: rgba(166,227,161,0.1);
  border: 1px solid rgba(166,227,161,0.3);
  border-radius: 8px; padding: 10px 14px;
  margin-bottom: 12px; font-weight: 600;
  color: #a6e3a1;
}
'''

# Note type específico para quizzes
QUIZ_MODEL = genanki.Model(
    1607392088,  # ID único para quizzes
    'NotebookLM Quiz',
    fields=[
        {'name': 'Pergunta'},    # Pergunta + opções (frente)
        {'name': 'Resposta'},    # Resposta correta + rationales (verso)
    ],
    templates=[{
        'name': 'Quiz Card',
        'qfmt': '<div class="front">{{Pergunta}}</div>',
        'afmt': '<div class="front">{{Pergunta}}</div><hr id="answer"><div class="back">{{Resposta}}</div>',
    }],
    css=QUIZ_CSS,
)


# ─── Categorização (mesmas regras de batch_por_categoria.py) ──
CATEGORIAS = [
    (["CS50", "ASIMOV", "Python", "Git", "SQL", "DS-CLI", "DS_CLI",
      "CLI", "Shell", "Bash", "Script", "Missing Semester",
      "Vim", "IDE", "Ambiente de Desenvolvimento", "Doc-as-code",
      "Ciência de Dados", "Linha de Comando", "Lógica de Programação",
      "Fundamentos do Desenvolvimento", "Ferramenta", "MCP", "Agno",
      "LangChain", "Streamlit", "Machine Learning",
      "Manipulação Correta de Nomes", "Automação de Tarefas com Cron",
      "Symlinks", "Matplotlib", "Plotly", "Seaborn", "OpenPyEx",
      "LM Studio", "API"], "Programação"),
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
    (["P2P", "Dados", "Data", "Modelagem", "DAX", "Power",
      "Planilha", "Dashboard", "Indicadores", "KNIME",
      "Warehouse", "Estatística", "Regressão", "Amostragem",
      "Hipótese", "Inferência", "EDA", "Visualização",
      "Narrativas de Dados", "Pareto", "Governança"], "Data"),
    (["Obsidian", "Zotero", "Hazel", "Keyboard Maestro",
      "SiteSucker", "Downie", "Text Blaze", "NotebookLM",
      "Dotfiles", "Backup", "SSH", "Navegador", "iPhone",
      "Máquinas Virtuais", "Contêiner"], "Ferramentas"),
    (["Lean", "Gestão", "UPA", "Jornada do Paciente",
      "SBIS", "Prontuário", "FRAM", "Regulação",
      "Superlotação", "Protocolo de Londres", "Workshop",
      "Operações", "Liderança", "Qualidade", "Serviço",
      "SAMU", "Excelência", "Certificação", "Rede Atenção",
      "GRADE"], "Gestão"),
    (["Investimento", "Renda Fixa", "Tesouro", "Dólar",
      "Finanças", "FIN"], "Finanças"),
]


def categorizar(titulo: str) -> str:
    for patterns, cat in CATEGORIAS:
        for p in patterns:
            if p.lower() in titulo.lower():
                return cat
    return "Outros"


def formatar_questao_frente(q: dict) -> str:
    """
    Gera o HTML da frente do card (pergunta + opções).

    As opções são listadas como A, B, C, D com estilo neutro
    (sem indicar qual é a correta).
    """
    html = f'<div style="margin-bottom: 16px;">{enriquecer_html(q["question"])}</div>'
    html += '<div class="options">'

    labels = 'ABCDEFGH'
    for i, opt in enumerate(q.get('answerOptions', [])):
        label = labels[i] if i < len(labels) else str(i + 1)
        text = enriquecer_html(opt['text'])
        html += f'<div class="opt"><span class="opt-label">{label})</span> {text}</div>'

    # Hint (se existir)
    hint = q.get('hint', '')
    if hint:
        html += f'<div class="hint">💡 Dica: {enriquecer_html(hint)}</div>'

    html += '</div>'
    return html


def formatar_questao_verso(q: dict) -> str:
    """
    Gera o HTML do verso (resposta correta + rationale de todas as opções).

    A opção correta é destacada em verde, as erradas em vermelho sutil.
    Cada opção mostra seu rationale — isso ensina POR QUE está certa/errada,
    não apenas QUAL é a certa.
    """
    # Encontrar resposta correta
    correct = [o for o in q.get('answerOptions', []) if o.get('isCorrect')]
    correct_text = correct[0]['text'] if correct else '?'

    html = f'<div class="correct-banner">✅ {enriquecer_html(correct_text)}</div>'
    html += '<div class="options">'

    labels = 'ABCDEFGH'
    for i, opt in enumerate(q.get('answerOptions', [])):
        label = labels[i] if i < len(labels) else str(i + 1)
        text = enriquecer_html(opt['text'])
        is_correct = opt.get('isCorrect', False)
        css_class = 'opt opt-correct' if is_correct else 'opt opt-wrong'
        marker = '✅' if is_correct else '❌'

        html += f'<div class="{css_class}">'
        html += f'<span class="opt-label">{label})</span> {marker} {text}'

        rationale = opt.get('rationale', '')
        if rationale:
            html += f'<div class="rationale">{enriquecer_html(rationale)}</div>'

        html += '</div>'

    html += '</div>'
    return html


def converter_quiz_json(json_path: str, deck_name: str = None) -> tuple[list, str]:
    """
    Converte 1 JSON de quiz em lista de notas genanki.

    Returns:
        (notas, título)
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get('title', Path(json_path).stem)
    questions = data.get('questions', [])

    if not questions:
        return [], title

    notas = []
    for q in questions:
        frente = formatar_questao_frente(q)
        verso = formatar_questao_verso(q)

        if frente and verso:
            tag = safe_name(title).lower()[:30]
            notas.append(genanki.Note(
                model=QUIZ_MODEL,
                fields=[frente, verso],
                tags=['notebooklm', 'quiz', tag],
            ))

    return notas, title


def converter_arquivo(json_path: str, deck_name: str = None, output_dir: str = None) -> str:
    """Converte 1 arquivo JSON de quiz para .apkg."""
    notas, title = converter_quiz_json(json_path, deck_name)

    if not notas:
        print(f"⚠️  0 questões em {json_path}")
        return ""

    if not deck_name:
        clean = limpar_titulo(title)
        deck_name = f"NLM::Quiz::{clean}"

    deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16) % (10**9) + 4000000000
    deck = genanki.Deck(deck_id, deck_name)
    for n in notas:
        deck.add_note(n)

    if not output_dir:
        output_dir = str(Path(__file__).parent.parent / "output")
    os.makedirs(output_dir, exist_ok=True)

    fname = f"Quiz_{safe_name(title)}.apkg"
    output_path = os.path.join(output_dir, fname)

    genanki.Package([deck]).write_to_file(output_path)
    print(f"✅ {output_path}: {len(notas)} questões → '{deck_name}'")
    return output_path


def scan_e_baixar_quizzes() -> list[str]:
    """
    Escaneia todos os notebooks, baixa quizzes existentes.

    Reutiliza a lista de notebooks_com_flashcards.json como base
    (notebooks com flashcards provavelmente têm quiz também).
    """
    base = Path(__file__).parent.parent
    dados_dir = base / "dados" / "nlm_quizzes"
    dados_dir.mkdir(parents=True, exist_ok=True)

    # Carregar lista de notebooks
    nb_list = base / "dados" / "notebooks_com_flashcards.json"
    if not nb_list.exists():
        print("⚠️  Execute primeiro: python3 scripts/batch_nlm_download.py")
        return []

    with open(nb_list) as f:
        notebooks = json.load(f)

    print(f"🔍 Verificando {len(notebooks)} notebooks para quizzes...\n")
    downloaded = []

    for i, (nid, title, _) in enumerate(notebooks):
        # Set context
        subprocess.run(["notebooklm", "use", nid], capture_output=True)

        # Check artifacts
        result = subprocess.run(
            ["notebooklm", "artifact", "list", "--json"],
            capture_output=True, text=True
        )

        try:
            artifacts = json.loads(result.stdout)
            quizzes = [a for a in artifacts.get('artifacts', [])
                       if a.get('type_id') == 'quiz' and a.get('status') == 'completed']
        except (json.JSONDecodeError, KeyError, OSError):
            continue

        if quizzes:
            fname = safe_name(title)
            json_path = str(dados_dir / f"quiz_{fname}.json")

            if not os.path.exists(json_path):
                r = subprocess.run(
                    ["notebooklm", "download", "quiz", json_path],
                    capture_output=True, text=True
                )
                if r.returncode == 0:
                    print(f"  ✅ [{i+1:3d}] {title[:55]}")
                    downloaded.append(json_path)
            else:
                downloaded.append(json_path)

        if (i + 1) % 20 == 0:
            print(f"  ... verificados {i+1}/{len(notebooks)}")

    print(f"\n📥 {len(downloaded)} quizzes baixados para dados/nlm_quizzes/")
    return downloaded


def categorizar_quizzes():
    """Organiza quizzes baixados por categoria e gera .apkg por tema."""
    base = Path(__file__).parent.parent
    quiz_dir = base / "dados" / "nlm_quizzes"
    output_dir = base / "output"

    if not quiz_dir.exists():
        print("⚠️  Nenhum quiz baixado. Rode com --scan primeiro.")
        return

    json_files = sorted(quiz_dir.glob("quiz_*.json"))
    print(f"📂 {len(json_files)} quizzes encontrados\n")

    # Agrupar por categoria
    por_cat = defaultdict(list)
    for jp in json_files:
        try:
            with open(jp, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"⚠️  Erro: {jp}: {e}")
            continue

        title = data.get('title', jp.stem)
        cat = categorizar(title)
        notas, _ = converter_quiz_json(str(jp))
        if notas:
            por_cat[cat].append((title, notas))

    print("📊 Distribuição:")
    for cat in sorted(por_cat):
        total = sum(len(n) for _, n in por_cat[cat])
        print(f"  {cat}: {len(por_cat[cat])} quizzes, {total} questões")

    print()

    for cat, items in sorted(por_cat.items()):
        decks = []
        total = 0
        for title, notas in items:
            clean = limpar_titulo(title)
            deck_name = f"NLM::Quiz::{cat}::{clean}"
            deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16) % (10**9) + 4000000000
            deck = genanki.Deck(deck_id, deck_name)
            for n in notas:
                deck.add_note(n)
            decks.append(deck)
            total += len(notas)

        if decks:
            apkg_path = output_dir / f"Quiz-{cat}.apkg"
            genanki.Package(decks).write_to_file(str(apkg_path))
            print(f"✅ {apkg_path.name}: {len(decks)} quizzes, {total} questões")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converter quizzes NotebookLM → Anki")
    parser.add_argument("json_file", nargs="?", help="JSON de quiz para converter")
    parser.add_argument("--deck", help="Nome do deck destino")
    parser.add_argument("--scan", action="store_true", help="Escanear e baixar quizzes de todos os notebooks")
    parser.add_argument("--categorize", action="store_true", help="Organizar quizzes baixados por categoria")
    args = parser.parse_args()

    if args.scan:
        scan_e_baixar_quizzes()
    elif args.categorize:
        categorizar_quizzes()
    elif args.json_file:
        converter_arquivo(args.json_file, args.deck)
    else:
        parser.print_help()
        print("\nExemplos:")
        print("  python3 scripts/quiz_to_anki.py dados/nlm_git_quiz.json")
        print("  python3 scripts/quiz_to_anki.py --scan         # baixar de todos os notebooks")
        print("  python3 scripts/quiz_to_anki.py --categorize   # gerar .apkg por categoria")
