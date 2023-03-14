#questo e' il file che fornisce accesso alle API di twitter
#tutto il codice (che ha bisogno di fare chiamate) deve importare il file e passare dai metodi di questa classe

import random
import os.path
from os import path
import time
import json
import tweepy
import nltk
import nltk.data
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
import re
import dateutil.parser
import math
from datetime import datetime, timedelta
class TwitterAPI:
    def __init__(self):
        with open("keys.json") as f:
            data = json.load(f)
            self.api_key = data["api_key"]
            self.api_key_secret = data["api_key_secret"]
            self.bearer_token = data["bearer_token"]
            self.client = tweepy.Client(self.bearer_token, return_type=dict)
            nltk.download(["stopwords", "vader_lexicon"])
            self.SIA = nltk.sentiment.SentimentIntensityAnalyzer()

    def generate_frequency_list(self, words):
        risultati = (pd.value_counts(np.array(words))).to_dict()
        tot_words = 0
        for key in risultati.keys():
            tot_words += 1

        frequency_list = []
        n=0
        for key in risultati.keys():
            if(n == 0):
                n_key = 75
            else:
                n_key = risultati[key]
                if(n > 0 and n <= tot_words/15):
                    n_key *= 7
                    if(n_key > 40):
                        n_key = 40
                    if(n_key <= 30):
                        n_key = 35
                elif(n > tot_words/15 and n <= tot_words/15 + tot_words/13):
                    n_key *= 6
                    if(n_key > 25):
                        n_key = 25
                    if(n_key <= 20):
                        n_key = 25
                elif(n > tot_words/15 + tot_words/13 and n <= tot_words/10 + tot_words/15 + tot_words/13):
                    n_key *= 4
                    if(n_key > 15):
                        n_key = 15
                    if(n_key <= 10):
                        n_key = 15
                elif(n > tot_words/10 + tot_words/15 + tot_words/18):
                    n_key *= 3
                    if(n_key > 10):
                        n_key = 10
            frequency_list.append({"text": key, "size": n_key})
            n += 1
        return frequency_list

    def generate_sentiment_analysis(self, tweets):
        sentiment = []
        for tweet in tweets:
            res = self.SIA.polarity_scores(tweet)
            if res["compound"] >= -0.05 and res["compound"] <= 0.05:
                sentiment.append("neutral")
            elif res["compound"] > 0.05:
                sentiment.append("positive")
            elif res["compound"] < -0.05:
                sentiment.append("negative")
                
        return sentiment

    def clean_tweets(self, tweets):
        #SENTIMENT (in comune)
        t_sent = []
        for tweet in tweets:
            #Pulisco testo da link, RT e caratteri speciali
            tweet = re.sub(r"RT @\S+", "", tweet)
            tweet = re.sub(r"http\S+", "", tweet)
            tweet = tweet.lower()
            tweet = re.sub("[^"u"\U0001F600-\U0001F64F"+u"\U0001F300-\U0001F5FF"+u"\U0001F680-\U0001F6FF"+u"\U0001F1E0-\U0001F1FF"+"A-Za-zÀ-ÖØ-öø-ÿ0-9@_"+"]+", " ", tweet)
            tweet = re.sub("["u"\U0001F600-\U0001F64F"+u"\U0001F300-\U0001F5FF"+u"\U0001F680-\U0001F6FF"+u"\U0001F1E0-\U0001F1FF"+"]", lambda ele: " " + ele[0] + " ", tweet)
            tweet = re.sub(r'\W*\b\w{1,2}\b', " ", tweet)
            tweet.strip()
            t_sent.append(tweet)
        
        t_term = t_sent
        
        #termcloud

        #stopword list
        stopwords= ["a", "abbastanza", "abbia", "abbiamo", "abbiano", "abbiate", "accidenti", "ad", "adesso", "affinché", "agl", "agli", "ahime", "ahimè", "ai", "al", "alcuna", "alcuni", "alcuno", "all", "alla", "alle", "allo", "allora", "altre", "altri", "altrimenti", "altro", "altrove", "altrui", "anche", "ancora", "anni", "anno", "ansa", "anticipo", "assai", "attesa", "attraverso", "avanti", "avemmo", "avendo", "avente", "aver", "avere", "averlo", "avesse", "avessero", "avessi", "avessimo", "aveste", "avesti", "avete", "aveva", "avevamo", "avevano", "avevate", "avevi", "avevo", "avrai", "avranno", "avrebbe", "avrebbero", "avrei", "avremmo", "avremo", "avreste", "avresti", "avrete", "avrà", "avrò", "avuta", "avute", "avuti", "avuto", "basta", "ben", "bene", "benissimo", "brava", "bravo", "buono", "c", "caso", "cento", "certa", "certe", "certi", "certo", "che", "chi", "chicchessia", "chiunque", "ci", "ciascuna", "ciascuno", "cima", "cinque", "cio", "cioe", "cioè", "circa", "citta", "città", "ciò", "co", "codesta", "codesti", "codesto", "cogli", "coi", "col", "colei", "coll", "coloro", "colui", "come", "cominci", "comprare", "comunque", "con", "concernente", "conclusione", "consecutivi", "consecutivo", "consiglio", "contro", "cortesia", "cos", "cosa", "cosi", "così", "cui", "d", "da", "dagl", "dagli", "dai", "dal", "dall", "dalla", "dalle", "dallo", "dappertutto", "davanti", "degl", "degli", "dei", "del", "dell", "della", "delle", "dello", "dentro", "detto", "deve", "devo", "di", "dice", "dietro", "dire", "dirimpetto", "diventa", "diventare", "diventato", "dopo", "doppio", "dov", "dove", "dovra", "dovrà", "dovunque", "due", "dunque", "durante", "e", "ebbe", "ebbero", "ebbi", "ecc", "ecco", "ed", "effettivamente", "egli", "ella", "entrambi", "eppure", "era", "erano", "eravamo", "eravate", "eri", "ero", "esempio", "esse", "essendo", "esser", "essere", "essi", "ex", "fa", "faccia", "facciamo", "facciano", "facciate", "faccio", "facemmo", "facendo", "facesse", "facessero", "facessi", "facessimo", "faceste", "facesti", "faceva", "facevamo", "facevano", "facevate", "facevi", "facevo", "fai", "fanno", "farai", "faranno", "fare", "farebbe", "farebbero", "farei", "faremmo", "faremo", "fareste", "faresti", "farete", "farà", "farò", "fatto", "favore", "fece", "fecero", "feci", "fin", "finalmente", "finche", "fine", "fino", "forse", "forza", "fosse", "fossero", "fossi", "fossimo", "foste", "fosti", "fra", "frattempo", "fu", "fui", "fummo", "fuori", "furono", "futuro", "generale", "gente", "gia", "giacche", "giorni", "giorno", "giu", "già", "gli", "gliela", "gliele", "glieli", "glielo", "gliene", "grande", "grazie", "gruppo", "ha", "haha", "hai", "hanno", "ho", "i", "ie", "ieri", "il", "improvviso", "in", "inc", "indietro", "infatti", "inoltre", "insieme", "intanto", "intorno", "invece", "io", "l", "la", "lasciato", "lato", "le", "lei", "li", "lì", "lo", "lontano", "loro", "lui", "lungo", "luogo", "là", "ma", "macche", "magari", "maggior", "mai", "male", "malgrado", "malissimo", "me", "medesimo", "mediante", "meglio", "meno", "mentre", "mesi", "mezzo", "mi", "mia", "mie", "miei", "mila", "miliardi", "milioni", "minimi", "mio", "modo", "molta", "molti", "moltissimo", "molto", "momento", "mondo", "ne", "negl", "negli", "nei", "nel", "nell", "nella", "nelle", "nello", "nemmeno", "neppure", "nessun", "nessuna", "nessuno", "niente", "no", "noi", "nome", "non", "nondimeno", "nonostante", "nonsia", "nostra", "nostre", "nostri", "nostro", "novanta", "nove", "nulla", "nuovi", "nuovo", "o", "od", "oggi", "ogni", "ognuna", "ognuno", "oltre", "oppure", "ora", "ore", "osi", "ossia", "ottanta", "otto", "paese", "parecchi", "parecchie", "parecchio", "parte", "partendo", "peccato", "peggio", "per", "perche", "perchè", "perché", "percio", "perciò", "perfino", "pero", "persino", "persone", "però", "piedi", "pieno", "piglia", "piu", "piuttosto", "più", "po", "pochissimo", "poco", "poi", "poiche", "possa", "possedere", "posteriore", "posto", "potrebbe", "preferibilmente", "presa", "press", "prima", "primo", "principalmente", "probabilmente", "promesso", "proprio", "puo", "pure", "purtroppo", "può", "qua", "qualche", "qualcosa",
        "qualcuna", "qualcuno", "quale", "quali", "qualunque", "quando", "quanta", "quante", "quanti", "quanto", "quantunque", "quarto", "quasi", "quattro", "quel", "quella", "quelle", "quelli", "quello", "quest", "questa", "queste", "questi", "questo", "qui", "quindi", "quinto", "realmente", "recente", "recentemente", "registrazione", "relativo", "riecco", "rispetto", "salvo", "sara", "sarai", "saranno", "sarebbe", "sarebbero", "sarei", "saremmo", "saremo", "sareste", "saresti", "sarete", "sarà", "sarò", "scola", "scopo", "scorso", "se", "secondo", "seguente", "seguito", "sei", "sembra", "sembrare", "sembrato", "sembrava", "sembri", "sempre", "senza", "sette", "si", "sia", "siamo", "siano", "siate", "siete", "sig", "solito", "solo", "soltanto", "sono", "sopra", "soprattutto", "sotto", "spesso", "sta", "stai", "stando", "stanno", "starai", "staranno", "starebbe", "starebbero", "starei", "staremmo", "staremo", "stareste", "staresti", "starete", "starà", "starò", "stata", "state", "stati", "stato", "stava", "stavamo", "stavano", "stavate", "stavi", "stavo", "stemmo", "stessa", "stesse", "stessero", "stessi", "stessimo", "stesso", "steste", "stesti", "stette", "stettero", "stetti", "stia", "stiamo", "stiano", "stiate", "sto", "su", "sua", "subito", "successivamente", "successivo", "sue", "sugl", "sugli", "sui", "sul", "sull", "sulla", "sulle", "sullo", "suo", "suoi", "tale", "tali", "talvolta", "tanto", "te", "tempo", "terzo", "th", "ti", "titolo", "tra", "tranne", "tre", "trenta", "triplo", "troppo", "trovato", "tu", "tua", "tue", "tuo", "tuoi", "tutta", "tuttavia", "tutte", "tutti", "tutto", "uguali", "ulteriore", "ultimo", "un", "una", "uno", "uomo", "va", "vai", "vale", "vari", "varia", "varie", "vario", "verso", "vi", "vicino", "visto", "vita", "voi", "volta", "volte", "vostra", "vostre", "vostri", "vostro", "è", "a", "a's", "able", "about", "above", "according", "accordingly", "across", "actually", "after", "afterwards", "again", "against", "ain't", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "aren't", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn't", "course", "currently", "d", "definitely", "described", "despite", "did", "didn't", "different", "do", "does", "doesn't", "doing", "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f", "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "j", "just", "k", "keep", "keeps", "kept", "know",
        "known", "knows", "l", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "s", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldn't", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "there's", "thereafter", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "very", "via", "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "welcome", "well", "went", "were", "weren't", "what", "what's", "whatever", "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who's", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "won't", "wonder", "would", "wouldn't", "x", "y", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "z", "zero", "a", "abord", "absolument", "afin", "ah", "ai", "aie", "ailleurs", "ainsi", "ait", "allaient", "allo", "allons", "allô", "alors", "anterieur", "anterieure", "anterieures", "apres", "après", "as", "assez", "attendu", "au", "aucun", "aucune", "aujourd", "aujourd'hui", "aupres", "auquel", "aura", "auraient", "aurait", "auront", "aussi", "autre", "autrefois", "autrement", "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avoir", "avons", "ayant", "b", "bah", "bas", "basee", "bat", "beau", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr", "c", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chacune", "chaque", "cher", "chers", "chez", "chiche", "chut", "chère", "chères", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième", "cinquième", "clac", "clic", "combien", "comme", "comment", "comparable", "comparables", "compris", "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors",
        "deja", "delà", "depuis", "dernier", "derniere", "derriere", "derrière", "des", "desormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement", "devant", "devers", "devra", "different", "differentes", "differents", "différent", "différente", "différentes", "différents", "dire", "directe", "directement", "dit", "dite", "dits", "divers", "diverse", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dixième", "doit", "doivent", "donc", "dont", "douze", "douzième", "dring", "du", "duquel", "durant", "dès", "désormais", "e", "effet", "egale", "egalement", "egales", "eh", "elle", "elle-même", "elles", "elles-mêmes", "en", "encore", "enfin", "entre", "envers", "environ", "es", "est", "et", "etant", "etc", "etre", "eu", "euh", "eux", "eux-mêmes", "exactement", "excepté", "extenso", "exterieur", "f", "fais", "faisaient", "faisant", "fait", "façon", "feront", "fi", "flac", "floc", "font", "g", "gens", "h", "ha", "hein", "hem", "hep", "hi", "ho", "holà", "hop", "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "huitième", "hum", "hurrah", "hé", "hélas", "i", "il", "ils", "importe", "j", "je", "jusqu", "jusque", "juste", "k", "l", "la", "laisser", "laquelle", "las", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "longtemps", "lors", "lorsque", "lui", "lui-meme", "lui-même", "là", "lès", "m", "ma", "maint", "maintenant", "mais", "malgre", "malgré", "maximale", "me", "meme", "memes", "merci", "mes", "mien", "mienne", "miennes", "miens", "mille", "mince", "minimale", "moi", "moi-meme", "moi-même", "moindres", "moins", "mon", "moyennant", "multiple", "multiples", "même", "mêmes", "n", "na", "naturel", "naturelle", "naturelles", "ne", "neanmoins", "necessaire", "necessairement", "neuf", "neuvième", "ni", "nombreuses", "nombreux", "non", "nos", "notamment", "notre", "nous", "nous-mêmes", "nouveau", "nul", "néanmoins", "nôtre", "nôtres", "o", "oh", "ohé", "ollé", "olé", "on", "ont", "onze", "onzième", "ore", "ou", "ouf", "ouias", "oust", "ouste", "outre", "ouvert", "ouverte", "ouverts", "o|", "où", "p", "paf", "pan", "par", "parce", "parfois", "parle", "parlent", "parler", "parmi", "parseme", "partant", "particulier", "particulière", "particulièrement", "pas", "passé", "pendant", "pense", "permet", "personne", "peu", "peut", "peuvent", "peux", "pff", "pfft", "pfut", "pif", "pire", "plein", "plouf", "plus", "plusieurs", "plutôt", "possessif", "possessifs", "possible", "possibles", "pouah", "pour", "pourquoi", "pourrais", "pourrait", "pouvait", "prealable", "precisement", "premier", "première", "premièrement", "pres", "probable", "probante", "procedant", "proche", "près", "psitt", "pu", "puis", "puisque", "pur", "pure", "q", "qu", "quand", "quant", "quant-à-soi", "quanta", "quarante", "quatorze", "quatre", "quatre-vingt", "quatrième", "quatrièmement", "que", "quel", "quelconque", "quelle", "quelles", "quelqu'un", "quelque", "quelques", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "rare", "rarement", "rares", "relative", "relativement", "remarquable", "rend", "rendre", "restant", "reste", "restent", "restrictif", "retour", "revoici", "revoilà", "rien", "s", "sa", "sacrebleu", "sait", "sans", "sapristi", "sauf", "se", "sein", "seize", "selon", "semblable", "semblaient", "semble", "semblent", "sent", "sept", "septième", "sera", "seraient", "serait", "seront", "ses", "seul", "seule", "seulement", "si", "sien", "sienne", "siennes", "siens", "sinon", "six", "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous", "souvent", "specifique", "specifiques", "speculatif", "stop", "strictement", "subtiles", "suffisant", "suffisante", "suffit", "suis", "suit", "suivant", "suivante", "suivantes", "suivants", "suivre", "superpose", "sur", "surtout", "t", "ta", "tac", "tant", "tardive", "te", "tel", "telle", "tellement", "telles", "tels", "tenant", "tend", "tenir", "tente", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc", "toi", "toi-même", "ton", "touchant", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "tres", "trois", "troisième", "troisièmement", "trop", "très", "tsoin", "tsouin", "tu", "té",
        "u", "un", "une", "unes", "uniformement", "unique", "uniques", "uns", "v", "va", "vais", "vas", "vers", "via", "vif", "vifs", "vingt", "vivat", "vive", "vives", "vlan", "voici", "voilà", "vont", "vos", "votre", "vous", "vous-mêmes", "vu", "vé", "vôtre", "vôtres", "w", "x", "y", "z", "zut", "à", "â", "ça", "ès", "étaient", "étais", "était", "étant", "été", "être", "ô", "a", "actualmente", "acuerdo", "adelante", "ademas", "además", "adrede", "afirmó", "agregó", "ahi", "ahora", "ahí", "al", "algo", "alguna", "algunas", "alguno", "algunos", "algún", "alli", "allí", "alrededor", "ambos", "ampleamos", "antano", "antaño", "ante", "anterior", "antes", "apenas", "aproximadamente", "aquel", "aquella", "aquellas", "aquello", "aquellos", "aqui", "aquél", "aquélla", "aquéllas", "aquéllos", "aquí", "arriba", "arribaabajo", "aseguró", "asi", "así", "atras", "aun", "aunque", "ayer", "añadió", "aún", "b", "bajo", "bastante", "bien", "breve", "buen", "buena", "buenas", "bueno", "buenos", "c", "cada", "casi", "cerca", "cierta", "ciertas", "cierto", "ciertos", "cinco", "claro", "comentó", "como", "con", "conmigo", "conocer", "conseguimos", "conseguir", "considera", "consideró", "consigo", "consigue", "consiguen", "consigues", "contigo", "contra", "cosas", "creo", "cual", "cuales", "cualquier", "cuando", "cuanta", "cuantas", "cuanto", "cuantos", "cuatro", "cuenta", "cuál", "cuáles", "cuándo", "cuánta", "cuántas", "cuánto", "cuántos", "cómo", "d", "da", "dado", "dan", "dar", "de", "debajo", "debe", "deben", "debido", "decir", "dejó", "del", "delante", "demasiado", "demás", "dentro", "deprisa", "desde", "despacio", "despues", "después", "detras", "detrás", "dia", "dias", "dice", "dicen", "dicho", "dieron", "diferente", "diferentes", "dijeron", "dijo", "dio", "donde", "dos", "durante", "día", "días", "dónde", "e", "ejemplo", "el", "ella", "ellas", "ello", "ellos", "embargo", "empleais", "emplean", "emplear", "empleas", "empleo", "en", "encima", "encuentra", "enfrente", "enseguida", "entonces", "entre", "era", "eramos", "eran", "eras", "eres", "es", "esa", "esas", "ese", "eso", "esos", "esta", "estaba", "estaban", "estado", "estados", "estais", "estamos", "estan", "estar", "estará", "estas", "este", "esto", "estos", "estoy", "estuvo", "está", "están", "ex", "excepto", "existe", "existen", "explicó", "expresó", "f", "fin", "final", "fue", "fuera", "fueron", "fui", "fuimos", "g", "general", "gran", "grandes", "gueno", "h", "ha", "haber", "habia", "habla", "hablan", "habrá", "había", "habían", "hace", "haceis", "hacemos", "hacen", "hacer", "hacerlo", "haces", "hacia", "haciendo", "hago", "han", "hasta", "hay", "haya", "he", "hecho", "hemos", "hicieron", "hizo", "horas", "hoy", "hubo", "i", "igual", "incluso", "indicó", "informo", "informó", "intenta", "intentais", "intentamos", "intentan", "intentar", "intentas", "intento", "ir", "j", "junto", "k", "l", "la", "lado", "largo", "las", "le", "lejos", "les", "llegó", "lleva", "llevar", "lo", "los", "luego", "lugar", "m", "mal", "manera", "manifestó", "mas", "mayor", "me", "mediante", "medio", "mejor", "mencionó", "menos", "menudo", "mi", "mia", "mias", "mientras", "mio", "mios", "mis", "misma", "mismas", "mismo", "mismos", "modo", "momento", "mucha", "muchas", "mucho", "muchos", "muy", "más", "mí", "mía", "mías", "mío", "míos", "n", "nada", "nadie", "ni", "ninguna", "ningunas", "ninguno", "ningunos", "ningún", "no", "nos", "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "nueva", "nuevas", "nuevo", "nuevos", "nunca", "o", "ocho", "os", "otra", "otras", "otro", "otros", "p", "pais", "para", "parece", "parte", "partir", "pasada", "pasado", "paìs", "peor", "pero", "pesar", "poca", "pocas", "poco", "pocos", "podeis", "podemos", "poder", "podria", "podriais", "podriamos", "podrian", "podrias", "podrá", "podrán", "podría", "podrían", "poner", "por", "porque", "posible", "primer", "primera", "primero", "primeros", "principalmente", "pronto", "propia", "propias", "propio", "propios", "proximo", "próximo", "próximos", "pudo", "pueda", "puede", "pueden", "puedo", "pues", "q", "qeu", "que", "quedó", "queremos", "quien", "quienes", "quiere", "quiza", "quizas", "quizá",
        "quizás", "quién", "quiénes", "qué", "r", "raras", "realizado", "realizar", "realizó", "repente", "respecto", "s", "sabe", "sabeis", "sabemos", "saben", "saber", "sabes", "salvo", "se", "sea", "sean", "segun", "segunda", "segundo", "según", "seis", "ser", "sera", "será", "serán", "sería", "señaló", "si", "sido", "siempre", "siendo", "siete", "sigue", "siguiente", "sin", "sino", "sobre", "sois", "sola", "solamente", "solas", "solo", "solos", "somos", "son", "soy", "soyos", "su", "supuesto", "sus", "suya", "suyas", "suyo", "sé", "sí", "sólo", "t", "tal", "tambien", "también", "tampoco", "tan", "tanto", "tarde", "te", "temprano", "tendrá", "tendrán", "teneis", "tenemos", "tener", "tenga", "tengo", "tenido", "tenía", "tercera", "ti", "tiempo", "tiene", "tienen", "toda", "todas", "todavia", "todavía", "todo", "todos", "total", "trabaja", "trabajais", "trabajamos", "trabajan", "trabajar", "trabajas", "trabajo", "tras", "trata", "través", "tres", "tu", "tus", "tuvo", "tuya", "tuyas", "tuyo", "tuyos", "tú", "u", "ultimo", "un", "una", "unas", "uno", "unos", "usa", "usais", "usamos", "usan", "usar", "usas", "uso", "usted", "ustedes", "v", "va", "vais", "valor", "vamos", "van", "varias", "varios", "vaya", "veces", "ver", "verdad", "verdadera", "verdadero", "vez", "vosotras", "vosotros", "voy", "vuestra", "vuestras", "vuestro", "vuestros", "w", "x", "y", "ya", "yo", "z", "él", "ésa", "ésas", "ése", "ésos", "ésta", "éstas", "éste", "éstos", "última", "últimas", "último", "últimos"]
    
        #tokenizzo
        t_term = [word for line in t_term for word in line.split()]

        t_term = [i for i in t_term if i not in stopwords]
        return t_term, t_sent

    def eredita(self, opzioni, cache=True):
        path_cache = "cache/eredita/"+str(opzioni["data_inizio"][:10])+"_"+str(opzioni["data_fine"][:10])+".json"
        if(cache):
            if path.isfile(path_cache):
                with open(path_cache, "r") as f:
                    return f.read()

        query = "from:quizzettone Amici #ereditiers, bentrovati per una nuova #ghigliottina su Twitter."

        data_oggi = datetime.today().astimezone()
        data_oggi = data_oggi - timedelta(seconds=15)
        #tweet sulle puntate della settimana
        response = self.client.search_all_tweets(query=query, 
                                                 max_results=10,
                                                 start_time=opzioni["data_inizio"],
                                                 end_time=opzioni["data_fine"] if (datetime.fromisoformat(opzioni["data_fine"]) < data_oggi) else data_oggi.isoformat(),
                                                 expansions="attachments.media_keys",
                                                 tweet_fields="lang,created_at,author_id,conversation_id",
                                                 media_fields="width,height,url,preview_image_url")
        
        #risposte
        res = {}
        res["puntate"] = []
        if response.get("data", None) != None:
            for puntata in response["data"]:
                risultato = {}
                time.sleep(1)
                lista = []
                tweet = puntata
                risultato["data_puntata"] = datetime.fromisoformat(tweet["created_at"][:19]).strftime("%Y-%m-%d")
                query = "from:quizzettone conversation_id:"+tweet["conversation_id"]
                response2 = self.client.search_all_tweets(query=query, 
                                                    max_results=25,
                                                    expansions="attachments.media_keys",
                                                    tweet_fields="lang,created_at,author_id",
                                                    media_fields="width,height,url,preview_image_url")
                #puliamo
                rev = response2["data"]
                for el in rev:
                    index = el["text"].find("Campioni")
                    if index == -1 : index=0
                    el["text"] = el["text"][index:]
                rev.reverse()
                lista += [tweet]+rev

                #PAROLE
                parole = lista[0]["text"].split("\n")
                par = []
                for parola in parole:
                    if parola.isupper() and len(parola)>1:
                        par += [parola]
                risultato["parole"] = par

                #PODIO

                #primo/i
                primo = []
                index = lista[1]["text"].find("🥇")
                tmp = lista[1]["text"][index:]
                tmp = tmp.split("🥇")[1:]
                for s in tmp:
                    s2 = s.split()
                    primo += [{"username": s2[0], "time": (tweet["created_at"][:10]+" "+s2[2])}]
                #secondo/i
                secondo = []
                index = lista[1]["text"].find("🥈")
                tmp = lista[1]["text"][index:]
                tmp = tmp.split("🥈")[1:]
                for s in tmp:
                    s2 = s.split()
                    secondo += [{"username": s2[0], "time": (tweet["created_at"][:10]+" "+s2[2])}]
                #terzo/i
                terzo = []
                index = lista[1]["text"].find("🥉")
                tmp = lista[1]["text"][index:]
                tmp = tmp.split("🥉")[1:]
                for s in tmp:
                    s2 = s.split()
                    terzo += [{"username": s2[0], "time": (tweet["created_at"][:10]+" "+s2[2])}]
                risultato["podio"] = {"primo": primo, "secondo": secondo, "terzo": terzo}
                    
                #CLASSIFICA (GRAFICI) 
                dati_grafico = {}
                classifica = []
                classifica += primo + secondo + terzo
                tmp_lista = lista[2:]
                for el in tmp_lista:
                    if(el["text"].find("Campioni") == 0): #solo i tweet con la lista dei giocatori
                        matches = re.findall("\d\..+", el["text"])
                        for m in matches:
                            m = m.split()
                            classifica.append({"username": m[1], "time": (tweet["created_at"][:10]+" "+m[3])})
                    elif(el["text"].find("Altri campioni de") != -1):
                        pass
                    else:
                        s = re.sub("\@\w+\s", "", el["text"])
                        matches = re.findall("\d+", s)
                        dati_grafico["totali"] = matches[1]
                        dati_grafico["indovinati"] = matches[2]
                        break
                risultato["classifica"] = classifica
                risultato["grafico"] = dati_grafico
                res["puntate"] += [risultato]

            res["data_inizio"] = datetime.fromisoformat(opzioni["data_inizio"]).strftime("%Y-%m-%d")
            res["data_fine"] = datetime.fromisoformat(opzioni["data_fine"]).strftime("%Y-%m-%d")
            
            if(path.isfile(path_cache)):
                with open(path_cache, "w") as f:
                    json.dump(res, f)
            else:
                f = open(path_cache, "x")
                json.dump(res, f)
                f.close()

            return json.dumps(res)
        
        with open("./cache/eredita/2023-01-09_2023-01-15.json", "r") as f:
            return f.read()

    def get_match_tweets(self, filtri, opzioni):
        query = "#" + filtri["hashtag"] + " -is:retweet lang:it"
        response = self.client.search_all_tweets(query=query, 
                                                 max_results=opzioni.get("max_tweets", None),
                                                 start_time=datetime.fromtimestamp(opzioni.get("primo_tempo_inizio", None)).strftime("%Y-%m-%dT%H:%M:%S")+"+01:00",
                                                 end_time=datetime.fromtimestamp(opzioni.get("secondo_tempo_fine", None)).strftime("%Y-%m-%dT%H:%M:%S")+"+01:00",
                                                 expansions="attachments.media_keys",
                                                 tweet_fields="lang,created_at,author_id",
                                                 media_fields="width,height,url,preview_image_url")
        
        #matcho l'username allo userid
        if response.get("data", None) != None:
            ids = []
            for tweet in response["data"]:
                ids.append(tweet["author_id"])
            response2 = self.client.get_users(ids=ids[0:(100 if 100<len(ids) else None)], user_fields="profile_image_url")
            for j in range(1, math.ceil(len(ids)/100)):
                response3 = self.client.get_users(ids=ids[100*j:(100*(j+1) if 100*(j+1)<len(ids) else None)], user_fields="profile_image_url")
                response2["data"] += response3["data"]
            for i in range (len(response["data"])):
                response["data"][i]["username"] = response2["data"][i]["username"]
                response["data"][i]["name"] = response2["data"][i]["name"]
                response["data"][i]["profile_image_url"] = response2["data"][i]["profile_image_url"]
                
        #modifico il json per includere i media allegati al tweet
        if response.get("includes", None) != None and response["includes"].get("media", None) != None:#se abbiamo trovato almeno un tweet con media
            tweets = response["data"]
            medias = response["includes"]["media"]
            for tweet in tweets:
                if tweet.get("attachments", None) != None: #se il tweet ha dei media associati
                    media_key = tweet["attachments"]["media_keys"][0]
                    for media in medias:
                        if media["media_key"] == media_key:
                            tweet["attachments"]["media"] = {}
                            tweet["attachments"]["media"]["height"] = media["height"]
                            tweet["attachments"]["media"]["width"] = media["width"]
                            tweet["attachments"]["media"]["url"] = media.get("url", "")
                            tweet["attachments"]["media"]["preview_url"] = media.get("preview_image_url", "")
                            tweet["attachments"]["media"]["type"] = media["type"]
        
        if response.get("data", None) != None:
            ar_tweets = []
            for tweet in response["data"]:
                ar_tweets.append(tweet["text"])

            #puliamo i tweets
            _ , ar_tweets_sent = self.clean_tweets(ar_tweets)

            #analizziamo il sentiment dei tweet
            sentiment_analysis = self.generate_sentiment_analysis(ar_tweets_sent)
            #inseriamo un campo che indica il sentiment nel tweet
            for i in range(len(response["data"])):
                response["data"][i]["sentiment"] = sentiment_analysis[i]
            #contiamo il numero di tweet positivi/neg/neu e mettiamo tutto in un dict per il grafico sotto "meta"
            grafico = {}
            grafico["labels"] = ["positivo", "negativo", "neutrale"]
            grafico["values"] = [sentiment_analysis.count("positive"), sentiment_analysis.count("negative"), sentiment_analysis.count("neutral")]
            response["meta"]["grafico_sentiment"] = grafico
        
        #grafico
        start = opzioni["primo_tempo_inizio"]
        end = opzioni["secondo_tempo_fine"]
        barre1 = {}
        n = math.ceil((end - start) / 60)
        barre1["x"] = [0] * n
        barre1["y"] = [0] * n
        for i in range(n):
            barre1["x"][i] = i+1
        if response.get("data", None) != None:
            for tweet in response["data"]:
                for i in range(n):                                                          #timezone...
                    if int(datetime.fromisoformat(tweet["created_at"][:-5]).strftime("%s"))+(60*60) <= start+(60*i):
                        barre1["y"][i] += 1
                        break
        response["meta"]["grafico_barre_minuti"] = barre1
        with open("log.json", "w") as f:
            f.write(json.dumps(response))
        return response

    def get_tweets(self, filtri, opzioni={}):
        #filtri
        query = ""
        if(filtri.get("keyword") != None):
            query += filtri["keyword"]
        if(filtri.get("hashtag") != None):
            query += " #" + filtri["hashtag"]
        if(filtri.get("username") != None):
            query += " from:" + filtri["username"]
        if(filtri.get("location") != None):
            query += " point_radius:["+filtri["location"][0]+" "+filtri["location"][1]+" "+filtri["location"][2]+"km]"
                      
        #opzioni
        if(opzioni.get("lingua", "all") != "all"):
            query += " lang:"+opzioni["lingua"]
        if(opzioni.get("image", False)):
            query += " has:images -is:retweet"
        
        response = self.client.search_all_tweets(query=query, 
                                                 max_results=opzioni.get("max_tweets", None),
                                                 start_time=opzioni.get("data_inizio", None),
                                                 end_time=opzioni.get("data_fine", None),
                                                 expansions="geo.place_id,attachments.media_keys",
                                                 place_fields="geo",
                                                 tweet_fields="lang,created_at,author_id",
                                                 media_fields="width,height,url,preview_image_url")
        
        #matcho l'username allo userid
        if response.get("data", None) != None:
            ids = []
            for tweet in response["data"]:
                ids.append(tweet["author_id"])
            response2 = self.client.get_users(ids=ids, user_fields="profile_image_url")
            for i in range (len(response["data"])):
                response["data"][i]["username"] = response2["data"][i]["username"]
                response["data"][i]["name"] = response2["data"][i]["name"]
                response["data"][i]["profile_image_url"] = response2["data"][i]["profile_image_url"]

        #modifico il json response per includere le coordinate generate direttamente insieme al tweet
        if response.get("includes", None) != None and response["includes"].get("places", None) != None:#se abbiamo trovato almeno un tweet geolocalizzato
            tweets = response["data"]
            places = response["includes"]["places"]
            for tweet in tweets:
                if tweet.get("geo", None) != None:#se il tweet ha la posizione
                    place_id = tweet["geo"]["place_id"]
                    for place in places:#troviamo il place che matcha
                        if place["id"] == place_id:
                            tweet["geo"]["full_name"] = place["full_name"]#aggiungo il nome
                            coor_lat = random.uniform(place["geo"]["bbox"][1], place["geo"]["bbox"][3])
                            coor_long = random.uniform(place["geo"]["bbox"][0], place["geo"]["bbox"][2])
                            tweet["geo"]["lat"] = coor_lat#^randomizzo le coordinate del tweet all'interno della bounding box
                            tweet["geo"]["long"] = coor_long

        #modifico il json per includere i media allegati al tweet
        if response.get("includes", None) != None and response["includes"].get("media", None) != None:#se abbiamo trovato almeno un tweet con media
            tweets = response["data"]
            medias = response["includes"]["media"]
            for tweet in tweets:
                if tweet.get("attachments", None) != None: #se il tweet ha dei media associati
                    media_key = tweet["attachments"]["media_keys"][0]
                    for media in medias:
                        if media["media_key"] == media_key:
                            tweet["attachments"]["media"] = {}
                            tweet["attachments"]["media"]["height"] = media["height"]
                            tweet["attachments"]["media"]["width"] = media["width"]
                            tweet["attachments"]["media"]["url"] = media.get("url", "")
                            tweet["attachments"]["media"]["preview_url"] = media.get("preview_image_url", "")
                            tweet["attachments"]["media"]["type"] = media["type"]
        
        frequency_list = [] #predichiaro frequency_list nel caso non siano stati trovati tweet

        if response.get("data", None) != None:
            ar_tweets = []
            for tweet in response["data"]:
                ar_tweets.append(tweet["text"])

            #puliamo i tweets
            ar_tweets_term, ar_tweets_sent = self.clean_tweets(ar_tweets)

            #creiamo la frequency list
            frequency_list = self.generate_frequency_list(ar_tweets_term)

            #analizziamo il sentiment dei tweet
            sentiment_analysis = self.generate_sentiment_analysis(ar_tweets_sent)
            #inseriamo un campo che indica il sentiment nel tweet
            for i in range(len(response["data"])):
                response["data"][i]["sentiment"] = sentiment_analysis[i]
            #contiamo il numero di tweet positivi/neg/neu e mettiamo tutto in un dict per il grafico sotto "meta"
            grafico = {}
            grafico["labels"] = ["positivo", "negativo", "neutrale"]
            grafico["values"] = [sentiment_analysis.count("positive"), sentiment_analysis.count("negative"), sentiment_analysis.count("neutral")]
            response["meta"]["grafico_sentiment"] = grafico

        #diagramma tempo
        if response.get("data", None) != None and opzioni.get("data_inizio", None) != None and opzioni.get("data_fine", None) != None:
            grafico2 = {}
            grafico2["x"] = []
            data_in = datetime.fromisoformat(opzioni["data_inizio"])
            data_fi = datetime.fromisoformat(opzioni["data_fine"])

            while(data_in < data_fi):
                grafico2["x"].append(data_in.strftime("%Y-%m-%d"))
                data_in = data_in + timedelta(days=1)
            
            grafico2["y"] = [0] * len(grafico2["x"])

            tweets = response["data"]
            for tweet in tweets:
                for i in range(len(grafico2["x"])):
                    if tweet["created_at"][:10] == grafico2["x"][i]:
                        grafico2["y"][i] += 1
            
            response["meta"]["grafico_barre"] = grafico2

        return json.dumps(response), json.dumps(frequency_list)