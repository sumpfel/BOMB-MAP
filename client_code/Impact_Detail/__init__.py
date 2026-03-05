from ._anvil_designer import Impact_DetailTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Impact_Detail(Impact_DetailTemplate):
  def __init__(self, impact_id: int, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Daten vom Server abrufen
    self.item = anvil.server.call("get_impact_details", impact_id)
    self.headline.text = self.item["einschlag_name"]

    self.init_bomb_card()
    self.init_impact_card()
    
  @handle("back_button", "click")
  def back_button_click(self, **event_args):
    open_form('Home')
    pass

  ####
  #### ------ bomb
  ####
  
  def init_bomb_card(self):
    self.init_bomb_text()
    
  def init_bomb_text(self):
    self.bomb_headline.text = self.item['waffen_name']
    self.bomb_label.text = f"""Explosion Power:{self.item['waffen_leistung']}
    Weapon-Type: {self.item['waffen_typ']}"""
    print(self.item)
  ####
  #### ------ impact
  ####
  def init_impact_card(self):
    self.init_impact_plot()
    
  def init_impact_plot(self):
    # Daten für das Diagramm vorbereiten
    labels = ['Todesopfer', 'Verletzte']
    values = [self.item['todesopfer'], self.item['verletzte']]

    self.impact_plot.data = [
      go.Pie(
        labels=labels,
        values=values,
        hole=0.4, # Macht ein Donut-Diagramm daraus (sieht moderner aus)
        marker=dict(colors=['#e74c3c', '#f39c12']), # Rot für Tote, Orange für Verletzte
        textinfo='value+percent' # Zeigt absolute Zahlen und Prozent an
      )
    ]

    # Layout anpassen (Titel, Farben, etc.)
    self.impact_plot.layout = {
      'paper_bgcolor': 'rgba(0,0,0,0)', # Transparent an den Hintergrund anpassen
      'plot_bgcolor': 'rgba(0,0,0,0)',
      'font': {'color': '#333'},
      'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
      'autosize': True,
    }

  def init_impact_map(self):
    self.impact_map.map_data.add(GoogleMap.Data.Feature(
      geometry=GoogleMap.Data.Point(
        GoogleMap.LatLng(self.item['latitude'],self.item['longitude']))))

    self.impact_map.map_data.style = GoogleMap.Data.StyleOptions(
      icon=GoogleMap.Symbol(
        path=GoogleMap.SymbolPath.CIRCLE,
        scale=30,
        fill_color='red',
        fill_opacity=0.3,
        stroke_opacity=1,
        stroke_weight=1
      )
    )

  ####
  #### ------ impact
  ####