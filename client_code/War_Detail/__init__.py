from ._anvil_designer import War_DetailTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class War_Detail(War_DetailTemplate):
  def __init__(self, impact_id, war_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.impact_id = impact_id
    self.war_id = war_id

    self.item = anvil.server.call("get_war_details", war_id)
    self.init_war_details()
    self.init_war_plot()
    self.init_map()

  def init_war_details(self):
    text = f"""
## Konflikt Details
**{self.item['krieg_name']}**

### Zeitraum
- **Beginn:** {self.item['krieg_start']}
- **Ende:** {self.item['krieg_ende']}

### Auswirkungen
- **Todesopfer:** {self.item['krieg_tote']}
- **Verletzte:** {self.item['krieg_verletzte']}

### Hintergrund
{self.item['krieg_beschreibung']}
"""
    self.war_text.content = text

  def init_war_plot(self):
    labels = ['Todesopfer', 'Verletzte']
    values = [self.item['krieg_tote'], self.item['krieg_verletzte']]
  
    self.war_plot.data = [
      go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#e74c3c', '#f39c12']),
        textinfo='value+percent'
      )
    ]
  
    self.war_plot.layout = {
      'paper_bgcolor': 'rgba(0,0,0,0)',
      'plot_bgcolor': 'rgba(0,0,0,0)',
      'font': {'color': '#333'},
      'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
      'autosize': True,
    }

  def init_map(self):
    impacts = anvil.server.call("get_impacts_by_war", self.war_id)

    for impact in impacts:
      marker = GoogleMap.Marker(
        position=GoogleMap.LatLng(impact['latitude'], impact['longitude']),
        title=impact['name']
      )

      marker.set_event_handler('click', lambda i_id=impact['einschlag_id'], **e: self.open_impact_details(i_id))

      self.map.add_component(marker)

    if impacts:
      self.map.center = GoogleMap.LatLng(impacts[0]['latitude'], impacts[0]['longitude'])
      self.map.zoom = 2
      text = f"# Aufgezeichnete Bombeneinschläge dieses Konfliktes: {impacts[0]['count']}"
      self.war_text2.content = text

  def open_impact_details(self, impact_id):
    """Navigiert zur Detailansicht des gewählten Einschlags"""
    open_form('Impact_Detail', impact_id)

  @handle("back_button", "click")
  def back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Impact_Detail", self.impact_id)

  @handle("home_button", "click")
  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')
