# Shell-Aliase für Claude Code

Zwei Aliase machen das Starten von Claude Code mit deinem CEO-GPT einfacher.

## Setup

Trag diese Zeilen in deine `~/.zshrc` ein (oder `~/.bashrc`):

```bash
alias cs='claude "/prime"'
alias cr='claude --dangerously-skip-permissions "/prime"'
```

Danach Shell neu laden: `source ~/.zshrc`

## Die Aliase

### `cs`: Claude Safe

```bash
alias cs='claude "/prime"'
```

Startet Claude Code und führt sofort `/prime` aus damit dein Mitarbeiter den CEO-GPT-Kontext lädt. Bei jedem Befehl, sensiblen Datei-Zugriff oder Änderung fragt dein Mitarbeiter erst nach.

**Wann nutzen:** Wenn du in einer neuen Session jede Aktion einzeln freigeben willst.

### `cr`: Claude Run

```bash
alias cr='claude --dangerously-skip-permissions "/prime"'
```

Startet Claude Code ohne Permission-Prompts und führt direkt `/prime` aus. Dein Mitarbeiter kann Befehle ausführen und Änderungen machen, ohne jedes Mal nachzufragen.

**Wann nutzen:** Wenn du dem Task vertraust, schnell iterieren willst, oder Routinearbeit machst bei der ständiges Bestätigen nervt.

## Warum beide?

- **`cs`** gibt dir Kontrolle: gut für unbekannte Aufgaben, sensible Operationen, oder wenn du sehen willst was dein Mitarbeiter macht
- **`cr`** gibt dir Tempo: gut für vertraute Workflows wo du deinem Mitarbeiter autonomes Arbeiten zutraust

Beide Aliase laufen `/prime` automatisch, damit dein Mitarbeiter jede Session voll orientiert startet.
