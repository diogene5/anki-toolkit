#!/usr/bin/env python3
"""
📊 analisar_colecao.py — Analisa uma coleção Anki e gera relatório

COMO O ANKI ARMAZENA DADOS:
─────────────────────────────
O Anki usa SQLite, um banco de dados leve que fica em um único arquivo.
O arquivo principal é `collection.anki2` dentro da pasta do perfil.

Tabelas principais:
  - notes   → o conteúdo (campos de texto, tags)
  - cards   → instâncias de estudo (scheduling, estado, intervalo)
  - decks   → os baralhos
  - notetypes → modelos de nota (Basic, Cloze, etc.)
  - revlog  → log de TODAS as revisões já feitas

Uma NOTA pode gerar múltiplos CARDS. Ex: uma nota "Basic (and reversed)"
gera 2 cards (frente→verso e verso→frente).

CAMPOS NA TABELA notes:
  - flds: todos os campos concatenados com \x1f (ASCII 31, "unit separator")
  - sfld: "sort field" — primeiro campo, usado para ordenação
  - tags: tags separadas por espaço, com espaço no início e fim
  - mid: ID do note type (modelo)

CAMPOS NA TABELA cards:
  - type: 0=new, 1=learning, 2=review, 3=relearning
  - queue: fila de revisão (similar a type, mas inclui suspended=-1, buried=-2)
  - ivl: intervalo atual em dias (negativo = segundos para learning)
  - factor: ease factor × 10 (ex: 2500 = 250% = "normal")
  - lapses: quantas vezes errou depois de aprender
  - reps: total de revisões

USO:
  python3 analisar_colecao.py                    # analisa perfil Data
  python3 analisar_colecao.py --perfil Principal  # analisa outro perfil
  python3 analisar_colecao.py --exportar          # exporta JSON com todas as notas
"""

import sqlite3
import json
import os
import argparse
from datetime import datetime
from pathlib import Path


# ─── Configuração ─────────────────────────────────────────────

# O Anki registra uma "collation" customizada chamada 'unicase' para
# comparações case-insensitive. O sqlite3 do Python não a conhece,
# então precisamos registrar uma versão equivalente.
# Sem isso, qualquer query com ORDER BY em colunas de texto falha.
def unicase_collation(a: str, b: str) -> int:
    """Collation case-insensitive compatível com Anki."""
    a, b = a.lower(), b.lower()
    return (a > b) - (a < b)  # retorna -1, 0 ou 1


def get_anki_path(perfil: str = "Data") -> str:
    """
    Retorna o caminho para o banco de dados do Anki.

    No macOS, os dados ficam em:
      ~/Library/Application Support/Anki2/<perfil>/collection.anki2

    Cada perfil é um diretório separado com seu próprio banco.
    """
    base = os.path.expanduser("~/Library/Application Support/Anki2")
    db_path = os.path.join(base, perfil, "collection.anki2")
    if not os.path.exists(db_path):
        # Listar perfis disponíveis para ajudar o usuário
        perfis = [d for d in os.listdir(base)
                  if os.path.isdir(os.path.join(base, d))
                  and not d.startswith('.')
                  and d not in ('addons21', 'logs')]
        raise FileNotFoundError(
            f"Perfil '{perfil}' não encontrado.\n"
            f"Perfis disponíveis: {', '.join(perfis)}\n"
            f"Caminho esperado: {db_path}"
        )
    return db_path


def conectar(perfil: str = "Data") -> sqlite3.Connection:
    """Abre conexão com o banco do Anki, registrando a collation necessária."""
    conn = sqlite3.connect(get_anki_path(perfil))
    conn.create_collation("unicase", unicase_collation)
    return conn


# ─── Análise ──────────────────────────────────────────────────

def analisar_decks(conn: sqlite3.Connection) -> list[dict]:
    """
    Analisa todos os decks: contagem de cards por estado, ease médio, etc.

    O campo 'type' do card indica seu estado no algoritmo SRS:
      0 = new   → nunca foi estudado
      1 = learning → em fase de aprendizado (intervalos curtos)
      2 = review → aprendido, em revisão espaçada
      3 = relearning → errou e voltou para aprendizado
    """
    decks = []
    for did, name in conn.execute("SELECT id, name FROM decks ORDER BY name"):
        row = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN type=0 THEN 1 ELSE 0 END) as new,
                SUM(CASE WHEN type=1 THEN 1 ELSE 0 END) as learning,
                SUM(CASE WHEN type=2 THEN 1 ELSE 0 END) as review,
                SUM(CASE WHEN type=3 THEN 1 ELSE 0 END) as relearning,
                ROUND(AVG(CASE WHEN factor > 0 THEN factor/10.0 END), 1) as avg_ease,
                SUM(lapses) as total_lapses,
                MAX(ivl) as max_interval
            FROM cards WHERE did=?
        """, (did,)).fetchone()

        decks.append({
            'id': did,
            'name': name,
            'total': row[0] or 0,
            'new': row[1] or 0,
            'learning': row[2] or 0,
            'review': row[3] or 0,
            'relearning': row[4] or 0,
            'avg_ease': row[5],
            'total_lapses': row[6] or 0,
            'max_interval_days': row[7] or 0,
        })
    return decks


def analisar_notetypes(conn: sqlite3.Connection) -> list[dict]:
    """Lista note types com contagem de uso."""
    return [
        {'id': r[0], 'name': r[1], 'count': r[2]}
        for r in conn.execute("""
            SELECT nt.id, nt.name, COUNT(n.id)
            FROM notetypes nt LEFT JOIN notes n ON n.mid=nt.id
            GROUP BY nt.id ORDER BY COUNT(n.id) DESC
        """)
    ]


def analisar_tags(conn: sqlite3.Connection) -> list[str]:
    """
    Extrai todas as tags únicas.

    No Anki, tags são armazenadas como string no campo 'tags' da nota,
    com espaços no início e fim: " tag1 tag2 tag3 "
    Isso permite buscar com LIKE " tag1 " de forma simples.
    """
    tags = set()
    for (raw_tags,) in conn.execute("SELECT tags FROM notes WHERE tags != ''"):
        for tag in raw_tags.strip().split():
            tags.add(tag)
    return sorted(tags)


def analisar_revisoes(conn: sqlite3.Connection) -> dict:
    """
    Analisa o histórico de revisões.

    A tabela revlog registra CADA revisão:
      - id: timestamp em milissegundos (serve como ID único E data)
      - cid: card ID
      - ease: botão pressionado (1=again, 2=hard, 3=good, 4=easy)
      - ivl: novo intervalo após a revisão
      - time: tempo gasto respondendo (milissegundos)
    """
    total = conn.execute("SELECT COUNT(*) FROM revlog").fetchone()[0]
    last = conn.execute("SELECT date(MAX(id)/1000, 'unixepoch') FROM revlog").fetchone()[0]

    # Revisões por mês
    meses = conn.execute("""
        SELECT strftime('%Y-%m', id/1000, 'unixepoch') as mes, COUNT(*)
        FROM revlog GROUP BY mes ORDER BY mes DESC LIMIT 12
    """).fetchall()

    # Tempo médio por card
    avg_time = conn.execute(
        "SELECT ROUND(AVG(time)/1000.0, 1) FROM revlog WHERE time > 0"
    ).fetchone()[0]

    # Distribuição de botões (quão bem você está respondendo)
    botoes = conn.execute("""
        SELECT ease, COUNT(*), ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM revlog), 1)
        FROM revlog GROUP BY ease ORDER BY ease
    """).fetchall()

    return {
        'total': total,
        'ultima_revisao': last,
        'meses': [{'mes': m, 'revisoes': c} for m, c in meses],
        'tempo_medio_segundos': avg_time,
        'botoes': [
            {'botao': e, 'nome': {1:'Again', 2:'Hard', 3:'Good', 4:'Easy'}.get(e, '?'),
             'count': c, 'pct': p}
            for e, c, p in botoes
        ],
    }


def exportar_notas(conn: sqlite3.Connection) -> list[dict]:
    """
    Exporta todas as notas com dados completos.

    O separador \x1f (chr(31), "unit separator") é um caractere ASCII
    especial que o Anki usa para separar campos dentro da coluna 'flds'.
    É invisível em editores de texto comuns, mas split('\x1f') funciona.
    """
    notas = []
    for row in conn.execute("""
        SELECT n.id, n.flds, n.tags, n.sfld, d.name, c.type, c.ivl,
               c.factor, c.lapses, c.reps, nt.name
        FROM notes n
        JOIN cards c ON c.nid = n.id
        JOIN decks d ON c.did = d.id
        JOIN notetypes nt ON n.mid = nt.id
        ORDER BY d.name, n.id
    """):
        nid, flds, tags, sfld, deck, ctype, ivl, factor, lapses, reps, notetype = row
        campos = flds.split('\x1f')

        notas.append({
            'id': nid,
            'deck': deck,
            'notetype': notetype,
            'campos': campos,
            'sfld': sfld,
            'tags': tags.strip(),
            'estado': {0:'new', 1:'learning', 2:'review', 3:'relearning'}.get(ctype, '?'),
            'intervalo_dias': ivl,
            'ease_pct': factor / 10 if factor > 0 else 0,
            'erros': lapses,
            'revisoes': reps,
        })
    return notas


# ─── Relatório ────────────────────────────────────────────────

def gerar_relatorio(perfil: str = "Data", exportar: bool = False) -> None:
    """Gera relatório completo da coleção."""
    conn = conectar(perfil)

    decks = analisar_decks(conn)
    notetypes = analisar_notetypes(conn)
    tags = analisar_tags(conn)
    revisoes = analisar_revisoes(conn)

    print(f"\n{'=' * 60}")
    print(f"  RELATÓRIO — Perfil: {perfil}")
    print(f"  Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 60}")

    # Decks
    total_cards = sum(d['total'] for d in decks)
    decks_ativos = [d for d in decks if d['total'] > 0]
    decks_vazios = [d for d in decks if d['total'] == 0]

    print(f"\n📁 DECKS ({len(decks_ativos)} ativos, {len(decks_vazios)} vazios, {total_cards} cards)")
    print(f"{'─' * 60}")
    for d in decks_ativos:
        ease_str = f"ease={d['avg_ease']}%" if d['avg_ease'] else "ease=—"
        print(f"  {d['name']}")
        print(f"    {d['total']} cards: new={d['new']} learn={d['learning']} review={d['review']} | {ease_str} | lapses={d['total_lapses']} | max_ivl={d['max_interval_days']}d")

    if decks_vazios:
        print(f"\n  ⚠️  Decks vazios: {', '.join(d['name'] for d in decks_vazios)}")

    # Note types
    usados = [nt for nt in notetypes if nt['count'] > 0]
    nao_usados = [nt for nt in notetypes if nt['count'] == 0]
    print(f"\n📋 NOTE TYPES ({len(usados)} em uso, {len(nao_usados)} sem uso)")
    print(f"{'─' * 60}")
    for nt in usados:
        print(f"  ✅ {nt['name']}: {nt['count']} notas")
    for nt in nao_usados:
        print(f"  ❌ {nt['name']}: SEM USO (pode ser removido)")

    # Revisões
    print(f"\n📊 REVISÕES")
    print(f"{'─' * 60}")
    print(f"  Total: {revisoes['total']} revisões")
    print(f"  Última: {revisoes['ultima_revisao']}")
    print(f"  Tempo médio/card: {revisoes['tempo_medio_segundos']}s")
    print(f"\n  Distribuição de respostas:")
    for b in revisoes['botoes']:
        bar = '█' * int(b['pct'] / 2)
        print(f"    {b['nome']:6s} {b['count']:4d} ({b['pct']:5.1f}%) {bar}")
    print(f"\n  Revisões por mês:")
    for m in revisoes['meses']:
        bar = '█' * (m['revisoes'] // 5)
        print(f"    {m['mes']}: {m['revisoes']:4d} {bar}")

    # Tags
    print(f"\n🏷️  TAGS ({len(tags)} únicas)")
    print(f"{'─' * 60}")
    # Filtrar tags "limpas" vs "sujas" (tags com caracteres estranhos)
    limpas = [t for t in tags if t.isalnum() or '/' in t or '::' in t or '_' in t]
    sujas = [t for t in tags if t not in limpas]
    print(f"  Tags válidas ({len(limpas)}): {', '.join(limpas[:30])}")
    if sujas:
        print(f"  ⚠️  Tags inválidas ({len(sujas)}): provavelmente dados que vazaram para campo de tags")

    # Problemas detectados
    print(f"\n🔍 PROBLEMAS DETECTADOS")
    print(f"{'─' * 60}")

    problems = []
    if decks_vazios:
        problems.append(f"  • {len(decks_vazios)} decks vazios (poluem a interface)")
    if nao_usados:
        problems.append(f"  • {len(nao_usados)} note types sem uso (podem ser removidos)")
    if sujas:
        problems.append(f"  • {len(sujas)} tags inválidas (dados vazaram para campo de tags)")

    # Overlap de decks
    sobrepostos = []
    nomes = [d['name'] for d in decks_ativos]
    if any('terminal' in n.lower() for n in nomes) and any('shell' in n.lower() or 'bash' in n.lower() for n in nomes):
        sobrepostos.append("terminal + Shell/Bash/Script + arquivos terminal")
    if any('python' in n.lower() for n in nomes) and any('eda' in n.lower() for n in nomes):
        sobrepostos.append("Python + Python EDA template")
    if sobrepostos:
        problems.append(f"  • Decks com sobreposição de conteúdo: {'; '.join(sobrepostos)}")

    for p in problems or ["  ✅ Nenhum problema crítico"]:
        print(p)

    # Exportar JSON
    if exportar:
        notas = exportar_notas(conn)
        output = Path(__file__).parent.parent / "dados" / f"notas_{perfil.lower()}.json"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump({
                'perfil': perfil,
                'gerado_em': datetime.now().isoformat(),
                'decks': decks,
                'notetypes': notetypes,
                'tags': limpas,
                'revisoes': revisoes,
                'notas': notas,
            }, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Exportado: {output}")

    conn.close()


# ─── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisar coleção Anki")
    parser.add_argument("--perfil", default="Data", help="Nome do perfil (default: Data)")
    parser.add_argument("--exportar", action="store_true", help="Exportar notas para JSON")
    args = parser.parse_args()

    gerar_relatorio(perfil=args.perfil, exportar=args.exportar)
