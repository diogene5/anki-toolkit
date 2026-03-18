#!/usr/bin/env python3
"""
shared.py — Modulo compartilhado com funcoes e constantes reutilizadas pelos scripts Anki.

OBJETIVO:
    Centralizar codigo duplicado entre os scripts do projeto para evitar
    inconsistencias e facilitar manutencao. Antes, cada script definia
    sua propria copia de funcoes como unicase_collation(), conectar(),
    enriquecer_html(), CARD_CSS, etc.

FUNCOES E CONSTANTES EXPORTADAS:
    CARD_CSS           - CSS tema "Terminal Scholar" (Catppuccin Mocha) para cards
    create_model()     - Cria e retorna o genanki.Model padrao do projeto
    unicase_collation  - Collation case-insensitive exigida pelo SQLite do Anki
    get_anki_path      - Localiza o arquivo collection.anki2 de um perfil
    conectar           - Abre conexao SQLite com o banco do Anki
    enriquecer_html    - Formata texto plano do NotebookLM com tags HTML
    safe_name          - Gera nome de arquivo seguro a partir de titulo
    limpar_titulo      - Remove prefixos padronizados de titulos de notebooks

COMO USAR:
    from shared import CARD_CSS, create_model, conectar, enriquecer_html
"""

import os
import re
import sqlite3

# ─── CARD_CSS ─────────────────────────────────────────────────────────────────
# CSS aplicado a todos os cards gerados pelo projeto.
# Usa o esquema de cores Catppuccin Mocha — um dark theme de alto contraste
# que funciona bem tanto no desktop quanto no AnkiMobile.
#
# POR QUE UM CSS UNICO?
# O Anki vincula o CSS ao "note type" (modelo). Se cada script definir
# um CSS ligeiramente diferente, cards do mesmo modelo podem ficar
# visualmente inconsistentes. Centralizar aqui garante uniformidade.
#
# DETALHES DAS CLASSES:
#   .card   - container principal (fundo escuro, fonte sans-serif)
#   .front  - texto da pergunta (maior, bold)
#   .back   - texto da resposta (menor, cor mais suave)
#   code    - inline code (verde menta, fundo sutil)
#   pre     - blocos de codigo (fundo ainda mais escuro)
#   .source - atribuicao/fonte (pequeno, italico, discreto)
#
# A media query @media (max-width: 480px) ajusta padding e fonte para celular.

CARD_CSS = '''
.card { font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; font-size: 15px; line-height: 1.6; text-align: left; color: #bac2de; background-color: #181825; padding: 28px 24px; max-width: 65ch; margin: 0 auto; }
.front { font-size: 17px; font-weight: 600; line-height: 1.45; color: #cdd6f4; }
.back { font-size: 15px; line-height: 1.65; color: #a6adc8; }
.back b, .back strong { color: #cdd6f4; font-weight: 600; }
code { font-family: "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace; font-size: 0.88em; color: #94e2d5; background: rgba(49,50,68,0.7); padding: 2px 7px; border-radius: 4px; border: 1px solid rgba(69,71,90,0.5); }
pre { background: #11111b; padding: 16px 18px; border-radius: 8px; border: 1px solid rgba(49,50,68,0.8); overflow-x: auto; margin: 12px 0; }
pre code { padding: 0; background: none; border: none; color: #a6e3a1; font-size: 13px; line-height: 1.7; }
hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #45475a 15%, #585b70 50%, #45475a 85%, transparent 100%); margin: 20px 0; }
.source { font-size: 12px; color: #585b70; margin-top: 12px; font-style: italic; }
.nightMode .card { background-color: #181825; }
@media (max-width: 480px) { .card { padding: 22px 18px; } .front { font-size: 16px; } }
'''


def create_model():
    """
    Cria e retorna o modelo genanki padrao do projeto.

    POR QUE UMA FUNCAO E NAO UMA CONSTANTE?
    O genanki.Model e um objeto mutavel. Se fosse uma constante global
    compartilhada, multiplos scripts importando o mesmo objeto poderiam
    causar conflitos (ex: o genanki usa o objeto Model internamente para
    rastrear quais notas foram adicionadas). Criar uma instancia nova
    a cada chamada evita esse problema.

    O ID 1607392077 e fixo para que todos os scripts gerem cards do
    mesmo note type no Anki. Se cada script usasse um ID diferente,
    o Anki criaria modelos separados — e atualizar o CSS depois
    exigiria editar cada modelo individualmente.

    CAMPOS:
        Frente - pergunta / prompt
        Verso  - resposta / explicacao

    TEMPLATE:
        Card 1 - frente mostra {{Frente}}, verso mostra ambos com <hr>
    """
    import genanki
    return genanki.Model(
        1607392077, 'NotebookLM Import',
        fields=[{'name': 'Frente'}, {'name': 'Verso'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '<div class="front">{{Frente}}</div>',
            'afmt': '<div class="front">{{Frente}}</div><hr id="answer"><div class="back">{{Verso}}</div>',
        }],
        css=CARD_CSS,
    )


# ─── Funcoes para acesso ao banco SQLite do Anki ─────────────────────────────

def unicase_collation(a: str, b: str) -> int:
    """
    Collation case-insensitive compativel com o Anki.

    POR QUE ISSO E NECESSARIO?
    O Anki registra uma collation customizada chamada "unicase" no SQLite
    para ordenar texto ignorando maiusculas/minusculas. Quando abrimos o
    banco fora do Anki (via Python), o SQLite nao conhece essa collation
    e lanca erro em qualquer query com ORDER BY em colunas de texto.

    Registrar esta funcao com conn.create_collation("unicase", ...) resolve
    o problema. A implementacao e simples: compara as versoes .lower() das
    strings e retorna -1, 0 ou 1 (protocolo padrao de collation do SQLite).
    """
    a, b = a.lower(), b.lower()
    return (a > b) - (a < b)


def get_anki_path(perfil: str = "Data") -> str:
    """
    Retorna o caminho para o arquivo collection.anki2 de um perfil.

    COMO O ANKI ORGANIZA PERFIS NO MACOS:
    Cada perfil e um diretorio separado em:
        ~/Library/Application Support/Anki2/<nome_do_perfil>/

    Dentro de cada perfil, o banco principal e:
        collection.anki2  (arquivo SQLite)

    Se o perfil nao existir, a funcao lista os perfis disponiveis para
    ajudar o usuario a corrigir o nome. Perfis especiais como 'addons21'
    e 'logs' sao filtrados porque nao sao perfis de usuario.
    """
    base = os.path.expanduser("~/Library/Application Support/Anki2")
    db_path = os.path.join(base, perfil, "collection.anki2")
    if not os.path.exists(db_path):
        # Listar perfis disponiveis para ajudar o usuario
        perfis = [d for d in os.listdir(base)
                  if os.path.isdir(os.path.join(base, d))
                  and not d.startswith('.')
                  and d not in ('addons21', 'logs')]
        raise FileNotFoundError(
            f"Perfil '{perfil}' nao encontrado.\n"
            f"Perfis disponiveis: {', '.join(perfis)}\n"
            f"Caminho esperado: {db_path}"
        )
    return db_path


def conectar(perfil: str = "Data") -> sqlite3.Connection:
    """
    Abre conexao SQLite com o banco do Anki e registra a collation unicase.

    IMPORTANTE: O Anki bloqueia o banco enquanto esta aberto (WAL mode).
    Scripts que apenas LEEM dados geralmente funcionam com o Anki aberto,
    mas scripts que ESCREVEM devem ser executados com o Anki fechado.

    Esta funcao combina get_anki_path() + create_collation() em um unico
    passo conveniente, que e o padrao usado por todos os scripts de analise.
    """
    conn = sqlite3.connect(get_anki_path(perfil))
    conn.create_collation("unicase", unicase_collation)
    return conn


# ─── Funcoes para processamento de texto NotebookLM ──────────────────────────

def enriquecer_html(texto: str) -> str:
    """
    Converte texto plano do NotebookLM em HTML formatado para o Anki.

    POR QUE ISSO E NECESSARIO?
    O NotebookLM exporta flashcards como texto plano, sem formatacao.
    O Anki renderiza HTML nos campos das notas. Esta funcao faz a ponte,
    detectando padroes comuns e envolvendo-os com tags HTML apropriadas.

    PADROES DETECTADOS:
    1. Backticks (`codigo`) -> <code>codigo</code>
       Mesma convencao do Markdown para inline code.

    2. Comandos conhecidos sem backticks:
       - git add, git commit --amend, etc.
       - ssh-keygen
       - pip install pacote
       - python3 script.py
       - SELECT, CREATE, INSERT (SQL)
       Esses sao detectados por regex e envolvidos com <code>.

    3. Anti-double-wrap: se um comando ja estava entre backticks E
       foi capturado pelo regex, o resultado seria <code><code>...</code></code>.
       O replace final corrige isso.
    """
    # 1. Backticks do Markdown -> <code>
    texto = re.sub(r'`([^`]+)`', r'<code>\1</code>', texto)

    # 2. Comandos conhecidos sem backticks -> <code>
    cmd_patterns = [
        r'\b(git\s+\w+(?:\s+--?\w+)*)',   # git add, git commit --amend
        r'\b(ssh-keygen\b)',                # ssh-keygen
        r'\b(pip\s+install\s+\S+)',         # pip install genanki
        r'\b(python3?\s+\S+)',              # python3 script.py
        r'\b(SELECT\s+\w+)',               # SELECT coluna (SQL)
        r'\b(CREATE\s+\w+)',               # CREATE TABLE (SQL)
        r'\b(INSERT\s+\w+)',               # INSERT INTO (SQL)
    ]
    for p in cmd_patterns:
        texto = re.sub(p, r'<code>\1</code>', texto)

    # 3. Corrigir double-wrap (<code><code>x</code></code> -> <code>x</code>)
    texto = texto.replace('<code><code>', '<code>').replace('</code></code>', '</code>')

    return texto


def safe_name(title: str) -> str:
    """
    Gera um nome de arquivo seguro a partir de um titulo.

    Substitui qualquer caractere que nao seja alfanumerico, underscore ou
    hifen por underscore. Limita a 50 caracteres para evitar problemas com
    sistemas de arquivos. Remove underscores nas pontas.

    Usado para nomear arquivos .apkg e .json de saida, garantindo que
    titulos como "CS50 - Aula 3: Algoritmos & Busca" virem
    "CS50___Aula_3__Algoritmos___Busca" (seguro para qualquer OS).
    """
    return re.sub(r'[^\w-]', '_', title)[:50].strip('_')


def limpar_titulo(titulo: str) -> str:
    """
    Remove prefixos padronizados de titulos de notebooks NotebookLM.

    POR QUE ISSO E NECESSARIO?
    Os notebooks do NotebookLM frequentemente tem prefixos como:
      - [EM] Via Aerea Dificil        -> tags de categoria
      - P2P_ment_pro_6: Modelagem     -> codigos internos de cursos
      - DS-CLI_3: Grep e Find         -> numeracao sequencial
      - MBE_12: Diagnostico           -> codigo de modulo

    Esses prefixos sao uteis no NotebookLM mas poluem os nomes dos decks
    no Anki. Esta funcao os remove para gerar nomes limpos como:
      "Via Aerea Dificil", "Modelagem", "Grep e Find", "Diagnostico"

    PADROES REMOVIDOS:
      [qualquer coisa]  -> tags entre colchetes
      P2P_xxx_NN:       -> prefixo de cursos P2P
      DS-CLI_N:         -> prefixo de aulas DS-CLI (substituido por "DS-CLI: ")
      MBE_NN:           -> prefixo de modulos MBE (substituido por "MBE: ")
    """
    # Remove [tags]
    titulo = re.sub(r'\[.*?\]\s*', '', titulo)
    # Remove prefixos P2P_ment_xxx_NN:
    titulo = re.sub(r'P2P_\w+_\d+:\s*', '', titulo)
    # Remove DS-CLI N / DS_CLI_N (mantem "DS-CLI: " como contexto)
    titulo = re.sub(r'DS[-_]CLI[-_]?\d+:?\s*', 'DS-CLI: ', titulo)
    # Remove MBE_NN: (mantem "MBE: " como contexto)
    titulo = re.sub(r'MBE_\d+:\s*', 'MBE: ', titulo)
    return titulo.strip()
