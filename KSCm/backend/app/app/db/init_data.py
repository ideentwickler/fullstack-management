import secrets
import string


def generate_random_password() -> str:
    alpha = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alpha) for i in range(20))
    return password


BASE_USER = [
    {'email': 'jan.scharbatke@poco.de', 'first_name': 'Jan', 'last_name': 'Scharbatke'},
    {'email': 'ersin.esme@poco.de', 'first_name': 'Ersin', 'last_name': 'Esme'},
    {'email': 'katharina.schmidt@poco.de', 'first_name': 'Katharina', 'last_name': 'Schmidt'},
    {'email': 'nico.neuendorf@poco.de', 'first_name': 'Nico', 'last_name': 'Neuendorf'},
    {'email': 'endri.cara@poco.de', 'first_name': 'Endri', 'last_name': 'Cara'},
    {'email': 'melissa.maiberg@poco.de', 'first_name': 'Melissa', 'last_name': 'Maiberg'},
]

BASE_STORES = """
1;Wuelfrath;Jost
2;Eching;Sieben
3;HH-Harburg;Windolf
4;Bielefeld;Noelle
5;B-Wedding;Windolf
6;HH-Wandsbek;Windolf
7;Bottrop;Gerlich
8;Mannheim;Stecher
9;Hannover DOM;Noelle
10;B-Kreuzberg;Windolf
12;Chemnitz;Windolf
13;Dessau;Windolf
14;Schwedt;Buosi
15;Nürnberg;Stecher
16;Erfurt;Noelle
17;Magdeburg;Noelle
18;Leipzig;Windolf
19;Nordhausen;Noelle
20;Rostock;Buosi
21;Trudering;Sieben
22;Kaiserslautern;Wieámann
24;Schwerin;Buosi
25;Bardowick;Windolf
27;B-Britz;Windolf
28;Weiterstadt;Stecher
31;B-Spandau;Windolf
32;B-Adlershof;Windolf
33;B-Lankwitz;Windolf
34;B-Marzahn;Windolf
35;DD-Nickern;Windolf
37;Neumuenster;Buosi
38;HH-Altona;Windolf
39;DD-Markthalle;Windolf
41;Würzburg;Stecher
42;Nürnberg-2;Stecher
45;Gersthofen;Sieben
48;Amberg;Stecher
49;Regensburg;Sieben
51;Deggendorf;Sieben
52;Altötting;Sieben
53;Weiden;Stecher
54;Landsberg;Sieben
55;M-Freimann;Sieben
56;Wassertrüdingen;Sieben
64;Waltersdorf;Windolf
65;Ingolstadt;Sieben
66;Halstenbek;Windolf
67;Luedinghausen;Jost
68;Oberhausen;Gerlich
69;Wetzlar;Uvermann
70;Saarlouis;Wieámann
71;Homburg;Wieámann
72;Osnabrück-2;Noelle
73;Görgeshausen;Uvermann
101;Bergkamen;Jost
104;Köln;Uvermann
105;Hagen;Jost
107;Dortmund;Jost
108;Essen;Gerlich
110;Krefeld;Gerlich
112;Kaarst;Gerlich
114;Kerpen;Uvermann
115;Hannover;Noelle
116;Wesel;Gerlich
117;Bremen;Buosi
118;Osnabrück;Noelle
119;Heilbronn;Wieámann
120;Dorsten;Gerlich
121;Viernheim;Stecher
123;Paderborn;Noelle
124;Münster;Jost
125;Braunschweig;Noelle
126;Pforzheim;van gen Hassend
128;Bochum;Gerlich
130;Ahlen;Jost
140;Iserlohn;Jost
150;Gelsenkirchen;Gerlich
151;Oldenburg;Buosi
152;Aachen;Uvermann
153;Duisburg;Gerlich
154;Wuppertal 2;Jost
155;Monheim;Gerlich
156;Arnsberg;Jost
157;Koblenz;Uvermann
158;Frankfurt;Stecher
159;Kiel;Buosi
160;Landshut;Sieben
161;Kassel;Windolf
162;Leer;Buosi
163;Salzbergen;Jost
164;Wilhelmshaven;Buosi
165;Rheda-Wiedenbrück;Noelle
166;Dinklage;Noelle
167;Mainz;Stecher
168;Düren;Uvermann
169;Eschborn;Stecher
171;Köln-2;Uvermann
172;Goch;Gerlich
173;Hildesheim;Noelle
175;Stade;Buosi
176;Zwickau;Windolf
177;Neubrandenburg;Buosi
178;Löhne;Noelle
179;Mönchengladbach;Gerlich
180;Augsburg;Sieben
181;Minden;Noelle
182;Bonn;Uvermann
183;Singen;van gen Hassend
184;Lübeck-2;Buosi
186;Trier;Uvermann
187;Bremerhaven;Buosi
188;Böblingen;van gen Hassend
189;Kreuztal;Uvermann
190;Petersberg;Windolf
201;Eningen;van gen Hassend
203;Neu-Ulm;van gen Hassend
204;Göppingen;van gen Hassend
205;Friedrichshafen;van gen Hassend
206;Fellbach;van gen Hassend
207;Stuttgart;van gen Hassend
211;Kempten;van gen Hassend
220;Donauwörth;Sieben
221;Kitzingen;Stecher
222;Biberach;van gen Hassend
223;Nobitz;Windolf
297;Lager eCommerce;Albrecht
299;eCommerce Lager;Brackmann
300;Unbekannt;Scharbatke
"""