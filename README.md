# pf2e-feat-tree

Generates a single self-contained HTML page of Pathfinder 2e feat prerequisite
diagrams (Class, Ancestry, Archetype, Skill and General tabs) from the data in
the sibling [pf2e-mcp](../pf2e-mcp) project. Diagrams are drawn by Mermaid
(ELK layout) loaded from a CDN, so the page needs a network connection.

```bash
uv sync
uv run python src/fetch_data.py     # prerequisite rows + class/ancestry lists -> data/
uv run python src/generate.py       # -> dist/feat_tree.html (or pass an output path)
```

- `src/generate.py` builds groups, dependency links and feat cards and fills the template.
- `src/template.html` is the page (CSS + script); `__DATA__`, `__FONT__` and `__VERSION__` are substituted.
- Deep links use the URL hash: `#Class/Wizard`, `#Skill/Arcana/recognize`.

Rules text comes from the foundryvtt/pf2e data. Pathfinder is a trademark of
Paizo Inc.; this is unofficial fan material.

Source code is Apache-2.0 (`LICENSE`). The generated page embeds Paizo's
OGL/ORC-licensed rules text; the page itself carries the required notices (footer button),
and `NOTICE.md` explains them.
