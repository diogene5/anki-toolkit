#!/usr/bin/env python3
"""
🧹 limpar_colecao.py — Remove note types e decks sem uso

⚠️  IMPORTANTE: Feche o Anki antes de rodar este script!
O Anki bloqueia o banco de dados enquanto está aberto.
Se tentar modificar com o Anki aberto, pode corromper seus dados.

COMO FUNCIONA:
──────────────
1. Cria backup automático antes de qualquer modificação
2. Lista note types e decks sem uso
3. Pede confirmação antes de deletar (modo interativo)
4. Remove com --auto para pular confirmações

O QUE É SAFE DELETAR:
  ✅ Note types com 0 notas → são modelos órfãos de add-ons removidos
  ✅ Decks vazios (0 cards) → poluem a interface sem motivo
  ❌ NUNCA deletar note types em uso → perderia notas!

USO:
  python3 limpar_colecao.py                    # modo interativo (pede confirmação)
  python3 limpar_colecao.py --auto             # remove tudo sem perguntar
  python3 limpar_colecao.py --perfil Principal # limpar outro perfil
  python3 limpar_colecao.py --dry-run          # mostra o que faria sem fazer
"""

import sqlite3
import shutil
import os
import argparse
from datetime import datetime

# Funções de acesso ao banco Anki centralizadas em shared.py
from shared import unicase_collation, conectar


def fazer_backup(perfil: str) -> str:
    """
    Cria cópia do banco antes de modificar.

    Esta é a regra #1 ao manipular dados do Anki:
    SEMPRE faça backup antes de qualquer alteração no SQLite.
    Se algo der errado, basta copiar o backup de volta.
    """
    base = os.path.expanduser("~/Library/Application Support/Anki2")
    src = os.path.join(base, perfil, "collection.anki2")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Salvar no diretório do projeto
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    dst = os.path.join(backup_dir, f"{perfil}_{timestamp}.anki2")

    shutil.copy2(src, dst)
    print(f"💾 Backup: {dst}")
    return dst


def listar_notetypes_orfaos(conn: sqlite3.Connection) -> list[tuple[int, str]]:
    """
    Encontra note types sem nenhuma nota associada.

    Note types com "+" no nome (ex: "Basic+", "Cloze+") geralmente
    foram criados por add-ons que duplicam o modelo original para
    adicionar campos extras. Quando o add-on é removido, o note type
    órfão permanece.
    """
    return conn.execute("""
        SELECT nt.id, nt.name
        FROM notetypes nt
        LEFT JOIN notes n ON n.mid = nt.id
        GROUP BY nt.id
        HAVING COUNT(n.id) = 0
    """).fetchall()


def listar_decks_vazios(conn: sqlite3.Connection) -> list[tuple[int, str]]:
    """
    Encontra decks sem nenhum card.

    No Anki, decks são hierárquicos: "Python::EDA" é um sub-deck.
    O separador no banco é '^_' (que o Anki exibe como '::' na UI).
    Decks vazios acontecem quando:
    - Você cria um deck mas nunca adiciona cards
    - Todos os cards foram movidos para outro deck
    - Um deck pai existe só para agrupar sub-decks
    """
    return conn.execute("""
        SELECT d.id, d.name
        FROM decks d
        LEFT JOIN cards c ON c.did = d.id
        WHERE c.id IS NULL AND d.id != 1
    """).fetchall()


def remover_notetypes(conn: sqlite3.Connection, ids: list[int], dry_run: bool = False) -> int:
    """
    Remove note types pelo ID.

    O Anki armazena a estrutura de cada note type em 3 tabelas:
      - notetypes: metadados (nome, config)
      - fields: campos do note type (Frente, Verso, etc.)
      - templates: templates de card (HTML frente/verso)

    Precisamos limpar as 3 tabelas para remoção completa.
    """
    count = 0
    for ntid in ids:
        name = conn.execute("SELECT name FROM notetypes WHERE id=?", (ntid,)).fetchone()
        if name:
            if dry_run:
                print(f"  [DRY RUN] Removeria: {name[0]} (id: {ntid})")
            else:
                conn.execute("DELETE FROM templates WHERE ntid=?", (ntid,))
                conn.execute("DELETE FROM fields WHERE ntid=?", (ntid,))
                conn.execute("DELETE FROM notetypes WHERE id=?", (ntid,))
                print(f"  ✅ Removido: {name[0]}")
            count += 1
    return count


def remover_decks(conn: sqlite3.Connection, ids: list[int], dry_run: bool = False) -> int:
    """Remove decks vazios pelo ID."""
    count = 0
    for did in ids:
        name = conn.execute("SELECT name FROM decks WHERE id=?", (did,)).fetchone()
        if name:
            if dry_run:
                print(f"  [DRY RUN] Removeria deck: {name[0]}")
            else:
                conn.execute("DELETE FROM decks WHERE id=?", (did,))
                print(f"  ✅ Removido deck: {name[0]}")
            count += 1
    return count


def limpar(perfil: str = "Data", auto: bool = False, dry_run: bool = False) -> None:
    """Executa a limpeza completa."""
    print(f"\n🧹 Limpeza — Perfil: {perfil}")
    print(f"{'─' * 50}")

    import subprocess
    result = subprocess.run(["pgrep", "-x", "Anki"], capture_output=True)
    if result.returncode == 0:
        print("⚠️  O Anki está aberto! Feche-o antes de modificar o banco.")
        if not auto:
            return
        print("  --auto forçando continuação...")

    if not dry_run:
        fazer_backup(perfil)

    conn = conectar(perfil)

    # Note types órfãos
    orfaos = listar_notetypes_orfaos(conn)
    print(f"\n📋 Note types sem uso: {len(orfaos)}")
    for _, name in orfaos:
        print(f"  • {name}")

    if orfaos and (auto or dry_run or input("\nRemover note types? [s/N] ").lower() == 's'):
        removed = remover_notetypes(conn, [r[0] for r in orfaos], dry_run)
        print(f"  → {removed} removidos")

    # Decks vazios
    vazios = listar_decks_vazios(conn)
    print(f"\n📁 Decks vazios: {len(vazios)}")
    for _, name in vazios:
        print(f"  • {name}")

    if vazios and (auto or dry_run or input("\nRemover decks vazios? [s/N] ").lower() == 's'):
        removed = remover_decks(conn, [r[0] for r in vazios], dry_run)
        print(f"  → {removed} removidos")

    if not dry_run:
        conn.commit()
        print("\n✅ Alterações salvas.")
    else:
        print("\n⚠️  Modo dry-run — nada foi alterado.")

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Limpar coleção Anki")
    parser.add_argument("--perfil", default="Data", help="Nome do perfil")
    parser.add_argument("--auto", action="store_true", help="Remover sem pedir confirmação")
    parser.add_argument("--dry-run", action="store_true", help="Simular sem alterar")
    args = parser.parse_args()

    limpar(perfil=args.perfil, auto=args.auto, dry_run=args.dry_run)
