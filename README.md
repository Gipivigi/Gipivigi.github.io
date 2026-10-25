# Circonferenza goniometrica interattiva

Sito statico in 6 lingue (inglese, italiano, spagnolo, francese, tedesco, portoghese) per vedere un angolo sulla circonferenza goniometrica con seno, coseno e tangente in forma esatta.

## Pubblicarlo su GitHub Pages

1. Il repository è `Gipivigi.github.io`.
2. Carica tutto il contenuto di questa cartella (non la cartella stessa) nella radice del repository.
3. Vai su **Settings → Pages**, in "Build and deployment" scegli **Deploy from a branch**, branch `main`, cartella `/ (root)`, e salva.
4. Dopo un paio di minuti il sito è online su `https://gipivigi.github.io/`.

## Una cosa da fare prima (importante per Google)

In `_src/build.py` cambia la riga `BASE_URL` con l’indirizzo vero del sito, poi lancia:

```
python3 _src/build.py
```

Questo rigenera tutte le pagine, la `sitemap.xml` e il `robots.txt` con l’indirizzo giusto. Serve perché i collegamenti tra le lingue (hreflang), l’indirizzo canonico e l’immagine di anteprima devono essere indirizzi completi.

Se cambi un testo, modifica `_src/build.py` (traduzioni) o `_src/template.html` (struttura) e rilancia lo stesso comando. Non modificare a mano i file `index.html`: vengono sovrascritti.

## Struttura

- `index.html` è la versione inglese (quella che Google mostra di default all’estero); `it/`, `es/`, `fr/`, `de/`, `pt/` sono le altre lingue.
- Chi apre la pagina principale viene portato da solo nella lingua del suo browser, se è tra quelle disponibili. Se sceglie un’altra lingua dal menu, il sito se la ricorda.
- `assets/` contiene stile, script, icone, immagine di anteprima e i font (ospitati sul sito stesso, quindi niente richieste a Google Fonts).
- `_src/` contiene i sorgenti; GitHub Pages non la pubblica.

## Per farlo trovare

1. Registra il sito su [Google Search Console](https://search.google.com/search-console) e invia `sitemap.xml`. Fai lo stesso su [Bing Webmaster Tools](https://www.bing.com/webmasters), che serve anche per DuckDuckGo.
2. Condividi i link con un angolo già impostato, per esempio `…/?a=5π/6`: chi lo apre vede subito quell’angolo.
3. Posti dove gli studenti cercano aiuto: gruppi di classe, subreddit come r/learnmath o r/matematica, forum di matematica, insegnanti che possono metterlo nei materiali del corso. I link da siti di scuole e università aiutano molto il posizionamento.

Se vuoi sapere quante visite ricevi senza banner per i cookie, puoi aggiungere un contatore rispettoso della privacy come GoatCounter o Plausible: basta incollare il loro script in `_src/template.html` prima di `</body>` e rigenerare.

## Licenze

Font STIX Two Text e Atkinson Hyperlegible sotto SIL Open Font License (vedi `assets/fonts/`).
