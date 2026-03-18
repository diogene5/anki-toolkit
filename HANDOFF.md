---
title: "Handoff — Anki Toolkit"
date: 2026-03-18
purpose: "Contexto completo para continuar este projeto em qualquer sessão ou ferramenta"
---

# Handoff — Anki Toolkit

> Este documento contém TUDO que é necessário para continuar o projeto, mesmo sem contexto prévio.

## 1. O que é este projeto

Um toolkit Python para manipular decks do Anki programaticamente. Inclui:
- Scripts para analisar, limpar e gerar coleções Anki
- Integração com Google NotebookLM (converter flashcards em massa)
- Decks de estudo gerados com CSS customizado ("Terminal Scholar")
- Documentação completa (56 páginas da doc oficial do Anki + guias próprios)

**Dono:** Diogenes — não é programador de profissão, usa código como ferramenta para organização pessoal, automação e análise de dados. Usa macOS, Obsidian, VS Code. Fala português brasileiro.

## 2. Caminhos e Localização

### Projeto

```
Diretório:  /Users/diogenes/projetos/anki/
GitHub:     https://github.com/diogene5/anki-toolkit
Branch:     main (único)
```

### Anki (macOS)

```
Base:       ~/Library/Application Support/Anki2/
Perfil 1:   Data/         ← PERFIL PRINCIPAL (375+ cards, programação + medicina)
Perfil 2:   Principal/    ← Perfil secundário (medicina, Photoshop, EBM)
Add-ons:    addons21/
```

> ⚠️ SEMPRE verificar qual perfil está ativo antes de modificar. O nome aparece na barra de título ("Data - Anki").

### Banco de dados

```
DB:         ~/Library/Application Support/Anki2/<perfil>/collection.anki2  (SQLite)
Mídia:      ~/Library/Application Support/Anki2/<perfil>/collection.media/ (sem subpastas)
Backups:    ~/Library/Application Support/Anki2/<perfil>/backups/
```

## 3. Dependências e Ambiente

### Python

```bash
# Versão
python3 --version  # Python 3.13

# Pacotes instalados globalmente (sem venv)
pip3 install genanki         # gerar .apkg
pip3 install notebooklm-py   # integração NotebookLM

# Built-in (não precisa instalar)
# sqlite3, csv, json, re, pathlib, argparse, hashlib
```

### CLI Tools

```bash
# Git
git --version  # instalado

# GitHub CLI
gh auth status  # logado como diogene5

# NotebookLM CLI
notebooklm status  # autenticado, 210 notebooks
```

### Sem venv

O projeto NÃO usa ambiente virtual. Pacotes estão instalados globalmente via pip3. Se quiser criar um venv no futuro:

```bash
cd /Users/diogenes/projetos/anki
python3 -m venv .venv
source .venv/bin/activate
pip install genanki notebooklm-py
```

## 4. Estrutura do Projeto

```
anki/
├── scripts/                         # Ferramentas Python
│   ├── shared.py                    # ⭐ Módulo compartilhado (CSS, DB, utils)
│   ├── analisar_colecao.py          # Relatório completo da coleção
│   ├── limpar_colecao.py            # Remove note types/decks sem uso
│   ├── importar_csv.py              # Gera CSVs prontos para importação
│   ├── comparar_decks.py            # Qualidade + sobreposições entre decks
│   ├── notebooklm_to_anki.py        # Converter 1 notebook NLM flashcards → .apkg
│   ├── quiz_to_anki.py              # Converter NLM quizzes (múltipla escolha) → .apkg
│   ├── batch_nlm_download.py        # Baixar flashcards de N notebooks
│   └── batch_por_categoria.py       # Organizar flashcards por categoria temática
├── gerar_deck.py                    # Deck Dev_Programacao.apkg (142 cards)
├── gerar_deck_meta.py               # Deck Meta_Anki_Flashcards.apkg (34 cards)
├── preview_cards.html               # Preview visual dos cards no browser
├── docs/
│   ├── SUMMARY.md                   # Índice doc oficial Anki (56 páginas)
│   ├── aprendizados.md              # ⭐ Tudo que aprendemos consolidado
│   ├── guia-manipulacao-arquivos-anki.md
│   └── shared_module.md             # Doc do módulo compartilhado
├── output/                          # .apkg gerados
│   ├── NLM-Programação.apkg         # 38 decks, 2075 cards
│   ├── NLM-Medicina.apkg            # 29 decks, 1916 cards
│   ├── NLM-Data.apkg                # 14 decks, 663 cards
│   ├── NLM-Ferramentas.apkg         # 4 decks, 244 cards
│   ├── NLM-Gestão.apkg              # 1 deck, 143 cards
│   ├── NLM-Finanças.apkg            # 1 deck, 50 cards
│   └── NLM-Outros.apkg              # 4 decks, 258 cards
├── dados/                           # JSONs exportados (gitignored parcial)
│   ├── notebooks_com_flashcards.json # Lista dos 91 notebooks com flashcards
│   ├── batch_report.json            # Relatório do batch download
│   └── nlm_batch/                   # JSONs brutos do NotebookLM (gitignored)
├── backups/                         # Backups do banco Anki (gitignored)
├── Dev_Programacao.apkg             # Deck de programação pronto
├── Meta_Anki_Flashcards.apkg        # Deck meta (sobre o Anki)
├── .gitignore
├── README.md
└── HANDOFF.md                       # ← este arquivo
```

## 5. Como rodar cada script

```bash
cd /Users/diogenes/projetos/anki

# Analisar a coleção (Anki DEVE estar fechado)
python3 scripts/analisar_colecao.py --perfil Data --exportar

# Limpar note types e decks sem uso (faz backup automático)
python3 scripts/limpar_colecao.py --dry-run     # simular
python3 scripts/limpar_colecao.py --auto         # executar

# Análise de qualidade dos cards
python3 scripts/comparar_decks.py
python3 scripts/comparar_decks.py --deck "Git"   # focar em um deck

# Gerar CSVs de exemplo para importação manual
python3 scripts/importar_csv.py

# Gerar decks .apkg
python3 gerar_deck.py                            # Dev (142 cards)
python3 gerar_deck_meta.py                       # Meta (34 cards)

# Converter 1 notebook NotebookLM → Anki
python3 scripts/notebooklm_to_anki.py dados/nlm_flashcards.json --deck "NLM::Git"
python3 scripts/notebooklm_to_anki.py --download --notebook <id>

# Batch: converter todos os notebooks com flashcards
python3 scripts/batch_nlm_download.py            # baixar JSONs flashcards
python3 scripts/batch_por_categoria.py           # categorizar → NLM-*.apkg

# Quizzes (múltipla escolha com rationale)
python3 scripts/quiz_to_anki.py dados/quiz.json  # converter 1 quiz
python3 scripts/quiz_to_anki.py --scan           # baixar quizzes de todos os notebooks
python3 scripts/quiz_to_anki.py --categorize     # categorizar → Quiz-*.apkg

# Importar no Anki: File > Import > selecionar .apkg
```

## 6. Conceitos Técnicos Essenciais

### Banco SQLite do Anki

- Arquivo: `collection.anki2`
- Tabelas: `notes` (conteúdo), `cards` (scheduling), `decks`, `notetypes`, `revlog`
- Separador de campos: `\x1f` (ASCII 31)
- Card types: 0=new, 1=learning, 2=review, 3=relearning
- **SEMPRE registrar collation `unicase` antes de queries** (ver `shared.py`)
- **NUNCA modificar com Anki aberto** — causa corrupção

### genanki

- Biblioteca para criar .apkg sem Anki instalado
- `random.seed()` DEVE ser diferente por gerador para evitar GUID collisions
- Seeds em uso: 42 (gerar_deck), 77 (notebooklm_to_anki), 78 (batch_nlm_download), 79 (batch_por_categoria), 88 (quiz_to_anki), 99 (gerar_deck_meta)
- Model IDs devem ser fixos e únicos — nunca mudar depois de importar

### NotebookLM

- 210 notebooks na conta do Diogenes
- 91 já têm flashcards gerados
- CLI: `notebooklm` (pip install notebooklm-py)
- Auth: `notebooklm login` (OAuth via browser)
- Formato flashcards: `{"title": "...", "cards": [{"front": "...", "back": "..."}]}`

### CSS Theme

- Nome: "Terminal Scholar" (Catppuccin Mocha)
- Definido em `scripts/shared.py` → constante `CARD_CSS`
- Paleta: fundo #181825, texto #cdd6f4, código #94e2d5, green #a6e3a1
- max-width: 65ch, line-height 1.65 (dark mode), prefers-reduced-motion

## 7. O que já foi feito

| Tarefa | Status | Detalhes |
|--------|--------|----------|
| Doc oficial Anki → Markdown | ✅ | 56 páginas em docs/ |
| Guia manipulação arquivos | ✅ | docs/guia-manipulacao-arquivos-anki.md |
| Scripts análise/limpeza | ✅ | 7 scripts + shared.py |
| Deck Dev Programação | ✅ | 142 cards (Git, Python, Terminal, Data tríade, Ferramentas) |
| Deck Meta Anki | ✅ | 34 cards (sobre manipulação do Anki) |
| CSS Terminal Scholar v2 | ✅ | Dark mode, responsive, Catppuccin Mocha |
| Preview HTML dos cards | ✅ | preview_cards.html |
| Integração NotebookLM → Anki | ✅ | Pipeline completo + batch por categoria |
| Batch 91 notebooks | ✅ | 5361 cards em 7 categorias .apkg |
| Limpeza perfil Data | ✅ | 9 note types + 1 deck vazio removidos |
| Limpeza perfil Principal | ✅ | 9 note types + 8 decks vazios removidos |
| Code review + fixes | ✅ | 8 de 15 issues corrigidas |
| Refactor shared.py | ✅ | CSS, DB, utils centralizados |
| Skill Claude Code | ✅ | ~/.claude/skills/anki-toolkit/SKILL.md |
| Documento de aprendizados | ✅ | docs/aprendizados.md |

## 8. O que NÃO foi feito (próximos passos)

### Prioridade Alta

1. **Guia Git/GitHub passo a passo**
   - Tutorial prático + referência para uso pessoal
   - Foco: versionamento, organização, automação, dados
   - Formato: guia Markdown + exercício prático (criar repo real)
   - Brainstorming iniciado na sessão anterior, abordagem aprovada (opção C: guia + prática)

2. **Fixar 78 problemas de qualidade nos cards existentes**
   - `python3 scripts/comparar_decks.py` lista todos
   - Principais: código sem `<code>` tags (42), múltiplas perguntas (8), imagens coladas (3)
   - Pode ser feito com script que edita o SQLite direto

3. **Consolidar decks sobrepostos**
   - `terminal` + `arquivos terminal` + `Shell/Bash/Script` → `Dev::Terminal & Shell`
   - `Python` + `Python EDA template` → `Dev::Python`
   - Requer mover cards no SQLite (Anki fechado)

### Prioridade Média

4. **Converter quizzes do NotebookLM**
   - `notebooklm download quiz quiz.json` — formato diferente (múltipla escolha)
   - Converter para Anki com note type Cloze

5. **Tags limpas no perfil Data**
   - 50 tags inválidas (texto que vazou para campo de tags)
   - Script para limpar no SQLite

6. **Sync automático NotebookLM → Anki**
   - Cron job que baixa novos flashcards e importa

### Prioridade Baixa

7. **Sugestões pendentes do code review (issues 4, 6, 8, 9, 12, 13, 14)**
   - CSS ainda duplicado em gerar_deck.py e gerar_deck_meta.py (poderiam importar de shared.py)
   - .gitignore poderia excluir *.apkg binários (usar GitHub Releases)
   - notas_data_profile.json ainda tracked (git rm --cached)

## 9. Referências Externas

| Recurso | URL / Caminho |
|---------|---------------|
| GitHub repo | https://github.com/diogene5/anki-toolkit |
| Anki docs oficial | https://docs.ankiweb.net/ |
| genanki docs | https://github.com/kerrickstaley/genanki |
| notebooklm-py | https://github.com/teng-lin/notebooklm-py |
| Projeto Impeccable (CSS refs) | ~/projetos/impeccable/ |
| Catppuccin Mocha palette | https://catppuccin.com/palette |
| Skill Claude Code | ~/.claude/skills/anki-toolkit/SKILL.md |
| Memória Claude Code | ~/.claude/projects/-Users-diogenes-projetos-anki/memory/ |

## 10. Gotchas e Armadilhas

1. **O Anki tem 2 perfis** — "Data" é o principal, "Principal" é secundário. Sempre confirmar.
2. **Collation `unicase`** — toda query SQLite fora do Anki precisa registrá-la. Sem isso, ORDER BY em texto falha.
3. **`\x1f` separator** — campos no banco são separados por ASCII 31, não tab.
4. **`random.seed()` por gerador** — seeds devem ser únicas. Colisão = notas sobrescritas silenciosamente.
5. **`hash()` é não-determinístico** — use `hashlib.md5` para IDs estáveis entre sessões.
6. **Anki DEVE estar fechado** para scripts Python acessarem o banco. O `limpar_colecao.py` verifica, mas os outros não.
7. **NotebookLM rate limits** — geração de flashcards pode falhar. Esperar 5-10 min e tentar de novo.
8. **WAL mode** — se Anki fecha incorretamente, pode haver um `.anki2-wal` file. Copiar ambos para análise.
