#!/usr/bin/env python3
"""
📥 importar_csv.py — Gera arquivos CSV/TXT prontos para importar no Anki

POR QUE CSV E NÃO .APKG?
─────────────────────────
Existem duas formas de importar dados no Anki:

1. CSV/TXT (este script)
   ✅ Simples de gerar e editar
   ✅ Atualiza notas existentes pelo primeiro campo
   ✅ Fácil de versionar no Git (é texto puro)
   ❌ Não inclui mídia (imagens, áudio)
   ❌ Não inclui CSS/estilo do note type

2. .APKG (genanki, veja gerar_deck.py)
   ✅ Inclui tudo: notas, mídia, note types, CSS
   ✅ Cria decks automaticamente
   ❌ Mais complexo de gerar
   ❌ Difícil de comparar/versionar (é binário)

FORMATO DO CSV PARA ANKI (versão 2.1.54+):
─────────────────────────────────────────────
O Anki suporta "headers especiais" no topo do arquivo que configuram
a importação automaticamente:

  #separator:Tab          → separador de campos
  #html:true              → interpretar HTML nos campos
  #notetype:Basic         → qual note type usar
  #deck:MeuDeck           → em qual deck colocar
  #tags:tag1 tag2         → tags automáticas

Depois dos headers, cada linha é uma nota:
  campo1<TAB>campo2<TAB>campo3

REGRA DE ATUALIZAÇÃO:
O Anki identifica notas pelo PRIMEIRO CAMPO. Se importar um CSV
com o mesmo primeiro campo de uma nota existente, ele ATUALIZA
a nota (não duplica). Isso é poderoso para manutenção.

USO:
  python3 importar_csv.py                          # gera exemplos
  python3 importar_csv.py --arquivo dados.json     # converte JSON para CSV
"""

import csv
import json
import os
import argparse
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent / "output"


def gerar_csv_anki(
    notas: list[tuple[str, str]],
    deck: str,
    notetype: str = "Basic",
    tags: str = "",
    filename: str = "import.txt",
    html: bool = True,
) -> str:
    """
    Gera arquivo CSV no formato que o Anki espera.

    Args:
        notas: lista de tuplas (frente, verso)
        deck: nome do deck destino (ex: "Dev::Git")
        notetype: nome do note type (deve existir no Anki)
        tags: tags separadas por espaço
        filename: nome do arquivo de saída
        html: se True, campos podem conter HTML

    Returns:
        Caminho do arquivo gerado
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        # Headers especiais do Anki (linhas começando com #)
        f.write(f"#separator:Tab\n")
        f.write(f"#html:{'true' if html else 'false'}\n")
        f.write(f"#notetype:{notetype}\n")
        f.write(f"#deck:{deck}\n")
        if tags:
            f.write(f"#tags:{tags}\n")

        # Uma nota por linha, campos separados por tab
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for frente, verso in notas:
            writer.writerow([frente, verso])

    print(f"✅ Gerado: {filepath} ({len(notas)} notas)")
    return str(filepath)


def gerar_exemplos() -> None:
    """Gera CSVs de exemplo para demonstrar o formato."""
    print("📥 Gerando CSVs de exemplo para importação no Anki\n")

    # Exemplo 1: Cards simples
    gerar_csv_anki(
        notas=[
            ("O que é Git?", "Sistema de controle de versão distribuído que rastreia mudanças em arquivos"),
            ("O que é um commit?", "Snapshot (foto) do estado dos arquivos em um momento específico"),
            ("O que é uma branch?", "Linha independente de desenvolvimento — permite trabalhar sem afetar a principal"),
            ("O que é um merge?", "Operação que une as mudanças de uma branch em outra"),
            ("O que é um remote?", "Cópia do repositório em outro lugar (ex: GitHub). 'origin' é o remote padrão"),
        ],
        deck="Exemplos::Git Conceitos",
        tags="git conceitos",
        filename="exemplo_git_conceitos.txt",
    )

    # Exemplo 2: Cards com HTML
    gerar_csv_anki(
        notas=[
            (
                "Como criar um repositório Git?",
                "<code>git init</code><br><br>Cria a pasta <code>.git/</code> no diretório atual. "
                "A partir daí, o Git rastreia mudanças nessa pasta."
            ),
            (
                "Como verificar o status dos arquivos?",
                "<code>git status</code><br><br>Mostra:<br>"
                "• Arquivos modificados (vermelho)<br>"
                "• Arquivos no staging (verde)<br>"
                "• Branch atual"
            ),
        ],
        deck="Exemplos::Git Comandos",
        tags="git comandos",
        filename="exemplo_git_comandos.txt",
        html=True,
    )

    # Exemplo 3: Tríade (precisa de note type com 4 campos)
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / "exemplo_triade.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("#separator:Tab\n")
        f.write("#html:true\n")
        f.write(f"#notetype:Programação - Tríade (Planilha↔Python↔SQL)\n")
        f.write("#deck:Exemplos::Tríade\n")
        f.write("#tags:data triade\n")

        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            "Filtrar linhas por condição",
            "Dados > Filtro > selecionar valores",
            "<code>df[df['idade'] > 18]</code>",
            "<code>SELECT * FROM t WHERE idade > 18</code>",
        ])
        writer.writerow([
            "Ordenar dados",
            "Dados > Classificar",
            "<code>df.sort_values('col', ascending=False)</code>",
            "<code>SELECT * FROM t ORDER BY col DESC</code>",
        ])

    print(f"✅ Gerado: {filepath} (2 notas, formato tríade)")

    print(f"""
{'─' * 50}
Para importar no Anki:
  1. Abra o Anki
  2. File > Import
  3. Selecione o arquivo .txt
  4. O Anki lê os headers (#separator, #deck, etc.)
     e configura tudo automaticamente
  5. Clique em Import

⚠️  O note type deve existir no Anki antes de importar.
    Para a tríade, importe primeiro o Dev_Programacao.apkg
    (que cria o note type "Programação - Tríade").
""")


def converter_json_para_csv(json_path: str, deck: str = "Importado") -> None:
    """
    Converte um JSON exportado por analisar_colecao.py em CSVs por deck.

    Útil para re-importar notas editadas ou migrar entre perfis.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Agrupar notas por deck
    notas_by_deck: dict[str, list] = {}
    notas_list = data.get('notas', data)  # suporta ambos formatos
    if isinstance(notas_list, dict):
        notas_list = notas_list.get('notas', [])

    for nota in notas_list:
        deck_name = nota.get('deck', deck)
        if deck_name not in notas_by_deck:
            notas_by_deck[deck_name] = []
        campos = nota.get('campos', nota.get('fields', []))
        if len(campos) >= 2:
            notas_by_deck[deck_name].append((campos[0], campos[1]))

    for deck_name, notas in notas_by_deck.items():
        safe_name = deck_name.replace('::', '_').replace('/', '_').replace(' ', '_')
        gerar_csv_anki(
            notas=notas,
            deck=deck_name,
            filename=f"reimport_{safe_name}.txt",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerar CSV para importação no Anki")
    parser.add_argument("--arquivo", help="JSON para converter em CSV")
    parser.add_argument("--deck", default="Importado", help="Deck destino")
    args = parser.parse_args()

    if args.arquivo:
        converter_json_para_csv(args.arquivo, args.deck)
    else:
        gerar_exemplos()
