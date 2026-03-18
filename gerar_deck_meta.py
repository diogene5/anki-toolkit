#!/usr/bin/env python3
"""
🧠 gerar_deck_meta.py — Deck sobre manipulação do Anki e design de flashcards

O QUE É ESTE DECK:
──────────────────
Cards sobre o que aprendemos hoje:
  1. Como o Anki armazena dados (SQLite, .apkg, .colpkg)
  2. Como manipular arquivos Anki programaticamente
  3. Princípios de design de flashcards eficazes
  4. CSS para cards (dark mode, tipografia, hierarquia)
  5. Workflow com Git para versionar decks

É um "meta-deck" — flashcards sobre como fazer flashcards melhores.
"""
from pathlib import Path
import genanki
import random

random.seed(99)

# ─── CSS refinado com insights do Impeccable ──────────────────
# Melhorias aplicadas:
#   - CSS variables para manutenção
#   - Tinted neutrals (hue 250° no cinza)
#   - Line-height 1.65 para dark mode
#   - 4pt spacing scale
#   - max-width: 65ch para medida ideal
#   - prefers-reduced-motion
CARD_CSS = '''
.card {
  font-family: "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  text-align: left;
  color: #bac2de;
  background-color: #181825;
  padding: 28px 24px;
  max-width: 65ch;
  margin: 0 auto;
}
.front {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.45;
  color: #cdd6f4;
}
.back {
  font-size: 15px;
  line-height: 1.65;
  color: #a6adc8;
}
.back b, .back strong { color: #cdd6f4; font-weight: 600; }
code {
  font-family: "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace;
  font-size: 0.88em;
  color: #94e2d5;
  background: rgba(49,50,68,0.7);
  padding: 2px 7px;
  border-radius: 4px;
  border: 1px solid rgba(69,71,90,0.5);
}
pre {
  background: #11111b;
  padding: 16px 18px;
  border-radius: 8px;
  border: 1px solid rgba(49,50,68,0.8);
  overflow-x: auto;
  margin: 12px 0;
}
pre code {
  padding: 0; background: none; border: none;
  color: #a6e3a1; font-size: 13px; line-height: 1.7;
}
hr {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent 0%, #45475a 15%, #585b70 50%, #45475a 85%, transparent 100%);
  margin: 20px 0;
}
.tip {
  background: rgba(166,227,161,0.06);
  border-left: 2px solid rgba(166,227,161,0.5);
  padding: 10px 14px; margin: 12px 0 4px;
  border-radius: 0 6px 6px 0; font-size: 13.5px;
  line-height: 1.55; color: #a6adc8;
}
.warn {
  background: rgba(249,226,175,0.06);
  border-left: 2px solid rgba(249,226,175,0.5);
  padding: 10px 14px; margin: 12px 0 4px;
  border-radius: 0 6px 6px 0; font-size: 13.5px;
  line-height: 1.55; color: #a6adc8;
}
.nightMode .card { background-color: #181825; }
@media (max-width: 480px) {
  .card { padding: 22px 18px; }
  .front { font-size: 16px; }
  pre code { font-size: 12.5px; }
}
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
'''

MODEL = genanki.Model(
    1607392099,
    'Meta Anki - Basic',
    fields=[{'name': 'Frente'}, {'name': 'Verso'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div class="front">{{Frente}}</div>',
        'afmt': '<div class="front">{{Frente}}</div><hr id="answer"><div class="back">{{Verso}}</div>',
    }],
    css=CARD_CSS,
)

# ─── Decks ─────────────────────────────────────────────────────
decks = {
    'root':    genanki.Deck(2002000000, 'Meta::Anki & Flashcards'),
    'sqlite':  genanki.Deck(2002000001, 'Meta::Anki & Flashcards::Como o Anki Funciona'),
    'manip':   genanki.Deck(2002000002, 'Meta::Anki & Flashcards::Manipulação Programática'),
    'design':  genanki.Deck(2002000003, 'Meta::Anki & Flashcards::Design de Cards Eficazes'),
    'css':     genanki.Deck(2002000004, 'Meta::Anki & Flashcards::CSS & Estilo'),
    'workflow':genanki.Deck(2002000005, 'Meta::Anki & Flashcards::Workflow & Git'),
}

def card(front, back, tags=None):
    return genanki.Note(model=MODEL, fields=[front, back], tags=tags or [])


# ═══════════════════════════════════════════════════════════════
# COMO O ANKI FUNCIONA
# ═══════════════════════════════════════════════════════════════

sqlite_cards = [
    ("Qual banco de dados o Anki usa internamente?",
     "<b>SQLite</b> — banco leve que fica em um único arquivo: <code>collection.anki2</code><br><br>Caminho no macOS:<br><code>~/Library/Application Support/Anki2/&lt;perfil&gt;/collection.anki2</code>",
     ["anki", "sqlite"]),

    ("Quais são as 5 tabelas principais do SQLite do Anki?",
     "<b>notes</b> — conteúdo (campos, tags)<br>"
     "<b>cards</b> — instâncias de estudo (scheduling)<br>"
     "<b>decks</b> — baralhos<br>"
     "<b>notetypes</b> — modelos (Basic, Cloze, etc.)<br>"
     "<b>revlog</b> — log de todas as revisões",
     ["anki", "sqlite"]),

    ("Qual a diferença entre uma NOTA e um CARD no Anki?",
     "<b>Nota</b> = o conteúdo (campos de texto, tags)<br>"
     "<b>Card</b> = instância de estudo gerada pela nota<br><br>"
     "Uma nota pode gerar <b>múltiplos cards</b>.<br>"
     "Ex: nota 'Basic (and reversed)' → 2 cards (frente→verso e verso→frente)",
     ["anki", "conceitos"]),

    ("Como o Anki separa campos dentro do banco de dados?",
     "Com o caractere <code>\\x1f</code> (ASCII 31, 'unit separator')<br><br>"
     "No Python: <code>campos = nota.flds.split('\\x1f')</code><br><br>"
     "<div class='tip'>💡 Não é tab, não é vírgula — é um caractere invisível especial</div>",
     ["anki", "sqlite"]),

    ("O que significam os estados 0, 1, 2, 3 na coluna <code>type</code> de cards?",
     "<b>0</b> = New (nunca estudado)<br>"
     "<b>1</b> = Learning (em aprendizado, intervalos curtos)<br>"
     "<b>2</b> = Review (aprendido, revisão espaçada)<br>"
     "<b>3</b> = Relearning (errou e voltou para aprendizado)",
     ["anki", "sqlite"]),

    ("O que é o ease factor e qual o valor padrão?",
     "Multiplicador que define quanto o intervalo cresce a cada revisão correta.<br><br>"
     "Padrão: <b>250%</b> (armazenado como 2500 no banco)<br>"
     "Se ease = 250% e intervalo atual = 10 dias → próximo = 25 dias<br><br>"
     "<div class='warn'>⚠️ Ease abaixo de 200% indica dificuldade — o card pode estar mal formulado</div>",
     ["anki", "srs"]),

    ("O que é um arquivo <code>.apkg</code>?",
     "É um <b>ZIP</b> contendo:<br>"
     "• Um banco SQLite (notas, cards, decks)<br>"
     "• Arquivo <code>media</code> (JSON mapeando nomes de mídia)<br>"
     "• Arquivos de mídia (imagens, áudio)<br><br>"
     "Na importação, <b>mescla</b> com sua coleção (não substitui).<br>"
     "Descompactar: <code>unzip deck.apkg -d conteudo/</code>",
     ["anki", "formatos"]),

    ("Qual a diferença entre <code>.apkg</code> e <code>.colpkg</code>?",
     "<b>.apkg</b> = deck empacotado → <b>mescla</b> na importação<br>"
     "<b>.colpkg</b> = coleção completa → <b>substitui tudo</b> na importação<br><br>"
     "<div class='warn'>⚠️ Importar .colpkg apaga toda a coleção atual! Use só para backup/restore</div>",
     ["anki", "formatos"]),

    ("Por que nunca modificar <code>collection.anki2</code> com o Anki aberto?",
     "O Anki mantém o banco <b>bloqueado</b> enquanto roda (usa WAL mode do SQLite).<br><br>"
     "Modificar externamente causa:<br>"
     "• Corrupção de dados<br>"
     "• Conflito de locks<br>"
     "• Perda de revisões em andamento<br><br>"
     "Sempre feche o Anki antes de scripts Python.",
     ["anki", "sqlite"]),

    ("O que é a collation <code>unicase</code> do Anki?",
     "Função de comparação case-insensitive que o Anki registra no SQLite.<br><br>"
     "O <code>sqlite3</code> da linha de comando <b>não a conhece</b> — queries com ORDER BY em texto falham.<br><br>"
     "Solução em Python:<br>"
     "<pre><code>conn.create_collation('unicase',\n  lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))</code></pre>",
     ["anki", "sqlite", "python"]),
]

# ═══════════════════════════════════════════════════════════════
# MANIPULAÇÃO PROGRAMÁTICA
# ═══════════════════════════════════════════════════════════════

manip_cards = [
    ("Como abrir o banco do Anki com Python?",
     "<pre><code>import sqlite3\n\nconn = sqlite3.connect('collection.anki2')\nconn.create_collation('unicase', ...)\ncursor = conn.execute('SELECT * FROM notes')\nconn.close()</code></pre>"
     "<div class='tip'>💡 Sempre registrar a collation 'unicase' antes de qualquer query</div>",
     ["python", "sqlite"]),

    ("Qual biblioteca Python cria arquivos <code>.apkg</code> do zero?",
     "<b>genanki</b><br><code>pip install genanki</code><br><br>"
     "Componentes:<br>"
     "• <code>genanki.Model</code> — define campos + templates HTML<br>"
     "• <code>genanki.Deck</code> — baralho<br>"
     "• <code>genanki.Note</code> — conteúdo<br>"
     "• <code>genanki.Package</code> — empacota em .apkg",
     ["python", "genanki"]),

    ("Por que usar <code>random.seed(42)</code> no genanki?",
     "O genanki gera <b>GUIDs aleatórios</b> para cada nota.<br><br>"
     "Com seed fixa, os GUIDs são <b>estáveis entre execuções</b>.<br>"
     "Sem isso, re-importar o .apkg <b>duplicaria</b> as notas em vez de atualizar.",
     ["python", "genanki"]),

    ("Como o Anki identifica notas para atualização na importação?",
     "Pelo <b>primeiro campo</b> (sfld = sort field).<br><br>"
     "Se importar um CSV com o mesmo primeiro campo de uma nota existente, "
     "o Anki <b>atualiza</b> a nota (não duplica).<br><br>"
     "Para .apkg: usa o <b>GUID</b> interno da nota.",
     ["anki", "importação"]),

    ("Como gerar um CSV pronto para importação no Anki?",
     "Usar headers especiais no topo do arquivo:<br>"
     "<pre><code>#separator:Tab\n#html:true\n#notetype:Basic\n#deck:MeuDeck\n#tags:tag1 tag2\ncampo1\\tcampo2</code></pre>"
     "Disponível desde Anki 2.1.54+",
     ["anki", "csv"]),

    ("Para que serve <code>genanki.Model</code>?",
     "Define um <b>note type</b> (modelo de nota):<br><br>"
     "• <b>fields</b>: campos da nota (Frente, Verso, etc.)<br>"
     "• <b>templates</b>: HTML que gera cada card<br>"
     "• <b>css</b>: estilo visual<br><br>"
     "Um Model com 2 templates gera <b>2 cards por nota</b>.<br>"
     "O ID do Model deve ser <b>fixo e único</b> — nunca mude depois de importar.",
     ["python", "genanki"]),

    ("O que é um note type com múltiplos templates?",
     "Um modelo que gera <b>vários cards</b> de uma única nota.<br><br>"
     "Exemplo: modelo Tríade com 4 campos (Operação, Planilha, Python, SQL) "
     "e 2 templates:<br>"
     "• Template 1: pergunta Python<br>"
     "• Template 2: pergunta SQL<br><br>"
     "Resultado: 1 nota → 2 cards com direções diferentes.",
     ["anki", "noteypes"]),
]

# ═══════════════════════════════════════════════════════════════
# DESIGN DE CARDS EFICAZES
# ═══════════════════════════════════════════════════════════════

design_cards = [
    ("O que é o princípio atômico de flashcards?",
     "Cada card deve testar <b>exatamente 1 conceito</b>.<br><br>"
     "❌ 'Qual comando remove pasta vazia? E com conteúdo?'<br>"
     "✅ Card 1: 'Como remover pasta vazia?' → <code>rmdir</code><br>"
     "✅ Card 2: 'Como remover pasta com conteúdo?' → <code>rm -r</code>",
     ["design", "princípios"]),

    ("Por que evitar respostas muito longas em flashcards?",
     "O SRS funciona por <b>recall rápido</b>.<br>"
     "Se a resposta tem 500+ caracteres, seu cérebro não consegue avaliar "
     "se 'lembrou' ou não — acaba avaliando parcialmente.<br><br>"
     "Limite ideal: <b>< 200 caracteres</b> ou 3-4 linhas.<br>"
     "Se precisar de mais, <b>divida em múltiplos cards</b>.",
     ["design", "princípios"]),

    ("Como formatar código em flashcards?",
     "Sempre usar HTML:<br>"
     "• Inline: <code>&lt;code&gt;git status&lt;/code&gt;</code><br>"
     "• Bloco: <code>&lt;pre&gt;&lt;code&gt;...&lt;/code&gt;&lt;/pre&gt;</code><br><br>"
     "Sem HTML, o código fica com fonte proporcional e se mistura com texto normal — "
     "dificulta scan visual durante revisão.",
     ["design", "html"]),

    ("O que é o padrão tríade para cards de programação?",
     "Comparar a <b>mesma operação</b> em 3 ferramentas:<br>"
     "Planilha ↔ Python ↔ SQL<br><br>"
     "1 nota com 4 campos gera 2 cards (pergunta Python + pergunta SQL).<br>"
     "Cada resposta mostra as 3 versões.<br><br>"
     "<div class='tip'>💡 Cria links mentais: quando lembra a versão pandas, reforça a SQL automaticamente</div>",
     ["design", "tríade"]),

    ("O que é o 'squint test' para hierarquia visual?",
     "Desfoque o card (aperte os olhos ou afaste a tela).<br><br>"
     "Você ainda consegue distinguir <b>pergunta</b> de <b>resposta</b>?<br><br>"
     "Se tudo parece do mesmo peso → hierarquia fraca.<br>"
     "Solução: diferenciar por <b>tamanho + peso + cor + espaço</b>.",
     ["design", "css"]),

    ("O que é similaridade de Jaccard e como usar para detectar sobreposição?",
     "Fórmula: <b>|A ∩ B| / |A ∪ B|</b><br><br>"
     "Extrai palavras-chave de dois cards e calcula quantas são comuns.<br>"
     "Acima de 40% → provável sobreposição.<br><br>"
     "Exemplo:<br>"
     "'Como criar branch?' vs 'Como criar nova branch?' → 60% similar",
     ["design", "análise"]),

    ("Qual o problema de imagens coladas (paste-xxx.jpg) em flashcards?",
     "As imagens vivem em <code>collection.media/</code> com nomes hash.<br><br>"
     "Problemas:<br>"
     "• Não exportam com .apkg sem mídia<br>"
     "• Não são versionáveis no Git<br>"
     "• Podem quebrar ao migrar entre dispositivos<br><br>"
     "Melhor: usar imagens com nomes descritivos e referências relativas.",
     ["design", "mídia"]),
]

# ═══════════════════════════════════════════════════════════════
# CSS & ESTILO
# ═══════════════════════════════════════════════════════════════

css_cards = [
    ("Por que usar <code>rgba()</code> em vez de cores sólidas para callouts?",
     "Com <code>background: rgba(166,227,161,0.06)</code> a callout é <b>semi-transparente</b>.<br><br>"
     "Se adapta ao fundo automaticamente — parece 'parte do card' em vez de bloco colado.<br><br>"
     "<div class='tip'>💡 Paletas incompletas se beneficiam de rgba. Para projetos maiores, defina cores explícitas</div>",
     ["css", "cores"]),

    ("O que são 'tinted neutrals' e por que usar?",
     "Cinzas com leve <b>tint do hue dominante</b>.<br><br>"
     "No Catppuccin Mocha (hue 250° = azul):<br>"
     "❌ Cinza puro: <code>#6c7086</code><br>"
     "✅ Cinza com tint azul: <code>oklch(50% 0.01 250)</code><br><br>"
     "Cria <b>coesão visual subconsciente</b> — tudo parece pertencer ao mesmo universo.",
     ["css", "cores"]),

    ("Por que line-height maior em dark mode?",
     "Texto claro em fundo escuro cria mais <b>halo/bleeding visual</b>.<br><br>"
     "Recomendação: +0.05 a +0.1 extra vs light mode.<br>"
     "Light mode: <code>line-height: 1.5</code><br>"
     "Dark mode: <code>line-height: 1.6–1.65</code>",
     ["css", "tipografia"]),

    ("Como o gradiente no <code>&lt;hr&gt;</code> melhora a divisão Q→A?",
     "<code>background: linear-gradient(90deg, transparent, #585b70, transparent)</code><br><br>"
     "O divisor 'respira' nas bordas em vez de cortar abruptamente.<br>"
     "É o tipo de detalhe que seu olho percebe como 'polido' sem saber por quê.",
     ["css", "detalhes"]),

    ("Qual a escala de espaçamento recomendada (spacing scale)?",
     "Base 4pt: <b>4, 8, 12, 16, 24, 32, 48px</b><br><br>"
     "Mais granular que 8pt (que é grosseira para padding de cards).<br><br>"
     "Usar line-height como unidade de ritmo:<br>"
     "15px × 1.6 = 24px → usar 24px como espaçamento vertical entre seções.",
     ["css", "espacamento"]),

    ("Por que <code>max-width: 65ch</code> melhora a leitura?",
     "<code>ch</code> = largura do caractere '0' na fonte atual.<br>"
     "65ch ≈ 65 caracteres por linha — medida ideal para leitura.<br><br>"
     "Linhas mais longas causam 'perda de retorno' (olho se perde ao voltar).<br>"
     "Linhas curtas demais quebram o fluxo de leitura.",
     ["css", "tipografia"]),
]

# ═══════════════════════════════════════════════════════════════
# WORKFLOW & GIT
# ═══════════════════════════════════════════════════════════════

workflow_cards = [
    ("Por que versionar scripts de Anki no Git?",
     "Scripts de geração de deck mudam com o tempo (novos cards, CSS melhorado).<br><br>"
     "Com Git:<br>"
     "• Histórico de todas as versões do deck<br>"
     "• Pode reverter se uma mudança quebrar algo<br>"
     "• Colaboração (outros podem contribuir cards)<br>"
     "• O .apkg é binário, mas o .py que o gera é texto puro → diff funciona",
     ["workflow", "git"]),

    ("Qual a vantagem de CSV sobre .apkg para manutenção?",
     "<b>CSV</b>: texto puro → fácil de editar, versionar no Git, diff<br>"
     "<b>.apkg</b>: binário → inclui mídia, CSS, cria decks automaticamente<br><br>"
     "Estratégia ideal: manter cards como <b>código Python</b> (gerar_deck.py), "
     "gerar .apkg quando quiser importar.",
     ["workflow", "formatos"]),

    ("Qual o fluxo para atualizar cards que já foram importados?",
     "1. Editar <code>gerar_deck.py</code><br>"
     "2. Rodar <code>python3 gerar_deck.py</code> (regenera .apkg)<br>"
     "3. No Anki: File > Import > selecionar .apkg<br>"
     "4. O Anki atualiza notas existentes (pelo GUID) sem duplicar<br><br>"
     "<div class='tip'>💡 random.seed(42) garante GUIDs estáveis entre execuções</div>",
     ["workflow", "atualização"]),

    ("Por que colocar <code>*.anki2</code> e <code>backups/</code> no <code>.gitignore</code>?",
     "<code>*.anki2</code> — bancos SQLite com dados pessoais (scheduling, histórico)<br>"
     "<code>backups/</code> — cópias de segurança, grandes e pessoais<br><br>"
     "O que versionar:<br>"
     "✅ Scripts Python (.py)<br>"
     "✅ .gitignore, README.md<br>"
     "✅ .apkg gerados (são o 'produto')<br>"
     "❌ Bancos pessoais, backups, JSONs de export",
     ["workflow", "git"]),
]


# ─── Montar decks ──────────────────────────────────────────────
for c in sqlite_cards:
    decks['sqlite'].add_note(card(*c))
for c in manip_cards:
    decks['manip'].add_note(card(*c))
for c in design_cards:
    decks['design'].add_note(card(*c))
for c in css_cards:
    decks['css'].add_note(card(*c))
for c in workflow_cards:
    decks['workflow'].add_note(card(*c))


# ─── Exportar ──────────────────────────────────────────────────
output = Path(__file__).parent / 'Meta_Anki_Flashcards.apkg'
package = genanki.Package([d for d in decks.values()])
package.write_to_file(output)

total = (len(sqlite_cards) + len(manip_cards) + len(design_cards)
         + len(css_cards) + len(workflow_cards))

print(f"✅ Deck gerado: {output}")
print(f"   Total: {total} cards")
print()
print("Estrutura:")
for d in sorted(decks.values(), key=lambda x: x.name):
    count = len(d.notes)
    if count > 0:
        print(f"  {d.name}: {count} cards")
