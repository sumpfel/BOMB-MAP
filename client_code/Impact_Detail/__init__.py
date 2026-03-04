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

    self.init_impact_plot()
    
  @handle("back_button", "click")
  def back_button_click(self, **event_args):
    open_form('Home')
    pass

  def init_bomb_card(self):
    self.init_bomb_text()
    self.init_impact_plot()
    
  def init_bomb_text(self):
    pass
  
  def init_impact_plot(self):
    # Daten für das Diagramm vorbereiten
    labels = ['Todesopfer', 'Verletzte']
    values = [self.item['todesopfer'], self.item['verletzte']]

    self.bomb_plot.data = [
      go.Pie(
        labels=labels,
        values=values,
        hole=0.4, # Macht ein Donut-Diagramm daraus (sieht moderner aus)
        marker=dict(colors=['#e74c3c', '#f39c12']), # Rot für Tote, Orange für Verletzte
        textinfo='value+percent' # Zeigt absolute Zahlen und Prozent an
      )
    ]

    # Layout anpassen (Titel, Farben, etc.)
    self.bomb_plot.layout = {
      'title': f"Opferstatistik: {self.item['waffe_name']}",
      'paper_bgcolor': 'rgba(0,0,0,0)', # Transparent an den Hintergrund anpassen
      'plot_bgcolor': 'rgba(0,0,0,0)',
      'font': {'color': '#333'}
    }