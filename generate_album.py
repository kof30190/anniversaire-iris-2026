import json, os, random

base_dir = os.path.expanduser("~/anniversaire_iris")
data_path = os.path.join(base_dir, "data.json")
output_path = os.path.join(base_dir, "index.html")

with open(data_path, 'r') as f:
    photos_list = json.load(f)

pm = {p['filename']: p for p in photos_list}

# Chapitres dédoublonnés — chaque image une seule fois sur toute la page
chapters = [
    {
        "id": "prologue", "title": "Prologue",
        "subtitle": "Le rendez-vous des marais",
        "text": "Un petit coin de paradis à Candillargues, entre ciel bleu et roseaux, pour une étape inoubliable : le tout premier anniversaire d'Iris.",
        "images": ["invitation.jpg", "lieu_repas.jpg", "arrivee_monde.jpg", "jeux_plein_air.jpg"]
    },
    {
        "id": "tribu", "title": "La Tribu d'Iris",
        "subtitle": "Trois générations de sourires",
        "text": "Mamie Sabine, Papi Patrick, Jean-Claude... Toute la lignée est là pour entourer la petite reine du jour.",
        "images": ["iris_maman.jpg", "yoan_papa.jpg", "iris_patrick_grandpere.jpg", "iris_michele_arrieregp.jpg", "jean_claude_arrieregp.jpg", "famille_iris.jpg", "sabine_sebastien.jpg"]
    },
    {
        "id": "banquet", "title": "Le Banquet",
        "subtitle": "Pique-nique & Tablée",
        "text": "Parce qu'un anniversaire, ça creuse ! Entre les cerises et les bons petits plats, on profite de la douceur de vivre sous le carbet.",
        "images": ["table_mise.jpg", "tablee.jpg", "repas.jpg", "iris_repas_bebe.jpg", "trois_generations_hommes.jpg", "pique_nique_famille.jpg", "pique_nique_rire.jpg"]
    },
    {
        "id": "double-fete", "title": "Double Fête",
        "subtitle": "1 an & 35 ans",
        "text": "Jeremy souffle ses 35 bougies pendant qu'Iris découvre le plaisir des gâteaux. Une même passion pour le chocolat !",
        "images": ["jeremy_35ans.jpg", "jeremy_cadeau.jpg", "gateaux.jpg", "dessert_herbe_1.jpg", "dessert_herbe_2.jpg", "dessert_herbe_3.jpg", "iris_cadeau_smartmax.jpg"]
    },
    {
        "id": "tontons", "title": "Le Gang des Tontons",
        "subtitle": "Barbus & Bêtises",
        "text": "Killian, Sébastien, Yoan... L'équipe de choc d'Iris. Toujours prêts pour une grimace ou un câlin, ils veillent au grain.",
        "images": ["killian_tonton.jpg", "killian_detention.jpg", "tonton_barbu.jpg", "sebastien_sourire.jpg", "discussion_hommes.jpg"]
    },
    {
        "id": "epilogue", "title": "Épilogue",
        "subtitle": "Rêves et Roseaux",
        "text": "Une fin de journée tout en douceur. Les nouvelles lunettes roses sur le nez, on marche vers demain en rêvant à la prochaine fête.",
        "images": ["iris_lunettes_rose.jpg", "marche.jpg", "patrick_sieste.jpg", "balade_etang.jpg", "pique_nique_grand_angle.jpg"]
    }
]

# Vérification stricte : chaque image est résolue et unique
seen = set()
for ch in chapters:
    resolved = []
    for f in ch["images"]:
        name = f if f.endswith(".jpg") else f.replace(".txt", ".jpg")
        if name in seen:
            continue  # skip doublon inter-chapitre
        if name not in pm:
            print(f"  ⚠ MANQUANT: {name}")
            continue
        seen.add(name)
        resolved.append(name)
    ch["images"] = resolved

# Ajout des photos non assignées dans une section "Bonus"
bonus = []
for name in pm:
    if name not in seen:
        bonus.append(name)
        seen.add(name)
if bonus:
    chapters.append({
        "id": "bonus", "title": "Instants volés",
        "subtitle": "Les petits plus",
        "text": "Quelques moments supplémentaires glanés au fil de l'objectif.",
        "images": bonus
    })

print(f"Photos uniques dans l'album: {len(seen)}")

# Template DARK MASONRY
html = """<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iris • 1 An • Carnet de Fête</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300&family=Manrope:wght@300;400;600&family=Caveat:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root { --bg: #0f172a; --card: #1e293b; --accent: #d66853; --gold: #f59e0b; --text: #e2e8f0; --muted: #94a3b8; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); font-family: 'Manrope', sans-serif; color: var(--text); }
  .font-title { font-family: 'Fraunces', serif; font-weight: 300; }
  .font-script { font-family: 'Caveat', cursive; }

  header.hero {
    position: relative; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden;
  }
  header.hero .bg-img { position: absolute; inset: 0; }
  header.hero .bg-img img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.35); }
  header.hero .overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, transparent 60%, var(--bg) 100%); }
  header.hero .content { position: relative; z-index: 10; text-align: center; }
  header.hero h1 { font-size: clamp(4rem, 10vw, 8rem); font-style: italic; color: #fff; margin-bottom: 0.5rem; }
  header.hero p { font-family: 'Caveat', cursive; font-size: clamp(1.5rem, 4vw, 2.5rem); color: rgba(255,255,255,0.7); }
  header.hero .badge { display: inline-block; margin-top: 2rem; padding: 0.6rem 2rem; border: 1px solid rgba(255,255,255,0.25); border-radius: 9999px; font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; color: rgba(255,255,255,0.8); backdrop-filter: blur(10px); }

  nav { position: sticky; top: 0; z-index: 100; background: rgba(15,23,42,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 0.8rem 0; }
  nav .inner { max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; }
  nav a { color: var(--muted); font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; text-decoration: none; transition: color 0.3s; }
  nav a:hover { color: var(--accent); }

  .section-title { padding: 8rem 0 2rem 0; max-width: 800px; margin: 0 auto; text-align: center; }
  .section-title .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
  .section-title .label { font-size: 0.65rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--accent); margin-bottom: 1rem; }
  .section-title h2 { font-size: clamp(2.5rem, 5vw, 3.5rem); font-style: italic; margin-bottom: 1rem; }
  .section-title p { color: var(--muted); font-size: 1rem; line-height: 1.7; max-width: 600px; margin: 0 auto; font-weight: 300; }

  .masonry { columns: 4 240px; column-gap: 1rem; max-width: 1400px; margin: 0 auto; padding: 0 1rem 6rem 1rem; }
  .masonry .item { break-inside: avoid; margin-bottom: 1rem; border-radius: 12px; overflow: hidden; background: var(--card); transition: transform 0.35s ease, box-shadow 0.35s ease; box-shadow: 0 4px 20px rgba(0,0,0,0.3); cursor: pointer; position: relative; }
  .masonry .item:hover { transform: translateY(-8px); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
  .masonry .item img { width: 100%; display: block; transition: transform 0.6s ease; }
  .masonry .item:hover img { transform: scale(1.04); }
  .masonry .item .caption { padding: 1rem 1rem 1.2rem 1rem; }
  .masonry .item .caption p { font-family: 'Caveat', cursive; font-size: 1.3rem; color: var(--muted); line-height: 1.4; }

  footer { text-align: center; padding: 6rem 2rem; border-top: 1px solid rgba(255,255,255,0.05); }
  footer h2 { font-size: 2.5rem; font-style: italic; margin-bottom: 0.5rem; }
  footer p { color: var(--muted); font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.5rem; }

  #lightbox { position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,0.95); display: none; align-items: center; justify-content: center; flex-direction: column; padding: 2rem; }
  #lightbox img { max-width: 90vw; max-height: 75vh; object-fit: contain; border-radius: 8px; }
  #lightbox .lb-text { color: #fff; font-family: 'Caveat', cursive; font-size: 2rem; margin-top: 2rem; text-align: center; max-width: 600px; }
  #lightbox button { position: absolute; top: 2rem; right: 2rem; background: none; border: none; color: #fff; font-size: 2rem; cursor: pointer; opacity: 0.6; transition: opacity 0.3s; }
  #lightbox button:hover { opacity: 1; }

  @media (max-width: 640px) {
    nav .inner { flex-direction: column; gap: 0.5rem; padding: 0.5rem 1rem; }
    nav a { font-size: 0.6rem; margin: 0 0.25rem; }
    .section-title { padding: 5rem 0 1.5rem 0; }
  }
</style>
</head>
<body>

<header class="hero">
  <div class="bg-img"><img src="__HERO__" alt=""></div>
  <div class="overlay"></div>
  <div class="content">
    <h1>Iris</h1>
    <p>Un an au fil de l'eau</p>
    <span class="badge">Candillargues • Mai 2026</span>
  </div>
</header>

<nav>
  <div class="inner">
    <a href="#" style="font-family:'Fraunces',serif;font-style:italic;font-size:1rem;text-transform:none;letter-spacing:0;">Iris.</a>
    <div>
"""

nav_links = " ".join(f'<a href="#{ch["id"]}">{ch["title"]}</a>' for ch in chapters)
html += nav_links
html += """
    </div>
  </div>
</nav>
"""

# Génération des sections
for ch in chapters:
    html += f"""
<div class="section-title">
  <div class="icon">{ch.get('icon','')}</div>
  <div class="label">{ch['subtitle']}</div>
  <h2 id="{ch['id']}" class="font-title">{ch['title']}</h2>
  <p>{ch['text']}</p>
</div>
<div class="masonry">
"""
    for name in ch["images"]:
        photo = pm.get(name)
        if not photo: continue
        html += f"""
  <div class="item" onclick="openLB('{photo["base64"]}', `{photo["description"]}`)">
    <img src="{photo['base64']}" loading="lazy">
    <div class="caption"><p>{photo['description']}</p></div>
  </div>"""
    html += "\n</div>\n"

# Footer + Lightbox
html += """
<footer>
  <h2 class="font-title">Merci !</h2>
  <p>Pour cette journée gravée dans le temps</p>
  <p style="margin-top:1.5rem;font-size:0.6rem;color:#475569;">Un album réalisé pour Iris • Hermes • 2026</p>
</footer>

<div id="lightbox">
  <button onclick="closeLB()">&times;</button>
  <img id="lb-img" src="">
  <div class="lb-text" id="lb-text"></div>
</div>

<script>
function openLB(src, txt) {
  document.getElementById('lb-img').src = src;
  document.getElementById('lb-text').innerText = txt;
  document.getElementById('lightbox').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}
function closeLB() {
  document.getElementById('lightbox').style.display = 'none';
  document.body.style.overflow = 'auto';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLB(); });
</script>
</body></html>
"""

# Remplace le placeholder hero
hero_img = pm.get("invitation.jpg", list(pm.values())[0])
html = html.replace("__HERO__", hero_img["base64"])

with open(output_path, 'w') as f:
    f.write(html)

print(f"\n✓ Album généré: {output_path}")
print(f"  Taille: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
