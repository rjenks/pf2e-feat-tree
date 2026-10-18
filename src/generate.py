import json, math, re, collections, sys
from pathlib import Path
from pf2e_mcp.server.rules_tools import rules_sql
HERE = Path(__file__).resolve().parent.parent
DATA = HERE / 'data'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'dist' / 'feat_tree.html'
feats = rules_sql("select id,name,level,category,traits,rarity,description from entries where pack='feats'", limit=100000, max_cell=200000)['rows']
prs = json.load(open(DATA / "prereq_rows.json"))
meta = json.load(open(DATA / "meta.json"))
version = rules_sql("select value from meta where key='data_version'")['rows'][0]['value']
ancestries = {a['name'].lower() for a in meta['anc']}
classes = {c['class_slug'] for c in meta['cls']}
for f in feats: f['traits'] = json.loads(f['traits'] or '[]')
# Mythic Destiny dedications carry 'destiny' instead of 'archetype'/'dedication'; treat them as archetypes.
SHOWN = {}
for f in feats:
    if f['name'].endswith(' Dedication') and ('destiny' in f['traits'] or 'dedication' in f['traits']) and 'archetype' not in f['traits']:
        SHOWN[f['id']] = list(f['traits']); f['traits'] = [t for t in f['traits'] if t != 'dedication'] + ['archetype', 'dedication']
byname = collections.defaultdict(list)
for f in feats: byname[f['name'].lower()].append(f)
byid = {f['id']: f for f in feats}

def names_from(p):
    k, raw = p['kind'], p['raw_text']
    s = json.loads(p['structured']) if p['structured'] else {}
    out = []
    if k == 'named_reference': return [[s.get('name', raw)]]
    if k == 'compound_named':
        return [s['any_of']] if s.get('any_of') else [[x] for x in s.get('all_of', [])]
    if k == 'unresolved':
        return [[y.strip() for y in re.split(r'\bor\b', x)] for x in re.split(r',|;|\band\b', raw)]
    return []
def cands(n):
    n = re.sub(r'\s+in (?:that|the same|a|any) skill$', '', n.lower().strip())
    return byname.get(n) or byname.get(n + ' dedication') or []


def arch_all(f, seen=()):
    """Every archetype a feat can be taken through (a feat gated on 'A Dedication or B Dedication' belongs to both)."""
    if 'archetype' not in f['traits'] or f['id'] in seen: return []
    if 'dedication' in f['traits']: return [re.sub(r' Dedication$', '', f['name'])]
    out = []
    for pid in sorted(parents.get(f['id'], ())):
        for a in arch_all(byid[pid], seen + (f['id'],)):
            if a not in out: out.append(a)
    return out

_own = {}
def owner(f, seen=()):
    """Archetype a non-archetype feat belongs to because its prerequisites run through an archetype feat."""
    if f['id'] in _own: return _own[f['id']]
    if f['id'] in seen: return None
    res = None
    for pid in sorted(parents.get(f['id'], ())):
        pf = byid[pid]
        res = arch_all(pf) if 'archetype' in pf['traits'] else owner(pf, seen + (f['id'],))
        if res: break
    if parents_done: _own[f['id']] = res
    return res
parents_done = False

import html as _html
ex = {r['id']: r for r in rules_sql("select id, json_extract(raw_json,'$.system.actionType.value') at, json_extract(raw_json,'$.system.actions.value') ac, json_extract(raw_json,'$.system.prerequisites.value') pr, json_extract(raw_json,'$.system.rules') rl, source_book, is_remaster from entries where pack='feats'", limit=100000, max_cell=20000)['rows']}
def clean(h, level=None):
    h = h or ''
    if level is not None:  # resolve level-scaled dice such as ((2*floor(@actor.level/4))d4) at the feat's own level
        def scaled(m):
            try:
                n = eval(m.group(1).replace('@actor.level', str(level)), {'floor': math.floor, '__builtins__': {}})
                return f'@Damage[{n}d{m.group(2)}['
            except Exception: return m.group(0)
        h = re.sub(r'@Damage\[\(\(([\d*+/ ()a-z@.]*@actor\.level[\d*+/ ()a-z@.]*)\)d(\d+)\)\[', scaled, h)
    h = re.sub(r'@UUID\[[^\]]*\]\{([^}]*)\}', r'\1', h)
    h = re.sub(r'@UUID\[[^\]]*\]', '', h)
    def chk(m):
        if m.group(2): return m.group(2)
        kind = m.group(1).split('|')[0].replace('type:', '')
        dc = re.search(r'dc:(\w+)', m.group(1))
        return f"{kind.title()} check" + (f" (DC {dc.group(1)})" if dc else '')
    h = re.sub(r'@Check\[([^\]]*)\](?:\{([^}]*)\})?', chk, h)
    def dmg(m):
        if m.group(2): return m.group(2)
        return re.sub(r'\[(?!healing\])([^\]]*)\]', r' \1', re.sub(r'\[healing\]', '', m.group(1).split('|')[0])).strip()
    h = re.sub(r'@Damage\[((?:[^\[\]]|\[[^\]]*\])*)\](?:\{([^}]*)\})?', dmg, h)
    h = re.sub(r'\[\[/(?:br)?r ([^\]]*)\]\](?:\{([^}]*)\})?', lambda m: m.group(2) or m.group(1).split('#')[0].strip(), h)
    def tpl(m):
        d = dict(x.split(':', 1) for x in m.group(1).split('|') if ':' in x)
        return f"{d.get('distance', '')}-foot {d.get('type', 'area')}"
    h = re.sub(r'@Template\[([^\]]*)\](?:\{[^}]*\})?', tpl, h)
    h = re.sub(r'@\w+\[[^\]]*\]\{([^}]*)\}', r'\1', h)
    h = re.sub(r'@\w+\[[^\]]*\]', '', h)
    h = re.sub(r'<span class="action-glyph">([^<]*)</span>', lambda m: '\ue000' + m.group(1) + '\ue001', h)
    h = re.sub(r'</?(?:strong|b)>', lambda m: '\ue003' if m.group(0)[1] == '/' else '\ue002', h)
    h = re.sub(r'<hr\s*/?>', '', h)
    h = re.sub(r'</(p|h\d|div)>', '\n\n', h)
    h = re.sub(r'</(li|tr)>|<br\s*/?>', '\n', h)
    h = re.sub(r'<li[^>]*>', '• ', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = _html.unescape(h)
    h = re.sub(r'\n\s*\n\s*\n+', '\n\n', re.sub(r'[ \t]+', ' ', h))
    h = re.sub(r'\s*([])\s*', r'\1', h)  # nested-action blocks are laid out by the card, not by blank lines
    return re.sub(r'[^]*', lambda m: re.sub(r'\n\s*\n', '\n', m.group(0)), h).strip()
# A heading paragraph with an action glyph starts a nested action that runs to the end of the text; mark it as a block.
# If the same action is also granted (often just an @Embed stub here), drop this copy in favour of the full granted text.
def nest_actions(h, granted=''):
    def block(m):
        return '' if f'<strong>{m.group(2)}</strong>' in granted else '' + m.group(1) + ''
    return re.sub(r'(?:<hr\s*/?>\s*)?(<p>\s*<strong>([^<]+)</strong>\s*<span class="action-glyph">[^<]*</span>\s*</p>.*)', block, h or '', count=1, flags=re.S)
# Feats that grant an action only link to it; pull the action's own text in so the card shows what it does.
acts = {r['id']: r for r in rules_sql("select id,name,description,json_extract(raw_json,'$.system.actionType.value') at, json_extract(raw_json,'$.system.actions.value') ac from entries where pack in ('actions','adventure-specific-actions')", limit=100000, max_cell=200000)['rows']}
def granted_actions(f):
    try: rules = json.loads(ex.get(f['id'], {}).get('rl') or '[]')
    except Exception: return ''
    out = []
    for r in rules:
        m = re.fullmatch(r'Compendium\.pf2e\.(?:actionspf2e|adventure-specific-actions)\.Item\.(\w+)', r.get('uuid') or '') if r.get('key') == 'GrantItem' else None
        a = m and acts.get(m.group(1))
        if not a or a['name'] in (f.get('description') or '') and not a['description']: continue
        g = {'reaction': 'R', 'free': 'f'}.get(a['at']) or (a['ac'] if a['at'] == 'action' and str(a['ac']) in '123' else '')
        out.append(f"<p><strong>{a['name']}</strong>" + (f' <span class="action-glyph">{g}</span>' if g else '') + '</p>' + (a['description'] or '') + '')
    return ''.join(out)
def card(f):
    e = ex.get(f['id'], {})
    try: pr = '; '.join(x['value'] for x in json.loads(e.get('pr') or '[]'))
    except Exception: pr = ''
    at, ac = e.get('at'), e.get('ac')
    act = {'reaction': 'Reaction', 'free': 'Free action'}.get(at) or (f'{ac} action' + ('s' if ac and int(ac) > 1 else '') if at == 'action' and ac else '')
    glyph = {'reaction': 'R', 'free': 'f'}.get(at) or (str(ac) if at == 'action' and ac in (1, 2, 3, '1', '2', '3') else '')
    ga = granted_actions(f)
    return {'d': clean(nest_actions(f.get('description'), ga) + ga, f['level']), 't': SHOWN.get(f['id'], f['traits']), 'a': act, 'ag': glyph, 'p': pr, 's': e.get('source_book') or ''}
SKILLS = {'acrobatics','arcana','athletics','crafting','deception','diplomacy','intimidation','medicine','nature','occultism','performance','religion','society','stealth','survival','thievery'}
_own_skills = {}
for p in prs:
    s = json.loads(p['structured']) if p['structured'] else {}
    names = [s['skill']] if p['kind'] == 'skill_rank' and s.get('skill') else (s.get('skills') or [] if p['kind'] == 'skill_rank_any' else [])
    for n in names:
        n = n.lower().strip()
        k = n if n in SKILLS else ('lore' if 'lore' in n else None)
        if k: _own_skills.setdefault(p['id'], set()).add(k.title())
def skills_of(f, seen=()):
    if f['id'] in _own_skills: return sorted(_own_skills[f['id']])
    if f['id'] in seen: return []
    out = set()
    for pid in parents.get(f['id'], ()):
        out.update(skills_of(byid[pid], seen + (f['id'],)))
    return sorted(out)

def groups_of(f):
    t = f['traits']
    if 'archetype' in t:
        return [('Archetype', a) for a in (arch_all(f) or ['Unassigned archetype feats'])]
    o = owner(f)
    if o: return [('Archetype', a) for a in o]
    if f['category'] == 'skill':
        return [('Skill', s) for s in skills_of(f)] or [('Skill', 'No specific skill')]
    if f['category'] == 'ancestry':
        g = [('Ancestry', x.title()) for x in t if x in ancestries]
        return g or [('Ancestry', 'Versatile heritages & other')]
    if f['category'] in ('general', 'bonus'):
        return [('General', 'General feats' if f['category'] == 'general' else 'Bonus feats')]
    if f['category'] == 'class':
        g = [('Class', x.title()) for x in t if x in classes]
        return g or [('Class', 'Mythic & other')]
    return []


reqs = {}  # id -> list of alternative-groups (each a list of ids)
parents = collections.defaultdict(set)
def pick(cs, me):
    if len(cs) == 1: return cs[0]
    mg = set(groups_of(me))
    for c in cs:
        if mg & set(groups_of(c)): return c
    return cs[0]
for p in prs:
    me = byid.get(p['id'])
    if not me: continue
    for alts in names_from(p):
        ids = []
        for n in alts:
            cs = [c for c in cands(n) if c['id'] != me['id']]
            if cs:
                c = pick(cs, me)
                if c['id'] not in ids: ids.append(c['id'])
        if ids:
            reqs.setdefault(me['id'], []).append(ids)
            for i in ids: parents[me['id']].add(i)

# Skill-proficiency prerequisites become synthetic nodes ("Legendary in Athletics"), shown only on feats already in a graph.
RANKS = ('trained', 'expert', 'master', 'legendary')
skreqs = {}
def skill_token(tok):
    t = re.sub(r'^(?:at least one of|either|a|an)\s+', '', tok.strip().strip('.').lower()).strip()
    if t in SKILLS or t == 'perception': return t.title()
    t = t.replace(' skill', '')
    if t.endswith('lore'): return t.title()
    if 'lore' in t.split(): return 'Lore'
    return None
def synth(rank, skill):
    sid = f'skill:{rank}:{skill}'
    if sid not in byid:
        byid[sid] = {'id': sid, 'name': f'{rank.title()} in {skill}', 'level': 0, 'category': 'skillrank',
                     'traits': [], 'rarity': 'common', 'description': '', 'synthetic': True}
    return sid
for p in prs:
    if p['kind'] not in ('skill_rank', 'skill_rank_any') or p['id'] not in byid: continue
    m = re.match(r'\s*(trained|expert|master|legendary)\s+(?:in|at)\s+(.*)', p['raw_text'].replace('\n', ' '), re.I | re.S)
    if not m: continue
    rank = m.group(1).lower()
    for part in re.split(r'\band\b', m.group(2)):
        toks = [skill_token(x) for x in re.split(r',|\bor\b', part) if x.strip()]
        ids = [synth(rank, t) for t in toks if t]
        if ids and None not in toks:
            skreqs.setdefault(p['id'], []).append(ids)

# Attribute-modifier prerequisites ("Dexterity +2") on general and skill feats.
ATTRS = ('strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma')
for p in prs:
    if p['kind'] != 'ability_score' or p['id'] not in byid or byid[p['id']]['category'] not in ('general', 'bonus', 'skill'): continue
    ids = []
    for a, n in re.findall(r'(' + '|'.join(ATTRS) + r')\s*\+(\d)', p['raw_text'], re.I):
        sid = f'attr:{a.lower()}:{n}'
        byid.setdefault(sid, {'id': sid, 'name': f'{a.title()} +{n}', 'level': 0, 'category': 'skillrank',
                              'traits': [], 'rarity': 'common', 'description': '', 'synthetic': True})
        ids.append(sid)
    if ids: skreqs.setdefault(p['id'], []).append(ids)

# Ranks chain: expert needs trained, master needs expert, legendary needs master.
todo = [k for k in byid if k.startswith('skill:')]
while todo:
    sid = todo.pop()
    _, rank, sk = sid.split(':', 2)
    r = RANKS.index(rank)
    if r and sid not in skreqs:
        prev = synth(RANKS[r - 1], sk)
        skreqs[sid] = [[prev]]
        todo.append(prev)

def arch_of(f, seen=None):
    if 'archetype' not in f['traits']: return None
    if 'dedication' in f['traits']: return re.sub(r' Dedication$', '', f['name'])
    seen = seen or set()
    for pid in sorted(parents.get(f['id'], ())):
        if pid in seen: continue
        seen.add(pid)
        if 'archetype' in byid[pid]['traits']:
            a = arch_of(byid[pid], seen)
            if a: return a
    return None

parents_done = True
members = collections.defaultdict(set)
for f in feats:
    if f['id'] in reqs or (f['category'] in ('skill', 'general', 'bonus') and 'archetype' not in f['traits'] and f['id'] in skreqs):
        for gg in groups_of(f): members[gg].add(f['id'])
allmem = collections.defaultdict(set)
for f in feats:
    for gg in groups_of(f): allmem[gg].add(f['id'])
nodes = {}
def need(i):
    if i in nodes: return
    f = byid[i]
    nodes[i] = {'n': f['name'], 'l': f['level'], 'r': f['rarity'], 'q': [], 'c': card(f),
                'g': [f'{k}: {n}' for k, n in groups_of(f)]}
    if f.get('synthetic'): nodes[i]['s'] = 1
    elif ex.get(i, {}).get('is_remaster') == 0: nodes[i]['lg'] = 1  # pre-Remaster (legacy) content
    for alts in reqs.get(i, []) + skreqs.get(i, []):
        for a in alts: need(a)
    nodes[i]['q'] = reqs.get(i, []) + skreqs.get(i, [])
def closure_ids(tops):
    seen, st = set(), list(tops)
    while st:
        i = st.pop()
        if i in seen: continue
        seen.add(i)
        for alts in reqs.get(i, []): st.extend(alts)
    return seen
data = {'Class': {}, 'Ancestry': {}, 'Archetype': {}, 'Skill': {}, 'General': {}}
# Archetype feats that grant "a class feat": Basic X (levels 1-2) / Advanced X (any level)
access = collections.defaultdict(lambda: {'basic': [], 'adv': []})  # (class title, archetype) -> feat ids
for f in feats:
    if 'archetype' not in f['traits'] or 'dedication' in f['traits']: continue
    txt = re.sub(r'<[^>]+>', ' ', f.get('description') or '')[:400]
    m = re.search(r'You gain (?:a|an|one) (1st- or 2nd-level )?(\w+) feat\b', txt)
    if not m or m.group(2).lower() not in classes: continue
    a = arch_of(f)
    if a: access[(m.group(2).title(), a)]['basic' if m.group(1) else 'adv'].append(f['id'])
extra = {}  # (kind,name) -> {feat id: [[access ids]]}
for (kind, name) in sorted(set(members) | set(allmem), key=lambda x: x[1]):
    ids = members.get((kind, name), set())
    xedges = {}
    cls_ids = set()
    if kind == 'Archetype':
        for (cls, arch), acc in access.items():
            if arch != name or ('Class', cls) not in members: continue
            ctops = [i for i in members[('Class', cls)]]
            cls_ids = {i for i in closure_ids(ctops) if ('Class', cls) in groups_of(byid[i])}
            for i in cls_ids:
                if reqs.get(i): continue
                alts = (acc['basic'] + acc['adv']) if byid[i]['level'] <= 2 else acc['adv']
                if alts: xedges[i] = alts
    allids = set(ids) | set(xedges) | {i for i in cls_ids if any(p in xedges or p in cls_ids for p in [i])} if xedges else set(ids)
    if xedges:
        allids = set(ids) | cls_ids
        # only keep class feats that actually reach an access feat
        keep = set()
        def reach(i, seen=()):
            if i in keep: return True
            ok = i in xedges or any(reach(c, seen + (i,)) for al in reqs.get(i, []) for c in al if c in cls_ids and c not in seen)
            if ok: keep.add(i)
            return ok
        for i in cls_ids: reach(i)
        allids = set(ids) | keep
    required = {a for i in allids for alts in reqs.get(i, []) for a in alts} | {a for i in xedges if i in allids for a in xedges[i]}
    tops = sorted((i for i in allids if i not in required), key=lambda i: (-byid[i]['level'], byid[i]['name']))
    for i in tops: need(i)
    for i, al in xedges.items():
        if i in allids:
            need(i)
            for a in al: need(a)
    shown = closure_ids(tops) | allids | required
    solo = sorted((i for i in allmem[(kind, name)] if i not in shown), key=lambda i: (byid[i]['level'], byid[i]['name']))
    for i in solo: need(i)
    data[kind][name] = {'tops': tops, 'solo': solo, 'n': len(allids) + len(solo), 'mem': sorted(set(ids) | {i for i in closure_ids(tops) if (kind, name) in groups_of(byid[i])})}
    if xedges: data[kind][name]['x'] = {i: [al] for i, al in xedges.items() if i in allids}
print({k: len(v) for k, v in data.items()}, len(nodes))
font = rules_sql("select value from meta where key='actions_font_woff2_b64'", max_cell=500000)['rows'][0]['value']
# Licence notices: every page carries the OGL text and the ORC/Community Use attributions for the
# sourcebooks of the feats it actually shows, since the page embeds their rules text.
books = {'orc': set(), 'ogl': set()}
for r in rules_sql("select id, is_remaster, source_book from entries where pack='feats'", limit=100000)['rows']:
    if r['id'] in nodes and r['source_book']: books['orc' if r['is_remaster'] else 'ogl'].add(r['source_book'])
def booklist(s): return ', '.join(f'<em>{_html.escape(b)}</em>' for b in sorted(s)) or '&mdash;'
licenses = f"""<h4>Paizo Community Use Policy</h4>
<p>This page uses trademarks and/or copyrights owned by Paizo Inc., used under Paizo&rsquo;s Community Use Policy (paizo.com/licenses/communityuse). We are expressly prohibited from charging you to use or access this content. This page is not published, endorsed, or specifically approved by Paizo. For more information about Paizo Inc. and Paizo products, visit paizo.com.</p>
<h4>ORC License attribution notice</h4>
<p>This work includes material from {booklist(books['orc'])}, &copy; Paizo Inc., used under the ORC License. The ORC License is available at paizo.com/orclicense and is registered with the U.S. Copyright Office, Library of Congress, TX&nbsp;9-307-067.</p>
<h4>Open Game License content</h4>
<p>Rules text on this page drawn from {booklist(books['ogl'])} is Open Game Content, licensed under the Open Game License v1.0a, reproduced in full below. The diagrams, layout and code are not Open Game Content.</p>
<h4>Data and icons</h4>
<p>Rules data comes from the foundryvtt/pf2e project (github.com/foundryvtt/pf2e), release {version}. The action icons use the community-made Pathfinder2eActions font, created by Reddit user u/baughberick and distributed by foundryvtt/pf2e. Pathfinder is a trademark of Paizo Inc.; this is unofficial fan material. Diagrams are drawn by Mermaid (MIT) with the ELK layout engine, loaded from the jsDelivr CDN, so this page needs a network connection.</p>
<h4>Open Game License Version 1.0a</h4>
<div class="ogl">{(HERE / 'src' / 'ogl.html').read_text(encoding='utf-8')}</div>"""
html = open(HERE / "src" / "template.html").read().replace('__LICENSES__', licenses).replace('__FONT__', font).replace('__DATA__', json.dumps({'groups': data, 'nodes': nodes}, separators=(',', ':'))).replace('__VERSION__', version)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
