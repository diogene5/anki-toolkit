---
title: Anki Toolkit
date: 2026-03-18
---

# Anki Toolkit

Ferramentas para analisar, limpar e gerar decks Anki programaticamente.

## Estrutura

```
anki/
├── scripts/                    # Ferramentas Python
│   ├── analisar_colecao.py     # Relatório completo da coleção
│   ├── limpar_colecao.py       # Remove note types/decks sem uso
│   └── importar_csv.py         # Gera CSVs prontos para importação
├── gerar_deck.py               # Gerador de .apkg (deck compilado)
├── docs/                       # Documentação do Anki (56 páginas .md)
│   ├── SUMMARY.md              # Índice
│   └── guia-manipulacao-arquivos-anki.md
├── output/                     # CSVs gerados para importação
├── dados/                      # JSONs exportados (análise)
├── backups/                    # Backups automáticos (não versionados)
└── Dev_Programacao.apkg        # Deck de programação (142 cards)
```

## Uso Rápido

```bash
# Analisar coleção (Anki deve estar fechado)
python3 scripts/analisar_colecao.py --perfil Data --exportar

# Simular limpeza (ver o que seria removido)
python3 scripts/limpar_colecao.py --dry-run

# Limpar de verdade (faz backup automático)
python3 scripts/limpar_colecao.py --auto

# Gerar CSVs de exemplo para importação
python3 scripts/importar_csv.py

# Gerar deck .apkg de programação
python3 gerar_deck.py
```

## Como o Anki armazena dados

```mermaid
graph TD
    A[collection.anki2<br/>SQLite] --> B[notes<br/>conteúdo + tags]
    A --> C[cards<br/>scheduling + estado]
    A --> D[decks<br/>baralhos]
    A --> E[notetypes<br/>modelos de nota]
    A --> F[revlog<br/>histórico de revisões]
    B -->|1 nota gera| C
    B -->|pertence a| E

    G[collection.media/] --> H[Imagens, áudio, vídeo<br/>sem subpastas]

    style A fill:#313244,color:#cdd6f4
    style G fill:#313244,color:#cdd6f4
```

## Dependências

```bash
pip install genanki  # apenas para gerar .apkg
# sqlite3 e csv são built-in do Python
```
