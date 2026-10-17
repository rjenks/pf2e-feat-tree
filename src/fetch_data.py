import json
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / 'data'
DATA.mkdir(exist_ok=True)
from pf2e_mcp.server.rules_tools import rules_sql
r = rules_sql("select e.id,e.name,e.slug,e.level,e.category,e.traits,e.rarity,p.kind,p.raw_text,p.structured from entries e join prerequisites p on p.entry_id=e.id where e.pack='feats'", limit=100000, max_cell=3000)
print(r['row_count'], r['truncated'], r.get('truncated_cells')[:2] if r.get('truncated_cells') else None)
json.dump(r['rows'], open(DATA / 'prereq_rows.json','w'))
a = rules_sql("select name, slug from entries where pack='ancestries'", limit=1000)
c = rules_sql("select class_slug from class_progression", limit=1000)
json.dump({'anc':a['rows'],'cls':c['rows']}, open(DATA / 'meta.json','w'))
