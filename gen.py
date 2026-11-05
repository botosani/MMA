#!/usr/bin/env python3
"""Generează tot site-ul BMC în folderul site/.  Folosire: python3 gen.py [domeniu.ro]"""
import sys, os, re, json, html as H, shutil, datetime
D = (sys.argv[1] if len(sys.argv) > 1 else '').replace('https://', '').strip('/')
B = 'https://' + D if D else ''
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'site')
e = lambda s: H.escape(s, quote=True)
NAV = [('p.html', 'gavel', 'Regulament'), ('ghid.html', 'shirt', 'Ghid Echipament'), ('time.html', 'location-dot', 'Locație &amp; Program')]
FNAV = ('<nav class="foot-nav" aria-label="Linkuri utile"><a href="index.html">Acasă</a><a href="despre.html">Despre BMC</a><a href="p.html">Regulament</a><a href="ghid.html">Ghid echipament</a>'
        '<a href="time.html">Locație și program</a><a href="inscrie.html">Înscrie-te</a><a href="confidentialitate.html">Confidențialitate</a></nav>')
SITEMAP = []

def meta(fn, title, desc, idx):
    url = B + ('/' if fn == 'index.html' else '/' + fn)
    m = f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n<meta name="theme-color" content="#000000">\n<link rel="icon" href="logo1.jpeg">\n'
    if not idx: return m + '<meta name="robots" content="noindex, nofollow">\n'
    m += f'<meta property="og:type" content="website"><meta property="og:locale" content="ro_RO"><meta property="og:site_name" content="BMC Botoșani"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">\n<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">\n'
    if B:
        m += f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}"><meta property="og:image" content="{B}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:image" content="{B}/og-image.png">\n'
        SITEMAP.append(url)
    return m

def page(fn, title, desc, body, idx=True, active='', nt=False, hdr=True, extra_head=''):
    nav = ''.join(f'<a href="{h}" class="nav-link{" on" if h == active else ""}"><i class="fas fa-{i}"></i> {t}</a>' for h, i, t in NAV) + '<a href="inscrie.html" class="nav-link nav-cta"><i class="fas fa-user-plus"></i> Înscrie-te</a>'
    header = ('<header id="header"><a href="index.html" class="logo"><img src="logo1.jpeg" alt="Logo BMC Botoșani" class="logo-img" width="48" height="48"><div><div class="logo-name">BMC <em>BOTOȘANI</em></div><span class="logo-sub">Martial Combat</span></div></a>'
              f'<nav aria-label="Principal">{nav}</nav><button class="hamburger" id="hamburger" aria-label="Meniu"><span></span><span></span><span></span></button></header><div class="mobile-menu" id="mobileMenu">{nav}</div>') if hdr else ''
    foot = f'<footer><div class="footer-logo">BMC <span>BOTOȘANI</span></div><div class="footer-copy">© 2026 Botoșani Martial Combat</div>{FNAV}</footer>' if hdr else ''
    out = ('<!DOCTYPE html>\n<html lang="ro">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + meta(fn, title, desc, idx) + extra_head +
           '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600;700&family=Barlow+Condensed:wght@600;700&display=swap" rel="stylesheet">\n'
           '<link rel="preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"></noscript>\n'
           '<link rel="stylesheet" href="site.min.css"><link rel="stylesheet" href="bmc.min.css">\n<script src="site.min.js" defer></script><script src="bmc.min.js" defer></script>\n</head>\n'
           f'<body{" data-no-theme" if nt else ""}>\n{header}\n{body}\n{foot}\n</body>\n</html>\n')
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(out)

def hero2(crumb, t1, t2, sub):
    return (f'<section class="page-hero"><div class="page-hero-inner"><div class="breadcrumb"><a href="index.html">Acasă</a><span>/</span><span class="cur">{crumb}</span></div>'
            f'<h1 class="page-title">{t1}<em>{t2}</em></h1><p class="sub">{sub}</p></div></section>')
def li(t, b, g=0): return f'<li><div class="rule-dot{" g" if g else ""}"></div><div><div class="rule-li-title">{t}</div><div class="rule-li-body">{b}</div></div></li>'
def card(n, ic, t, sub, inner):
    return (f'<div class="reg-section reveal"><div class="section-label">Articolul 0{n}</div><div class="rule-card"><div class="rule-card-header"><div class="rule-icon"><i class="fas fa-{ic}"></i></div>'
            f'<div><div class="rule-card-title">{t}</div><div class="rule-card-sub">{sub}</div></div><div class="rule-num">0{n}</div></div><div class="rule-card-body">{inner}</div></div></div>')
def ul(*x): return '<ul class="rule-list">' + ''.join(x) + '</ul>'
def blk(ic, t, sub, inner, d=''):
    return (f'<div class="block reveal {d}"><div class="block-header"><div class="block-header-icon"><i class="fas fa-{ic}"></i></div><div><div class="block-header-title">{t}</div><div class="block-header-sub">{sub}</div></div></div><div class="block-body">{inner}</div></div>')
def loc(ic, t, b): return f'<div class="location-card"><div class="loc-icon"><i class="fas fa-{ic}"></i></div><div><div class="loc-title">{t}</div><div class="loc-body">{b}</div></div></div>'
def routine(m, t, b): return f'<div class="routine-item"><div class="time-badge">{m} MIN</div><div class="routine-desc"><strong>{t}</strong><span>{b}</span></div></div>'
def row(ic, l, v): return f'<div class="schedule-row"><i class="fas fa-{ic}"></i><div class="schedule-row-label">{l}</div><div class="schedule-row-value">{v}</div></div>'
SOC = ('<a href="https://www.instagram.com/mma.botosani" target="_blank" rel="noopener" class="social-btn soc-insta"><i class="fab fa-instagram"></i> Instagram</a>'
       '<a href="https://www.facebook.com/share/1HV6CSWt2Y/" target="_blank" rel="noopener" class="social-btn soc-fb"><i class="fab fa-facebook"></i> Facebook</a>'
       '<a href="https://www.youtube.com/@mma.botosani" target="_blank" rel="noopener" class="social-btn soc-yt"><i class="fab fa-youtube"></i> YouTube</a>'
       '<a href="https://www.tiktok.com/@bmc.botosani" target="_blank" rel="noopener" class="social-btn soc-tt"><i class="fab fa-tiktok"></i> TikTok</a>')
CTA = '<a href="inscrie.html" class="btn btn-primary"><i class="fas fa-user-plus"></i> Înscrie-te Acum</a>'

# ───────── INDEX ─────────
badges = ''.join(f'<div class="badge"><div class="badge-icon"><i class="fas fa-{i}"></i></div><div><div class="badge-text">{t}</div><div class="badge-sub">{s}</div></div></div>' for i, t, s in
    [('heart', '100% Gratuit', 'Fără taxe sau abonament'), ('users', 'Comunitate', 'Ne susținem reciproc'), ('ban', 'Anti-vicii', 'Sport în loc de droguri'), ('hand-holding-heart', 'Donații voluntare', 'Nu condiționează participarea')])
pill = ''.join(f'<div class="pillar reveal {d}"><div class="pillar-number">0{n}</div><div class="pillar-icon"><i class="fas fa-{i}"></i></div><div class="pillar-title">{t}</div><div class="pillar-body">{b}</div></div>' for n, i, t, b, d in [
    (1, 'brain', 'Calm sub Presiune', 'Sportul de contact te învață să rămâi lucid atunci când situația devine dificilă. Înveți să îți controlezi emoțiile și frica în mod real.', ''),
    (2, 'balance-scale', 'Disciplină de Fier', 'Consecvența la antrenament se traduce în consecvență în viață. Devii mai organizat, mai responsabil și mai bun în tot ce faci.', 'd1'),
    (3, 'heartbeat', 'Sănătate Totală', 'Corpul devine mai puternic, mintea mai limpede. Sportul este cel mai bun antidot împotriva viciilor și a stresului zilnic.', 'd2'),
    (4, 'handshake', 'Respect &amp; Caracter', 'Înveți respectul față de ceilalți, autocontrolul și gestionarea emoțiilor sub presiune. Artele marțiale formează caractere, nu bătăuși.', 'd3')])
tr = ''.join(f'<div class="training-item reveal {d}"><div class="t-icon"><i class="fas fa-{i}"></i></div><div><div class="t-title">{t}</div><div class="t-body">{b}</div></div></div>' for i, t, b, d in [
    ('users', 'Comunitate de Suport', 'Ne susținem reciproc să rămânem pe drumul cel bun. Nimeni nu rămâne în urmă, nimeni nu este lăsat singur.', ''),
    ('hand-holding-heart', 'Sparring 100% Opțional', 'Contactul fizic este strict opțional. Poți face doar tehnică și condiție fizică — nimeni nu te va forța.', 'd1'),
    ('running', 'Eliberare de Energie', 'Antrenamentele te ajută să dormi liniștit, să scapi de agitație și să transformi energia negativă în ceva constructiv.', 'd2'),
    ('dumbbell', 'Nivel Adaptat', 'Antrenamentele sunt echilibrate și personalizate în funcție de nivelul tău. Beginner sau avansat — toți sunt bineveniți. Vezi <a href="ghid.html">ce echipament îți trebuie</a> și <a href="time.html">când ne antrenăm</a>.', 'd3')])
mp = ''.join(f'<p class="mission-para reveal {d}">{t}</p>' for t, d in [
    ('Știm că viața de adolescent poate fi grea. Mulți tineri ajung să caute refugiul în <span class="red">vicii — alcool, țigări, substanțe interzise</span> — doar pentru a scăpa de presiune, de singurătate sau de problemele de acasă.', ''),
    ('<strong>Noi nu îi judecăm pe tineri pentru alegerile lor din trecut.</strong> Suntem aici să le oferim o mână de ajutor și o alternativă reală.', 'd1'),
    ('Ne propunem să înlocuim dependențele nocive cu <strong>disciplina sportului</strong> și bucuria unui stil de viață sănătos. Înțelegem că, de cele mai multe ori, costurile mari sunt principala barieră care ține copiii departe de sport.', 'd2'),
    ('Misiunea noastră este să eliminăm aceste obstacole financiare și sociale, transformând, împreună, <strong>potențialul fiecăruia în performanță reală.</strong>', 'd3')])
page('index.html', 'BMC Botoșani — antrenamente MMA gratuite pentru tineri', 'Grup sportiv voluntar din Botoșani: MMA și calisthenics gratuite pentru tineri, într-un mediu fără judecată. Înscrie-te azi.', f'''<main id="continut">
<section class="hero"><div class="hero-bg"></div><div class="hero-content"><div class="hero-eyebrow">Botoșani · 2026</div>
<h1 class="hero-title"><span class="line">Botoșani</span><span class="line">Martial</span><span class="line">Combat</span></h1>
<p class="hero-sub">Grup de Dezvoltare Personală și Sportivă pentru tineret.</p>
<div class="hero-actions"><a href="inscrie.html" class="btn btn-primary"><i class="fas fa-user-plus"></i> Hai în Echipă</a><a href="despre.html" class="btn btn-ghost"><i class="fas fa-location-dot"></i> Ce este BMC și unde ne găsești</a></div></div></section>
<section><div class="about"><div>
<div class="section-label reveal">Cine suntem</div><h2 class="section-title reveal d1">Doi tineri.<br>Un vis comun.</h2><div class="divider reveal d2"></div>
<div class="peer-note reveal d2"><p><i class="fas fa-user-friends"></i> <strong>Shared Learning:</strong> Nu suntem antrenori certificați sau maeștri. Dăm mai departe din ce am învățat, ne antrenăm cot la cot și creștem împreună.</p></div>
<p class="about-text reveal d3">BMC Botoșani a luat naștere din inițiativa a <strong>doi tineri de 17 și 18 ani</strong> din județul Botoșani, conștienți de o problemă reală: <span class="accent">lipsa activităților sănătoase pentru tineret</span>.</p>
<div class="callout reveal d3"><p><i class="fas fa-shield-alt"></i> <strong>ZERO TOLERANȚĂ:</strong> Suntem împotriva violenței și a bătăilor de stradă. Nu organizăm lupte — organizăm antrenamente. Citește <a href="p.html">regulamentul complet</a>.</p></div>
<p class="about-text reveal d3">Vrem să eliminăm barierele financiare și sociale, oferind o <strong>șansă egală</strong> tuturor tinerilor, indiferent de situația de acasă.</p>
<div class="about-badge-row reveal d3">{badges}</div></div>
<div class="about-right"><div class="about-img-frame reveal"><img src="manusi.jpg" alt="Mănuși de box pregătite pentru antrenament la BMC Botoșani" width="800" height="600" loading="lazy" decoding="async"></div></div></div></section>
<section class="mission"><div class="mission-inner"><div class="section-label reveal">Misiunea noastră</div><div class="mission-grid"><div><div class="mission-quote reveal">Niciun talent irosit din<br><em>lipsă de resurse.</em></div></div><div class="mission-body">{mp}</div></div></div></section>
<section><div class="pillars"><div class="section-label reveal">Ce câștigi</div><h2 class="section-title reveal d1">De ce<br>acest sport?</h2><div class="pillars-grid">{pill}</div></div></section>
<section class="training"><div class="training-inner"><div class="section-label reveal">Cum funcționează</div><h2 class="section-title reveal d1">Cum ne<br>antrenăm?</h2>
<p class="reveal d2" style="font-size:1.1rem;font-weight:300;color:var(--ink2);max-width:560px">La noi <strong>tu alegi ritmul</strong>. Respectăm dorința fiecăruia. Mediul este unul de respect reciproc, fără judecată.</p><div class="training-list">{tr}</div></div></section>
<section class="contact"><div class="contact-inner"><div class="section-label reveal">Urmărește-ne</div><h2 class="section-title reveal d1">Fii parte<br>din comunitate</h2>
<p class="contact-sub reveal d2">Urmărește-ne parcursul pe rețelele sociale și fii primul care află noutăți.</p>
<div class="social-grid reveal d3">{SOC}<a href="mailto:botosanimma@gmail.com" class="social-btn soc-mail"><i class="fas fa-envelope"></i> Scrie-ne</a></div>
<div class="contact-cta reveal"><p>Gata să faci parte din echipă?</p>{CTA}</div></div></section></main>''')

# ───────── REGULAMENT ─────────
cards = (
 card(1, 'users-cog', 'Despre Noi', 'Structura și caracterul grupului', '<p>BMC Botoșani funcționează ca un grup de inițiativă sportivă comunitară (peer-to-peer), nu ca o sală comercială.</p>' + ul(
   li('Acces 100% Gratuit', 'Antrenamentele sunt și vor rămâne complet gratuite pentru toți participanții.', 1),
   li('Donații Voluntare', 'Pentru cei care vor să susțină proiectul, există posibilitatea donațiilor, în mod complet voluntar. Acestea ne ajută să acoperim cheltuielile și să continuăm antrenamentele — nu condiționează participarea.', 1),
   li('Mentori, Nu Antrenori Licențiați', 'Persoanele care coordonează sesiunile nu sunt antrenori licențiați. Aceștia sunt membri cu experiență care oferă suport voluntar, împărtășind din cunoștințele lor celorlalți participanți.', 1))) +
 card(2, 'balance-scale', 'Codul Penal &amp; Violența', 'Cea mai critică parte a pregătirii', '<p>Membrii trebuie să discearnă clar între sport și agresiune. Tehnicile învățate sunt instrumente de apărare și disciplină, nu de atac.</p>'
   '<div class="danger-inset"><h4><i class="fas fa-shield-alt"></i> Art. 19 — Legitima Apărare</h4><p>Tehnicile învățate pot fi folosite în afara sălii <strong>DOAR</strong> pentru a respinge un atac material, direct, imediat și injust.</p><p><strong>Regula de Aur:</strong> Riposta trebuie să fie proporțională cu pericolul. Orice exces transformă victima în agresor.</p></div>' + ul(
   li('Art. 193 — Lovirea și Violențele', 'Agresiunea nejustificată în afara cadrului sportiv atrage răspunderea penală individuală a celui care o comite.'),
   li('Consimțământul în Sală', 'Vătămările accidentale sunt considerate „asumarea riscului sportiv”, atâta timp cât se respectă regulile de siguranță și sparring-ul este controlat.'),
   li('Zero Toleranță la Violență Gratuită', 'Sparring-ul este controlat. Intenția de a răni partenerul duce la excluderea imediată și definitivă din grup.'))) +
 card(3, 'heartbeat', 'Sănătate &amp; Legea Sportului', 'Siguranța fizică este responsabilitatea fiecăruia', ul(
   li('Apt pentru Efort', 'Prin participare, declari pe proprie răspundere că ești apt medical. Recomandăm o adeverință de la medicul de familie.', 1),
   li('Protecția Minorilor', 'Cei sub 18 ani au nevoie <strong>obligatoriu</strong> de acordul scris al părinților sau tutorelui legal înainte de prima participare.', 1),
   li('Asigurare Medicală', 'Fiind o activitate gratuită, grupul nu oferă asigurare medicală. Recomandăm participanților să dețină o asigurare privată.', 1))) +
 card(4, 'user-shield', 'GDPR &amp; Dreptul la Imagine', 'Regulamentul European 679/2016', '<p>Respectăm intimitatea membrilor conform legislației europene în vigoare privind protecția datelor cu caracter personal.</p>' + ul(
   li('Foto &amp; Video', 'Antrenamentele pot fi filmate pentru analiză tehnică sau promovare (Social Media). Dacă nu dorești să apari, te rugăm să notifici coordonatorul înainte de ședință.'),
   li('Date Personale', 'Datele colectate la înscriere sunt folosite strict pentru organizarea grupului și nu sunt vândute. Lista completă a serviciilor terțe care le procesează este în <a href="confidentialitate.html">politica de confidențialitate</a>.'))) +
 card(5, 'gavel', 'Răspunderea Civilă', 'Volenti non fit injuria', '<p>Participarea implică o asumare conștientă a riscurilor inerente sporturilor de contact.</p>' + ul(
   li('Asumarea Riscului', 'Artele marțiale implică contact fizic. Vânătăile sau accidentările minore sunt posibile și reprezintă riscuri asumate prin participare.'),
   li('Exonerarea Coordonatorilor', 'Deoarece activitatea este gratuită și bazată pe voluntariat, coordonatorii nu pot fi trași la răspundere pentru accidentări, decât în caz de culpă gravă intenționată.'),
   li('Echipament Deteriorat', 'Orice echipament sau bun deteriorat din vina membrului va fi achitat integral de acesta, din fonduri proprii, nu din bugetul echipei BMC.'),
   li('Lipsa Echipamentului de Protecție', 'Participarea fără echipamentul de protecție recomandat anulează dreptul la orice reclamație privind accidentările survenite.'))) +
 card(6, 'shield-alt', 'Echipament &amp; Conduită', 'Reguli de bun-simț pentru o comunitate sănătoasă',
   '<div class="offer-box"><i class="fas fa-gift"></i><div><h4>Start-Up Pack — Echipament de Împrumut</h4><p>Pentru început, oferim echipament de împrumut timp de <strong>4 ședințe</strong>. Ulterior, din motive de igienă, echipamentul propriu devine obligatoriu. Vezi <a href="ghid.html">ghidul de echipament</a>.</p></div></div>' + ul(
   li('Respect Reciproc', 'Lipsa de respect față de membri sau coordonatori, precum și prezența sub influența alcoolului sau a drogurilor, duc la excludere definitivă.', 1),
   li('Igienă Obligatorie', 'Echipament curat, haine de schimb și unghii tăiate scurt — indispensabile pentru respectul față de partenerul de antrenament.', 1))) +
 card(7, 'door-open', 'Retragere &amp; Ștergerea Datelor', 'Poți pleca oricând', ul(
   li('Fără costuri, fără explicații', 'Participarea nu implică abonament sau perioadă de probă. Te poți opri oricând.', 1),
   li('Datele tale', 'Scrie la <a href="mailto:botosanimma@gmail.com">botosanimma@gmail.com</a> și îți ștergem datele în cel mult 30 de zile.', 1))))
page('p.html', 'Regulament și termeni — BMC Botoșani', 'Regulile grupului BMC Botoșani: siguranță, legitimă apărare, protecția minorilor, GDPR și echipament.', f'''<main id="continut">{hero2('Regulament', 'Regulament', '&amp; Termeni', 'Regulile care definesc comunitatea BMC — drepturi, obligații și responsabilități pentru toți membrii.')}
<div class="content-wrap">{cards}
<div class="rule-card reveal"><div class="rule-card-header"><div class="rule-icon"><i class="fas fa-file-signature"></i></div><div><div class="rule-card-title">Declarație de Asumare</div><div class="rule-card-sub">Acceptată implicit prin prezența la antrenamente</div></div></div><div class="rule-card-body">
<p>Prin prezența la antrenamente, membrul (sau tutorele legal, în cazul minorilor) înțelege și acceptă în mod explicit următoarele:</p>
<div class="mandatory-text">Declar că am înțeles caracterul voluntar al grupului BMC Botoșani și faptul că coordonatorii nu sunt antrenori certificați, ci mentori. Îmi asum întreaga responsabilitate pentru starea mea de sănătate și integritatea fizică. Mă angajez să nu folosesc tehnicile învățate în scopuri agresive, conform Art. 19 Cod Penal.</div>
<p>Coordonatorii își rezervă dreptul de a selecta participanții și de a refuza sau revoca accesul oricărei persoane care nu respectă valorile și regulile comunității BMC Botoșani.</p></div></div>
<div class="cta-strip reveal"><div><h3>Ai înțeles regulile?</h3><p>Acum e rândul tău să faci parte din echipă.</p></div>{CTA}</div></div></main>''', active='p.html')

# ───────── PROGRAM ─────────
page('time.html', 'Locație și program antrenamente — BMC Botoșani', 'Sala Arlechin, str. Mihai Eminescu 48, Botoșani, plus antrenamente în aer liber. Vezi orarul de toamnă, iarnă și vară.', f'''<main id="continut">{hero2('Locație &amp; Program', 'Locație &amp;', 'Program', 'Află unde ne antrenăm, cum arată o sesiune tipică și când ne putem vedea — toamnă, iarnă sau vară.')}
<div class="content-wrap">
{blk('map-marker-alt', 'Unde ne antrenăm', 'Locație fixă + aer liber · Botoșani',
  loc('dumbbell', 'Sala Arlechin', '<strong>Str. Mihai Eminescu nr. 48</strong>, Botoșani.<br>Sala noastră principală pentru antrenamentele de interior — MMA, pad work și sparring tehnic. <a href="despre.html#locatie">Vezi harta și indicațiile de drum</a>.') +
  loc('cloud-sun', 'Aer Liber', 'Antrenamente de calisthenics, alergare și condiție fizică generală în locații publice din Botoșani. <strong>Locul exact se anunță pe Instagram și în grupul de WhatsApp.</strong>') +
  loc('fist-raised', 'Disciplinele noastre', 'Combinăm <strong>MMA (Arte Marțiale Mixte)</strong> cu <strong>Calisthenics</strong> — tehnică marțială, mobilitate și forță cu greutatea corpului.') +
  '<div class="alert-banner"><i class="fas fa-bullhorn"></i><p><strong>Anunțuri importante:</strong> Locația exactă a fiecărui antrenament și orice schimbare de program se postează pe Instagram și în grupul intern de WhatsApp.</p></div>'
  '<a href="https://www.instagram.com/mma.botosani" target="_blank" rel="noopener" class="insta-btn"><i class="fab fa-instagram"></i> @mma.botosani</a>')}
{blk('stopwatch', 'Structura unui Antrenament', 'Sesiune tipică · ~2h', '<p style="color:var(--ink2);margin-bottom:22px">Fiecare sesiune este structurată pentru a maximiza rezultatele — de la mobilitate și condiție fizică până la tehnică marțială aplicată.</p><div class="routine-grid">' +
  routine(20, 'Încălzire Specifică', 'Fandări, pendulări, încălzirea articulațiilor și a coloanei vertebrale pentru mobilitate maximă și prevenirea accidentărilor.') +
  routine(30, 'Condiție Fizică · Calisthenics', 'Exerciții cu greutatea corpului: flotări, genuflexiuni, abdomene, cardio. Forță funcțională fără echipament.') +
  routine(30, 'Lucru cu Partenerul · Palmare', 'Exerciții de distanță, coordonare și timing cu manușile. Focus pe tehnică, nu pe forță.') +
  routine(30, 'Light Sparring &amp; Drill-uri', 'Sparring ușor opțional, drill-uri de reacție și exerciții explozive. Nimeni nu este forțat — ritmul îl alegi tu.') + '</div>', 'd1')}
{blk('calendar-alt', 'Orar Antrenamente', 'Toamnă/Iarnă · Vară', '<div class="schedule-grid">'
  '<div class="schedule-block"><div class="schedule-tag"><i class="fas fa-leaf"></i> Toamnă &amp; Iarnă</div><div class="schedule-title">Program de Toamnă / Iarnă</div><div class="schedule-rows">' + row('calendar-day', 'Ziua', '<strong>Sâmbătă</strong>') + row('dumbbell', 'La Sală', '12:30 – <strong>15:00</strong>') + row('cloud-sun', 'Aer Liber', '13:25 – <strong>16:00</strong>') + '</div><p class="schedule-note">Locația se confirmă săptămânal pe Instagram și WhatsApp în funcție de vreme și disponibilitate.</p></div>'
  '<div class="schedule-block"><div class="schedule-tag"><i class="fas fa-sun"></i> Vară</div><div class="schedule-title">Program de Vară</div><div class="schedule-rows">' + row('calendar-week', 'Zilele', '<strong>Luni, Marți, Joi</strong>') + row('clock', 'Interval', '18:00 – <strong>20:00</strong>') + row('calendar-week', 'Vineri', '<strong>08:00 – 10:00</strong>') + row('location-dot', 'Locație', 'Sală sau Aer Liber') + '</div><p class="schedule-note">Vara avem mai mult timp liber — frecvența crește semnificativ. E cel mai bun moment să începi!</p></div></div>'
  '<div class="contact-strip"><div><div class="contact-strip-title">Ai întrebări? Scrie-ne direct.</div><p style="color:var(--muted);font-size:.9rem">Contactează-ne pe WhatsApp sau prin email pentru detalii.</p></div><div class="contact-numbers"><a href="https://wa.me/40743780139" target="_blank" rel="noopener" class="phone-chip"><i class="fab fa-whatsapp"></i> 0743 780 139</a><a href="https://wa.me/40759855350" target="_blank" rel="noopener" class="phone-chip"><i class="fab fa-whatsapp"></i> 0759 855 350</a></div></div>', 'd2')}
<div style="text-align:center;padding:10px 0 30px"><p style="color:var(--muted);margin-bottom:18px">Gata să faci parte din echipă?</p>{CTA}</div></div></main>''', active='time.html')

# ───────── ÎNSCRIERE ─────────
fld = lambda lab, inner: f'<div class="form-group"><label for="{inner[0]}">{lab}</label>{inner[1]}</div>'
page('inscrie.html', 'Înscriere gratuită — BMC Botoșani', 'Completează formularul și intră în echipa BMC Botoșani. Antrenamentele sunt gratuite și nu ai nevoie de experiență.', f'''<div class="overlay" id="popupOverlay"><div class="popup"><img src="logo1.jpeg" alt="Logo BMC" width="80" height="80"><h2>Bun venit în BMC</h2>
<p>Vrei să vii în echipa BMC? Ne-ar plăcea să te avem alături! Te rugăm doar să arunci o privire peste regulament înainte de a începe, ca să fim siguri că suntem pe aceeași lungime de undă.</p>
<div class="popup-actions"><a href="p.html" class="btn btn-ghost"><i class="fas fa-file-shield"></i> Citește Regulamentul</a><button class="btn btn-primary" type="button" onclick="closePopup()"><i class="fas fa-check"></i> Accept și continui</button></div></div></div>
<main class="page-wrap" id="continut"><div class="form-outer"><div class="section-label">Înscrie-te</div><h1 class="page-title">Devino<em>Membru</em></h1>
<p style="color:var(--ink2);margin-top:14px">Intră în echipa BMC Botoșani și începe antrenamentul. Gratuit, fără obligații.</p>
<div class="form-card"><div class="form-card-header"><div class="t-icon"><i class="fas fa-user-plus"></i></div><div><h2>Formular de Înscriere</h2><p>Completează datele de mai jos</p></div></div><div class="form-body">
<form id="registrationForm"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_subject" value="Înscriere Nouă - BMC Botoșani!"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
{fld('Nume și Prenume', ('nume', '<input type="text" name="Nume complet" id="nume" placeholder="Numele tău complet" autocomplete="name" required>'))}
<div class="form-grid"><div class="form-group" style="margin:0"><label for="varsta">Vârstă</label><input type="number" name="Varsta" id="varsta" min="5" max="99" placeholder="Vârsta ta" required></div>
<div class="form-group" style="margin:0"><label for="experienta">Experiență</label><select name="Experienta" id="experienta"><option value="Incepator">Începător</option><option value="Mediu">Am mai practicat</option><option value="Avansat">Sportiv activ</option></select></div></div>
{fld('Adresă Email', ('email', '<input type="email" name="Email" id="email" placeholder="email@exemplu.com" autocomplete="email" required>'))}
{fld('Număr Telefon (opțional)', ('telefon', '<input type="tel" name="Telefon" id="telefon" placeholder="07xxxxxxxx" autocomplete="tel">'))}
{fld('Motivația ta', ('mesaj', '<textarea name="Mesaj" id="mesaj" rows="3" placeholder="De ce vrei să te alături echipei noastre?"></textarea>'))}
<div class="form-divider"></div>
<div class="fisa-block"><div class="fisa-block-title"><i class="fas fa-file-signature"></i> Termenii și Condițiile BMC</div><ul><li>Completarea formularului reprezintă acordul tău cu <a href="p.html" target="_blank">Termenii și Condițiile BMC</a>.</li><li>Finalizează procedura completând și Fișa Digitală de mai jos.</li></ul>
<a href="https://docs.google.com/forms/d/e/1FAIpQLSdZOIzMcuUNbahjI9xVaRNWa5Ny-XMbS5XguY6q_BJT60MftQ/viewform" target="_blank" rel="noopener" class="btn-fisa"><i class="fas fa-external-link-alt"></i> Completează Fișa Digitală</a></div>
<div class="check-group green-check"><input type="checkbox" id="check_fisa_digitala" name="Fisa_Digitala_Completata" value="DA" required><label for="check_fisa_digitala">Confirm că am completat <strong>Fișa Digitală</strong>.</label></div>
<div class="check-group"><input type="checkbox" id="termeni" name="Acord_Regulament" required><label for="termeni">Confirm că am citit regulamentul, înțeleg că antrenamentele se desfășoară pe propria răspundere și respect codul BMC.</label></div>
<button type="submit" class="btn-submit" id="submitBtn"><i class="fas fa-paper-plane"></i> Trimite Înscrierea</button></form></div></div></div></main>''', active='', extra_head='')

# ───────── ISTORIC + THANKS ─────────
page('istoric.html', 'Arhiva sesiunilor de sparring tehnic — BMC Botoșani', 'Arhiva sesiunilor de sparring tehnic ale grupului BMC Botoșani.', f'''<main id="continut">{hero2('Arhivă', 'Istoric', 'Evoluție', 'Arhivă tehnică a sesiunilor de sparring ale grupului.')}
<div class="content-wrap"><div class="alert-banner"><i class="fas fa-circle-info"></i><p><strong>Important:</strong> Această arhivă conține sesiuni de <strong>SPARRING TEHNIC</strong>. Acestea nu sunt lupte de stradă sau agresiuni, ci exerciții de pregătire sportivă desfășurate în siguranță.</p></div>
<div class="empty-state"><h2 class="section-title" style="font-size:2rem">Arhiva se construiește</h2><p style="color:var(--ink2)">Nu avem încă sesiuni publicate. Când postăm primele filmări, vor apărea aici. Între timp vezi <a href="time.html">programul antrenamentelor</a> sau urmărește-ne pe <a href="https://www.youtube.com/@mma.botosani" target="_blank" rel="noopener">YouTube</a>.</p></div></div></main>''', idx=False, nt=True)
page('s.html', 'Cerere trimisă — BMC Botoșani', 'Am primit cererea ta de înscriere.', f'''<main id="continut" style="display:flex;padding:24px"><div class="success-container"><img src="logo1.jpeg" alt="Logo BMC" width="104" height="104"><h1>Cerere trimisă!</h1>
<p>Am primit datele tale. Echipa <strong>BMC Botoșani</strong> te va contacta în termen de 24–48 ore pentru confirmare.</p><div class="social-grid">{SOC}</div><a href="index.html" class="btn btn-ghost" style="width:100%"><i class="fas fa-arrow-left"></i> Înapoi la site</a></div></main>''', idx=False, nt=True, hdr=False)

# ───────── pagini deja făcute (despre, confidențialitate, 404): titlu/meta + meniu subsol ─────────
for fn, t, d, idx in [('despre.html', 'Ce este BMC Botoșani — sport gratuit, locație și hartă', 'Află ce este BMC Botoșani, cum arată un antrenament, unde ne găsești (Sala Arlechin, Botoșani, cu hartă), programul și cum te înscrii.', 1),
                      ('confidentialitate.html', 'Politica de confidențialitate — BMC Botoșani', 'Ce date colectăm, cu cine le împărțim și cum le poți șterge.', 1),
                      ('404.html', 'Pagina nu există — BMC Botoșani', 'Pagina căutată nu există.', 0)]:
    s = open(os.path.join(HERE, fn), encoding='utf-8').read()
    s = re.sub(r'<meta name="description"[^>]*>\s*', '', s)
    s = re.sub(r'<title>.*?</title>', lambda m: meta(fn, t, d, idx).strip(), s, count=1, flags=re.S)
    s = s.replace('logo1.jpeg" alt="Logo BMC" ', 'logo1.jpeg" alt="Logo BMC" width="48" height="48" ') if 'width=' not in s[:3000] else s
    if 'foot-nav' not in s: s = s.replace('</footer>', FNAV + '</footer>', 1)
    s = s.replace('<link rel="stylesheet" href="bmc.min.css">', '<link rel="stylesheet" href="site.min.css"><link rel="stylesheet" href="bmc.min.css">', 1) if 'site.min.css' not in s else s
    s = re.sub(r'bmc\.css', 'bmc.min.css', re.sub(r'bmc\.js', 'bmc.min.js', s)) if 'bmc.min' not in s else s
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(s)

if B:
    open(os.path.join(OUT, 'CNAME'), 'w').write(D + '\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {B}/sitemap.xml\n')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{u}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n' for u in SITEMAP) + '</urlset>\n')
for f in ('og-image.png',):
    if os.path.exists(os.path.join(HERE, f)): shutil.copy(os.path.join(HERE, f), OUT)
print('OK', len(os.listdir(OUT)), 'fișiere în', OUT)
