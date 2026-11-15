---
title: "Ograniczenia, aktualizacje i warunki"
nav_order: 7
lang: pl
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Ograniczenia, aktualizacje i warunki {#limits-updates-and-terms}

## Nieodczytane {#not-read}

- **Kto kogo zabił i obrażenia zadane żołnierzom przez trafienie.** Są przekazywane w wynikach trafień zdalnych wywołań broni i stanów graczy (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), których struktura nie jest odczytywana; są zachowane w całości w pliku towarzyszącym entities. Odczytywane jest tylko zdrowie ofiar.
- **Drużyna bota.** Stan bota niesie liczbę, która może być jego drużyną; niepotwierdzona, nieużywana.
- **Patrzenie żołnierza na boki** poza yaw ciała.

## Aktualizacje gry {#game-updates}

Czytnik zależy od formatu replay silnika i od garstki nazw klas i właściwości Squad. Nie zależy od układów właściwości, których nie widzi: replay sam je nazywa.

**Co może się zepsuć przy aktualizacji Squad:**

- **Aktualizacja silnika.** Squad przeszedł na UE 5.7 wraz z v10.4; tego nie testowano. Aktualizacja może zmienić nagłówek wiązki, dane pojawienia się albo `FRepMovement`. Są one warunkowane wersją w kodzie tam, gdzie znany jest ten krok. Nieznane kroki (`ENG_PARTIAL_CUSTOM_EXPORTS`, końcowy bit ruchu) są przypięte do tego, co robi v10.3.1.
- **Replikacja Iris.** Gdyby Squad przeszedł na Iris, strumień wewnątrz fragmentów byłby nowy i ten czytnik by go nie odczytał. Squad v10.3.1 używa klasycznego systemu (działa na ReplicationGraph).
- **Zmienione nazwy klas lub właściwości.** Gdyby Squad zmienił nazwy swoich klas gracza, drużyny lub sekcji albo ich właściwości, zaginęłyby nazwy i drużyny, ale pozycje by nie zaginęły.
- **Co się dzieje przy awarii.** Gdy format się zmieni, czytnik zawodzi głośno, z błędami strumienia lub ruchu w diagnostyce. Nie produkuje po cichu błędnych pozycji: `FRepMovement` jest akceptowany tylko wtedy, gdy jego bity zgadzają się co do jednego.

## Dane osobowe {#personal-data}

Demo zawiera nazwy i identyfikatory online wszystkich na serwerze. Tabela i dokument meczu niosą nazwy, nie identyfikatory. Pliki towarzyszące zachowują bity każdej właściwości, więc trzymają identyfikatory tak, jak robi to demo (nieodszyfrowane). Traktuj je wszystkie jak samo demo.

## Licencja i źródła {#licence-and-sources}

MIT; zob. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Wszystko tutaj napisano na potrzeby tego pakietu. Nie ma w nim ani nie jest dołączony żaden kod zewnętrzny: jedyne zależności to pyarrow (Apache-2.0) i numpy (BSD-3-Clause).

Fakty o formacie pochodzą z tych źródeł:

- **Unreal.Core** w [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Opisuje ogólny układ replay Unreal: blok informacyjny, fragmenty, ramki, wiązki i pola eksportu sieciowego.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Jego parser został przeczytany pod kątem układu, tak jak Squad v10.3.1 go zapisuje, pod kątem sprawdzeń wersji i tego, które klasy Squad przenoszą dane o składach. Jego opublikowane dema testowe i liczby z migawek posłużyły jako niezależna kontrola krzyżowa. Żaden jego kod nie został skopiowany ani przetłumaczony: ten czytnik ma inną strukturę (archiwum bitowe w Pythonie nad całymi pakietami, części wiązek łączone bit po bicie, właściwości przydzielane po nazwie), a dwie rzeczy, których tamten nie robi, odkryto tutaj na samych demach: trzecią flagę częściowej wiązki i końcowy bit ruchu.

Squad to znak towarowy Offworld Industries. Ten pakiet czyta pliki, które zapisuje serwer Squad; nie ingeruje w grę, jej kod ani archiwa. Polityka licencjonowania i administrowania serwerami Offworld nie mówi nic o nagrywaniu i analizie dem. Umowa licencyjna Squad (EULA) zabrania inżynierii wstecznej samej gry, czego to narzędzie nie robi.
