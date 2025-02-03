# Optimalisatie Route Peilbuizen


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Beschrijving

Dit project helpt bij het bepalen van de meest efficiënte route langs
alle peilbuizen binnen een project. Het gebruikt OpenRouteService voor
routeberekening en optimaliseert de volgorde van bezoeken om reistijd te
minimaliseren.

## Belangrijkste Functionaliteiten

- Ophalen van peilbuislocaties uit Azure SQL Database
- Optimaliseren van routes per projectgroep
- Genereren van Google Maps URLs voor eenvoudige navigatie
- Export van routes naar Excel voor praktisch gebruik
- Ondersteuning voor verschillende routeprofielen (auto, fiets, etc.)

## Installatie

Er zijn verschillende manieren om het pakket te installeren:

### 1. Direct vanaf GitHub

``` sh
pip install git+https://github.com/Hopsakee/optimalisatie_route_peilbuizen.git
```

### 2. Ontwikkelingsinstallatie

``` sh
# Clone de repository
git clone https://github.com/Hopsakee/optimalisatie_route_peilbuizen.git
cd optimalisatie_route_peilbuizen

# Installeer in development mode
pip install -e .
```

## Vereisten

- Python \>= 3.10
- Toegang tot WDODelta Azure SQL Database
- OpenRouteService API key

## Configuratie

1.  Maak een `.env` bestand aan in de root directory met de volgende
    variabelen:

<!-- -->

    OPENROUTESERVICE_KEY=your_api_key

2.  Pas indien nodig de instellingen aan in `settings.yaml`:

- Locaties van de input bestanden
- Locatie van de output directory
- Connectie gegevens met de Azure SQL Database
- Startlocatie voor de route
- Route profiel (auto/fiets)
- SQL queries

## Gebruik

### Basis Gebruik

``` python
from project.main import process_peilbuizen_routes
from project.data_get import get_data_from_azuresql

# Haal peilbuis data op
peilbuizen_df = get_data_from_azuresql()

# Bereken optimale routes
process_peilbuizen_routes(
    df=peilbuizen_df,
    start_address="Dokter Van Deenweg 186, Zwolle",
    route_profile="driving-car"
)
```

### Output

Het programma genereert: 1. Excel bestanden met geoptimaliseerde routes
per project 2. Google Maps URLs voor eenvoudige navigatie 3. Logging
informatie voor procesmonitoring

## Development

Dit project gebruikt nbdev voor ontwikkeling. Om wijzigingen door te
voeren:

1.  Werk in de notebooks in de `nbs/` directory
2.  Voer `nbdev_prepare` uit om wijzigingen te compileren

## Licentie

Dit project is gelicenseerd onder de MIT-licentie - zie het
[LICENSE](LICENSE) bestand voor details.

## Contact

Voor vragen of suggesties, neem contact op met: - Jelle de Jong
(jelledejong@wdodelta.nl)

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/Hopsakee/optimalisatie_route_peilbuizen)’s
[pages](https://Hopsakee.github.io/optimalisatie_route_peilbuizen/).
