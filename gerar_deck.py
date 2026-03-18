#!/usr/bin/env python3
"""
🎴 gerar_deck.py — Gerador de deck Anki (.apkg) de Programação

O QUE ESTE SCRIPT FAZ:
─────────────────────────
Cria um arquivo .apkg (deck empacotado) com 142+ cards organizados em
hierarquia de sub-decks, dois note types customizados com CSS dark mode,
e tags consistentes.

COMO O GENANKI FUNCIONA:
─────────────────────────
genanki é uma biblioteca Python para criar arquivos .apkg sem precisar
do Anki instalado. Ela monta a estrutura SQLite que o Anki espera:

  Model (note type)  →  define campos e templates HTML
  Deck               →  baralho onde as notas vivem
  Note               →  conteúdo (campos preenchidos)
  Package            →  empacota tudo em .apkg (ZIP com SQLite + mídia)

IDs NUMÉRICOS:
Todo Model e Deck precisa de um ID numérico ÚNICO e ESTÁVEL.
Se mudar o ID entre execuções, o Anki trata como objeto novo
(duplica em vez de atualizar). Use números fixos, não random().

HIERARQUIA DE DECKS:
O Anki usa "::" como separador de hierarquia.
  "Dev::Git & GitHub::Fundamentos"
  └── cria: Dev > Git & GitHub > Fundamentos (3 níveis)

USO:
  python3 gerar_deck.py
  # Resultado: Dev_Programacao.apkg (importar via File > Import no Anki)

DEPENDÊNCIAS:
  pip install genanki
"""
from pathlib import Path
import genanki
import random

# Seed fixa garante que genanki gere os mesmos GUIDs para as notas
# entre execuções. Sem isso, re-importar criaria duplicatas.
random.seed(42)

# ─── Note Types (Modelos de Nota) ─────────────────────────────
#
# Um "note type" (modelo) define:
#   1. CAMPOS (fields): os dados que você preenche (Frente, Verso, etc.)
#   2. TEMPLATES: o HTML que gera cada card a partir dos campos
#   3. CSS: estilo visual dos cards
#
# Uma nota com 4 campos pode gerar múltiplos cards se tiver
# múltiplos templates. Ex: o modelo Tríade abaixo gera 2 cards
# por nota (um pergunta Python, outro pergunta SQL).
#
# {{Campo}} no template é substituído pelo conteúdo do campo.
# {{FrontSide}} no template do verso inclui o HTML da frente.

BASIC_MODEL = genanki.Model(
    1607392001,  # ID fixo — NUNCA mude isso depois de importar
    'Programação - Basic',
    fields=[
        {'name': 'Frente'},
        {'name': 'Verso'},
    ],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="front">{{Frente}}</div>',
        'afmt': '<div class="front">{{Frente}}</div><hr id="answer"><div class="back">{{Verso}}</div>',
    }],
    # CSS v2 — "Terminal Scholar" theme (Catppuccin Mocha)
    # Otimizado para scan rápido durante sessões de estudo:
    # - Pergunta com peso visual alto (600 weight, cor mais clara)
    # - Código com borda sutil para destacar do texto
    # - Divider com gradiente (landmark visual Q→A)
    # - Callouts semi-transparentes (integrados, não bolted-on)
    css='''
    .card { font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; font-size: 15px; line-height: 1.55; text-align: left; color: #bac2de; background-color: #181825; padding: 28px 24px; max-width: 65ch; margin: 0 auto; }
    .front { font-size: 17px; font-weight: 600; line-height: 1.45; color: #cdd6f4; letter-spacing: -0.15px; }
    .back { font-size: 15px; line-height: 1.65; color: #a6adc8; }
    .back b, .back strong { color: #cdd6f4; font-weight: 600; }
    code { font-family: "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace; font-size: 0.88em; color: #94e2d5; background: rgba(49,50,68,0.7); padding: 2px 7px; border-radius: 4px; border: 1px solid rgba(69,71,90,0.5); }
    pre { background: #11111b; padding: 16px 18px; border-radius: 8px; border: 1px solid rgba(49,50,68,0.8); overflow-x: auto; margin: 12px 0; }
    pre code { padding: 0; background: none; border: none; color: #a6e3a1; font-size: 13px; line-height: 1.7; letter-spacing: 0.3px; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #45475a 15%, #585b70 50%, #45475a 85%, transparent 100%); margin: 20px 0; }
    .tip { background: rgba(166,227,161,0.06); border-left: 2px solid rgba(166,227,161,0.5); padding: 10px 14px; margin: 12px 0 4px; border-radius: 0 6px 6px 0; font-size: 13.5px; line-height: 1.55; color: #a6adc8; }
    .tip code { font-size: 0.9em; color: #a6e3a1; }
    .warn { background: rgba(249,226,175,0.06); border-left: 2px solid rgba(249,226,175,0.5); padding: 10px 14px; margin: 12px 0 4px; border-radius: 0 6px 6px 0; font-size: 13.5px; line-height: 1.55; color: #a6adc8; }
    .warn code { color: #f9e2af; }
    .nightMode .card { background-color: #181825; }
    @media (max-width: 480px) { .card { padding: 22px 18px; font-size: 14px; } .front { font-size: 16px; } pre { padding: 14px; } pre code { font-size: 12.5px; } }
    '''
)

TRIADE_MODEL = genanki.Model(
    1607392002,
    'Programação - Tríade (Planilha↔Python↔SQL)',
    fields=[
        {'name': 'Operação'},
        {'name': 'Planilha'},
        {'name': 'Python'},
        {'name': 'SQL'},
    ],
    templates=[
        {
            'name': 'Operação → Python',
            'qfmt': '<div class="front">🐍 Como fazer em <b>Python/pandas</b>:<br><br>{{Operação}}</div>',
            'afmt': '<div class="front">🐍 {{Operação}}</div><hr id="answer"><div class="back">{{Python}}<div class="tip">📊 Planilha: {{Planilha}}</div><div class="tip">🗄️ SQL: {{SQL}}</div></div>',
        },
        {
            'name': 'Operação → SQL',
            'qfmt': '<div class="front">🗄️ Como fazer em <b>SQL</b>:<br><br>{{Operação}}</div>',
            'afmt': '<div class="front">🗄️ {{Operação}}</div><hr id="answer"><div class="back">{{SQL}}<div class="tip">🐍 Python: {{Python}}</div><div class="tip">📊 Planilha: {{Planilha}}</div></div>',
        },
    ],
    css='''
    .card { font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; font-size: 15px; line-height: 1.55; text-align: left; color: #bac2de; background-color: #181825; padding: 28px 24px; max-width: 65ch; margin: 0 auto; }
    .front { font-size: 17px; font-weight: 600; line-height: 1.45; color: #cdd6f4; letter-spacing: -0.15px; }
    .back { font-size: 15px; line-height: 1.65; color: #a6adc8; }
    .back b, .back strong { color: #cdd6f4; font-weight: 600; }
    code { font-family: "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace; font-size: 0.88em; color: #94e2d5; background: rgba(49,50,68,0.7); padding: 2px 7px; border-radius: 4px; border: 1px solid rgba(69,71,90,0.5); }
    pre { background: #11111b; padding: 16px 18px; border-radius: 8px; border: 1px solid rgba(49,50,68,0.8); overflow-x: auto; margin: 12px 0; }
    pre code { padding: 0; background: none; border: none; color: #a6e3a1; font-size: 13px; line-height: 1.7; letter-spacing: 0.3px; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #45475a 15%, #585b70 50%, #45475a 85%, transparent 100%); margin: 20px 0; }
    .tip { background: rgba(166,227,161,0.06); border-left: 2px solid rgba(166,227,161,0.5); padding: 10px 14px; margin: 12px 0 4px; border-radius: 0 6px 6px 0; font-size: 13.5px; line-height: 1.55; color: #a6adc8; }
    .tip code { font-size: 0.9em; color: #a6e3a1; }
    .nightMode .card { background-color: #181825; }
    @media (max-width: 480px) { .card { padding: 22px 18px; font-size: 14px; } .front { font-size: 16px; } pre { padding: 14px; } pre code { font-size: 12.5px; } }
    '''
)


# ─── Decks ─────────────────────────────────────────────────────

decks = {
    'root':       genanki.Deck(2001000000, 'Dev'),
    'terminal':   genanki.Deck(2001000001, 'Dev::Terminal & Shell'),
    'nav':        genanki.Deck(2001000002, 'Dev::Terminal & Shell::Navegação'),
    'arquivos':   genanki.Deck(2001000003, 'Dev::Terminal & Shell::Arquivos & Permissões'),
    'redir':      genanki.Deck(2001000004, 'Dev::Terminal & Shell::Redirecionamento & Pipes'),
    'scripts':    genanki.Deck(2001000005, 'Dev::Terminal & Shell::Scripts Bash'),
    'git':        genanki.Deck(2001000010, 'Dev::Git & GitHub'),
    'git_fund':   genanki.Deck(2001000011, 'Dev::Git & GitHub::Fundamentos'),
    'git_branch': genanki.Deck(2001000012, 'Dev::Git & GitHub::Branches & Merge'),
    'git_colab':  genanki.Deck(2001000013, 'Dev::Git & GitHub::Colaboração'),
    'git_fix':    genanki.Deck(2001000014, 'Dev::Git & GitHub::Troubleshooting'),
    'python':     genanki.Deck(2001000020, 'Dev::Python'),
    'py_fund':    genanki.Deck(2001000021, 'Dev::Python::Fundamentos'),
    'py_pandas':  genanki.Deck(2001000022, 'Dev::Python::Pandas'),
    'py_eda':     genanki.Deck(2001000023, 'Dev::Python::EDA & Visualização'),
    'data':       genanki.Deck(2001000030, 'Dev::Data (Planilha↔Python↔SQL)'),
    'tools':      genanki.Deck(2001000040, 'Dev::Ferramentas'),
    'md':         genanki.Deck(2001000041, 'Dev::Ferramentas::Markdown & Obsidian'),
    'regex':      genanki.Deck(2001000042, 'Dev::Ferramentas::Regex'),
    'vscode':     genanki.Deck(2001000043, 'Dev::Ferramentas::VS Code'),
}

def card(front, back, tags=None):
    return genanki.Note(model=BASIC_MODEL, fields=[front, back], tags=tags or [])

def triade(op, planilha, python, sql, tags=None):
    return genanki.Note(model=TRIADE_MODEL, fields=[op, planilha, python, sql], tags=tags or [])

# ═══════════════════════════════════════════════════════════════
# TERMINAL & SHELL
# ═══════════════════════════════════════════════════════════════

# Navegação
nav_cards = [
    ("Qual comando mostra o diretório atual?", "<code>pwd</code> — print working directory", ["terminal", "navegação"]),
    ("Como voltar ao diretório home?", "<code>cd</code> ou <code>cd ~</code>", ["terminal", "navegação"]),
    ("O que significam <code>.</code> e <code>..</code>?", "<code>.</code> = diretório atual<br><code>..</code> = diretório pai<br><br>Ex: <code>cd ../projeto</code> sobe um nível e entra em 'projeto'", ["terminal", "navegação"]),
    ("Qual a diferença entre caminho absoluto e relativo?", "<b>Absoluto</b>: começa com <code>/</code> — caminho completo desde a raiz<br><code>/Users/diogenes/projetos</code><br><br><b>Relativo</b>: parte do diretório atual<br><code>./projetos</code> ou <code>../outro</code>", ["terminal", "navegação"]),
    ("O que faz <code>cd -</code>?", "Volta para o diretório anterior (toggle entre dois diretórios)", ["terminal", "navegação"]),
    ("Como criar um diretório com subdiretórios de uma vez?", "<code>mkdir -p projeto/src/utils</code><br><br>O <code>-p</code> cria todos os diretórios intermediários", ["terminal", "navegação"]),
    ("Como listar arquivos incluindo ocultos?", "<code>ls -la</code><br><br><code>-l</code> = formato longo (permissões, tamanho)<br><code>-a</code> = inclui ocultos (começam com .)", ["terminal", "navegação"]),
    ("Como listar apenas diretórios?", "<code>ls -d */</code><br><br>Ou com detalhes: <code>ls -la | grep ^d</code>", ["terminal", "navegação"]),
]

# Arquivos & Permissões
arq_cards = [
    ("Como copiar um arquivo?", "<code>cp origem.txt destino.txt</code><br><br>Para copiar diretório inteiro: <code>cp -r pasta/ backup/</code>", ["terminal", "arquivos"]),
    ("Como mover/renomear um arquivo?", "<code>mv arquivo.txt novo_nome.txt</code> (renomear)<br><code>mv arquivo.txt ~/Documents/</code> (mover)<br><br>Mesmo comando para ambos!", ["terminal", "arquivos"]),
    ("Como remover arquivo? E diretório com conteúdo?", "<code>rm arquivo.txt</code> — remove arquivo<br><code>rm -r pasta/</code> — remove diretório recursivamente<br><br><div class='warn'>⚠️ rm é irreversível! Não vai para lixeira.</div>", ["terminal", "arquivos"]),
    ("O que significam as permissões <code>rwxr-xr--</code>?", "<code>rwx</code> = dono (ler, escrever, executar)<br><code>r-x</code> = grupo (ler, executar)<br><code>r--</code> = outros (só ler)<br><br>Numérico: 7-5-4 → <code>chmod 754</code>", ["terminal", "arquivos"]),
    ("Como tornar um arquivo executável?", "<code>chmod +x script.sh</code><br><br>Ou numérico: <code>chmod 755 script.sh</code>", ["terminal", "arquivos"]),
    ("Como criar um arquivo vazio?", "<code>touch arquivo.txt</code><br><br>Se o arquivo já existe, apenas atualiza a data de modificação", ["terminal", "arquivos"]),
    ("Como ver o conteúdo de um arquivo no terminal?", "<code>cat arquivo.txt</code> — mostra tudo<br><code>head -20 arquivo.txt</code> — primeiras 20 linhas<br><code>tail -20 arquivo.txt</code> — últimas 20 linhas<br><code>less arquivo.txt</code> — navegável (q para sair)", ["terminal", "arquivos"]),
    ("Como acompanhar um log em tempo real?", "<code>tail -f /var/log/system.log</code><br><br>O <code>-f</code> (follow) mostra novas linhas conforme são escritas. Ctrl+C para sair.", ["terminal", "arquivos"]),
    ("Qual a diferença entre hard link e soft link (symlink)?", "<b>Soft link</b> (symlink): atalho que aponta para o caminho<br><code>ln -s alvo.txt link.txt</code><br>Quebra se o original for movido<br><br><b>Hard link</b>: segunda referência ao mesmo dado no disco<br><code>ln alvo.txt link.txt</code><br>Funciona mesmo se original for deletado", ["terminal", "arquivos"]),
    ("Como encontrar arquivos por nome?", "<code>find . -name '*.py'</code> — busca recursiva por nome<br><code>find ~/projetos -name '*.md' -mtime -7</code> — modificados nos últimos 7 dias", ["terminal", "arquivos"]),
    ("Como comprimir e descomprimir arquivos?", "<b>ZIP:</b><br><code>zip -r arquivo.zip pasta/</code><br><code>unzip arquivo.zip</code><br><br><b>TAR.GZ:</b><br><code>tar czf arquivo.tar.gz pasta/</code><br><code>tar xzf arquivo.tar.gz</code><br><br>Lembre: <b>c</b>reate, e<b>x</b>tract, <b>z</b>=gzip, <b>f</b>=file", ["terminal", "arquivos"]),
    ("Como ver o tipo real de um arquivo?", "<code>file documento.pdf</code><br><br>Mostra o tipo real baseado no conteúdo, não na extensão", ["terminal", "arquivos"]),
    ("Como verificar integridade de um arquivo com hash?", "<code>shasum -a 256 arquivo.iso</code><br>ou<br><code>md5 arquivo.iso</code> (macOS)<br><br>Compare o hash com o fornecido pelo site de download", ["terminal", "arquivos"]),
    ("Como comparar dois arquivos?", "<code>diff arquivo1.txt arquivo2.txt</code><br><br>Para formato colorido lado a lado:<br><code>diff --color -y file1 file2</code>", ["terminal", "arquivos"]),
    ("Como mudar o proprietário de um arquivo?", "<code>sudo chown usuario:grupo arquivo</code><br><br>Recursivo: <code>sudo chown -R usuario:grupo pasta/</code>", ["terminal", "arquivos"]),
]

# Redirecionamento & Pipes
redir_cards = [
    ("O que faz o <code>></code> no terminal?", "Redireciona saída para um arquivo, <b>sobrescrevendo</b><br><code>echo 'hello' > arquivo.txt</code><br><br>Para <b>adicionar</b> (append): <code>>></code><br><code>echo 'more' >> arquivo.txt</code>", ["terminal", "pipes"]),
    ("Para que serve o pipe <code>|</code>?", "Conecta a <b>saída</b> de um comando à <b>entrada</b> do próximo<br><br><code>ls -la | grep '.py' | wc -l</code><br>↳ lista arquivos → filtra .py → conta linhas", ["terminal", "pipes"]),
    ("Como buscar texto dentro de arquivos?", "<code>grep 'texto' arquivo.txt</code> — busca simples<br><code>grep -r 'TODO' ./src/</code> — busca recursiva<br><code>grep -i 'erro' log.txt</code> — case-insensitive<br><code>grep -n 'def ' *.py</code> — mostra número da linha", ["terminal", "pipes"]),
    ("Como salvar a lista de arquivos em um txt?", "<code>ls -la > lista.txt</code><br><br>Só nomes: <code>ls > lista.txt</code><br>Recursivo: <code>find . -name '*.md' > lista.txt</code>", ["terminal", "pipes"]),
    ("O que faz <code>cat > arquivo.txt << 'EOF'</code>?", "Cria um arquivo com conteúdo multi-linha (heredoc):<br><pre><code>cat > config.txt << 'EOF'\nhost=localhost\nport=3000\nEOF</code></pre>O shell escreve tudo entre os dois EOF no arquivo", ["terminal", "pipes"]),
    ("Como contar linhas, palavras e caracteres?", "<code>wc arquivo.txt</code> → linhas, palavras, bytes<br><code>wc -l arquivo.txt</code> → só linhas<br><br>Com pipe: <code>cat log.txt | grep ERROR | wc -l</code>", ["terminal", "pipes"]),
    ("Qual comando mostra o caminho completo de um programa?", "<code>which python3</code> → <code>/usr/bin/python3</code><br><br>Mostra qual executável o shell encontra no PATH", ["terminal", "pipes"]),
    ("Como executar o último comando novamente?", "<code>!!</code> — repete o último comando<br><code>sudo !!</code> — repete com sudo (muito útil!)<br><code>!grep</code> — repete o último grep", ["terminal", "pipes"]),
    ("Como interromper um processo no terminal?", "<code>Ctrl+C</code> — interrompe o processo atual<br><code>Ctrl+Z</code> — suspende (bg/fg para retomar)<br><code>Ctrl+D</code> — envia EOF (sai de shells interativos)", ["terminal", "pipes"]),
    ("Como executar múltiplos comandos em sequência?", "<code>cmd1 && cmd2</code> — executa cmd2 só se cmd1 der certo<br><code>cmd1 || cmd2</code> — executa cmd2 só se cmd1 falhar<br><code>cmd1 ; cmd2</code> — executa ambos independente do resultado", ["terminal", "pipes"]),
]

# Scripts Bash
script_cards = [
    ("O que é o shebang e para que serve?", "<code>#!/bin/bash</code> ou <code>#!/usr/bin/env bash</code><br><br>Primeira linha do script — diz ao sistema qual interpretador usar.<br><code>env bash</code> é mais portável (busca no PATH)", ["bash", "script"]),
    ("Como definir e usar uma variável em bash?", "<pre><code>nome=\"mundo\"\necho \"Olá, $nome\"</code></pre><b>Sem espaços</b> ao redor do <code>=</code>!<br><code>${nome}</code> quando concatenar: <code>${nome}_backup</code>", ["bash", "script"]),
    ("O que são <code>$1</code>, <code>$2</code>, <code>$@</code> em bash?", "Parâmetros posicionais (argumentos do script/função):<br><code>$1</code> = primeiro argumento<br><code>$2</code> = segundo argumento<br><code>$@</code> = todos os argumentos<br><code>$#</code> = quantidade de argumentos<br><br><code>./script.sh arg1 arg2</code>", ["bash", "script"]),
    ("Como ler input do usuário num script?", "<pre><code>read -p \"Seu nome: \" nome\necho \"Olá, $nome\"</code></pre>", ["bash", "script"]),
    ("Como criar uma função em bash?", "<pre><code>backup() {\n  local origem=$1\n  local destino=$2\n  cp -r \"$origem\" \"$destino\"\n  echo \"Backup de $origem feito!\"\n}\n\nbackup ~/docs ~/backup/</code></pre>", ["bash", "script"]),
    ("O que é a variável <code>$PATH</code>?", "Lista de diretórios onde o shell procura executáveis, separados por <code>:</code><br><br><code>echo $PATH</code><br><code>/usr/local/bin:/usr/bin:/bin</code><br><br>Quando você digita <code>python3</code>, o shell busca em cada diretório da lista", ["bash", "script"]),
    ("Como fazer um script funcionar de qualquer lugar?", "Duas opções:<br><br><b>1.</b> Mover para diretório no PATH:<br><code>mv script.sh /usr/local/bin/</code><br><br><b>2.</b> Adicionar seu diretório ao PATH (no ~/.zshrc):<br><code>export PATH=\"$HOME/scripts:$PATH\"</code>", ["bash", "script"]),
    ("Qual a diferença entre executar <code>./script.sh</code> e <code>source script.sh</code>?", "<code>./script.sh</code> — roda em <b>subshell</b> (processo filho). Variáveis definidas lá NÃO afetam o shell atual.<br><br><code>source script.sh</code> — roda no <b>shell atual</b>. Variáveis e mudanças de diretório persistem.<br><br>Por isso usamos <code>source ~/.zshrc</code> para recarregar configuração", ["bash", "script"]),
    ("Como usar if/else em bash?", "<pre><code>if [ -f \"arquivo.txt\" ]; then\n  echo \"Existe\"\nelif [ -d \"pasta\" ]; then\n  echo \"É diretório\"\nelse\n  echo \"Não encontrado\"\nfi</code></pre>Testes comuns: <code>-f</code> arquivo existe, <code>-d</code> diretório, <code>-z</code> string vazia, <code>-eq</code> igual numérico", ["bash", "script"]),
    ("Como fazer loop em bash?", "<pre><code># Loop em lista\nfor f in *.py; do\n  echo \"Processando $f\"\ndone\n\n# Loop numérico\nfor i in {1..5}; do\n  echo \"Item $i\"\ndone\n\n# While\nwhile read linha; do\n  echo \"$linha\"\ndone < arquivo.txt</code></pre>", ["bash", "script"]),
    ("Scripts bash funcionam no zsh (padrão do macOS)?", "Na maioria sim, mas há diferenças:<br><br>• Arrays: bash começa em 0, zsh em 1<br>• Glob: zsh é mais restrito por padrão<br>• Use <code>#!/bin/bash</code> no shebang se precisar de compatibilidade bash", ["bash", "script"]),
]

# ═══════════════════════════════════════════════════════════════
# GIT & GITHUB
# ═══════════════════════════════════════════════════════════════

git_fund_cards = [
    ("Qual comando inicia um repositório Git?", "<code>git init</code><br><br>Cria a pasta <code>.git/</code> que armazena todo o histórico. Um diretório sem .git não é um repo.", ["git", "fundamentos"]),
    ("Qual o fluxo básico do Git (3 áreas)?", "<pre><code>Working Dir → Staging → Repository\n   (edit)    (git add)  (git commit)</code></pre>1. Edita arquivos<br>2. <code>git add</code> → staging area<br>3. <code>git commit</code> → salva snapshot permanente", ["git", "fundamentos"]),
    ("Como adicionar arquivos para commit?", "<code>git add arquivo.py</code> — arquivo específico<br><code>git add .</code> — tudo no diretório atual<br><code>git add -p</code> — interativo (escolhe pedaços)<br><br><div class='warn'>⚠️ Evite <code>git add .</code> cegamente — revise com <code>git status</code> antes</div>", ["git", "fundamentos"]),
    ("Como fazer um commit com mensagem?", "<code>git commit -m \"feat: adiciona login com OAuth\"</code><br><br>Boas mensagens: verbo imperativo + o que faz + por quê<br><br>Padrão Conventional Commits:<br><code>feat:</code> <code>fix:</code> <code>docs:</code> <code>refactor:</code> <code>test:</code>", ["git", "fundamentos"]),
    ("Como ver o status e o histórico?", "<code>git status</code> — o que mudou? o que está staged?<br><code>git log --oneline</code> — histórico resumido<br><code>git log --graph --oneline</code> — com visual de branches<br><code>git diff</code> — mudanças não staged", ["git", "fundamentos"]),
    ("O que é o <code>.gitignore</code>?", "Arquivo que define o que o Git deve ignorar:<br><pre><code># .gitignore\nnode_modules/\n.env\n*.pyc\n__pycache__/\n.DS_Store\n*.log</code></pre>Crie antes do primeiro commit!", ["git", "fundamentos"]),
    ("Como clonar um repositório?", "<code>git clone https://github.com/user/repo.git</code><br><br>SSH (recomendado):<br><code>git clone git@github.com:user/repo.git</code><br><br>Já configura o remote 'origin' automaticamente", ["git", "fundamentos"]),
    ("Diferença entre <code>git pull</code> e <code>git fetch</code>?", "<code>git fetch</code> — baixa mudanças remotas mas <b>não aplica</b><br><code>git pull</code> — fetch + merge (aplica as mudanças)<br><br><div class='tip'>💡 <code>git pull --rebase</code> é mais limpo: reaplica seus commits em cima das mudanças remotas</div>", ["git", "fundamentos"]),
    ("Como ver quem modificou cada linha?", "<code>git blame arquivo.py</code><br><br>Mostra autor, data e commit de cada linha. Útil para entender o contexto de uma mudança.", ["git", "fundamentos"]),
    ("Como ver o histórico de um arquivo específico?", "<code>git log -- arquivo.py</code><br><code>git log -p -- arquivo.py</code> — com diff de cada commit<br><br>Para ver diferenças entre versões:<br><code>git diff HEAD~3 -- arquivo.py</code>", ["git", "fundamentos"]),
]

git_branch_cards = [
    ("Como criar e trocar de branch?", "<code>git branch feature</code> — cria branch<br><code>git checkout feature</code> — troca para ela<br><br>Atalho (cria + troca):<br><code>git checkout -b feature</code><br>ou moderno:<br><code>git switch -c feature</code>", ["git", "branch"]),
    ("Qual a diferença entre merge e rebase?", "<b>Merge</b>: cria um commit de merge unindo as duas linhas<br><code>git merge feature</code><br>✅ Preserva histórico real<br><br><b>Rebase</b>: reaplica commits em cima de outra branch<br><code>git rebase main</code><br>✅ Histórico linear e limpo<br><br><div class='warn'>⚠️ Nunca faça rebase de commits já publicados (pushed)</div>", ["git", "branch"]),
    ("Como resolver conflitos de merge?", "1. Git marca conflitos no arquivo:<pre><code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD\nseu código\n=======\ncódigo do outro\n&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature</code></pre>2. Edite o arquivo mantendo o que quiser<br>3. <code>git add arquivo.py</code><br>4. <code>git commit</code> (finaliza o merge)", ["git", "branch"]),
    ("O que é <code>git stash</code>?", "Salva mudanças temporariamente sem commit:<br><pre><code>git stash          # guarda\ngit stash list      # lista stashes\ngit stash pop       # restaura e remove\ngit stash apply     # restaura sem remover</code></pre>Útil quando precisa trocar de branch sem commitar trabalho incompleto", ["git", "branch"]),
    ("Como deletar uma branch?", "<code>git branch -d feature</code> — deleta local (safe: só se já foi merged)<br><code>git branch -D feature</code> — deleta forçado<br><code>git push origin --delete feature</code> — deleta no remoto", ["git", "branch"]),
    ("O que faz <code>git cherry-pick</code>?", "Aplica um commit específico na branch atual:<br><code>git cherry-pick abc1234</code><br><br>Útil para trazer um fix específico sem fazer merge da branch inteira", ["git", "branch"]),
    ("Como listar todas as branches?", "<code>git branch</code> — branches locais<br><code>git branch -a</code> — inclui remotas<br><code>git branch -v</code> — com último commit de cada", ["git", "branch"]),
]

git_colab_cards = [
    ("Como adicionar um remote e fazer push?", "<code>git remote add origin git@github.com:user/repo.git</code><br><code>git push -u origin main</code><br><br><code>-u</code> vincula a branch local com a remota (só precisa na primeira vez)", ["git", "github"]),
    ("Qual o fluxo para contribuir via Pull Request?", "1. Fork o repo no GitHub<br>2. <code>git clone</code> seu fork<br>3. <code>git checkout -b minha-feature</code><br>4. Faz commits<br>5. <code>git push origin minha-feature</code><br>6. Abre PR no GitHub (base: repo original)", ["git", "github"]),
    ("Como manter seu fork atualizado?", "<pre><code>git remote add upstream URL_ORIGINAL\ngit fetch upstream\ngit checkout main\ngit merge upstream/main\ngit push origin main</code></pre>", ["git", "github"]),
    ("O que é um <code>git tag</code> e para que serve?", "Marca um ponto específico no histórico (geralmente releases):<br><pre><code>git tag v1.0.0           # tag leve\ngit tag -a v1.0.0 -m \"Release 1.0\"  # annotated\ngit push origin v1.0.0   # enviar tag</code></pre>", ["git", "github"]),
    ("Como configurar SSH para GitHub?", "<pre><code># Gerar chave\nssh-keygen -t ed25519 -C \"email@example.com\"\n\n# Copiar chave pública\ncat ~/.ssh/id_ed25519.pub | pbcopy\n\n# Colar em GitHub > Settings > SSH Keys\n\n# Testar\nssh -T git@github.com</code></pre>", ["git", "github"]),
    ("O que são GitHub Actions?", "CI/CD integrado ao GitHub. Arquivo YAML em <code>.github/workflows/</code> que roda automaticamente:<br><pre><code>on: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: npm test</code></pre>Roda testes, deploy, linting automaticamente", ["git", "github"]),
]

git_fix_cards = [
    ("Como desfazer o último commit (mantendo as mudanças)?", "<code>git reset --soft HEAD~1</code> — volta um commit, mantém staging<br><code>git reset HEAD~1</code> — volta um commit, mantém no working dir<br><br><div class='warn'>⚠️ <code>git reset --hard HEAD~1</code> APAGA tudo. Cuidado!</div>", ["git", "troubleshooting"]),
    ("Diferença entre <code>git reset</code> e <code>git revert</code>?", "<b>reset</b>: apaga commits do histórico (reescreve)<br>→ Use em commits <b>locais</b> não publicados<br><br><b>revert</b>: cria um NOVO commit que desfaz o anterior<br><code>git revert abc1234</code><br>→ Use em commits <b>já publicados</b> (safe)", ["git", "troubleshooting"]),
    ("O que é detached HEAD e como sair?", "Acontece quando você faz checkout de um commit (não branch):<br><code>git checkout abc1234</code><br><br>Para sair:<br><code>git checkout main</code><br><br>Se fez mudanças que quer manter:<br><code>git checkout -b nova-branch</code>", ["git", "troubleshooting"]),
    ("Como desfazer mudanças em um arquivo (não committed)?", "<code>git checkout -- arquivo.py</code> — descarta mudanças<br>ou moderno:<br><code>git restore arquivo.py</code><br><br>Para tirar do staging:<br><code>git restore --staged arquivo.py</code>", ["git", "troubleshooting"]),
    ("Como recuperar commits \"perdidos\"?", "<code>git reflog</code> — mostra TUDO que aconteceu nos últimos 90 dias<br><br>Encontre o hash do commit perdido e:<br><code>git checkout abc1234</code><br><code>git checkout -b recuperado</code><br><br><div class='tip'>💡 reflog é seu seguro de vida no Git</div>", ["git", "troubleshooting"]),
    ("Como corrigir a mensagem do último commit?", "<code>git commit --amend -m \"mensagem corrigida\"</code><br><br><div class='warn'>⚠️ Só use se o commit NÃO foi pushed. Amend reescreve o histórico.</div>", ["git", "troubleshooting"]),
]

# ═══════════════════════════════════════════════════════════════
# PYTHON
# ═══════════════════════════════════════════════════════════════

py_fund_cards = [
    ("Qual a diferença entre método (parênteses) e atributo (sem parênteses)?", "<b>Método</b> = ação, precisa de <code>()</code>:<br><code>lista.append(5)</code>, <code>texto.upper()</code><br><br><b>Atributo</b> = propriedade, sem <code>()</code>:<br><code>df.shape</code>, <code>df.columns</code><br><br>Regra: parênteses = \"faça algo\"; sem = \"me diga algo\"", ["python", "fundamentos"]),
    ("O que <code>type()</code> retorna?", "O tipo do objeto:<br><code>type(42)</code> → <code>&lt;class 'int'&gt;</code><br><code>type('hello')</code> → <code>&lt;class 'str'&gt;</code><br><code>type([1,2])</code> → <code>&lt;class 'list'&gt;</code><br><br><div class='tip'>💡 <code>type('05123')</code> → str (não int!). Aspas = sempre string</div>", ["python", "fundamentos"]),
    ("Como arredondar um número em Python?", "<code>round(3.14159, 2)</code> → <code>3.14</code><br><code>round(3.5)</code> → <code>4</code><br><br>Para sempre arredondar para cima:<br><code>import math; math.ceil(3.1)</code> → <code>4</code><br>Para baixo: <code>math.floor(3.9)</code> → <code>3</code>", ["python", "fundamentos"]),
    ("Como formatar strings em Python (f-strings)?", "<pre><code>nome = \"Ana\"\nidade = 25\nprint(f\"Nome: {nome}, idade: {idade}\")\nprint(f\"Preço: R${49.9:.2f}\")  # R$49.90\nprint(f\"{1000000:,.0f}\")  # 1,000,000</code></pre>", ["python", "fundamentos"]),
    ("Como lidar com erros em Python (try/except)?", "<pre><code>try:\n    resultado = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Divisão por zero!\")\nexcept Exception as e:\n    print(f\"Erro: {e}\")\nfinally:\n    print(\"Sempre executa\")</code></pre>", ["python", "fundamentos"]),
    ("Como ler e escrever arquivos em Python?", "<pre><code># Ler\nwith open('dados.txt', 'r') as f:\n    conteudo = f.read()\n\n# Escrever\nwith open('saida.txt', 'w') as f:\n    f.write('Hello\\n')\n\n# Append\nwith open('log.txt', 'a') as f:\n    f.write('nova linha\\n')</code></pre><code>with</code> garante que o arquivo é fechado corretamente", ["python", "fundamentos"]),
    ("Como criar e usar list comprehension?", "<pre><code># Simples\nquadrados = [x**2 for x in range(10)]\n\n# Com filtro\npares = [x for x in range(20) if x % 2 == 0]\n\n# Com transformação\nnomes = [n.upper() for n in lista if len(n) > 3]</code></pre>Mais legível e rápido que loop + append", ["python", "fundamentos"]),
    ("Como instalar e gerenciar pacotes Python?", "<code>pip install pandas</code> — instala pacote<br><code>pip install -r requirements.txt</code> — instala dependências<br><code>pip freeze > requirements.txt</code> — salva dependências<br><br><div class='tip'>💡 Use <code>python3 -m venv .venv</code> para ambiente virtual isolado</div>", ["python", "fundamentos"]),
]

py_pandas_cards = [
    ("O que é um DataFrame?", "Tabela 2D do pandas (linhas × colunas):<br><pre><code>import pandas as pd\ndf = pd.read_csv('dados.csv')\ndf.head()     # primeiras 5 linhas\ndf.shape      # (linhas, colunas)\ndf.info()     # tipos e nulos\ndf.describe() # estatísticas</code></pre>", ["python", "pandas"]),
    ("Como selecionar colunas e linhas?", "<pre><code># Coluna\ndf['nome']           # Series\ndf[['nome','idade']] # DataFrame\n\n# Linhas por condição\ndf[df['idade'] > 18]\ndf.query('idade > 18')  # alternativa legível\n\n# Por posição\ndf.iloc[0:5]     # por índice\ndf.loc[0:5, 'nome':'idade']  # por label</code></pre>", ["python", "pandas"]),
    ("Como remover colunas e linhas?", "<pre><code># Colunas\ndf = df.drop(columns=['coluna1', 'coluna2'])\n\n# Linhas por índice\ndf = df.drop(index=[0, 1, 2])\n\n# Linhas por condição (manter onde size > 1)\ndf = df[df['size'] > 1]</code></pre><div class='warn'>⚠️ pandas NÃO modifica in-place por padrão. Sempre reatribua: <code>df = df.drop(...)</code></div>", ["python", "pandas"]),
    ("Como lidar com valores nulos?", "<pre><code>df.isnull().sum()          # contar nulos por coluna\ndf.dropna()                # remover linhas com nulo\ndf.dropna(subset=['nome']) # só se 'nome' for nulo\ndf['col'].fillna(0)        # substituir nulos por 0\ndf['col'].fillna(df['col'].mean()) # pela média</code></pre>", ["python", "pandas"]),
    ("Como agrupar e agregar dados?", "<pre><code># GroupBy\ndf.groupby('cidade')['vendas'].sum()\ndf.groupby('cidade').agg(\n    total=('vendas', 'sum'),\n    media=('vendas', 'mean'),\n    qtd=('vendas', 'count')\n)\n\n# Tabela dinâmica\npd.pivot_table(df, values='vendas',\n               index='cidade',\n               columns='mes',\n               aggfunc='sum')</code></pre>", ["python", "pandas"]),
    ("Como juntar dois DataFrames (merge/join)?", "<pre><code># Equivalente ao PROCV/VLOOKUP\nresult = pd.merge(df1, df2,\n                  on='id',         # coluna em comum\n                  how='left')      # tipo do join\n\n# Tipos: 'left', 'right', 'inner', 'outer'\n\n# Empilhar (append)\ndf_total = pd.concat([df1, df2], ignore_index=True)</code></pre>", ["python", "pandas"]),
    ("Como criar colunas calculadas e condicionais?", "<pre><code># Calculada\ndf['total'] = df['preco'] * df['quantidade']\n\n# Condicional (equivalente ao SE/IF)\nimport numpy as np\ndf['status'] = np.where(\n    df['nota'] >= 7, 'Aprovado', 'Reprovado'\n)\n\n# Faixas (equivalente a classificar)\ndf['faixa'] = pd.cut(df['idade'],\n    bins=[0, 18, 35, 60, 100],\n    labels=['Jovem','Adulto','Meia-idade','Idoso']\n)</code></pre>", ["python", "pandas"]),
    ("Como ordenar e remover duplicados?", "<pre><code># Ordenar\ndf = df.sort_values('vendas', ascending=False)\ndf = df.sort_values(['cidade','vendas'])\n\n# Duplicados\ndf.duplicated().sum()      # contar\ndf = df.drop_duplicates()  # remover\ndf = df.drop_duplicates(subset=['email']) # por coluna</code></pre>", ["python", "pandas"]),
    ("Como alterar tipos de coluna?", "<pre><code>df['preco'] = df['preco'].astype(float)\ndf['data'] = pd.to_datetime(df['data'])\ndf['codigo'] = df['codigo'].astype(str)\n\n# Padronizar texto\ndf['nome'] = df['nome'].str.lower().str.strip()</code></pre>", ["python", "pandas"]),
    ("Como salvar e exportar DataFrame?", "<pre><code>df.to_csv('saida.csv', index=False)\ndf.to_excel('saida.xlsx', index=False)\ndf.to_json('saida.json', orient='records')\ndf.to_parquet('saida.parquet')  # formato eficiente</code></pre>", ["python", "pandas"]),
]

py_eda_cards = [
    ("Qual o checklist básico de EDA?", "1. <code>df.shape</code> — dimensões<br>2. <code>df.info()</code> — tipos e nulos<br>3. <code>df.describe()</code> — estatísticas<br>4. <code>df.isnull().sum()</code> — nulos por coluna<br>5. <code>df.duplicated().sum()</code> — duplicados<br>6. <code>df.nunique()</code> — valores únicos<br>7. Histogramas e boxplots das numéricas<br>8. Value counts das categóricas", ["python", "eda"]),
    ("Como criar visualizações rápidas com pandas?", "<pre><code># Histograma\ndf['idade'].hist(bins=20)\n\n# Barras\ndf['cidade'].value_counts().plot.bar()\n\n# Scatter\ndf.plot.scatter(x='peso', y='altura')\n\n# Boxplot\ndf.boxplot(column='vendas', by='regiao')\n\n# Correlação\nimport seaborn as sns\nsns.heatmap(df.corr(), annot=True)</code></pre>", ["python", "eda", "visualização"]),
    ("Como identificar e tratar outliers?", "<pre><code># Método IQR\nQ1 = df['col'].quantile(0.25)\nQ3 = df['col'].quantile(0.75)\nIQR = Q3 - Q1\n\nfiltro = (df['col'] >= Q1 - 1.5*IQR) & \\\n         (df['col'] <= Q3 + 1.5*IQR)\ndf_clean = df[filtro]\n\n# Visual: boxplot mostra outliers como pontos\ndf['col'].plot.box()</code></pre>", ["python", "eda"]),
]

# ═══════════════════════════════════════════════════════════════
# DATA - TRÍADE (Planilha ↔ Python ↔ SQL)
# ═══════════════════════════════════════════════════════════════

triade_cards = [
    ("Filtrar linhas por condição",
     "Ícone de filtro → selecionar valores<br>Ou: Dados > Filtro Avançado",
     "<code>df[df['idade'] > 18]</code><br>ou<br><code>df.query('idade > 18')</code>",
     "<code>SELECT * FROM tabela<br>WHERE idade > 18</code>",
     ["data", "filtrar"]),
    ("Ordenar dados",
     "Dados > Classificar<br>Selecionar coluna e ordem (A-Z ou Z-A)",
     "<code>df.sort_values('vendas', ascending=False)</code>",
     "<code>SELECT * FROM tabela<br>ORDER BY vendas DESC</code>",
     ["data", "ordenar"]),
    ("Selecionar colunas específicas",
     "Ocultar colunas não desejadas<br>Ou: copiar apenas as colunas necessárias",
     "<code>df[['nome', 'idade', 'cidade']]</code>",
     "<code>SELECT nome, idade, cidade<br>FROM tabela</code>",
     ["data", "selecionar"]),
    ("Remover duplicados",
     "Dados > Remover Duplicatas<br>Selecionar colunas para comparação",
     "<code>df.drop_duplicates(subset=['email'])</code>",
     "<code>SELECT DISTINCT nome, email<br>FROM tabela</code>",
     ["data", "limpeza"]),
    ("Substituir valores nulos",
     "Ctrl+H → buscar vazio, substituir por valor<br>Ou: =SE(A1=\"\"; 0; A1)",
     "<code>df['col'].fillna(0)</code><br><code>df['col'].fillna(df['col'].mean())</code>",
     "<code>SELECT COALESCE(col, 0)<br>FROM tabela</code><br>ou<br><code>SELECT IFNULL(col, 0) FROM tabela</code>",
     ["data", "limpeza"]),
    ("Remover linhas com nulos",
     "Filtrar → desmarcar \"Vazios\"<br>Ou: selecionar e deletar manualmente",
     "<code>df.dropna()</code><br><code>df.dropna(subset=['nome'])</code>",
     "<code>SELECT * FROM tabela<br>WHERE col IS NOT NULL</code>",
     ["data", "limpeza"]),
    ("Agrupar e somar (tabela dinâmica)",
     "Inserir > Tabela Dinâmica<br>Linha: cidade | Valor: soma de vendas",
     "<code>df.groupby('cidade')['vendas'].sum()</code>",
     "<code>SELECT cidade, SUM(vendas)<br>FROM tabela<br>GROUP BY cidade</code>",
     ["data", "agregação"]),
    ("Agrupar e contar",
     "Tabela Dinâmica → Contagem",
     "<code>df.groupby('cidade')['id'].count()</code><br>ou<br><code>df['cidade'].value_counts()</code>",
     "<code>SELECT cidade, COUNT(*)<br>FROM tabela<br>GROUP BY cidade</code>",
     ["data", "agregação"]),
    ("Calcular média por grupo",
     "Tabela Dinâmica → Média<br>Ou: =MÉDIASES()",
     "<code>df.groupby('cidade')['vendas'].mean()</code>",
     "<code>SELECT cidade, AVG(vendas)<br>FROM tabela<br>GROUP BY cidade</code>",
     ["data", "agregação"]),
    ("Juntar duas tabelas (PROCV/VLOOKUP)",
     "<code>=PROCV(A2; Tabela2; 2; FALSO)</code><br>Busca valor da coluna A na Tabela2 e retorna coluna 2",
     "<code>pd.merge(df1, df2, on='id', how='left')</code>",
     "<code>SELECT * FROM tabela1<br>LEFT JOIN tabela2<br>ON tabela1.id = tabela2.id</code>",
     ["data", "join"]),
    ("Empilhar dados (append/union)",
     "Copiar e colar abaixo<br>Ou: Power Query > Anexar Consultas",
     "<code>pd.concat([df1, df2], ignore_index=True)</code>",
     "<code>SELECT * FROM tabela1<br>UNION ALL<br>SELECT * FROM tabela2</code>",
     ["data", "join"]),
    ("Criar coluna condicional (SE/IF)",
     "<code>=SE(A2>=7; \"Aprovado\"; \"Reprovado\")</code>",
     "<code>import numpy as np<br>df['status'] = np.where(<br>&nbsp;&nbsp;df['nota']>=7, 'Aprovado', 'Reprovado')</code>",
     "<code>SELECT CASE<br>&nbsp;&nbsp;WHEN nota >= 7 THEN 'Aprovado'<br>&nbsp;&nbsp;ELSE 'Reprovado'<br>END AS status<br>FROM tabela</code>",
     ["data", "transformação"]),
    ("Criar coluna calculada",
     "<code>=B2*C2</code> (preço × quantidade)",
     "<code>df['total'] = df['preco'] * df['qtd']</code>",
     "<code>SELECT preco * qtd AS total<br>FROM tabela</code>",
     ["data", "transformação"]),
    ("Classificar em faixas",
     "=SE(A2<=18;\"Jovem\";SE(A2<=35;\"Adulto\";\"Idoso\"))",
     "<code>pd.cut(df['idade'],<br>&nbsp;&nbsp;bins=[0,18,35,60,100],<br>&nbsp;&nbsp;labels=['Jovem','Adulto',<br>&nbsp;&nbsp;&nbsp;&nbsp;'Meia-idade','Idoso'])</code>",
     "<code>SELECT CASE<br>&nbsp;&nbsp;WHEN idade <= 18 THEN 'Jovem'<br>&nbsp;&nbsp;WHEN idade <= 35 THEN 'Adulto'<br>&nbsp;&nbsp;ELSE 'Idoso'<br>END FROM tabela</code>",
     ["data", "transformação"]),
    ("Padronizar textos (maiúscula/minúscula)",
     "<code>=MINÚSCULA(A2)</code> ou <code>=ARRUMAR(A2)</code>",
     "<code>df['nome'] = df['nome'].str.lower().str.strip()</code>",
     "<code>SELECT LOWER(TRIM(nome))<br>FROM tabela</code>",
     ["data", "limpeza"]),
    ("Alterar formato de coluna",
     "Formatar Células > Número/Data/Texto",
     "<code>df['preco'] = df['preco'].astype(float)<br>df['data'] = pd.to_datetime(df['data'])</code>",
     "<code>SELECT CAST(preco AS DECIMAL)<br>FROM tabela</code>",
     ["data", "transformação"]),
    ("Transformar colunas em linhas (unpivot/melt)",
     "Power Query > Transformar > Remover Pivô",
     "<code>df.melt(id_vars=['nome'],<br>&nbsp;&nbsp;value_vars=['jan','fev','mar'],<br>&nbsp;&nbsp;var_name='mes',<br>&nbsp;&nbsp;value_name='vendas')</code>",
     "<code>SELECT nome, 'jan' AS mes, jan AS vendas FROM t<br>UNION ALL<br>SELECT nome, 'fev', fev FROM t</code>",
     ["data", "transformação"]),
    ("Transformar linhas em colunas (pivot)",
     "Tabela Dinâmica (linhas→colunas naturalmente)",
     "<code>df.pivot_table(values='vendas',<br>&nbsp;&nbsp;index='nome',<br>&nbsp;&nbsp;columns='mes',<br>&nbsp;&nbsp;aggfunc='sum')</code>",
     "<code>SELECT nome,<br>&nbsp;&nbsp;SUM(CASE WHEN mes='jan' THEN vendas END) as jan,<br>&nbsp;&nbsp;SUM(CASE WHEN mes='fev' THEN vendas END) as fev<br>FROM t GROUP BY nome</code>",
     ["data", "transformação"]),
]

# ═══════════════════════════════════════════════════════════════
# FERRAMENTAS
# ═══════════════════════════════════════════════════════════════

md_cards = [
    ("Como criar link interno no Obsidian (wikilink)?", "<code>[[nome da nota]]</code> — link simples<br><code>[[nota|texto exibido]]</code> — com alias<br><code>[[nota#Heading]]</code> — link para seção<br><code>[[nota#Heading|alias]]</code> — seção com alias", ["markdown", "obsidian"]),
    ("Como embedar conteúdo de outra nota?", "<code>![[nota]]</code> — embeda nota inteira<br><code>![[nota#seção]]</code> — embeda só a seção<br><code>![[imagem.png]]</code> — embeda imagem<br><code>![[imagem.png|300]]</code> — com largura fixa", ["markdown", "obsidian"]),
    ("Como inserir imagem em Markdown puro?", "<code>![alt text](imagens/figura.png)</code><br><br>Com tamanho (não padrão, funciona em alguns renderers):<br><code>![alt](fig.png){width=300}</code><br><br>Em HTML: <code>&lt;img src=\"fig.png\" width=\"300\"&gt;</code>", ["markdown"]),
    ("Sintaxe Markdown essencial", "<pre><code># H1  ## H2  ### H3\n**negrito** *itálico* ~~riscado~~\n- lista\n1. lista numerada\n[link](url)\n`código inline`\n```python\nbloco de código\n```\n> citação\n---  (linha horizontal)</code></pre>", ["markdown"]),
]

regex_cards = [
    ("O que é regex e para que serve?", "Expressão regular — padrão de busca em texto<br><br>Exemplos de uso:<br>• Validar email, CPF, telefone<br>• Buscar/substituir em código<br>• Extrair dados de texto<br>• grep, sed, Python re, VS Code Find", ["regex"]),
    ("Metacaracteres básicos de regex", "<code>.</code> — qualquer caractere<br><code>\\d</code> — dígito (0-9)<br><code>\\w</code> — letra, dígito ou _<br><code>\\s</code> — espaço/tab/newline<br><code>^</code> — início da linha<br><code>$</code> — fim da linha<br><code>\\b</code> — limite de palavra", ["regex"]),
    ("Quantificadores em regex", "<code>*</code> — 0 ou mais<br><code>+</code> — 1 ou mais<br><code>?</code> — 0 ou 1 (opcional)<br><code>{3}</code> — exatamente 3<br><code>{2,5}</code> — de 2 a 5<br><br>Ex: <code>\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}</code> → CPF", ["regex"]),
    ("Como usar grupos e alternância?", "<code>(abc)</code> — grupo de captura<br><code>(?:abc)</code> — grupo sem captura<br><code>a|b</code> — a OU b<br><code>[abc]</code> — qualquer um: a, b ou c<br><code>[^abc]</code> — qualquer um EXCETO a, b, c<br><code>[0-9a-z]</code> — range", ["regex"]),
    ("Regex em Python", "<pre><code>import re\n\n# Buscar\nre.search(r'\\d+', 'abc123')  # Match '123'\n\n# Todas as ocorrências\nre.findall(r'\\d+', 'a1 b2 c3')  # ['1','2','3']\n\n# Substituir\nre.sub(r'\\d', 'X', 'abc123')  # 'abcXXX'\n\n# Grupos\nm = re.search(r'(\\w+)@(\\w+)', 'user@mail')\nm.group(1)  # 'user'</code></pre>", ["regex", "python"]),
]

vscode_cards = [
    ("Atalhos essenciais do VS Code (macOS)", "<code>Cmd+P</code> — abrir arquivo por nome<br><code>Cmd+Shift+P</code> — paleta de comandos<br><code>Cmd+B</code> — toggle sidebar<br><code>Cmd+`</code> — toggle terminal<br><code>Cmd+D</code> — selecionar próxima ocorrência<br><code>Opt+↑/↓</code> — mover linha<br><code>Cmd+/</code> — comentar linha", ["vscode", "atalhos"]),
    ("Como usar multi-cursor no VS Code?", "<code>Opt+Click</code> — adicionar cursor<br><code>Cmd+D</code> — selecionar próxima ocorrência igual<br><code>Cmd+Shift+L</code> — selecionar TODAS as ocorrências<br><code>Opt+Shift+↓</code> — duplicar linha<br><br>Útil para renomear variáveis, editar múltiplas linhas", ["vscode"]),
    ("Como usar o terminal integrado do VS Code?", "<code>Cmd+`</code> — abrir/fechar terminal<br><code>Cmd+Shift+`</code> — novo terminal<br><code>Cmd+\\</code> — split terminal<br><br><div class='tip'>💡 O terminal usa o mesmo shell do sistema (zsh). Ative o venv aqui: <code>source .venv/bin/activate</code></div>", ["vscode", "terminal"]),
]


# ─── Montar decks ──────────────────────────────────────────────

for c in nav_cards:
    decks['nav'].add_note(card(*c))
for c in arq_cards:
    decks['arquivos'].add_note(card(*c))
for c in redir_cards:
    decks['redir'].add_note(card(*c))
for c in script_cards:
    decks['scripts'].add_note(card(*c))

for c in git_fund_cards:
    decks['git_fund'].add_note(card(*c))
for c in git_branch_cards:
    decks['git_branch'].add_note(card(*c))
for c in git_colab_cards:
    decks['git_colab'].add_note(card(*c))
for c in git_fix_cards:
    decks['git_fix'].add_note(card(*c))

for c in py_fund_cards:
    decks['py_fund'].add_note(card(*c))
for c in py_pandas_cards:
    decks['py_pandas'].add_note(card(*c))
for c in py_eda_cards:
    decks['py_eda'].add_note(card(*c))

for c in triade_cards:
    decks['data'].add_note(triade(*c))

for c in md_cards:
    decks['md'].add_note(card(*c))
for c in regex_cards:
    decks['regex'].add_note(card(*c))
for c in vscode_cards:
    decks['vscode'].add_note(card(*c))


# ─── Exportar ──────────────────────────────────────────────────

output_path = Path(__file__).parent / 'Dev_Programacao.apkg'

package = genanki.Package([d for d in decks.values()])
package.write_to_file(output_path)

# Stats
total = sum(
    len(nav_cards) + len(arq_cards) + len(redir_cards) + len(script_cards)
    + len(git_fund_cards) + len(git_branch_cards) + len(git_colab_cards) + len(git_fix_cards)
    + len(py_fund_cards) + len(py_pandas_cards) + len(py_eda_cards)
    + len(md_cards) + len(regex_cards) + len(vscode_cards)
    for _ in [1]
)
triade_total = len(triade_cards) * 2  # 2 cards por nota (Python e SQL)

print(f"✅ Deck gerado: {output_path}")
print(f"   Basic cards: {total}")
print(f"   Tríade cards: {triade_total} ({len(triade_cards)} notas × 2 direções)")
print(f"   Total: {total + triade_total} cards")
print()
print("Estrutura:")
for d in sorted(decks.values(), key=lambda x: x.name):
    count = len(d.notes)
    if count > 0:
        print(f"  {d.name}: {count} notas")
