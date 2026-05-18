import json
import os
import base64
from datetime import datetime

# Configuration
base_dir = os.path.expanduser("~/anniversaire_iris")
data_path = os.path.join(base_dir, "data.json")
output_path = os.path.join(base_dir, "index.html")

# Chargement intelligent des données pour éviter les doublons de contenu (hash base64)
with open(data_path, 'r') as f:
    raw_photos = json.load(f)

unique_hashes = set()
unique_photos = []

# Photos à exclure (doublons évidents ou fichiers système)
denylist = ['photo_map', 'filename'] 

for p in raw_photos:
    b64_hash = hash(p['base64'][:1000]) # Hash partiel pour rapidité
    if b64_hash not in unique_hashes and p['filename'] not in denylist:
        unique_hashes.add(b64_hash)
        unique_photos.append(p)

pm = {p['filename']: p for p in unique_photos}
all_files = set(pm.keys())

# Organisation en "Story" pour optimiser l'espace et le ton
story = [
    {
        "title": "L'Invitation au Voyage",
        "text": "Tout a commencé avec ce petit carton aux teintes de nénuphars. Direction Candillargues, au cœur de la Maison des Marais, pour souffler une première bougie historique.",
        "files": ["invitation.jpg", "lieu_repas.jpg", "arrivee_monde.jpg", "jeux_plein_air.jpg", "iris_carte_anniv.jpg"]
    },
    {
        "title": "La Dynastie Iris",
        "text": "Regardez ces visages... De Maman Amandine aux arrière-grands-parents, la ressemblance et la tendresse sautent aux yeux. Une lignée unie autour d'un petit bout de chou qui mène tout son monde à la baguette (de roseau) !",
        "files": ["famille_iris.jpg", "iris_maman.jpg", "yoan_papa.jpg", "yoan_papa_2.jpg", "mamie_sabine.jpg", "iris_patrick_grandpere.jpg", "iris_michele_arrieregp.jpg", "jean_claude_arrieregp.jpg", "jean_claude.jpg", "generations_filles.jpg", "sabine_sebastien.jpg"]
    },
    {
        "title": "Le Festin des Marais",
        "text": "Sous le carbet, l'ambiance monte d'un cran. Pendant que les grands refont le monde entre deux tranches de saucisson, Iris nous montre qu'elle a déjà un sacré coup de fourchette. Une vraie petite épicurienne en devenir !",
        "files": ["table_mise.jpg", "tablee.jpg", "repas.jpg", "iris_repas_bebe.jpg", "pique_nique_famille.jpg", "pique_nique_rire.jpg", "trois_generations_hommes.jpg", "groupe_pique_nique.jpg"]
    },
    {
        "title": "Cadeaux, Gâteaux & Émotions",
        "text": "Le moment fatidique ! 35 ans pour Jeremy, 1 an pour Iris. Le match du jour ? Qui soufflera le plus fort ? Côté cadeaux, les Smartmax font déjà fureur. Et entre le chocolat et le cheesecake, personne n'a résisté.",
        "files": ["gateaux.jpg", "sebastien_gateau.jpg", "jeremy_35ans.jpg", "jeremy_cadeau.jpg", "dessert_herbe_1.jpg", "dessert_herbe_2.jpg", "dessert_herbe_3.jpg", "iris_cadeau_smartmax.jpg", "iris_cadeaux_famille.jpg", "groupe_gateau_cadeaux.jpg"]
    },
    {
        "title": "Le Clan des Barbus (et des Tontons)",
        "text": "Que serait un anniversaire sans les tontons ? Killian en mode 'confinement' ou 'détention' (on ne sait plus trop), Sébastien tout sourire, et toute cette joyeuse bande de protecteurs barbus qui veillent sur la petite.",
        "files": ["killian_tonton.jpg", "killian_couillon.jpg", "killian_detention.jpg", "killian_jeanclaude.jpg", "tonton_barbu.jpg", "sebastien_sourire.jpg", "discussion_hommes.jpg"]
    },
    {
        "title": "Douceur de Fin de Journée",
        "text": "Après l'agitation, le calme revient. Une petite balade au bord de l'étang, des lunettes roses pour voir la vie en couleur, et une sieste bien méritée pour Papi. C'était ça, la magie des 1 an d'Iris.",
        "files": ["iris_lunettes_rose.jpg", "iris_lunettes_rose_portrait.jpg", "marche.jpg", "balade_etang.jpg", "etang_1.jpg", "etang_2.jpg", "etang_3.jpg", "patrick_sieste.jpg", "pique_nique_grand_angle.jpg"]
    }
]

# Récupérer les photos oubliées
structured_files = set()
for s in story:
    structured_files.update(s['files'])

leftovers = list(all_files - structured_files)
if leftovers:
    story.append({
        "title": "Encore quelques souvenirs...",
        "text": "Parce que chaque instant comptait, voici les dernières pépites de la journée.",
        "files": leftovers
    })

# Template HTML avec thème "Mosaic Masonry" pour supprimer le blanc
html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IRIS • 1 AN</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&family=Plus+Jakarta+Sans:wght@200..800&family=Caveat:wght@400..700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin: 0;
            padding: 0;
        }}
        .font-title {{ font-family: 'Fraunces', serif; }}
        .font-script {{ font-family: 'Caveat', cursive; }}
        
        /* Mosaic Grid */
        .masonry {{
            column-count: 1;
            column-gap: 1.5rem;
        }}
        @media (min-width: 640px) {{ .masonry {{ column-count: 2; }} }}
        @media (min-width: 1024px) {{ .masonry {{ column-count: 3; }} }}
        @media (min-width: 1280px) {{ .masonry {{ column-count: 4; }} }}
        
        .masonry-item {{
            break-inside: avoid;
            margin-bottom: 1.5rem;
            position: relative;
            border-radius: 1rem;
            overflow: hidden;
            background: #1e293b;
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .masonry-item:hover {{
            transform: scale(1.02);
            z-index: 10;
        }}
        
        .image-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 40%);
            opacity: 0;
            transition: opacity 0.3s ease;
            display: flex;
            align-items: flex-end;
            padding: 1.5rem;
        }}
        
        .masonry-item:hover .image-overlay {{ opacity: 1; }}

        .section-break {{
            padding: 8rem 0 4rem;
            text-align: center;
        }}
    </style>
</head>
<body class="selection:bg-emerald-500 selection:text-white">

    <!-- HERO -->
    <header class="relative h-screen flex flex-col justify-end p-12 overflow-hidden">
        <div class="absolute inset-0">
            <img src="{pm.get('famille_iris.jpg', unique_photos[0])['base64']}" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0f172a] via-[#0f172a]/20 to-transparent"></div>
        </div>
        <div class="relative z-10 max-w-4xl">
            <h1 class="text-9xl md:text-[12rem] font-title italic leading-none mb-4">Iris.</h1>
            <p class="text-2xl md:text-4xl font-script text-emerald-400 mb-8 max-w-xl">Le grand saut dans la deuxième année de ma vie...</p>
            <div class="flex items-center space-x-6 text-xs uppercase tracking-[0.5em] text-slate-400">
                <span>Mai 2026</span>
                <span class="w-12 h-px bg-slate-700"></span>
                <span>Candillargues</span>
            </div>
        </div>
    </header>

    <main class="px-6 pb-32">
"""

for section in story:
    html_template += f"""
        <div class="section-break max-w-3xl mx-auto">
            <h2 class="text-4xl md:text-6xl font-title italic mb-6 text-emerald-100">{section['title']}</h2>
            <p class="text-slate-400 text-lg md:text-xl font-light leading-relaxed">{section['text']}</p>
        </div>
        
        <div class="masonry max-w-[1600px] mx-auto">
    """
    
    for filename in section['files']:
        photo = pm.get(filename)
        if not photo: continue
        
        html_template += f"""
            <div class="masonry-item cursor-pointer" onclick="openLightbox('{photo['base64']}', `{photo['description']}`)">
                <img src="{photo['base64']}" class="w-full h-auto block" loading="lazy">
                <div class="image-overlay">
                    <p class="font-script text-2xl text-white drop-shadow-lg">{photo['description']}</p>
                </div>
            </div>
        """
        
    html_template += "</div>"

html_template += """
    </main>

    <footer class="bg-slate-950 py-32 text-center">
        <div class="font-title italic text-6xl mb-8">À Iris.</div>
        <p class="text-slate-500 uppercase tracking-widest text-[10px]">Hermes &bull; Claude &bull; 2026</p>
    </footer>

    <!-- LIGHTBOX -->
    <div id="lightbox" class="fixed inset-0 bg-slate-950/fb flex-col items-center justify-center p-4 z-[100] hidden backdrop-blur-xl transition-all duration-300 opacity-0">
        <button onclick="closeLightbox()" class="absolute top-8 right-8 text-white p-4">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="1.5"></path></svg>
        </button>
        <div class="w-full h-full flex flex-col items-center justify-center max-w-6xl mx-auto">
            <img id="lb-img" class="max-w-full max-h-[80vh] rounded-lg shadow-2xl border border-slate-800">
            <p id="lb-text" class="mt-8 text-white font-script text-4xl text-center"></p>
        </div>
    </div>

    <script>
        function openLightbox(src, text) {
            const lb = document.getElementById('lightbox');
            document.getElementById('lb-img').src = src;
            document.getElementById('lb-text').innerText = text;
            lb.classList.remove('hidden');
            setTimeout(() => lb.classList.add('opacity-100'), 10);
            document.body.style.overflow = 'hidden';
        }
        function closeLightbox() {
            const lb = document.getElementById('lightbox');
            lb.classList.remove('opacity-100');
            setTimeout(() => lb.classList.add('hidden'), 300);
            document.body.style.overflow = 'auto';
        }
    </script>
</body>
</html>
"""

with open(output_path, 'w') as f:
    f.write(html_template)

print(f"Album optimisé généré: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
