### PL
# Wieloosobowa gra zręcznościowa 2D z wykorzystaniem przetwarzania rozproszonego
## Wymagania
- Python 3.11+ (aplikacja nie testowana na niższych wersjach języka)
- RabbitMQ
## Instalacja i uruchomienie
1. Zainstalowanie wszystkich zależności:
```bash
pip install -r requirements.txt
```
2. Konfiguracja sieciowa w plikach `servers_config.py`, `network_settings.py`, `producer.py`, `consumer.py` (opcjonalnie, obecna konfiguracja pozwala na uruchomienie całej infrastruktury na interfejsie `localhost` jednego komputera)
3. Uruchomienie usługi **RabbitMQ**
4. Uruchomienie serwerów obydwu dostępnych krain w osobnych procesach
```bash
python servers/server.py FOREST
```
oraz
```bash
python servers/server.py CASTLE
```
5. Uruchomienie dowolnej liczby procesów klienckich gry
```bash
python game.py
```
6. Na początku gracz jest proszony o wprowadzenie swojego imienia oraz wybrania swojego bohatera, po czym przenoszony jest do świata gry

## Zasady gry oraz sterowanie
Gra polega na poruszaniu się po planszy oraz pokonywaniu przeciwników poprzez wykonywanie celnych ataków swoim bohaterem. Za każdego trafionego (pokonanego) przeciwnika gracz otrzymuje jeden punkt na swoje konto. Ponadto gracz w sytuacji zagrożenia może przenieść się do innej krainy używając znajdującego się na planszy portalu.

Jeżeli gracz zostanie trafiony przez przeciwnika, zostaje przenoszony do ekranu punktacji gdzie znajduje się lista graczy, którzy osiągnęli najlepsze wyniki w danej krainie.

### Sterowanie

**Poruszanie się**
- W - Ruch do góry 
- A - Ruch w lewo
- D - Ruch w prawo
- S - Ruch do dołu

**Ataki**
- ⬆️ - Atak do góry 
- ⬅️ - Atak w lewo
- ➡️ - Atak w prawo
- ⬇️ - Atak do dołu

**Interakcje**
- Spacja - Użycie portalu (gracz musi znajdować się w pobliżu portalu)