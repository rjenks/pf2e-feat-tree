# Notice

This file covers licensing for third-party content this project *uses* and
that its generated output *contains*, as distinct from `LICENSE` (Apache
2.0), which covers this project's own original source code
(`src/generate.py`, `src/fetch_data.py`, `src/template.html`, and the
documentation).

## What's in this repository

This repository stores **no Pathfinder 2nd Edition game data, rules text,
or artwork**. `data/` and `dist/` are git-ignored build products. The source
contains only Pathfinder vocabulary needed to do its job: skill and rank
names, class and archetype names, and a few regular expressions that match
the phrasing of feat descriptions (for example "You gain a ... feat").

## What the generated page contains

`dist/feat_tree.html` is a **redistribution of Pathfinder content**, unlike
the source in this repository. Running the build embeds in that single file:

- Feat names, levels, rarity, traits, action costs, prerequisites, source
  book titles, and the full **description text** of every feat shown.
- The community-made **`Pathfinder2eActions`** icon font
  (`pathfinder-2e-actions.woff2`), base64-encoded. It was created by Reddit
  user **u/baughberick** (https://www.reddit.com/user/baughberick/) and is
  distributed by the `foundryvtt/pf2e` project for community use.

To satisfy the licenses below, every generated page carries them itself:
the footer's **Licenses & attribution** button opens a dialog with the Paizo
Community Use Policy notice, the ORC attribution notice and OGL notice
naming the sourcebooks of the feats actually shown (split by each feat's
`is_remaster` flag), the data and icon-font credits, and the full OGL 1.0a
text including its Section 15 copyright notice. `src/generate.py` builds
that section and `src/ogl.html` holds the OGL text (taken from pf2e-mcp's
character sheet renderer). The full ORC License text is not reproduced; the
page gives its Library of Congress registration and paizo.com/orclicense.

## Where the data comes from

The data is read from the **pf2e-mcp** package
(https://pypi.org/project/pf2e-mcp/), which downloads it at build time from
the public **foundryvtt/pf2e** project (https://github.com/foundryvtt/pf2e),
maintained by the PF2E for Foundry VTT volunteer development team and
published under Foundry Gaming LLC's license arrangement with Paizo Inc. The
`foundryvtt/pf2e` release the page was built from is stated in its footer.
See pf2e-mcp's own `NOTICE.md` for how it handles that data.

## Licensing of the underlying game content

Paizo Inc. licenses the content under two licenses, depending on the
sourcebook:

- **Open Game License Version 1.0a ("OGL")** -- legacy Pathfinder 2nd
  Edition content (Core Rulebook through 2022-era books). Full text below.
- **ORC License** -- Pathfinder 2nd Edition Remaster content (Player Core,
  GM Core, and everything from late 2023 onward). Registered at the U.S.
  Copyright Office, TX 9-307-067.

Both licenses require a running list of every sourcebook whose content is
included. These lists are hundreds of entries long and change with every
Paizo release, so a frozen copy here would go stale. The live lists are:

- OGL Copyright Notice: https://github.com/foundryvtt/pf2e/blob/master/static/licenses/OpenGameLicense.md
- ORC Attribution Notice: https://github.com/foundryvtt/pf2e/blob/master/static/licenses/ORCLicense.md

### Open Game License Version 1.0a -- full text

The following text is the property of Wizards of the Coast, Inc. and is
Copyright 2000 Wizards of the Coast, Inc. ("Wizards"). All Rights Reserved.

1. **Definitions:** (a)"Contributors" means the copyright and/or trademark
   owners who have contributed Open Game Content; (b)"Derivative Material"
   means copyrighted material including derivative works and translations
   (including into other computer languages), potation, modification,
   correction, addition, extension, upgrade, improvement, compilation,
   abridgment or other form in which an existing work may be recast,
   transformed or adapted; (c) "Distribute" means to reproduce, license,
   rent, lease, sell, broadcast, publicly display, transmit or otherwise
   distribute; (d)"Open Game Content" means the game mechanic and includes
   the methods, procedures, processes and routines to the extent such
   content does not embody the Product Identity and is an enhancement over
   the prior art and any additional content clearly identified as Open
   Game Content by the Contributor, and means any work covered by this
   License, including translations and derivative works under copyright
   law, but specifically excludes Product Identity. (e) "Product Identity"
   means product and product line names, logos and identifying marks
   including trade dress; artifacts; creatures characters; stories,
   storylines, plots, thematic elements, dialogue, incidents, language,
   artwork, symbols, designs, depictions, likenesses, formats, poses,
   concepts, themes and graphic, photographic and other visual or audio
   representations; names and descriptions of characters, spells,
   enchantments, personalities, teams, personas, likenesses and special
   abilities; places, locations, environments, creatures, equipment,
   magical or supernatural abilities or effects, logos, symbols, or
   graphic designs; and any other trademark or registered trademark
   clearly identified as Product identity by the owner of the Product
   Identity, and which specifically excludes the Open Game Content; (f)
   "Trademark" means the logos, names, mark, sign, motto, designs that are
   used by a Contributor to identify itself or its products or the
   associated products contributed to the Open Game License by the
   Contributor (g) "Use", "Used" or "Using" means to use, Distribute,
   copy, edit, format, modify, translate and otherwise create Derivative
   Material of Open Game Content. (h) "You" or "Your" means the licensee
   in terms of this agreement.
2. **The License:** This License applies to any Open Game Content that
   contains a notice indicating that the Open Game Content may only be
   Used under and in terms of this License. You must affix such a notice
   to any Open Game Content that you Use. No terms may be added to or
   subtracted from this License except as described by the License
   itself. No other terms or conditions may be applied to any Open Game
   Content distributed using this License.
3. **Offer and Acceptance:** By Using the Open Game Content You indicate
   Your acceptance of the terms of this License.
4. **Grant and Consideration:** In consideration for agreeing to use this
   License, the Contributors grant You a perpetual, worldwide,
   royalty-free, non-exclusive license with the exact terms of this
   License to Use, the Open Game Content.
5. **Representation of Authority to Contribute:** If You are contributing
   original material as Open Game Content, You represent that Your
   Contributions are Your original creation and/or You have sufficient
   rights to grant the rights conveyed by this License.
6. **Notice of License Copyright:** You must update the COPYRIGHT NOTICE
   portion of this License to include the exact text of the COPYRIGHT
   NOTICE of any Open Game Content You are copying, modifying or
   distributing, and You must add the title, the copyright date, and the
   copyright holder's name to the COPYRIGHT NOTICE of any original Open
   Game Content you Distribute.
7. **Use of Product Identity:** You agree not to Use any Product Identity,
   including as an indication as to compatibility, except as expressly
   licensed in another, independent Agreement with the owner of each
   element of that Product Identity. You agree not to indicate
   compatibility or co-adaptability with any Trademark or Registered
   Trademark in conjunction with a work containing Open Game Content
   except as expressly licensed in another, independent Agreement with
   the owner of such Trademark or Registered Trademark. The use of any
   Product Identity in Open Game Content does not constitute a challenge
   to the ownership of that Product Identity. The owner of any Product
   Identity used in Open Game Content shall retain all rights, title and
   interest in and to that Product Identity.
8. **Identification:** If you distribute Open Game Content You must
   clearly indicate which portions of the work that you are distributing
   are Open Game Content.
9. **Updating the License:** Wizards or its designated Agents may publish
   updated versions of this License. You may use any authorized version
   of this License to copy, modify and distribute any Open Game Content
   originally distributed under any version of this License.
10. **Copy of this License:** You MUST include a copy of this License
    with every copy of the Open Game Content You Distribute.
11. **Use of Contributor Credits:** You may not market or advertise the
    Open Game Content using the name of any Contributor unless You have
    written permission from the Contributor to do so.
12. **Inability to Comply:** If it is impossible for You to comply with
    any of the terms of this License with respect to some or all of the
    Open Game Content due to statute, judicial order, or governmental
    regulation then You may not Use any Open Game Material so affected.
13. **Termination:** This License will terminate automatically if You
    fail to comply with all terms herein and fail to cure such breach
    within 30 days of becoming aware of the breach. All sublicenses shall
    survive the termination of this License.
14. **Reformation:** If any provision of this License is held to be
    unenforceable, such provision shall be reformed only to the extent
    necessary to make it enforceable.
15. **COPYRIGHT NOTICE:** Open Game License v 1.0 Copyright 2000, Wizards
    of the Coast, Inc. The full, current per-sourcebook copyright notice
    (which titles' content is included) is maintained live by
    `foundryvtt/pf2e` -- see "Where the attribution lists live" above
    rather than a snapshot here.

### ORC License -- summary

The ORC License's own Section 1 notice, as reproduced in `foundryvtt/pf2e`:
"This product is licensed under the ORC License located at the Library of
Congress at TX 9-307-067 and available online at various locations. All
warranties are disclaimed as set forth therein."

Its Section 3 ("Reserved Material") is the direct source for the next
section below -- it explicitly carves out "all trademarks, registered
trademarks, proper nouns (characters, deities, locations, etc.[...]),
artworks, characters, dialogue, locations, organizations, plots,
storylines, and trade dress" from the license's open grant.

## Content not covered by an open license

Both licenses exclude a category of content (OGL "Product Identity", ORC
"Reserved Material"): proper nouns, named characters and locations, artwork,
and narrative content. `foundryvtt/pf2e` includes that material under
Foundry Gaming LLC's own arrangement with Paizo Inc., which does not
automatically extend to third parties. Feat descriptions are mostly
mechanical text, but this project does not separate out any Product
Identity/Reserved Material that appears in them. This is disclosed rather
than resolved; it is not a legal conclusion.

## Trademark disclaimer

**Pathfinder** and associated marks are trademarks of **Paizo Inc.** This
project is not affiliated with, endorsed by, or sponsored by **Paizo Inc.**
Its use of those marks is solely to describe the subject matter of this
software.

## Third-party libraries loaded at view time

The generated page loads **Mermaid** (MIT) and **@mermaid-js/layout-elk**
(MIT) from the jsDelivr CDN. They are not bundled in the file.
