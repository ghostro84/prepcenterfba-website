# PrepCenter FBA — Publicare pe prepcenterfba.eu prin GitHub

Fluxul final: **modifici cu Claude sau Replit → push în GitHub → site-ul se
actualizează singur** (în ~1 minut).

---

## Pasul 1 — Creează repo-ul pe GitHub (o singură dată)

1. Intră pe [github.com](https://github.com) → **New repository**.
2. Nume: `prepcenterfba-website` · vizibilitate: **Private** sau Public · fără README.
3. Urcă fișierele: pe pagina repo-ului → **uploading an existing file** → trage
   TOATE fișierele din acest folder (inclusiv `CNAME` și `_config.yml`) → **Commit changes**.
   - Alternativ, din terminal:
     ```bash
     cd acest-folder
     git init && git add -A && git commit -m "Site PrepCenter FBA"
     git branch -M main
     git remote add origin https://github.com/CONTUL-TAU/prepcenterfba-website.git
     git push -u origin main
     ```

## Pasul 2 — Activează GitHub Pages (o singură dată)

1. În repo: **Settings → Pages**.
2. La *Build and deployment*: Source = **Deploy from a branch**,
   Branch = **main** / folder **/ (root)** → Save.
3. După ~1 minut site-ul e live la `https://CONTUL-TAU.github.io/prepcenterfba-website/`.

## Pasul 3 — Leagă domeniul prepcenterfba.eu (o singură dată)

1. Tot în **Settings → Pages → Custom domain**: scrie `prepcenterfba.eu` → Save.
   (Fișierul `CNAME` din repo face același lucru — e deja inclus.)
2. În **Hostinger hPanel → Domains → prepcenterfba.eu → DNS / Nameservers**,
   setează înregistrările DNS:

   | Tip   | Nume | Valoare               |
   |-------|------|-----------------------|
   | A     | @    | 185.199.108.153       |
   | A     | @    | 185.199.109.153       |
   | A     | @    | 185.199.110.153       |
   | A     | @    | 185.199.111.153       |
   | CNAME | www  | CONTUL-TAU.github.io  |

   Șterge vechile înregistrări A pentru `@` care arată spre Hostinger.
3. Așteaptă propagarea DNS (de la câteva minute la câteva ore), apoi în
   GitHub Pages bifează **Enforce HTTPS**.

## Pasul 4 — Fluxul de modificare de zi cu zi

**Cu Replit:** Create Repl → **Import from GitHub** → alege repo-ul. Modifici
(cu Replit AI sau manual), apoi în panoul *Git* din Replit: Commit + Push.
Site-ul se actualizează singur.

**Cu Claude:** ceri modificarea (aici sau în Claude Code conectat la repo),
primești fișierele modificate, le urci în GitHub (drag & drop peste cele vechi
→ Commit, sau `git push`). Claude Code / Claude cu conector GitHub poate face
push direct dacă îi dai acces la repo.

**Direct pe GitHub:** orice fișier → tasta `.` sau butonul ✏️ → editezi →
Commit. Bun pentru corecturi rapide de text.

---

## Varianta alternativă: rămâi pe hosting Hostinger

Dacă preferi ca site-ul să fie servit tot de Hostinger (nu de GitHub Pages):
NU faci Pasul 2 și 3, ci activezi workflow-ul din
`.github/workflows/deploy-hostinger.yml.disabled` (instrucțiuni în fișier).
La fiecare push, GitHub urcă automat fișierele prin FTP în `public_html`.

## ⚠️ Securitate

- **Nu urca niciodată parole în repo** (ex. `ftp-config.json` din alt proiect
  conține parola FTP în text clar — astfel de fișiere nu au ce căuta pe GitHub;
  parolele se pun doar în GitHub → Settings → Secrets).
- Dacă repo-ul e public, oricine îi vede conținutul — pentru un site de
  prezentare e OK, dar verifică să nu existe date sensibile în el.

---

## Notă importantă despre `_config.yml` (nu șterge fișierul)

GitHub Pages rulează Jekyll. Fișierul `_config.yml` din rădăcină exclude din
publicare folderele interne: `tools/`, `src-legal/`, `README-DEPLOY.md` și
`SEO-SETUP.md`. Fără el, scripturile de build și documentația internă sunt
public accesibile la `https://prepcenterfba.eu/tools/…`.

**Nu adăuga un fișier `.nojekyll`** — acesta dezactivează Jekyll și odată cu el
și excluderile de mai sus.

## Fluxul de build (rulează după orice modificare de conținut)

Paginile germane din rădăcină sunt SURSA. Versiunile `/en/`, `/it/`, `/fr/` sunt
generate — orice modificare făcută direct în ele se pierde la următorul build.

```bash
pip install beautifulsoup4 lxml    # o singură dată
python3 tools/build_langs.py       # regenerează /en/ /it/ /fr/ (inclusiv textele juridice)
python3 tools/gen_sitemap.py       # regenerează sitemap.xml și robots.txt
```

Ce se editează unde:

| Vrei să schimbi | Editează |
|---|---|
| Text german | pagina germană din rădăcină |
| Traducere EN/IT/FR | `js/lang/en.js` · `it.js` · `fr.js` |
| Preț | `js/config.js` (sursă unică) |
| Text juridic german | `impressum.html` · `datenschutz.html` · `agb.html` |
| Text juridic tradus | `src-legal/<limbă>/…` |
| Titlu/description traduse | `tools/meta_i18n.py` |

Nu există workflow GitHub Actions — build-ul se rulează local, înainte de push.
