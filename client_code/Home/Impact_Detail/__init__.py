from ._anvil_designer import Impact_DetailTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Impact_Detail(Impact_DetailTemplate):
  def __init__(self, impact_id: int, **properties):
    self.init_components(**properties)
    
    self.impact_id = impact_id
    self.item = anvil.server.call("get_impact_details", impact_id)
    self.headline.text = self.item["einschlag_name"]

    self.init_bomb_card()
    self.init_impact_card()
    self.init_target_card()
    self.init_war_card()
    
  @handle("back_button", "click")
  def back_button_click(self, **event_args):
    open_form('Home')
    pass

  ####
  ####------- Target
  ####
  def init_target_card(self):
    self.init_target_text()

  def init_target_text(self):
    self.target_headline.text = f"Ziel: {self.item['zieltyp_name']}"
    self.target_text.content = f"{self.item['zieltyp_info']}"
  ####
  ####------- War
  ####

  def init_war_card(self):
    self.init_war_plot()
    self.war_headline.text = "Konflikt: " + self.item["krieg_name"]

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
  
  ####
  #### ------ Bomb
  ####
  
  def init_bomb_card(self):
    self.init_bomb_text()

    
  def init_bomb_text(self):
    self.bomb_headline.text = "Bombe: " + self.item['waffen_name']
    self.bomb_text.content = f"""**Explosions Kraft:** {self.item['waffen_leistung']}
**Waffen-Typ:** {self.item['waffen_typ']}"""
  ####
  #### ------ Impact
  ####
  def init_impact_card(self):
    self.init_impact_plot()
    self.init_impact_map()
    
  def init_impact_plot(self):
    labels = ['Todesopfer', 'Verletzte']
    values = [self.item['todesopfer'], self.item['verletzte']]

    self.impact_plot.data = [
      go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#e74c3c', '#f39c12']),
        textinfo='value+percent'
      )
    ]

    self.impact_plot.layout = {
      'paper_bgcolor': 'rgba(0,0,0,0)',
      'plot_bgcolor': 'rgba(0,0,0,0)',
      'font': {'color': '#333'},
      'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
      'autosize': True,
    }

  def legend_item(self, color, text):
    item = FlowPanel(spacing="tiny")

    color_box = Label(
      text="            ",
      background=color,
      border="1px solid black"
    )
  
    label = Label(text=text)
  
    item.add_component(color_box)
    item.add_component(label)
  
    return item
  
  def init_impact_map(self):
    #----map legend
    self.legend_panel.clear()
    self.legend_panel.role = "card"
    
    title = Label(text="Verletzungs Legende", bold=True)
    
    row = FlowPanel(spacing="large")
    
    row.add_component(self.legend_item("orange", "sicherer Tod"))
    row.add_component(self.legend_item("#fddc3b", "schwer Verletzt"))
    row.add_component(self.legend_item("yellow", "leicht Verletzt"))
    
    self.legend_panel.add_component(title)
    self.legend_panel.add_component(row)
    
    #----map
    pos = GoogleMap.LatLng(self.item['latitude'],self.item['longitude'])
    self.impact_map.center = pos
    self.impact_map.zoom = 13

    death_circle = GoogleMap.Circle(
      center=pos,
      radius=self.item["certain_death_radius"],
      fill_color="red",
      fill_opacity=0.7,
      stroke_color="red",
      stroke_opacity=1,
      stroke_weight=1
    )

    heavy_injury_circle = GoogleMap.Circle(
      center=pos,
      radius=self.item["heavy_injury_radius"],
      fill_color="orange",
      fill_opacity=0.6,
      stroke_color="orange",
      stroke_opacity=1,
      stroke_weight=1
    )

    light_injury_circle = GoogleMap.Circle(
      center=pos,
      radius=self.item["small_injury_radius"],
      fill_color="yellow",
      fill_opacity=0.4,
      stroke_color="yellow",
      stroke_opacity=1,
      stroke_weight=1
    )

    self.impact_map.add_component(light_injury_circle)
    self.impact_map.add_component(heavy_injury_circle)
    self.impact_map.add_component(death_circle)

  ####
  #### ------ 
  ####

  @handle("war_button", "click")
  def war_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home.War_Detail', self.impact_id, self.item["krieg_id"])
