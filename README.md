# Website ACOD Telecom-Vliegwezen

Statische site, geen frameworks. `build.py` (alleen Python-standaardbibliotheek) plakt de
kop en voet van een thema rond elke pagina in `src/pages/` en schrijft het resultaat weg.
Er zijn twee thema's met dezelfde inhoud:

- `src/themes/v2/`: warm affiche in geel, rood en wijnrood, met hangarbogen. Komt in `site/`.
- `src/themes/v1/`: rood en nachtblauw, met het vertrekbord. Komt in `site/v1/`.

Een thema kan pagina's (`pages/`) en bestanden (`assets/`) van de gedeelde versie overschrijven.
v2 heeft een eigen startpagina en duotoonversies van de foto's. Voeg je een foto toe, maak dan
ook een duotoonversie voor v2:

```sh
magick src/assets/img/foto.jpg -colorspace gray -contrast-stretch 1%x1% \
  +level-colors '#43121f,#ffd9b8' -quality 80 src/themes/v2/assets/img/foto.jpg
```

De map `site/` kan zo op eender welke webhost.

## Publiceren

Elke push naar `main` bouwt de site en zet ze op GitHub Pages
(`.github/workflows/pages.yml`). De map `site/` zelf staat niet in git.

Zolang de site een ontwerp is, staat er een `noindex`-tag in zodat zoekmachines ze
overslaan. Maak `robots` in `build.py` leeg bij de echte lancering.

```sh
python3 build.py
python3 -m http.server 8765 -d site   # bekijken op http://localhost:8765
```

## Nog aan te leveren

Alles wat nog ontbreekt staat geel gearceerd op de site.

- Adres en e-mailadres van het secretariaat (`SITE` in `build.py`).
- Namen, gsm-nummers en e-mailadressen per gewestelijk secretariaat (`src/pages/contact.html`).
- E-mailadres voor de stakingsvergoeding en link naar de privacyverklaring (`src/pages/hulp.html`).
- Rekentools voor bonus en merite (`src/pages/hulp.html`).
- Naam van de nieuwsbrief en de eerste edities (`src/pages/nieuwsbrief.html`).
- Foto's en namen van het team (`src/pages/over-ons.html`).
- Cao-timing en procedures (stakingsvergoeding, syndicale premie) voor skeyes, Brussels Airport
  Company en het BIPT. De huidige tekst volgt de Proximus-procedures van de Waalse site.
- Bron en toestemming voor het ontwerpbeeld van Proximus op Tour & Taxis (`src/pages/bedrijven.html`).
- Facebookpagina, optioneel (`SITE` in `build.py`).

## Formulieren

Zolang `FORM_ENDPOINT` bovenaan `src/assets/site.js` leeg is, openen de formulieren het
mailprogramma van de bezoeker met de ingevulde gegevens. Vul je een endpoint in (bv.
Formspree), dan worden ze rechtstreeks verstuurd.
