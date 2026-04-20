# Czyste Energie i Ochrona Środowiska
Laboratorium 3

Karolina Piotrowska, 20.04.2026

## 1. Co to jest współczynnik PR i dlaczego nie wynosi 100%
Współczynnik PR (Performance Ratio) to miara efektywności instalacji fotowoltaicznej, określająca stosunek energii faktycznie wyprodukowanej do tej, którą system wygenerowałby w warunkach idealnych.

Współczynnik ten nigdy nie wynosi 100%, ponieważ podczas pracy zawsze występują nieuniknione straty energii, takie jak:
* wysoka temperatura: Panele nagrzewają się, co obniża ich sprawność (największy wpływ na wynik).
* straty na inwerterze: Proces zamiany prądu stałego na zmienny generuje straty rzędu 2–5%.
* zabrudzenia i okablowanie: Kurz, liście oraz opór elektryczny przewodów dodatkowo uszczuplają końcową ilość energii.
* odbicie światła: Nie każde promienie słoneczne padające na panel zostają pochłonięte przez ogniwa.

Dla dobrze zaprojektowanej instalacji PR mieści się zazwyczaj w przedziale 75% – 85%.

## 2. Europejski kraje o największym i najmniejszym potencjale pozyskiwania energii słonecznej

Na podstawie danych z PVGIS oraz map SolarGIS można wskazać wyraźny gradient nasłonecznienia w Europie z południa na północ.

**Kraje o największym potencjale:**
* **Cypr** – roczna suma napromieniowania poziomego ok. **1940 kWh/m²/rok**; jako najbardziej wysunięta na południe wyspa UE korzysta z ponad 300 słonecznych dni w roku.
* **Malta** – ok. **1854 kWh/m²/rok**; podobne warunki klimatyczne jak Cypr.
* **Hiszpania** – ok. **1500–1900 kWh/m²/rok** (Sewilla ~1904, Madryt ~1779); Płaskowyż Iberyjski i południe kraju to jedne z najlepiej nasłonecznionych obszarów kontynentalnej Europy.
* **Grecja** – ok. **1630–1800 kWh/m²/rok**; śródziemnomorski klimat z dominacją bezchmurnego nieba.
* **Portugalia** – ok. **1640–1760 kWh/m²/rok**; Alentejo i Algarve należą do najbardziej słonecznych regionów Europy Zachodniej.

**Kraje o najmniejszym potencjale:**
* **Islandia** – ok. **700–900 kWh/m²/rok**; najniższe wartości w Europie — położenie na granicy koła podbiegunowego, bardzo duże zachmurzenie i częste mgły.
* **Norwegia** – ok. **950 kWh/m²/rok** (Oslo); wysokie szerokości geograficzne, krótkie dni zimowe i częste zachmurzenie.
* **Wielka Brytania** – ok. **920–1070 kWh/m²/rok** (Edynburg–Londyn); atlantycki klimat z dużym zachmurzeniem przez większą część roku.
* **Finlandia** – ok. **984 kWh/m²/rok** (Helsinki); podobne ograniczenia jak Norwegia.

Różnica między najbardziej a najmniej nasłonecznionymi krajami wynosi ponad **150%** (Cypr ~1940 vs Islandia ~700–900 kWh/m²/rok), co bezpośrednio przekłada się na opłacalność inwestycji w systemy PV.

![alt text](pvgis_analysis/figures/zad2-map.png)

## 3. Zakres optymalnych kątów nachylenia modułów fotowoltaicznych w Europie
W celu wykonania zadania użyto otwartego API strony PVGIS. Umożliwia ono szybki i zautomatyzowany dostęp do danych znajdujących się na stronie. W języku Python napisano:
* klienta API z funkcjonalnością limitowania częstości wysyłania żądań (PVGIS ma limit trzydziestu żądań na sekundę) oraz przechowywania pobranych danych w pamięci podręcznej ("cache'owanie"),
* funkcje pozwalające na zebranie i przeanalizowanie danych,
* funkcje wizualizujące wyniki obliczeń na wykresach.

![alt text](pvgis_analysis/figures/q1_tilt_map.png)

*Rys.1 Wykres zależności optymalnego kąta nachylenia modułu fotowoltaicznego od położenia geograficznego na terenie Europy*

Na podstawie Rys.1 można stwierdzić, że optymalny kąt nachylenia modułu fotowoltaicznego zależy od **szerokości** geograficznej. Wniosek ten jest zgodny z oczekiwaniami - wysokość słońca nad horyzontem i kąt padania promieni słonecznych zależą właśnie od szerokości geograficznej. Zakres optymalnych kątów nachylenia dla Europy to **~26°-51°** ze średnią wartością optymalnego kąta **39,2°**.

## 4. Relacja matematyczna pomiędzy optymalnym kątem nachylenia modułów fotowoltaicznych a szerokością geograficzną
W celu wykonania zadania ponownie posłużono się danymi zebranymi dzięki otwartemu API. 

![alt text](pvgis_analysis/figures/q2_tilt_vs_lat.png)

*Rys.2 Wykres zależności optymalnego kąta nachylenia od szerokości geograficznej*

Wykonano dwa modele:
* liniowy, gdzie $tilt = 0{,}5006 \cdot lat + 13{,}57°$
* kwadratowy, gdzie $tilt = 0{,}0054 \cdot lat^2 - 0{,}0607 \cdot lat + 27{,}62°$

W obydwu modelach optymalny kąt nachylenia rośnie wraz ze wzrostem szerokości geograficznej. Model liniowy charakteryzuje się wysokim współczynnikiem determinacji R², co potwierdza, że szerokość geograficzna jest dominującym i wystarczającym predyktorem optymalnego kąta nachylenia.

## 5. Optymalny, całoroczny kąt nachylenia modułów fotowoltaicznych w Polsce
Posłużono się piętnastoma punktami pomiarowymi z terenu Polski (dane jak zwykle pozyskane przy pomocy API). Zakres optymalnych kątów nachylenia to **30°-40°**; jego średnia wartość to **38.1° +- 2.5°**. Wykonano także analizę dla poszczególnych miast, a efekty zamieszczono w Tabeli 1.

*Tab. 1 Optymalny kąt nachylenia paneli w poszczególnych miastach oraz kąt uzyskany z zależności matematycznej z zad. 4*
| Miasto    | Optymalny kąt | Szerokość geograficzna | Optymalny kąt ze wzoru |
|-----------|---------------|------------------------|------------------------|
| Warszawa  | 39.0°         | ~52°                   | 39°                    |
| Kraków    | 39.0°         | ~50°                   | 39°                    |
| Gdańsk    | 41.0°         | ~54°                   | 41°                    |
| Wrocław   | 40.0°         | ~51°                   | 39°                    |
| Poznań    | 40.0°         | ~52°                   | 40°                    |
| Łódź      | 39.0°         | ~51°                   | 40°                    |
| Lublin    | 39.0°         | ~51°                   | 40°                    |
| Białystok | 39.0°         | ~53°                   | 40°                    |
| Rzeszów   | 39.0°         | ~50°                   | 39°                    |
| Szczecin  | 40.0°         | ~53°                   | 40°                    |


## 6. Przyrost produkcji energii dzięki zastosowaniu trackera jednoosiowego

Do analizy wykorzystano tracker jednoosiowy nachylony z optymalnym kątem osi (`inclined_axis` z parametrem `optimalinclination=1` w API PVGIS). Zebrano dane dla siatki punktów pomiarowych pokrywającej całą Europę i porównano roczną produkcję energii systemu ze śledzeniem z systemem o stałym, optymalnym kącie nachylenia.

Zakres przyrostu produkcji energii w Europie wynosi od **ok. -4% do ok. +27%**, ze średnią wartością **17.3%**. Wartości ujemne (sporadyczne, poniżej zera) pojawiają się w punktach z bardzo wysokim udziałem promieniowania rozproszonego i dużym zachmurzeniem, gdzie straty mechaniczne trackera mogą przewyższyć zyski ze śledzenia.

![alt text](pvgis_analysis/figures/q4_tracker_gain_map.png)

*Rys.3 Mapa przyrostu produkcji energii dzięki zastosowaniu trackera jednoosiowego w Europie*

![alt text](pvgis_analysis/figures/q4_tracker_gain_by_country.png)

*Rys.4 Przyrost produkcji energii dla poszczególnych krajów (słupki błędów = zakres min–max)*

*Tab. 2 Kraje z największym przyrostem:*

| Kraj | Średni przyrost | Zakres |
|---|---|---|
| Portugalia | 21.4% | 11.9% – 24.2% |
| Grecja | 19.9% | 13.1% – 25.4% |
| Norwegia | 18.7% | 11.2% – 26.6% |
| Turcja | 18.4% | 11.6% – 22.6% |
| Włochy | 18.4% | 9.8% – 22.9% |

Główną przyczyną większego przyrostu dla krajów południowych jest wyższy udział promieniowania bezpośredniego w stosunku do promieniowania rozproszonego. W krajach śródziemnomorskich niebo jest bezchmurne przez znaczną część roku, a promieniowanie słoneczne jest głównie bezpośrednie. Tracker maksymalizuje zyski właśnie na promieniowaniu bezpośrednim – przez cały dzień utrzymuje optymalny kąt padania promieni na moduł. W krajach o klimacie atlantyckim i kontynentalnym (Niemcy, Polska, Wielka Brytania) zachmurzenie jest częste i promieniowanie rozproszone stanowi większy odsetek całkowitego; tracker ma wówczas mniejszy wpływ na wynik.

Wysoka średnia wartość przyrostu dla Norwegii (18.7%) oraz najwyższy wynik w całej Europie (26.6%) wynikają ze specyfiki bardzo wysokich szerokości geograficznych (powyżej 65°N). W lecie słońce nie zachodzi i zatacza niski łuk przez całą dobę — tracker śledzący ruch słońca w płaszczyźnie horyzontalnej może uchwycić znacznie więcej energii niż panel skierowany stale na południe.

Średni przyrost produkcji energii dzięki zastosowaniu trackera jednoosiowego wynosi w Polsce **~15%**. Jest to wartość niższa niż dla krajów południa Europy, lecz wciąż ekonomicznie istotna w przypadku większych instalacji naziemnych.

## 7. Porównanie dostępności energii słonecznej w polskich miastach z innymi europejskimi miastami

Do porównania wybrano 10 polskich miast oraz 30 miast z pozostałych krajów Europy. Dla każdego miasta zebrano miesięczne sumy napromieniowania poziomego z API PVGIS i obliczono roczną sumę.

![alt text](pvgis_analysis/figures/q5_city_comparison.png)

*Rys.5 Roczna suma napromieniowania w europejskich miastach pogrupowanych według kraju*

![alt text](pvgis_analysis/figures/q5_poland_vs_europe.png)

*Rys.6 Porównanie średnich wartości nasłonecznienia i jednorodności warunków w poszczególnych krajach*

*Tab. 3 Wartości średnie i miejsca w rankingu europejskim:*

| Kraj | Średnia (kWh/m²/rok) | CV (jednorodność) |
|---|---|---|
| Cypr | ~1939 | — (1 miasto) |
| Malta | ~1854 | — (1 miasto) |
| Hiszpania | ~1782 | 6.8% |
| Grecja | ~1715 | 7.0% |
| Portugalia | ~1698 | 5.0% |
| Włochy | ~1618 | 8.5% |
| Francja | ~1456 | 22.6% |
| Niemcy | ~1163 | 5.8% |
| **Polska** | **~1118** | **2.7%** |
| Wielka Brytania | ~978 | 8.2% |
| Norwegia | ~949 | — (1 miasto) |

*CV – współczynnik zmienności (odchylenie standardowe / średnia × 100%); niższy CV oznacza bardziej jednorodne warunki w skali kraju.*

Polska osiąga roczną sumę napromieniowania ok. **1118 kWh/m²/rok**, co plasuje ją poniżej środka stawki europejskiej — wyraźnie poniżej krajów śródziemnomorskich, lecz powyżej Skandynawii i Wysp Brytyjskich.

Kluczowym wyróżnikiem Polski jest wyjątkowo niski współczynnik zmienności wynoszący zaledwie **2.7%** — najniższy spośród wszystkich krajów reprezentowanych przez więcej niż jedno miasto. Roczna suma GHI w polskich miastach zawiera się w przedziale 1064 kWh/m²/rok (Szczecin) – 1148 kWh/m²/rok (Lublin), co stanowi różnicę zaledwie ~84 kWh/m²/rok (~8%). Słabszymi warunkami charakteryzują się miasta północno-zachodnie (Szczecin, Gdańsk) i północno-wschodnie (Białystok), najlepszymi – miasta południowe i środkowe (Lublin, Wrocław, Rzeszów, Kraków).

Polska wyróżnia się na tle Europy bardzo jednorodnymi warunkami słonecznymi w całym kraju. Wynika to z relatywnie płaskiej rzeźby terenu i braku silnych efektów klimatycznych różnicujących regiony (brak wybrzeża śródziemnomorskiego z jednej strony i wysokich gór z drugiej). W odróżnieniu od Włoch, Francji czy Wielkiej Brytanii, planując instalację PV w Polsce, nie trzeba uwzględniać istotnych regionalnych różnic w uzysku energii.


## 8. Dostępność energii słonecznej w Europie i na innych kontynentach

Na podstawie map GHI dostępnych w portalu [SolarGIS](https://solargis.com/resources/free-maps-and-gis-data) można porównać roczną sumę napromieniowania poziomego (GHI) dla różnych kontynentów i regionów świata.

![alt text](pvgis_analysis/figures/zad8-map2.png)

*Tab. 4 Zestawienie regionalne (roczna suma GHI, kWh/m²/rok):*

| Region | Zakres GHI | Charakterystyka |
|---|---|---|
| **Sahara / Afryka Płn.** | 2000–2800 | Największy potencjał na świecie; niemal brak zachmurzenia, suche powietrze |
| **Półwysep Arabski / Bliski Wschód** | 1800–2500 | Drugie miejsce globalnie; pustynne klimaty z bardzo wysokim DNI |
| **Australia (centrum)** | 1800–2400 | Kontynent z wyjątkowo dużym i jednorodnym potencjałem; interior znacznie lepszy niż wybrzeże południowe |
| **Ameryka Płd. (Atacama)** | 2000–2700 | Najwyższe wartości DNI na Ziemi; pustynie andyjskie |
| **Ameryka Płn. (SW USA, Meksyk)** | 1600–2400 | Arizona, Nevada, Nowy Meksyk wśród najlepszych obszarów półkuli zachodniej |
| **Azja Pd./Pd.-Wsch.** | 1400–2000 | Indie (centrum) i Azja Pd.-Wsch. z dobrym potencjałem; monsun ogranicza część roku |
| **Europa Południowa** | 1400–1900 | Kraje śródziemnomorskie: Cypr, Hiszpania, Grecja, Portugalia |
| **Europa Środkowa (Polska)** | 1000–1200 | Umiarkowane warunki; dominacja promieniowania rozproszonego w miesiącach zimowych |
| **Europa Północna / Skandynawia** | 700–1100 | Najniższe wartości w Europie; krótkie dni zimowe, duże zachmurzenie |

Europa jest regionem o przeciętnym potencjale solarnym w skali globalnej. Nawet najlepiej nasłonecznione kraje południa Europy (Cypr ~1940 kWh/m²/rok) osiągają wartości o 30–40% niższe niż obszary Sahary czy Bliskiego Wschodu. Najbardziej uprzywilejowane strefy to tropikalne i subtropikalne pustynie — Sahara, Pustynia Arabska, Atacama i centrum Australii. Łączy je niskie zachmurzenie, suche powietrze (mała absorpcja promieniowania) oraz wysoki kąt padania słońca przez cały rok. Australia jest wyjątkowa jako cały kontynent — większość jego powierzchni przekracza 1800 kWh/m²/rok, co czyni ją najbardziej jednorodnie słonecznym zamieszkałym kontynentem. Polska i Europa Środkowa uzyskują ok. 40–60% potencjału solarnego obszarów saharyńskich, co wciąż czyni instalacje PV ekonomicznie uzasadnionymi — szczególnie dzięki spadkowi kosztów paneli i efektywnym systemom wsparcia.

## 9. Zestawienie nasłonecznienia wybranych krajów Europy według danych SolarGIS

*Tab. 5 Wartości GHI i produkcji energii w kWh/m²/rok*

| Kraj | GHI min | GHI max | Produkcja min | Produkcja max | Uwagi |
|---|---|---|---|---|---|
| Islandia | 700 | 900 | <525 | 825 | Jednolita; najniższe wartości |
| Cypr | 1800 | >2000 | 1900 | >2100 | Jednolity; najwyższe wartości |
| Niemcy | <1000 | >1200 | <825 | 1050 | Na południu lepsze warunki niż na północy; w centralnej części najgorsze |
| Hiszpania | 1200 | 2000 | 900 | >1575 | Południe i centrum z najlepszymi warunkami |
| Czechy | 1000 | >1200 | 825 | >975 | Jednolite warunki w całym kraju |
| Francja | 1000 | >1600 | <900 | 1500 | Południe (szczególnie okolice Marsylii) z najlepszymi warunkami |
| Niderlandy | 1000 | 1150 | <850 | 1000 | Jednolite warunki w całym kraju |
| Włochy | <1200 | >1800 | <600 | >1650 | Duży rozstrzał wartości; najlepsze warunki na południu oraz Sycylii i Sardynii |
| Wielka Brytania | <800 | >1200 | <600 | >1050 | Lepsze warunki na południu, szczególnie w okolicach Londynu |
| Polska | 1000 | 1150 | >825 | >975 | Bardzo jednolite warunki; minima na terenach górzystych |

## 10. Polityka wsparcia a rozwój rynku PV — przykład Niemiec i Hiszpanii
Taryfa gwarantowana (FiT) to instrument polityki energetycznej, w ramach którego producent energii z OZE (np. właściciel instalacji PV) ma zagwarantowane prawo do sprzedaży każdej wyprodukowanej kilowatogodziny do sieci publicznej po stałej, z góry ustalonej cenie, przez długi okres (zazwyczaj 15–25 lat). Stawka FiT jest odgórnie ustalana przez państwo i — w zamierzeniu — ma zapewnić rentowność inwestycji przy danym poziomie nasłonecznienia. Koszty systemu są następnie rozkładane na wszystkich odbiorców energii elektrycznej poprzez specjalną opłatę doliczaną do rachunków za prąd (tzw. surcharge/levy).

* Niemcy (ok. 2006): Stawka FiT dla małych instalacji dachowych wynosiła ok. **0,50 €/kWh**, przy hurtowej cenie energii sieciowej ~0,04–0,06 €/kWh i cenie detalicznej ~0,17–0,19 €/kWh. Przy rocznej produkcji ok. 900–1100 kWh/kWp instalacja była rentowna, ale zyski były umiarkowane i przewidywalne. System stymulował stabilny, stopniowy wzrost rynku.

* Hiszpania (ok. 2007–2008): Dekret królewski 661/2007 ustalił stawkę FiT na ok. **0,44 €/kWh** (dla instalacji naziemnych) — niemal identyczną jak w Niemczech. Jednak przy rocznej produkcji ok. 1600–1900 kWh/kWp (70–100% więcej niż w Niemczech) stopa zwrotu z inwestycji była nieproporcjonalnie wysoka — rzędu 20–30% rocznie. Wywołało to lawinę spekulacyjnych inwestycji: tylko w 2008 r. zainstalowano w Hiszpanii ok. 2,6 GW, czyli ponad połowę ówczesnych globalnych mocy PV.

Koszty taryf gwarantowanych nie są finansowane z budżetu państwa bezpośrednio — są przerzucane na wszystkich odbiorców energii elektrycznej poprzez obowiązkowy narzut doliczany do każdego rachunku za prąd. Im więcej energii z OZE kupuje operator sieci po zawyżonych stawkach FiT, tym wyższy narzut płacą gospodarstwa domowe i przedsiębiorstwa. W Hiszpanii skala inwestycji była tak ogromna, że zobowiązania z tytułu FiT przekroczyły możliwości finansowe systemu — powstał tzw. deficyt taryfowy rzędu kilkudziesięciu miliardów euro. Państwo musiało się zadłużyć, aby regulować należności wobec producentów, a następnie gwałtownie ograniczyło lub retroaktywnie obniżyło stawki FiT. Zniszczyło to zaufanie inwestorów i doprowadziło do głębokiego kryzysu hiszpańskiej branży PV na kolejne lata.

Ten sam mechanizm FiT działa prawidłowo tylko wtedy, gdy stawki są skalibrowane do lokalnej irradiancji. Przeniesienie stawek z kraju o gorszym nasłonecznieniu (Niemcy) do kraju o znacznie lepszym (Hiszpania) bez korekty równoznaczne jest z rozdawaniem nadmiernych subwencji finansowanych przez wszystkich konsumentów energii.

## 11. Wnioski

Fotowoltaika jest technologią, której efektywność w bardzo dużym stopniu zależy od geografii — i to nie tylko w oczywistym sensie „południe Europy jest lepsze od północy". Przeprowadzone analizy pokazują, że zasoby solarne kształtują niemal każdy aspekt projektowania i ekonomiki systemów PV: od optymalnego kąta nachylenia panelu, przez dobór technologii montażu, aż po kształt polityki wsparcia. Europa, mimo że w skali globalnej dysponuje jedynie umiarkowanym potencjałem solarnym — kilkukrotnie niższym niż obszary Sahary, Półwyspu Arabskiego czy centrum Australii — wciąż stanowi duży i rozwijający się rynek, co zawdzięcza przede wszystkim dynamicznemu spadkowi kosztów technologii oraz odpowiednim instrumentom politycznym.

Szczególnie interesującym przypadkiem na tle kontynentu jest Polska. Choć kraj ten nie wyróżnia się wysokim bezwzględnym nasłonecznieniem, jego wyjątkową cechą jest bardzo duża jednorodność warunków solarnych w skali całego terytorium — co jest rzadkością wśród krajów europejskich o porównywalnej powierzchni. Oznacza to, że w Polsce warunki dla rozwoju fotowoltaiki są podobne niezależnie od regionu, co sprzyja równomiernemu rozwojowi rynku i upraszcza planowanie inwestycji.

Doświadczenia Niemiec i Hiszpanii z systemami taryf gwarantowanych są przestrogą o charakterze ogólniejszym: nawet dobrze zaprojektowany instrument wsparcia może przynieść odwrotne skutki, jeśli nie uwzględnia lokalnej specyfiki zasobów. Polityka energetyczna nie działa w próżni geograficznej — dane o nasłonecznieniu powinny być podstawą każdej decyzji regulacyjnej dotyczącej OZE.