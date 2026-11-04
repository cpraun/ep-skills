# Claim conventions (EN → DE)

Part of the `translate-en-de` skill. Read this file whenever the source contains claims.

## Claim phraseology

Use the established German claim phraseology. These are defaults; a binding glossary or the user's answer in Step 3 overrides them. Whichever rendering is chosen for "comprising", "configured to", etc. is itself a term-map entry and is used identically in every claim.

| English | German |
|---|---|
| A device comprising … | Vorrichtung, umfassend … |
| consisting of | bestehend aus |
| characterised in that | dadurch gekennzeichnet, dass |
| wherein | wobei |
| according to claim 1 | nach Anspruch 1 |
| according to any one of claims 1 to 3 | nach einem der Ansprüche 1 bis 3 |
| at least one | mindestens ein |
| configured to / adapted to | dazu ausgebildet, … zu / eingerichtet, … zu |
| Use of X for … | Verwendung von X zur … |

Each claim remains **one sentence**; dependencies and back-references are unchanged.

## Example

Source (EN):

```
1. A fastening device (1) comprising a housing (10) and a fixing element (12), characterised in that the fixing element (12) is resiliently biased against the housing (10).

2. The fastening device (1) according to claim 1, wherein the housing (10) is made of a plastic material.
```

Term map (excerpt): *fastening device* → *Befestigungsvorrichtung*; *fixing element* → *Fixierelement* (kept distinct from *fastening*); *housing* → *Gehäuse*; *resiliently biased* → *elastisch vorgespannt*; *comprising* → *umfassend*.

Output file `claims.de.txt`:

```
1. Befestigungsvorrichtung (1), umfassend ein Gehäuse (10) und ein Fixierelement (12), dadurch gekennzeichnet, dass das Fixierelement (12) elastisch gegen das Gehäuse (10) vorgespannt ist.

2. Befestigungsvorrichtung (1) nach Anspruch 1, wobei das Gehäuse (10) aus einem Kunststoffmaterial besteht.
```
