import os, json, base64

base = os.path.expanduser("~/anniversaire_iris")

with open(os.path.join(base, 'sorted_photos.json'), 'r') as f:
    photos = json.load(f)

# 1. Encode
print("Encodage...")
for i, p in enumerate(photos):
    path = os.path.join(base, p['filename'])
    with open(path, 'rb') as pf:
        p['b64'] = base64.b64encode(pf.read()).decode()
print(f"  {len(photos)} photos encodées")

# 2. Commentaires
comments = {
    "invitation.jpg": "Tout commence par ce petit carton. Candillargues, un dimanche de mai. Le décor est planté, la famille prévenue.",
    "lieu_repas.jpg": "Le carbet nous ouvre ses bras. Ombragé, paisible, posé au bord de l'eau.",
    "jean_claude.jpg": "Jean-Claude, l'arrière-grand-père. Quatre générations aujourd'hui, et c'est lui qui ouvre le bal.",
    "killian_tonton.jpg": "Killian est déjà là. Fidèle au poste, le sourire en bandoulière.",
    "arrivee_monde.jpg": "Ça arrive de partout. Les embrassades, les éclats de voix. La mécanique des retrouvailles.",
    "yoan_papa.jpg": "Yoan, le papa. Un an qu'il exerce ce métier-là. Sur son visage, tout est dit.",
    "repas.jpg": "À table. Les plats voyagent, les verres trinquent, les histoires se croisent.",
    "famille_iris.jpg": "Le trio : Iris, Amandine, Yoan. La photo qui fait battre le cœur un peu plus fort.",
    "marche.jpg": "Regardez-moi ça. Debout, déterminée, elle avance. Le monde n'a qu'à bien se tenir.",
    "tablee.jpg": "Une belle tablée. Chacun sa place, chacun son histoire, tous réunis pour elle.",
    "yoan_papa_2.jpg": "Yoan encore. Un papa ne se lasse jamais de contempler sa fille.",
    "jean_claude_arrieregp.jpg": "Jean-Claude, toujours droit. Le patriarche qui a vu naître toutes les branches.",
    "killian_couillon.jpg": "Killian en mode one-man-show. Grimaces, vannes, fous rires garantis.",
    "iris_michele_arrieregp.jpg": "Iris entre Michèle et Jean-Claude. La petite dernière au milieu des aînés.",
    "jeux_plein_air.jpg": "En attendant le repas, une parenthèse en plein air. Rien de sérieux, tout est parfait.",
    "iris_repas_bebe.jpg": "Iris n'a pas lu le protocole. Quand c'est l'heure, c'est l'heure.",
    "tonton_barbu.jpg": "Un barbu mystérieux dans le cadre. Encore un tonton, évidemment.",
    "table_mise.jpg": "La table est dressée. Les assiettes s'alignent. Place au festin.",
    "iris_patrick_grandpere.jpg": "Patrick et sa petite-fille. Pas besoin de mots.",
    "dessert_herbe_1.jpg": "Le dessert change de décor. Pourquoi rester assis quand l'herbe tend les bras ?",
    "dessert_herbe_2.jpg": "Il y en a un qui ne lâche rien. Application maximale, plaisir intégral.",
    "dessert_herbe_3.jpg": "Pique-nique improvisé, version horizontale. Les meilleurs lits sont en chlorophylle.",
    "killian_jeanclaude.jpg": "Killian et Jean-Claude côte à côte. Le jeune tonton et le doyen réunis.",
    "mamie_sabine.jpg": "Mamie Sabine fait son entrée. Un sourire qui réchauffe tout.",
    "sebastien_gateau.jpg": "Sébastien monte la garde. Officiellement pour protéger le gâteau. Officieusement...",
    "pique_nique_famille.jpg": "Le camp de base dans toute sa splendeur. Canisses et éclats de voix.",
    "discussion_hommes.jpg": "Conciliabule à l'ombre. On refait le monde, ou le classement du Top 14.",
    "sabine_sebastien.jpg": "Sabine et Sébastien. Une mère et son fils, deux sourires assortis.",
    "groupe_pique_nique.jpg": "Vue d'ensemble. Chacun a trouvé son coin d'herbe et son bout de ciel.",
    "sebastien_sourire.jpg": "Sébastien tout sourire. La définition de la bonne humeur.",
    "iris_cadeau_smartmax.jpg": "Iris découvre son Smartmax avec Patrick. Les yeux écarquillés, les doigts qui explorent.",
    "jeremy_35ans.jpg": "Rebondissement : c'est aussi l'anniversaire de Jeremy. 35 ans, même plaisir.",
    "jeremy_cadeau.jpg": "Jeremy déballe. Le sourire d'un gamin de 35 piges qui n'a jamais grandi.",
    "iris_cadeaux_famille.jpg": "Iris ouvre ses trésors, la famille en cercle. Les petits paquets, les grands bonheurs.",
    "iris_lunettes_rose_portrait.jpg": "Les nouvelles lunettes sont arrivées. L'accessoire indispensable.",
    "iris_lunettes_rose.jpg": "Trop belle. Point final.",
    "generations_filles.jpg": "Quatre générations de filles dans un cadre. Et le papa venu s'inviter.",
    "iris_carte_anniv.jpg": "Joyeux anniversaire Iris. Un an. Le premier d'une longue liste.",
    "pique_nique_rire.jpg": "Un éclat de rire traverse le pique-nique. Instinctif, inoubliable.",
    "trois_generations_hommes.jpg": "Trois générations d'hommes autour d'un saladier de cerises. Simple et parfait.",
    "patrick_sieste.jpg": "Patrick post-gâteau. La sieste était-elle optionnelle ?",
    "killian_detention.jpg": "Killian en plein bain de soleil. L'art de ne rien faire avec style.",
    "groupe_gateau_cadeaux.jpg": "Tout le monde converge. Gâteau, cadeaux. Le grand moment.",
    "pique_nique_grand_angle.jpg": "Plan large sur la fête. Pour mesurer l'ampleur du bonheur.",
    "gateaux.jpg": "Les voilà. Un pour Iris, un pour Jeremy. Double ration de douceur.",
    "etang_1.jpg": "L'étang, miroir calme après l'effervescence.",
    "etang_2.jpg": "Promenade les pieds dans l'herbe, le regard sur l'eau.",
    "etang_3.jpg": "Derniers rayons sur les roseaux. La lumière baisse, les souvenirs montent.",
    "balade_etang.jpg": "Fin de parcours. On embarque les souvenirs. Vivement l'année prochaine.",
}

chapters = [
    ("ouverture", "Ouverture", "🌿", "Avant que tout commence", 0, 1),
    ("arrivees", "Les Arrivées", "👋", "Les premiers visages", 1, 6),
    ("repas", "Le Repas", "🍽️", "À table, en famille", 6, 18),
    ("pique-nique", "Pique-Nique & Détente", "☀️", "Tout le monde dans l'herbe", 18, 31),
    ("gateaux-cadeaux", "Gâteaux & Cadeaux", "🎁", "Le grand moment", 31, 45),
    ("balade", "Balade au Crépuscule", "🌅", "Derniers instants au bord de l'eau", 45, 49),
]

html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iris — 1 An — Candillargues 2026</title>
<style>
  :root {
    --bg: #1a1614;
    --card: #25211e;
    --text: #e8e0d9;
    --muted: #a3968a;
    --accent: #c17d60;
    --border: #3a3530;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  .hero {
    text-align: center;
    padding: 6rem 1.5rem 4rem;
    max-width: 700px;
    margin: 0 auto;
  }
  .hero h1 {
    font-size: clamp(3rem, 10vw, 6rem);
    font-weight: normal;
    letter-spacing: -0.02em;
    margin-bottom: 0.75rem;
  }
  .hero .sub {
    font-size: 1.3rem;
    color: var(--muted);
    font-style: italic;
    line-height: 1.6;
  }
  .hero .date {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    color: var(--accent);
    margin-top: 1.5rem;
  }
  .hero .divider {
    width: 40px;
    height: 1px;
    background: var(--accent);
    margin: 2rem auto;
  }
  .chapter {
    max-width: 1100px;
    margin: 0 auto 5rem;
    padding: 0 1.5rem;
  }
  .chapter-header {
    text-align: center;
    margin-bottom: 3rem;
    padding-top: 1.5rem;
  }
  .chapter-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
  .chapter-title {
    font-size: 2.2rem;
    font-weight: normal;
    letter-spacing: -0.01em;
  }
  .chapter-sub { font-size: 1rem; color: var(--muted); font-style: italic; }
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }
  .card {
    background: var(--card);
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border);
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    border-color: var(--accent);
  }
  .card img { width: 100%; height: auto; display: block; }
  .card-body { padding: 1.2rem 1.4rem 1.4rem; }
  .card-body p { font-size: 0.95rem; color: var(--muted); font-style: italic; line-height: 1.6; }
  .card-num {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--accent);
    margin-bottom: 0.5rem;
    font-style: normal;
  }
  footer {
    text-align: center;
    padding: 4rem 1.5rem 3rem;
    color: var(--muted);
    font-size: 0.9rem;
    max-width: 700px;
    margin: 0 auto;
    font-style: italic;
    line-height: 1.8;
  }
  footer .fdivider {
    width: 40px;
    height: 1px;
    background: var(--accent);
    margin: 0 auto 2rem;
  }
  @media (max-width: 640px) {
    .gallery { grid-template-columns: 1fr; gap: 1.5rem; }
    .hero { padding: 4rem 1rem 2.5rem; }
    .chapter { padding: 0 1rem; }
  }
</style>
</head>
<body>

<div class="hero">
  <h1>Iris</h1>
  <p class="sub">Un an.<br>Une famille.<br>Un dimanche suspendu.</p>
  <div class="divider"></div>
  <p class="date">Candillargues · Mai 2026</p>
</div>
'''

counter = 0
for cid, ctitle, cicon, csub, start, end in chapters:
    html += f'''
<section class="chapter" id="{cid}">
  <div class="chapter-header">
    <div class="chapter-icon">{cicon}</div>
    <h2 class="chapter-title">{ctitle}</h2>
    <p class="chapter-sub">{csub}</p>
  </div>
  <div class="gallery">
'''
    for p in photos[start:end]:
        counter += 1
        comment = comments.get(p['filename'], p.get('note', ''))
        html += f'''
    <div class="card">
      <img src="data:image/jpeg;base64,{p['b64']}" alt="{comment}" loading="lazy">
      <div class="card-body">
        <div class="card-num">Photo {counter}</div>
        <p>{comment}</p>
      </div>
    </div>'''
    html += '\n  </div>\n</section>\n'

html += '''
<footer>
  <div class="fdivider"></div>
  Pour Iris,<br>avec tout l'amour de ta tribu.<br>
  <span style="font-size:0.7rem;opacity:0.4;">Album Hermes · Mai 2026</span>
</footer>
</body></html>
'''

out = os.path.join(base, 'index.html')
with open(out, 'w') as f:
    f.write(html)

print(f"✓ {out}")
print(f"  {counter} photos, {os.path.getsize(out)/(1024*1024):.1f} MB")
