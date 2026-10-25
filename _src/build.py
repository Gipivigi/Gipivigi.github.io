#!/usr/bin/env python3
"""Genera le pagine del sito in tutte le lingue.

Uso:  python3 _src/build.py
Prima di pubblicare cambia BASE_URL con l’indirizzo vero del tuo sito.
"""
import json
from pathlib import Path
from urllib.parse import quote

# >>> CAMBIA QUI con l’indirizzo del tuo sito GitHub Pages (con la barra finale) <<<
BASE_URL = "https://gipivigi.github.io/"

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")

# La prima lingua va nella cartella principale del sito, le altre in sottocartelle.
ORDER = ["en", "it", "es", "fr", "de", "pt"]
NBSP = "\u202f"

T = {
"en": dict(
  name="English", locale="en", og="en_US",
  title="Unit Circle – exact sin, cos and tan for any angle",
  description="Free interactive unit circle: type any angle in radians or degrees and get exact sine, cosine and tangent values as fractions, like √3/2. Works on phones.",
  h1="Unit circle",
  sub="Type an angle in radians with π, or in degrees, and see exactly where it lands. Sine, cosine and tangent are written as exact fractions for the special angles.",
  label_angle="Angle", show="Show", keypad="Insert a symbol", copy="Copy link", copied="Link copied",
  hint="Try 3π/4, −π/6, 7π/3, 2.5 or 135°. You can also drag the point around the circle.",
  err="Can’t read that angle. Try 3π/4, -pi/6 or 135°.",
  quadrants=["first quadrant", "second quadrant", "third quadrant", "fourth quadrant"],
  axes="on an axis", equiv="same point as", undef="undefined",
  sin="sin", tan="tan",
  note="Cosine is the x-coordinate of the point (red), sine is the y-coordinate (green).",
  svg_aria="Unit circle showing the chosen angle. Drag the point, or use the arrow keys to move by π/12.",
  table_title="Special angles",
  table_intro="The values worth knowing by heart: every other special angle follows from these by symmetry. Tap an angle to see it on the circle.",
  col_deg="Degrees", col_rad="Radians",
  how_title="How to read the unit circle",
  how=["The unit circle has radius 1 and its centre at the origin. Every angle θ, measured anticlockwise from the positive x-axis, picks out exactly one point on it.",
       "The coordinates of that point are (cos θ, sin θ). Cosine tells you how far the point is to the right or left, sine how far it is up or down, and tan θ = sin θ / cos θ is the slope of the radius.",
       "Angles that differ by a full turn, 2π or 360°, land on the same point, which is why sine and cosine repeat. Negative angles go clockwise.",
       "Every result has its own link, so you can send a specific angle to a classmate or keep it for revision."],
  footer="Free, made for students.", language="Language", close="Close",
  suggest_text="This page is also available in English.", suggest_link="Switch to English",
),
"it": dict(
  name="Italiano", locale="it", og="it_IT",
  title="Circonferenza goniometrica interattiva – seno e coseno esatti di ogni angolo",
  description="Circonferenza goniometrica interattiva e gratuita: inserisci un angolo in radianti o in gradi e ottieni seno, coseno e tangente esatti, come √3/2. Funziona anche sul telefono.",
  h1="Circonferenza goniometrica",
  sub="Scrivi un angolo in radianti con π, oppure in gradi, e guarda dove cade sulla circonferenza. Per gli angoli notevoli seno, coseno e tangente sono scritti come frazioni esatte.",
  label_angle="Angolo", show="Mostra", keypad="Inserisci un simbolo", copy="Copia link", copied="Link copiato",
  hint="Prova con 3π/4, −π/6, 7π/3, 2,5 oppure 135°. Puoi anche trascinare il punto lungo la circonferenza.",
  err="Non riesco a leggere l’angolo. Prova con 3π/4, -pi/6 oppure 135°.",
  quadrants=["primo quadrante", "secondo quadrante", "terzo quadrante", "quarto quadrante"],
  axes="sugli assi", equiv="stesso punto di", undef="non definita",
  sin="sen", tan="tan",
  note="Il coseno è l’ascissa del punto (rosso), il seno è l’ordinata (verde).",
  svg_aria="Circonferenza goniometrica con l’angolo scelto. Trascina il punto oppure usa le frecce per spostarti di π/12.",
  table_title="Angoli notevoli",
  table_intro="I valori da sapere a memoria: tutti gli altri angoli notevoli si ricavano da questi per simmetria. Tocca un angolo per vederlo sulla circonferenza.",
  col_deg="Gradi", col_rad="Radianti",
  how_title="Come si legge la circonferenza goniometrica",
  how=["La circonferenza goniometrica ha raggio 1 e centro nell’origine. Ogni angolo θ, misurato in senso antiorario a partire dal semiasse positivo delle x, individua un solo punto della circonferenza.",
       "Le coordinate di quel punto sono (cos θ, sen θ): il coseno dice quanto il punto è a destra o a sinistra, il seno quanto è in alto o in basso, e tan θ = sen θ / cos θ è la pendenza del raggio.",
       "Angoli che differiscono di un giro completo, 2π o 360°, finiscono nello stesso punto: per questo seno e coseno sono periodici. Gli angoli negativi si misurano in senso orario.",
       "Ogni risultato ha il suo link, così puoi mandare un angolo preciso a un compagno o salvarlo per il ripasso."],
  footer="Gratuito, fatto per gli studenti.", language="Lingua", close="Chiudi",
  suggest_text="Questa pagina è disponibile anche in italiano.", suggest_link="Passa all’italiano",
),
"es": dict(
  name="Español", locale="es", og="es_ES",
  title="Circunferencia unitaria interactiva – seno y coseno exactos de cualquier ángulo",
  description="Circunferencia unitaria (goniométrica) interactiva y gratuita: escribe un ángulo en radianes o grados y obtén el seno, el coseno y la tangente exactos, como √3/2.",
  h1="Circunferencia unitaria",
  sub="Escribe un ángulo en radianes con π, o en grados, y mira dónde cae. Para los ángulos notables, el seno, el coseno y la tangente aparecen como fracciones exactas.",
  label_angle="Ángulo", show="Mostrar", keypad="Insertar un símbolo", copy="Copiar enlace", copied="Enlace copiado",
  hint="Prueba con 3π/4, −π/6, 7π/3, 2,5 o 135°. También puedes arrastrar el punto por la circunferencia.",
  err="No se puede leer ese ángulo. Prueba con 3π/4, -pi/6 o 135°.",
  quadrants=["primer cuadrante", "segundo cuadrante", "tercer cuadrante", "cuarto cuadrante"],
  axes="sobre un eje", equiv="mismo punto que", undef="no definida",
  sin="sen", tan="tan",
  note="El coseno es la coordenada x del punto (rojo) y el seno es la coordenada y (verde).",
  svg_aria="Circunferencia unitaria con el ángulo elegido. Arrastra el punto o usa las flechas para moverte de π/12 en π/12.",
  table_title="Ángulos notables",
  table_intro="Los valores que conviene saber de memoria: los demás ángulos notables se obtienen de estos por simetría. Toca un ángulo para verlo en la circunferencia.",
  col_deg="Grados", col_rad="Radianes",
  how_title="Cómo leer la circunferencia unitaria",
  how=["La circunferencia unitaria tiene radio 1 y centro en el origen. Cada ángulo θ, medido en sentido antihorario desde el semieje x positivo, determina un único punto sobre ella.",
       "Las coordenadas de ese punto son (cos θ, sen θ): el coseno indica cuánto está el punto a la derecha o a la izquierda, el seno cuánto está arriba o abajo, y tan θ = sen θ / cos θ es la pendiente del radio.",
       "Los ángulos que se diferencian en una vuelta completa, 2π o 360°, caen en el mismo punto: por eso el seno y el coseno son periódicos. Los ángulos negativos van en sentido horario.",
       "Cada resultado tiene su propio enlace, así que puedes enviar un ángulo concreto a un compañero o guardarlo para repasar."],
  footer="Gratis, hecho para estudiantes.", language="Idioma", close="Cerrar",
  suggest_text="Esta página también está disponible en español.", suggest_link="Ver en español",
),
"fr": dict(
  name="Français", locale="fr", og="fr_FR",
  title="Cercle trigonométrique interactif – sinus et cosinus exacts de tout angle",
  description=f"Cercle trigonométrique interactif et gratuit{NBSP}: saisis un angle en radians ou en degrés et obtiens le sinus, le cosinus et la tangente exacts, comme √3/2.",
  h1="Cercle trigonométrique",
  sub="Saisis un angle en radians avec π, ou en degrés, et vois exactement où il tombe. Pour les angles remarquables, le sinus, le cosinus et la tangente s’affichent en valeurs exactes.",
  label_angle="Angle", show="Afficher", keypad="Insérer un symbole", copy="Copier le lien", copied="Lien copié",
  hint="Essaie 3π/4, −π/6, 7π/3, 2,5 ou 135°. Tu peux aussi faire glisser le point sur le cercle.",
  err="Impossible de lire cet angle. Essaie 3π/4, -pi/6 ou 135°.",
  quadrants=["premier quadrant", "deuxième quadrant", "troisième quadrant", "quatrième quadrant"],
  axes="sur un axe", equiv="même point que", undef="non définie",
  sin="sin", tan="tan",
  note="Le cosinus est l’abscisse du point (rouge), le sinus est son ordonnée (vert).",
  svg_aria="Cercle trigonométrique avec l’angle choisi. Fais glisser le point ou utilise les flèches pour avancer de π/12.",
  table_title="Angles remarquables",
  table_intro=f"Les valeurs à connaître par cœur{NBSP}: tous les autres angles remarquables s’en déduisent par symétrie. Touche un angle pour le voir sur le cercle.",
  col_deg="Degrés", col_rad="Radians",
  how_title="Comment lire le cercle trigonométrique",
  how=["Le cercle trigonométrique a pour rayon 1 et pour centre l’origine. Chaque angle θ, mesuré dans le sens inverse des aiguilles d’une montre à partir de l’axe des abscisses positif, correspond à un seul point du cercle.",
       f"Les coordonnées de ce point sont (cos θ, sin θ){NBSP}: le cosinus indique de combien le point est à droite ou à gauche, le sinus de combien il est en haut ou en bas, et tan θ = sin θ / cos θ est la pente du rayon.",
       f"Deux angles qui diffèrent d’un tour complet, 2π ou 360°, tombent sur le même point{NBSP}: c’est pour cela que le sinus et le cosinus sont périodiques. Les angles négatifs se mesurent dans le sens des aiguilles d’une montre.",
       f"Chaque résultat a son propre lien{NBSP}: tu peux envoyer un angle précis à un camarade ou le garder pour réviser."],
  footer="Gratuit, fait pour les élèves.", language="Langue", close="Fermer",
  suggest_text="Cette page est aussi disponible en français.", suggest_link="Passer au français",
),
"de": dict(
  name="Deutsch", locale="de", og="de_DE",
  title="Einheitskreis interaktiv – exakte Sinus- und Kosinuswerte für jeden Winkel",
  description="Kostenloser interaktiver Einheitskreis: Winkel im Bogenmaß oder in Grad eingeben und exakte Werte für Sinus, Kosinus und Tangens erhalten, zum Beispiel √3/2.",
  h1="Einheitskreis",
  sub="Gib einen Winkel im Bogenmaß mit π oder in Grad ein und sieh genau, wo er landet. Für die besonderen Winkel werden Sinus, Kosinus und Tangens als exakte Brüche angezeigt.",
  label_angle="Winkel", show="Anzeigen", keypad="Symbol einfügen", copy="Link kopieren", copied="Link kopiert",
  hint="Probier 3π/4, −π/6, 7π/3, 2,5 oder 135°. Du kannst den Punkt auch auf dem Kreis ziehen.",
  err="Dieser Winkel lässt sich nicht lesen. Probier 3π/4, -pi/6 oder 135°.",
  quadrants=["erster Quadrant", "zweiter Quadrant", "dritter Quadrant", "vierter Quadrant"],
  axes="auf einer Achse", equiv="gleicher Punkt wie", undef="nicht definiert",
  sin="sin", tan="tan",
  note="Der Kosinus ist die x-Koordinate des Punktes (rot), der Sinus die y-Koordinate (grün).",
  svg_aria="Einheitskreis mit dem gewählten Winkel. Zieh den Punkt oder benutze die Pfeiltasten, um in Schritten von π/12 weiterzugehen.",
  table_title="Besondere Winkel",
  table_intro="Die Werte, die man auswendig kennen sollte: Alle anderen besonderen Winkel folgen daraus durch Symmetrie. Tippe auf einen Winkel, um ihn auf dem Kreis zu sehen.",
  col_deg="Grad", col_rad="Bogenmaß",
  how_title="So liest man den Einheitskreis",
  how=["Der Einheitskreis hat den Radius 1 und den Mittelpunkt im Ursprung. Jeder Winkel θ, gegen den Uhrzeigersinn ab der positiven x-Achse gemessen, legt genau einen Punkt auf dem Kreis fest.",
       "Die Koordinaten dieses Punktes sind (cos θ, sin θ): Der Kosinus sagt, wie weit der Punkt rechts oder links liegt, der Sinus, wie weit oben oder unten, und tan θ = sin θ / cos θ ist die Steigung des Radius.",
       "Winkel, die sich um eine volle Umdrehung unterscheiden, also um 2π oder 360°, landen auf demselben Punkt. Deshalb sind Sinus und Kosinus periodisch. Negative Winkel laufen im Uhrzeigersinn.",
       "Jedes Ergebnis hat einen eigenen Link, so kannst du einen bestimmten Winkel an Mitschüler schicken oder zum Lernen speichern."],
  footer="Kostenlos, gemacht für Schülerinnen und Schüler.", language="Sprache", close="Schließen",
  suggest_text="Diese Seite gibt es auch auf Deutsch.", suggest_link="Auf Deutsch ansehen",
),
"pt": dict(
  name="Português", locale="pt-BR", og="pt_BR",
  title="Círculo trigonométrico interativo – seno e cosseno exatos de qualquer ângulo",
  description="Círculo trigonométrico interativo e gratuito: digite um ângulo em radianos ou graus e obtenha seno, cosseno e tangente exatos, como √3/2. Funciona no celular.",
  h1="Círculo trigonométrico",
  sub="Digite um ângulo em radianos com π, ou em graus, e veja exatamente onde ele cai. Para os ângulos notáveis, o seno, o cosseno e a tangente aparecem como frações exatas.",
  label_angle="Ângulo", show="Mostrar", keypad="Inserir um símbolo", copy="Copiar link", copied="Link copiado",
  hint="Experimente 3π/4, −π/6, 7π/3, 2,5 ou 135°. Você também pode arrastar o ponto pelo círculo.",
  err="Não foi possível ler esse ângulo. Experimente 3π/4, -pi/6 ou 135°.",
  quadrants=["primeiro quadrante", "segundo quadrante", "terceiro quadrante", "quarto quadrante"],
  axes="sobre um eixo", equiv="mesmo ponto que", undef="não definida",
  sin="sen", tan="tan",
  note="O cosseno é a coordenada x do ponto (vermelho) e o seno é a coordenada y (verde).",
  svg_aria="Círculo trigonométrico com o ângulo escolhido. Arraste o ponto ou use as setas para avançar de π/12 em π/12.",
  table_title="Ângulos notáveis",
  table_intro="Os valores que vale a pena saber de cor: todos os outros ângulos notáveis saem destes por simetria. Toque num ângulo para vê-lo no círculo.",
  col_deg="Graus", col_rad="Radianos",
  how_title="Como ler o círculo trigonométrico",
  how=["O círculo trigonométrico tem raio 1 e centro na origem. Cada ângulo θ, medido no sentido anti-horário a partir do semieixo x positivo, determina um único ponto do círculo.",
       "As coordenadas desse ponto são (cos θ, sen θ): o cosseno diz o quanto o ponto está à direita ou à esquerda, o seno o quanto está acima ou abaixo, e tan θ = sen θ / cos θ é a inclinação do raio.",
       "Ângulos que diferem por uma volta completa, 2π ou 360°, caem no mesmo ponto: é por isso que o seno e o cosseno são periódicos. Ângulos negativos vão no sentido horário.",
       "Cada resultado tem o seu próprio link, então você pode mandar um ângulo específico para um colega ou guardá-lo para revisar."],
  footer="Gratuito, feito para estudantes.", language="Idioma", close="Fechar",
  suggest_text="Esta página também está disponível em português.", suggest_link="Ver em português",
),
}


# Sulla pagina principale: porta il visitatore nella sua lingua, la prima volta.
# Se ha già scelto una lingua dal menu, rispetta la sua scelta. I motori di ricerca restano sulla pagina.
AUTOLANG = """<script>
(function () {
  try {
    var A = __AVAIL__, s = null, t = null;
    if (navigator.webdriver || /bot|crawl|spider|slurp|preview|lighthouse/i.test(navigator.userAgent)) return;
    try { s = localStorage.getItem('ucLang'); } catch (e) {}
    if (s) { if (A.indexOf(s) > 0) t = s; }
    else {
      var p = navigator.languages || [navigator.language || ''];
      for (var i = 0; i < p.length; i++) {
        var l = String(p[i]).slice(0, 2).toLowerCase();
        if (A.indexOf(l) >= 0) { if (l !== A[0]) t = l; break; }
      }
    }
    if (t) location.replace(t + '/' + (location.protocol === 'file:' ? 'index.html' : '') + location.search + location.hash);
  } catch (e) {}
})();
</script>"""


# Testi aggiuntivi pensati per le ricerche reali degli studenti in ogni paese.
EXTRA = {
"en": dict(
  title="Unit Circle – exact sin, cos and tan values, chart and calculator",
  description="Interactive unit circle with a full chart of special angles: type any angle in radians or degrees and get exact sine, cosine and tangent values like √3/2. Free, works on phones.",
  alt_names=["Unit circle", "Trigonometric circle", "Unit circle chart", "Unit circle calculator"],
  how0="The unit circle, also called the trigonometric circle, has radius 1 and its centre at the origin. Every angle θ, measured anticlockwise from the positive x-axis, picks out exactly one point on it.",
  table_title="Unit circle chart: all special angles",
  table_intro="Every special angle from 0 to 2π, that is from 0° to 360°, with exact sine, cosine and tangent values. The highlighted rows in the first quadrant are the ones to learn by heart; the rest follow by symmetry. Tap an angle to see it on the circle.",
  faq_title="Frequently asked questions",
  faq=[
    ("What are sin and cos of 30°, 45° and 60°?", "sin 30° = 1/2 and cos 30° = √3/2; sin 45° = cos 45° = √2/2; sin 60° = √3/2 and cos 60° = 1/2. In radians these angles are π/6, π/4 and π/3."),
    ("How do you convert degrees to radians?", "Multiply by π/180: for example 135° = 135 × π/180 = 3π/4. To go back to degrees, multiply by 180/π. This page accepts both: just add ° for degrees."),
    ("Is there an easy way to remember the unit circle values?", "For 0°, 30°, 45°, 60° and 90° the sine is √0/2, √1/2, √2/2, √3/2 and √4/2, that is 0, 1/2, √2/2, √3/2 and 1. The cosine follows the same sequence backwards."),
    ("Why is tan 90° undefined?", "Because tan θ = sin θ / cos θ and cos 90° = 0, so you would be dividing by zero. The same happens at every angle of the form π/2 + kπ, such as 90° and 270°."),
    ("How do you find sin and cos of angles bigger than 90°?", "Use the symmetry of the circle. For example 150° is the mirror image of 30° across the y-axis, so sin 150° = sin 30° = 1/2 and cos 150° = −cos 30° = −√3/2. The sign depends on the quadrant the point lands in."),
  ],
),
"it": dict(
  title="Circonferenza goniometrica interattiva – angoli notevoli, seno, coseno e tangente",
  description="Circonferenza goniometrica interattiva con la tabella completa degli angoli notevoli: inserisci un angolo in radianti o in gradi e ottieni seno, coseno e tangente esatti, come √3/2.",
  alt_names=["Circonferenza goniometrica", "Cerchio goniometrico", "Circonferenza trigonometrica", "Tabella angoli notevoli"],
  how0="La circonferenza goniometrica, chiamata anche cerchio goniometrico o circonferenza trigonometrica, ha raggio 1 e centro nell’origine. Ogni angolo θ, misurato in senso antiorario a partire dal semiasse positivo delle x, individua un solo punto della circonferenza.",
  table_title="Tabella degli angoli notevoli",
  table_intro="Tutti gli angoli notevoli da 0 a 2π, cioè da 0° a 360°, con i valori esatti di seno, coseno e tangente. Le righe evidenziate del primo quadrante sono quelle da sapere a memoria: le altre si ricavano per simmetria. Tocca un angolo per vederlo sulla circonferenza.",
  faq_title="Domande frequenti",
  faq=[
    ("Quanto valgono seno e coseno di 30°, 45° e 60°?", "sen 30° = 1/2 e cos 30° = √3/2; sen 45° = cos 45° = √2/2; sen 60° = √3/2 e cos 60° = 1/2. In radianti questi angoli sono π/6, π/4 e π/3."),
    ("Come si passa dai gradi ai radianti?", "Si moltiplica per π/180: per esempio 135° = 135 · π/180 = 3π/4. Per tornare ai gradi si moltiplica per 180/π. Questa pagina accetta entrambe le scritture: per i gradi basta aggiungere °."),
    ("C’è un trucco per ricordare i valori degli angoli notevoli?", "Per 0°, 30°, 45°, 60° e 90° il seno vale √0/2, √1/2, √2/2, √3/2 e √4/2, cioè 0, 1/2, √2/2, √3/2 e 1. Il coseno segue la stessa sequenza al contrario."),
    ("Perché la tangente di 90° non esiste?", "Perché tan θ = sen θ / cos θ e cos 90° = 0: si dovrebbe dividere per zero. Succede per tutti gli angoli del tipo π/2 + kπ, come 90° e 270°."),
    ("Come si trovano seno e coseno di angoli maggiori di 90°?", "Si sfrutta la simmetria della circonferenza. Per esempio 150° è il simmetrico di 30° rispetto all’asse y, quindi sen 150° = sen 30° = 1/2 e cos 150° = −cos 30° = −√3/2. Il segno dipende dal quadrante in cui cade il punto."),
  ],
),
"es": dict(
  title="Circunferencia unitaria (goniométrica) – seno, coseno y tangente exactos",
  description="Circunferencia unitaria interactiva con la tabla completa de ángulos notables: escribe un ángulo en radianes o grados y obtén el seno, el coseno y la tangente exactos, como √3/2.",
  alt_names=["Circunferencia unitaria", "Circunferencia goniométrica", "Círculo unitario", "Círculo trigonométrico", "Tabla de ángulos notables"],
  how0="La circunferencia unitaria, también llamada circunferencia goniométrica, círculo unitario o círculo trigonométrico, tiene radio 1 y centro en el origen. Cada ángulo θ, medido en sentido antihorario desde el semieje x positivo, determina un único punto sobre ella.",
  table_title="Tabla de ángulos notables",
  table_intro="Todos los ángulos notables de 0 a 2π, es decir de 0° a 360°, con los valores exactos de seno, coseno y tangente. Las filas resaltadas del primer cuadrante son las que conviene saber de memoria: las demás se obtienen por simetría. Toca un ángulo para verlo en la circunferencia.",
  faq_title="Preguntas frecuentes",
  faq=[
    ("¿Cuánto valen el seno y el coseno de 30°, 45° y 60°?", "sen 30° = 1/2 y cos 30° = √3/2; sen 45° = cos 45° = √2/2; sen 60° = √3/2 y cos 60° = 1/2. En radianes estos ángulos son π/6, π/4 y π/3."),
    ("¿Cómo se pasa de grados a radianes?", "Se multiplica por π/180: por ejemplo 135° = 135 · π/180 = 3π/4. Para volver a grados se multiplica por 180/π. Esta página acepta las dos formas: para grados basta con añadir °."),
    ("¿Hay un truco para recordar los valores de los ángulos notables?", "Para 0°, 30°, 45°, 60° y 90° el seno vale √0/2, √1/2, √2/2, √3/2 y √4/2, es decir 0, 1/2, √2/2, √3/2 y 1. El coseno sigue la misma secuencia al revés."),
    ("¿Por qué no existe la tangente de 90°?", "Porque tan θ = sen θ / cos θ y cos 90° = 0, así que habría que dividir entre cero. Pasa con todos los ángulos de la forma π/2 + kπ, como 90° y 270°."),
    ("¿Cómo se calculan el seno y el coseno de ángulos mayores de 90°?", "Se usa la simetría de la circunferencia. Por ejemplo, 150° es simétrico de 30° respecto al eje y, así que sen 150° = sen 30° = 1/2 y cos 150° = −cos 30° = −√3/2. El signo depende del cuadrante en el que cae el punto."),
  ],
),
"fr": dict(
  title="Cercle trigonométrique interactif – valeurs remarquables de sin, cos et tan",
  description=f"Cercle trigonométrique interactif avec le tableau complet des valeurs remarquables{NBSP}: saisis un angle en radians ou en degrés et obtiens sinus, cosinus et tangente exacts, comme √3/2.",
  alt_names=["Cercle trigonométrique", "Cercle unité", "Tableau des valeurs remarquables"],
  how0="Le cercle trigonométrique, aussi appelé cercle unité, a pour rayon 1 et pour centre l’origine. Chaque angle θ, mesuré dans le sens inverse des aiguilles d’une montre à partir de l’axe des abscisses positif, correspond à un seul point du cercle.",
  table_title="Tableau des valeurs remarquables",
  table_intro=f"Tous les angles remarquables de 0 à 2π, c’est-à-dire de 0° à 360°, avec les valeurs exactes du sinus, du cosinus et de la tangente. Les lignes surlignées du premier quadrant sont à connaître par cœur{NBSP}: les autres s’en déduisent par symétrie. Touche un angle pour le voir sur le cercle.",
  faq_title="Questions fréquentes",
  faq=[
    (f"Que valent le sinus et le cosinus de 30°, 45° et 60°{NBSP}?", "sin 30° = 1/2 et cos 30° = √3/2 ; sin 45° = cos 45° = √2/2 ; sin 60° = √3/2 et cos 60° = 1/2. En radians, ces angles valent π/6, π/4 et π/3."),
    (f"Comment convertir des degrés en radians{NBSP}?", f"On multiplie par π/180{NBSP}: par exemple 135° = 135 × π/180 = 3π/4. Pour revenir aux degrés, on multiplie par 180/π. Cette page accepte les deux écritures{NBSP}: pour les degrés, il suffit d’ajouter °."),
    (f"Existe-t-il une astuce pour retenir les valeurs remarquables{NBSP}?", "Pour 0°, 30°, 45°, 60° et 90°, le sinus vaut √0/2, √1/2, √2/2, √3/2 et √4/2, soit 0, 1/2, √2/2, √3/2 et 1. Le cosinus suit la même suite à l’envers."),
    (f"Pourquoi la tangente de 90° n’existe-t-elle pas{NBSP}?", "Parce que tan θ = sin θ / cos θ et cos 90° = 0 : il faudrait diviser par zéro. C’est le cas pour tous les angles de la forme π/2 + kπ, comme 90° et 270°."),
    (f"Comment trouver le sinus et le cosinus d’un angle supérieur à 90°{NBSP}?", "On utilise la symétrie du cercle. Par exemple, 150° est le symétrique de 30° par rapport à l’axe des ordonnées, donc sin 150° = sin 30° = 1/2 et cos 150° = −cos 30° = −√3/2. Le signe dépend du quadrant où tombe le point."),
  ],
),
"de": dict(
  title="Einheitskreis interaktiv – Sinus, Kosinus und Tangens exakt, mit Tabelle",
  description="Interaktiver Einheitskreis mit vollständiger Tabelle der besonderen Werte: Winkel im Bogenmaß oder in Grad eingeben und exakte Werte für Sinus, Kosinus und Tangens erhalten, zum Beispiel √3/2.",
  alt_names=["Einheitskreis", "Trigonometrischer Kreis", "Einheitskreis Tabelle"],
  how0="Der Einheitskreis, auch trigonometrischer Kreis genannt, hat den Radius 1 und den Mittelpunkt im Ursprung. Jeder Winkel θ, gegen den Uhrzeigersinn ab der positiven x-Achse gemessen, legt genau einen Punkt auf dem Kreis fest.",
  table_title="Einheitskreis-Tabelle: alle besonderen Werte",
  table_intro="Alle besonderen Winkel von 0 bis 2π, also von 0° bis 360°, mit den exakten Werten für Sinus, Kosinus und Tangens. Die hervorgehobenen Zeilen im ersten Quadranten sollte man auswendig kennen, der Rest folgt durch Symmetrie. Tippe auf einen Winkel, um ihn auf dem Kreis zu sehen.",
  faq_title="Häufige Fragen",
  faq=[
    ("Was sind Sinus und Kosinus von 30°, 45° und 60°?", "sin 30° = 1/2 und cos 30° = √3/2; sin 45° = cos 45° = √2/2; sin 60° = √3/2 und cos 60° = 1/2. Im Bogenmaß sind diese Winkel π/6, π/4 und π/3."),
    ("Wie rechnet man Grad in Bogenmaß um?", "Man multipliziert mit π/180, zum Beispiel 135° = 135 · π/180 = 3π/4. Zurück in Grad geht es mit 180/π. Diese Seite versteht beides: Für Grad einfach ° anhängen."),
    ("Gibt es einen Trick, um sich die Werte am Einheitskreis zu merken?", "Für 0°, 30°, 45°, 60° und 90° ist der Sinus √0/2, √1/2, √2/2, √3/2 und √4/2, also 0, 1/2, √2/2, √3/2 und 1. Der Kosinus durchläuft dieselbe Folge rückwärts."),
    ("Warum ist der Tangens von 90° nicht definiert?", "Weil tan θ = sin θ / cos θ und cos 90° = 0 ist, man müsste also durch null teilen. Das gilt für alle Winkel der Form π/2 + kπ, etwa 90° und 270°."),
    ("Wie findet man Sinus und Kosinus von Winkeln über 90°?", "Mit der Symmetrie des Kreises. Zum Beispiel ist 150° das Spiegelbild von 30° an der y-Achse, also sin 150° = sin 30° = 1/2 und cos 150° = −cos 30° = −√3/2. Das Vorzeichen hängt vom Quadranten ab, in dem der Punkt liegt."),
  ],
),
"pt": dict(
  title="Círculo trigonométrico interativo – seno, cosseno e tangente dos ângulos notáveis",
  description="Círculo trigonométrico (ciclo trigonométrico) interativo com a tabela completa dos ângulos notáveis: digite um ângulo em radianos ou graus e obtenha seno, cosseno e tangente exatos, como √3/2.",
  alt_names=["Círculo trigonométrico", "Ciclo trigonométrico", "Circunferência trigonométrica", "Tabela trigonométrica"],
  how0="O círculo trigonométrico, também chamado de ciclo trigonométrico ou circunferência trigonométrica, tem raio 1 e centro na origem. Cada ângulo θ, medido no sentido anti-horário a partir do semieixo x positivo, determina um único ponto do círculo.",
  table_title="Tabela trigonométrica dos ângulos notáveis",
  table_intro="Todos os ângulos notáveis de 0 a 2π, ou seja de 0° a 360°, com os valores exatos de seno, cosseno e tangente. As linhas destacadas do primeiro quadrante são as que vale a pena saber de cor: as outras saem por simetria. Toque num ângulo para vê-lo no círculo.",
  faq_title="Perguntas frequentes",
  faq=[
    ("Quanto valem o seno e o cosseno de 30°, 45° e 60°?", "sen 30° = 1/2 e cos 30° = √3/2; sen 45° = cos 45° = √2/2; sen 60° = √3/2 e cos 60° = 1/2. Em radianos esses ângulos são π/6, π/4 e π/3."),
    ("Como converter graus em radianos?", "Multiplica-se por π/180: por exemplo 135° = 135 · π/180 = 3π/4. Para voltar a graus, multiplica-se por 180/π. Esta página aceita as duas formas: para graus basta acrescentar °."),
    ("Existe um truque para lembrar os valores dos ângulos notáveis?", "Para 0°, 30°, 45°, 60° e 90° o seno vale √0/2, √1/2, √2/2, √3/2 e √4/2, ou seja 0, 1/2, √2/2, √3/2 e 1. O cosseno segue a mesma sequência ao contrário."),
    ("Por que a tangente de 90° não existe?", "Porque tan θ = sen θ / cos θ e cos 90° = 0, então seria preciso dividir por zero. Isso acontece com todos os ângulos da forma π/2 + kπ, como 90° e 270°."),
    ("Como achar o seno e o cosseno de ângulos maiores que 90°?", "Usa-se a simetria do círculo. Por exemplo, 150° é o simétrico de 30° em relação ao eixo y, então sen 150° = sen 30° = 1/2 e cos 150° = −cos 30° = −√3/2. O sinal depende do quadrante em que o ponto cai."),
  ],
),
}
for _l, _e in EXTRA.items():
    _how0 = _e.pop("how0")
    T[_l].update(_e)
    T[_l]["how"] = [_how0] + T[_l]["how"][1:]


def path_of(lang):
    return "" if lang == ORDER[0] else f"{lang}/"


def rel(from_lang, to_lang):
    up = "" if from_lang == ORDER[0] else "../"
    target = path_of(to_lang)
    return (up + target) or "./"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def frac(n, d):
    return f'<span class="frac"><span>{n}</span><span>{d}</span></span>'


def root(n):
    return f'√<span class="rad">{n}</span>'


def _exact(v, tan=False):
    import math
    s2, s3 = math.sqrt(2), math.sqrt(3)
    table = [(0, "0"), (1, "1"), (0.5, frac("1", "2")), (s2 / 2, frac(root(2), "2")), (s3 / 2, frac(root(3), "2"))]
    if tan:
        table = [(0, "0"), (1, "1"), (s3, root(3)), (s3 / 3, frac(root(3), "3"))]
    for x, h in table:
        if abs(abs(v) - x) < 1e-9:
            if x == 0:
                return "0"
            return ('<span class="sign">−</span>' if v < 0 else "") + h
    raise ValueError(v)


def table_rows(t):
    import math
    undef = f'<span class="u">{esc(t["undef"])}</span>'
    degs = sorted(set(list(range(0, 361, 30)) + list(range(45, 361, 90))))
    out = []
    for deg in degs:
        g = math.gcd(deg, 180)
        k, d = deg // g, 180 // g
        num = ("" if k == 1 else str(k)) + "π"
        rad = "0" if k == 0 else (num if d == 1 else frac(num, d))
        a_txt = "0" if k == 0 else (num if d == 1 else f"{num}/{d}")
        a = math.radians(deg)
        c, s_ = math.cos(a), math.sin(a)
        tn = undef if abs(c) < 1e-12 else _exact(s_ / c, tan=True)
        href = "?a=" + quote(a_txt)
        cls = ' class="key"' if deg <= 90 else ""
        out.append(f'<tr{cls}><td><a href="{href}" data-a="{a_txt}">{deg}°</a></td><td><a href="{href}" data-a="{a_txt}">{rad}</a></td>'
                   f'<td>{_exact(c)}</td><td>{_exact(s_)}</td><td>{tn}</td></tr>')
    return "".join(out)


def faq_html(t):
    return "\n      ".join(f'<h3>{esc(q)}</h3>\n      <p>{esc(a)}</p>' for q, a in t["faq"])


def build():
    langs_map = {}
    for lang in ORDER:
        langs_map[lang] = None  # filled per page (relative)
    suggest = {l: {"text": T[l]["suggest_text"], "link": T[l]["suggest_link"]} for l in ORDER}

    alternates = "\n".join(
        [f'<link rel="alternate" hreflang="{l}" href="{BASE_URL}{path_of(l)}">' for l in ORDER]
        + [f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">']
    )

    for lang in ORDER:
        t = T[lang]
        canonical = BASE_URL + path_of(lang)
        root_rel = "" if lang == ORDER[0] else "../"
        rel_links = {l: rel(lang, l) for l in ORDER}

        lang_options = "".join(
            f'<option value="{l}"{" selected" if l == lang else ""} lang="{l}">{T[l]["name"]}</option>' for l in ORDER)
        lang_links = "".join(
            f'<li><a href="{rel_links[l]}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{T[l]["name"]}</a></li>'
            for l in ORDER)
        og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{T[l]["og"]}">' for l in ORDER if l != lang)

        jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": t["h1"],
            "alternateName": t["alt_names"],
            "headline": t["title"],
            "description": t["description"],
            "url": canonical,
            "inLanguage": t["locale"],
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript",
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
            "educationalLevel": "Secondary school",
            "learningResourceType": "Interactive resource",
            "about": ["Unit circle", "Trigonometry", "Sine", "Cosine"],
        }, ensure_ascii=False)

        i18n = json.dumps({
            "lang": lang, "locale": t["locale"], "err": t["err"], "quadrants": t["quadrants"],
            "axes": t["axes"], "equiv": t["equiv"], "undef": t["undef"], "copied": t["copied"],
            "close": t["close"], "langs": rel_links, "suggest": suggest,
        }, ensure_ascii=False).replace("</", "<\\/")

        how_html = "\n      ".join(f"<p>{esc(p)}</p>" for p in t["how"])

        autolang = ""
        if lang == ORDER[0]:
            autolang = AUTOLANG.replace("__AVAIL__", json.dumps(ORDER)) + "\n"
        values = {
            "autolang": autolang,
            "lang": t["locale"], "title": esc(t["title"]), "description": esc(t["description"]),
            "canonical": canonical, "alternates": alternates, "og_locale": t["og"], "og_alternates": og_alt,
            "base": BASE_URL, "root": root_rel, "self": rel_links[lang], "jsonld": jsonld,
            "h1": esc(t["h1"]), "sub": esc(t["sub"]), "label_angle": esc(t["label_angle"]), "show": esc(t["show"]),
            "keypad": esc(t["keypad"]), "copy": esc(t["copy"]), "hint": esc(t["hint"]),
            "svg_aria": esc(t["svg_aria"]), "sin": t["sin"], "tan": t["tan"], "note": esc(t["note"]),
            "table_title": esc(t["table_title"]), "table_intro": esc(t["table_intro"]),
            "col_deg": esc(t["col_deg"]), "col_rad": esc(t["col_rad"]), "table_rows": table_rows(t),
            "how_title": esc(t["how_title"]), "how_html": how_html,
            "faq_title": esc(t["faq_title"]), "faq_html": faq_html(t), "footer": esc(t["footer"]),
            "language": esc(t["language"]), "lang_options": lang_options, "lang_links": lang_links,
            "i18n_json": i18n,
        }
        html = TEMPLATE
        for k, v in values.items():
            html = html.replace("{{" + k + "}}", v)
        assert "{{" not in html, f"placeholder rimasto in {lang}"
        out = ROOT / path_of(lang) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("scritto", out.relative_to(ROOT))

    # sitemap con le versioni in tutte le lingue
    urls = []
    for lang in ORDER:
        alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{path_of(l)}"/>' for l in ORDER)
        alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}"/>'
        urls.append(f"  <url>\n    <loc>{BASE_URL}{path_of(lang)}</loc>{alts}\n  </url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")

    manifest = {
        "name": "Unit circle – Circonferenza goniometrica",
        "short_name": "Unit circle",
        "start_url": "./",
        "display": "standalone",
        "background_color": "#FBFCFE",
        "theme_color": "#1F3C88",
        "icons": [
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }
    (ROOT / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("scritti sitemap.xml, robots.txt, manifest.webmanifest")


if __name__ == "__main__":
    build()
