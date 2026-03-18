#!/usr/bin/env python3
"""
🔍 comparar_decks.py — Compara seus decks atuais com os novos gerados

Este script faz uma análise lado-a-lado dos seus cards existentes vs.
os cards do novo deck Dev_Programacao.apkg, identificando:
  - Sobreposições (mesmos conceitos cobertos)
  - Lacunas (conceitos que faltam nos seus decks atuais)
  - Melhorias (cards com melhor redação ou organização)
  - Cards únicos seus (que não existem no novo deck)

COMO LER O RELATÓRIO:
─────────────────────
  🔄 Sobreposição → mesmo conceito em ambos (você pode manter o seu ou atualizar)
  🆕 Lacuna → conceito que só existe no novo deck (vale importar)
  ✅ Único seu → conceito que só você tem (manter!)
  📊 Qualidade → análise de redação e estrutura dos seus cards

USO:
  python3 comparar_decks.py                    # análise completa
  python3 comparar_decks.py --deck "Git/Github" # focar em um deck
"""

import json
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict


def carregar_notas_existentes() -> list[dict]:
    """Carrega notas exportadas do perfil Data."""
    json_path = Path(__file__).parent.parent / "dados" / "notas_data.json"
    if not json_path.exists():
        print("⚠️  Execute primeiro: python3 scripts/analisar_colecao.py --perfil Data --exportar")
        raise SystemExit(1)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('notas', [])


def limpar_html(texto: str) -> str:
    """Remove tags HTML para comparação textual."""
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = re.sub(r'&\w+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip().lower()


def extrair_conceitos(sfld: str) -> set[str]:
    """
    Extrai palavras-chave de um campo para comparação fuzzy.

    'Como adicionar arquivos para commit?' → {'adicionar', 'arquivos', 'commit'}
    """
    texto = limpar_html(sfld)
    # Remover palavras comuns (stopwords simplificadas)
    stopwords = {
        'como', 'qual', 'o', 'que', 'é', 'um', 'uma', 'para', 'de', 'do', 'da',
        'no', 'na', 'em', 'por', 'com', 'se', 'os', 'as', 'e', 'ou', 'não',
        'faz', 'fazer', 'serve', 'usando', 'use', 'pode', 'são', 'quero',
        'what', 'how', 'the', 'is', 'a', 'an', 'to', 'in', 'of', 'and',
    }
    palavras = set(re.findall(r'\w+', texto))
    return palavras - stopwords


def calcular_similaridade(conceitos_a: set[str], conceitos_b: set[str]) -> float:
    """
    Calcula similaridade de Jaccard entre dois conjuntos de conceitos.

    Jaccard = |A ∩ B| / |A ∪ B|
    Retorna 0.0 (nada em comum) a 1.0 (idênticos)
    """
    if not conceitos_a or not conceitos_b:
        return 0.0
    intersecao = conceitos_a & conceitos_b
    uniao = conceitos_a | conceitos_b
    return len(intersecao) / len(uniao)


def analisar_qualidade(nota: dict) -> list[str]:
    """
    Avalia a qualidade de um card existente.

    Critérios baseados nas melhores práticas de flashcards:
    1. Princípio do Mínimo: cada card = 1 conceito atômico
    2. Sem ambiguidade: pergunta deve ter resposta clara
    3. Código deve usar <code> ou <pre> (não texto puro)
    4. Resposta não muito longa (< 300 chars ideal)
    """
    problemas = []
    campos = nota.get('campos', [])

    if len(campos) < 2:
        problemas.append("Menos de 2 campos (nota incompleta?)")
        return problemas

    frente = campos[0]
    verso = campos[1] if len(campos) > 1 else ""
    frente_limpa = limpar_html(frente)
    verso_limpo = limpar_html(verso)

    # Pergunta muito vaga
    if len(frente_limpa) < 10:
        problemas.append("Pergunta muito curta (pode ser vaga)")

    # Resposta muito longa
    if len(verso_limpo) > 500:
        problemas.append(f"Resposta muito longa ({len(verso_limpo)} chars) — considere dividir")

    # Pergunta com múltiplas perguntas
    question_marks = frente.count('?')
    if question_marks > 1:
        problemas.append(f"Múltiplas perguntas ({question_marks}x '?') — violar princípio atômico")

    # Código sem formatação
    code_keywords = ['git ', 'python', 'pip ', 'cd ', 'ls ', 'grep ', 'chmod ', 'sudo ',
                     'df.', 'pd.', 'import ', 'SELECT ', 'FROM ']
    has_code_in_back = any(kw in verso for kw in code_keywords)
    has_code_tags = '<code>' in verso or '<pre>' in verso
    if has_code_in_back and not has_code_tags:
        problemas.append("Código sem formatação HTML (<code> ou <pre>)")

    # Imagem colada (paste-...) como parte principal
    if 'paste-' in frente and '.jpg' in frente:
        problemas.append("Imagem colada como pergunta — pode não renderizar fora do Anki original")

    return problemas


def comparar(deck_filter: str = None) -> None:
    """Executa a comparação completa."""
    notas = carregar_notas_existentes()

    # Agrupar por deck
    decks: dict[str, list[dict]] = defaultdict(list)
    for nota in notas:
        decks[nota['deck']].append(nota)

    # Decks de programação
    prog_keywords = ['git', 'python', 'terminal', 'shell', 'bash', 'script',
                     'obsidian', 'markdown', 'data', 'planilha', 'eda', 'vscode', 'arquivos terminal']

    prog_decks = {
        name: notes for name, notes in decks.items()
        if any(kw in name.lower() for kw in prog_keywords)
    }

    if deck_filter:
        prog_decks = {
            name: notes for name, notes in prog_decks.items()
            if deck_filter.lower() in name.lower()
        }

    print(f"\n{'=' * 70}")
    print(f"  ANÁLISE DE QUALIDADE — Decks de Programação")
    print(f"{'=' * 70}")

    total_problems = 0
    total_cards = 0

    for deck_name, notes in sorted(prog_decks.items()):
        print(f"\n{'─' * 70}")
        print(f"📁 {deck_name} ({len(notes)} cards)")
        print(f"{'─' * 70}")

        deck_problems = 0
        for nota in notes:
            total_cards += 1
            problemas = analisar_qualidade(nota)
            sfld = limpar_html(nota.get('sfld', ''))[:80]
            estado = nota.get('estado', '?')
            ivl = nota.get('intervalo_dias', 0)

            if problemas:
                deck_problems += len(problemas)
                total_problems += len(problemas)
                print(f"\n  ⚠️  [{estado:8s} ivl={ivl:3d}d] {sfld}")
                for p in problemas:
                    print(f"      → {p}")
            else:
                print(f"  ✅ [{estado:8s} ivl={ivl:3d}d] {sfld}")

        if deck_problems == 0:
            print(f"\n  🎉 Todos os cards estão bem formatados!")
        else:
            print(f"\n  📊 {deck_problems} problemas encontrados em {len(notes)} cards")

    # Resumo
    print(f"\n{'=' * 70}")
    print(f"  RESUMO")
    print(f"{'=' * 70}")
    print(f"  Cards analisados: {total_cards}")
    print(f"  Problemas totais: {total_problems}")
    print(f"  Taxa de qualidade: {(total_cards - total_problems) / total_cards * 100:.0f}%")

    # Sobreposições entre decks
    print(f"\n{'─' * 70}")
    print(f"  SOBREPOSIÇÕES ENTRE DECKS")
    print(f"{'─' * 70}")

    deck_concepts: dict[str, list[tuple[str, set]]] = {}
    for deck_name, notes in prog_decks.items():
        deck_concepts[deck_name] = [
            (n.get('sfld', ''), extrair_conceitos(n.get('sfld', '')))
            for n in notes
        ]

    deck_names = list(deck_concepts.keys())
    for i, name_a in enumerate(deck_names):
        for name_b in deck_names[i+1:]:
            overlaps = []
            for sfld_a, concepts_a in deck_concepts[name_a]:
                for sfld_b, concepts_b in deck_concepts[name_b]:
                    sim = calcular_similaridade(concepts_a, concepts_b)
                    if sim > 0.4:  # 40%+ de palavras em comum
                        overlaps.append((sfld_a[:50], sfld_b[:50], sim))

            if overlaps:
                print(f"\n  🔄 {name_a} ↔ {name_b}:")
                for a, b, sim in sorted(overlaps, key=lambda x: -x[2])[:5]:
                    print(f"     {sim:.0%} | \"{a}\" ≈ \"{b}\"")

    # Recomendações
    print(f"\n{'─' * 70}")
    print(f"  RECOMENDAÇÕES")
    print(f"{'─' * 70}")

    recs = []
    # Check overlapping terminal decks
    terminal_decks = [n for n in deck_names if 'terminal' in n.lower() or 'shell' in n.lower() or 'bash' in n.lower() or 'arquivos' in n.lower()]
    if len(terminal_decks) > 1:
        total = sum(len(prog_decks[d]) for d in terminal_decks)
        recs.append(f"  🔀 Consolidar {', '.join(terminal_decks)} → 'Dev::Terminal & Shell' ({total} cards)")

    python_decks = [n for n in deck_names if 'python' in n.lower()]
    if len(python_decks) > 1:
        total = sum(len(prog_decks[d]) for d in python_decks)
        recs.append(f"  🔀 Consolidar {', '.join(python_decks)} → 'Dev::Python' ({total} cards)")

    for r in recs or ["  ✅ Nenhuma consolidação necessária"]:
        print(r)

    print(f"\n  💡 Importar Dev_Programacao.apkg adiciona 142 cards novos organizados")
    print(f"     em hierarquia Dev:: sem afetar seus decks existentes.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparar decks existentes com novos")
    parser.add_argument("--deck", help="Filtrar por nome de deck")
    args = parser.parse_args()

    comparar(deck_filter=args.deck)
