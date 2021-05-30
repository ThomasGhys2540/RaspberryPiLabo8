# RaspberryPiLabo8

## Team
- Claeys Ailko
- Ghys Thomas
- Van den Broeck Sarah

## Components
### Broker
- MQTT
### Game engine
- Maakt de keuze welke speler met welke racket speelt
- Houd de achterliggende logica, events en acties bij 
- Communiceert via de broker
### Game client
- Tekenen grafische objecten in een GUI
- 3 drukknoppen om het spel te besturen
  - 1 knop voor naar boven te bewegen
  - 1 knop voor naar beneden te bewegen
  - 1 knop voor snelheid
- 2 Led's voor aanduiding welke speler je bent
- 1 Led die zal knipperen net voor het spel start
- Grafische button om het spel te starten

## Libraries used
- Tkinter
- RPi.GPIO
- threading
- math
- paho
