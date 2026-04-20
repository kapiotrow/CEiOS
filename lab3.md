# Czyste Energie i Ochrona Środowiska
Laboratorium 2

Karolina Piotrowska, 6.04.2026

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
* **Norwegia** – ok. **950 kWh/m²/rok** (Oslo); wysokie szerokości geograficzne, krótkie dni zimowe i częste zachmurzenie.
* **Wielka Brytania** – ok. **920–1070 kWh/m²/rok** (Edynburg–Londyn); atlantycki klimat z dużym zachmurzeniem przez większą część roku.
* **Finlandia** – ok. **984 kWh/m²/rok** (Helsinki); podobne ograniczenia jak Norwegia.
* **Szwecja** – ok. **990–1107 kWh/m²/rok**; wyraźny gradient między północą a południem kraju.

Różnica między najbardziej a najmniej nasłonecznionymi krajami wynosi ponad **100%** (Cypr ~1940 vs Norwegia ~950 kWh/m²/rok), co bezpośrednio przekłada się na opłacalność inwestycji w systemy PV.


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

**Kraje z największym przyrostem:**

| Kraj | Średni przyrost | Zakres |
|---|---|---|
| Portugalia | 21.4% | 11.9% – 24.2% |
| Grecja | 19.9% | 13.1% – 25.4% |
| Norwegia | 18.7% | 11.2% – 26.6% |
| Turcja | 18.4% | 11.6% – 22.6% |
| Włochy | 18.4% | 9.8% – 22.9% |

**Dlaczego kraje południowe osiągają większy przyrost?**

Główną przyczyną jest **wyższy udział promieniowania bezpośredniego (DNI)** w stosunku do promieniowania rozproszonego (DHI). W krajach śródziemnomorskich niebo jest bezchmurne przez znaczną część roku, a promieniowanie słoneczne jest głównie bezpośrednie. Tracker maksymalizuje zyski właśnie na promieniowaniu bezpośrednim – przez cały dzień utrzymuje optymalny kąt padania promieni na moduł. W krajach o klimacie atlantyckim i kontynentalnym (Niemcy, Polska, Wielka Brytania) zachmurzenie jest częste i promieniowanie rozproszone stanowi większy odsetek całkowitego; tracker ma wówczas mniejszy wpływ na wynik.

**Uwaga dotycząca Norwegii:** Wysoka średnia wartość przyrostu dla Norwegii (18.7%) oraz najwyższy wynik w całej Europie (26.6%) wynikają ze specyfiki bardzo wysokich szerokości geograficznych (powyżej 65°N). W lecie słońce nie zachodzi i zatacza niski łuk przez całą dobę — tracker śledzący ruch słońca w płaszczyźnie horyzontalnej może uchwycić znacznie więcej energii niż panel skierowany stale na południe.

**Polska:** Średni przyrost produkcji energii dzięki zastosowaniu trackera jednoosiowego wynosi w Polsce **~15%**. Jest to wartość niższa niż dla krajów południa Europy, lecz wciąż ekonomicznie istotna w przypadku większych instalacji naziemnych.

## 7. Porównanie dostępności energii słonecznej w polskich miastach z innymi europejskimi miastami

Do porównania wybrano 10 polskich miast oraz 30 miast z pozostałych krajów Europy. Dla każdego miasta zebrano miesięczne sumy napromieniowania poziomego (GHI) z API PVGIS i obliczono roczną sumę.

![alt text](pvgis_analysis/figures/q5_city_comparison.png)
*Rys.5 Roczna suma napromieniowania w europejskich miastach pogrupowanych według kraju*

![alt text](pvgis_analysis/figures/q5_poland_vs_europe.png)
*Rys.6 Porównanie średnich wartości nasłonecznienia i jednorodności warunków w poszczególnych krajach*

**Wartości średnie i miejsca w rankingu europejskim:**

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

**Polska na tle Europy:**

Polska osiąga roczną sumę napromieniowania ok. **1118 kWh/m²/rok**, co plasuje ją poniżej środka stawki europejskiej — wyraźnie poniżej krajów śródziemnomorskich, lecz powyżej Skandynawii i Wysp Brytyjskich.

**Jednorodność warunków słonecznych:**

Kluczowym wyróżnikiem Polski jest wyjątkowo niski współczynnik zmienności wynoszący zaledwie **2.7%** — najniższy spośród wszystkich krajów reprezentowanych przez więcej niż jedno miasto. Roczna suma GHI w polskich miastach zawiera się w przedziale **1064 kWh/m²/rok (Szczecin) – 1148 kWh/m²/rok (Lublin)**, co stanowi różnicę zaledwie **~84 kWh/m²/rok** (~8%). Słabszymi warunkami charakteryzują się miasta północno-zachodnie (Szczecin, Gdańsk) i północno-wschodnie (Białystok), najlepszymi – miasta południowe i środkowe (Lublin, Wrocław, Rzeszów, Kraków).

Dla porównania:
* **Włochy** (CV = 8.5%): Mediolan ~1470 vs Palermo ~1740 kWh/m²/rok — różnica ~270 kWh/m²/rok (~18%). Wyraźny podział na północ i południe.
* **Wielka Brytania** (CV = 8.2%): Edynburg ~923 vs Londyn ~1070 kWh/m²/rok — różnica ~147 kWh/m²/rok (~16%). Gradient południe–północ.
* **Francja** (CV = 22.6%): Paryż ~1223 vs Marsylia ~1689 kWh/m²/rok — różnica ~466 kWh/m²/rok (~38%). Ogromna różnica między północą a słonecznym Prowansją.

**Wniosek:** Polska wyróżnia się na tle Europy **bardzo jednorodnymi warunkami słonecznymi** w całym kraju. Wynika to z relatywnie płaskiej rzeźby terenu i braku silnych efektów klimatycznych różnicujących regiony (brak wybrzeża śródziemnomorskiego z jednej strony i wysokich gór z drugiej). W odróżnieniu od Włoch, Francji czy Wielkiej Brytanii, planując instalację PV w Polsce, nie trzeba uwzględniać istotnych regionalnych różnic w uzysku energii.


## 8. Dostępność energii słonecznej w Europie i na innych kontynentach

Na podstawie map GHI dostępnych w portalu [SolarGIS](https://solargis.com/resources/free-maps-and-gis-data) oraz danych z [Global Solar Atlas](https://globalsolaratlas.info/) można porównać roczną sumę napromieniowania poziomego (GHI) dla różnych kontynentów i regionów świata.

**Zestawienie regionalne (roczna suma GHI, kWh/m²/rok):**

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

**Wnioski z porównania:**

1. **Europa jest regionem o przeciętnym potencjale solarnym w skali globalnej.** Nawet najlepiej nasłonecznione kraje południa Europy (Cypr ~1940 kWh/m²/rok) osiągają wartości o 30–40% niższe niż obszary Sahary czy Bliskiego Wschodu.

2. **Najbardziej uprzywilejowane strefy to tropikalne i subtropikalne pustynie** — Sahara, Pustynia Arabska, Atacama i centrum Australii. Łączy je niskie zachmurzenie, suche powietrze (mała absorpcja promieniowania) oraz wysoki kąt padania słońca przez cały rok.

3. **Australia jest wyjątkowa jako cały kontynent** — większość jego powierzchni przekracza 1800 kWh/m²/rok, co czyni ją najbardziej jednorodnie słonecznym zamieszkałym kontynentem.

4. **Polska i Europa Środkowa** uzyskują ok. 40–60% potencjału solarnego obszarów saharyńskich, co wciąż czyni instalacje PV ekonomicznie uzasadnionymi — szczególnie dzięki spadkowi kosztów paneli i efektywnym systemom wsparcia.

## 9. Zestawienie nasłonecznienia wybranych krajów Europy według danych SolarGIS

*Wartości GHI i produkcji energii w kWh/m²/rok na podstawie map SolarGIS.*

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
Różnica w tempie rozwoju rynków niemieckiego i hiszpańskiego wynikała z niedostosowania sztywnych stawek taryf gwarantowanych do lokalnej irradiancji. W Niemczech system FiT zapewniał umiarkowaną rentowność, stymulując stabilny wzrost, podczas gdy w nasłonecznionej Hiszpanii te same stawki wygenerowały nienaturalnie wysokie zyski, prowadząc do spekulacyjnego boomu. Ponieważ koszty taryf przerzucane są bezpośrednio na odbiorców końcowych w rachunkach za prąd, skala hiszpańskich inwestycji doprowadziła do gigantycznego deficytu taryfowego i destabilizacji finansów państwa. Ostatecznie Hiszpania została zmuszona do gwałtownego wycofania wsparcia, co w przeciwieństwie do stabilnego modelu niemieckiego, wywołało głęboki kryzys zaufania i załamanie tamtejszej branży PV.

## 11. Wnioski

1. **Optymalny kąt nachylenia modułów PV zależy niemal wyłącznie od szerokości geograficznej.** Analiza siatki punktów pomiarowych dla całej Europy wykazała korelację Pearsona między kątem a szerokością geograficzną na poziomie >0,97, podczas gdy korelacja z długością geograficzną jest pomijalnie mała. Model liniowy $tilt \approx 0{,}50 \cdot lat + 13{,}6°$ dobrze opisuje tę zależność. Wynika to bezpośrednio z geometrii ruchu Słońca — wysokość kulminacyjna Słońca nad horyzontem jest funkcją wyłącznie szerokości geograficznej i deklinacji.

2. **Dla Polski optymalny kąt nachylenia wynosi około 38–40°**, co jest spójne zarówno z danymi z siatki pomiarowej (38,1° ± 2,5°), jak i z wynikami dla poszczególnych miast (39–41°). Wartości uzyskane ze wzoru matematycznego zgadzają się z danymi PVGIS z dokładnością do 1°, co potwierdza praktyczną przydatność modelu.

3. **Europa wykazuje silny gradient nasłonecznienia z południa na północ.** Roczna suma GHI waha się od ~950 kWh/m²/rok (Oslo) do ~1940 kWh/m²/rok (Nikozja) — ponad dwukrotna różnica. Kraje śródziemnomorskie (Cypr, Malta, Hiszpania, Grecja, Portugalia) dysponują znacząco lepszymi warunkami niż Europa Środkowa i Północna.

4. **Polska plasuje się w środku dolnej części europejskiego rankingu** (~1118 kWh/m²/rok), wyraźnie poniżej krajów śródziemnomorskich, lecz powyżej Skandynawii i Wysp Brytyjskich. Kluczową zaletą polskiego rynku PV jest jednak wyjątkowa jednorodność warunków w skali całego kraju — współczynnik zmienności CV wynosi zaledwie 2,7%, najniższy w Europie wśród krajów z wieloma miastami w analizie. Różnica między najlepiej (Lublin, Wrocław ~1148 kWh/m²/rok) a najsłabiej (Szczecin ~1064 kWh/m²/rok) nasłonecznionym miastem wynosi jedynie ~8%, co upraszcza planowanie inwestycji i ujednolica warunki prowadzenia biznesu w branży OZE w całym kraju.

5. **Zastosowanie jednoosiowego trackera zwiększa produkcję energii w Polsce o około 15%.** W skali Europy przyrost ten mieści się w przedziale od ~–4% do ~+27%, przy czym największe korzyści odnoszą kraje o wysokim udziale promieniowania bezpośredniego (DNI) — Portugalia (~21%), Grecja (~20%), Włochy (~18%) i Hiszpania (~18%). Tracker jest najbardziej opłacalny tam, gdzie niebo jest bezchmurne przez większą część roku; przy dominacji promieniowania rozproszonego (zachmurzony klimat Polski czy Wielkiej Brytanii) zyski ze śledzenia są mniejsze.

6. **W skali globalnej Europa dysponuje umiarkowanym potencjałem solarnym.** Regiony o najwyższym potencjale — Sahara, Półwysep Arabski, Atacama i centrum Australii — osiągają 2000–2800 kWh/m²/rok GHI, czyli 2–3 razy więcej niż Europa Środkowa. Mimo to instalacje PV są w Europie ekonomicznie uzasadnione dzięki gwałtownemu spadkowi kosztów technologii i odpowiednim instrumentom polityki energetycznej.

7. **Polityka wsparcia musi uwzględniać lokalne warunki nasłonecznienia.** Przykład Niemiec i Hiszpanii pokazuje, że jednolite stawki taryf gwarantowanych (FiT), nieuwzględniające regionalnych różnic w irradiancji, mogą prowadzić do poważnych zaburzeń rynkowych. Projektując system wsparcia dla OZE, należy kalibrować stawki tak, aby zapewniały podobną rentowność inwestycji niezależnie od lokalizacji — lub stosować mechanizmy aukcyjne pozwalające rynkowi wycenić lokalny potencjał.