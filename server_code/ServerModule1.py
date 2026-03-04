import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

@anvil.server.callable
def get_bomb_impacts():
  with sqlite3.connect(data_files["bomb_impacts.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
            SELECT 
                b.einschlag_id, 
                b.name AS einschlag_name, 
                w.name AS bomben_name, 
                b.datum, 
                b.latitude, 
                b.longitude, 
                b.todesopfer, 
                b.verletzte, 
                b.beschreibung
            FROM bombeneinschlag b
            JOIN waffe w ON b.waffe_id = w.waffe_id
        """)

    return [dict(row) for row in cur.fetchall()]

@anvil.server.callable
def get_impact_details(impact_id):
  """
    Ruft alle Details zu einem spezifischen Bombeneinschlag ab.
    Inklusive verknüpfter Informationen zu Krieg, Land, Waffe und Zieltyp.
    """
  with sqlite3.connect(data_files["bomb_impacts.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
            SELECT 
                -- Basisdaten des Einschlags
                b.einschlag_id,
                b.name AS einschlag_name,
                b.datum AS einschlag_datum,
                b.latitude,
                b.longitude,
                b.todesopfer,
                b.verletzte,
                b.beschreibung AS einschlag_beschreibung,
                
                -- Informationen zum historischen Kontext (Krieg)
                k.name AS krieg_name,
                k.beginn AS krieg_start,
                k.ende AS krieg_ende,
                k.beschreibung AS krieg_beschreibung,
                k.todesopfer_gesamt AS krieg_tote_insgesamt,
                
                -- Geografische Daten
                l.name AS land_name,
                l.kontinent,
                
                -- Technische Daten (Waffe)
                w.name AS waffen_name,
                w.typ AS waffen_typ,
                w.sprengkraft AS waffen_leistung,
                
                -- Strategische Daten (Zieltyp)
                z.bezeichnung AS zieltyp_name,
                z.beschreibung AS zieltyp_info
                
            FROM bombeneinschlag b
            JOIN krieg k ON b.krieg_id = k.krieg_id
            JOIN land l ON b.land_id = l.land_id
            JOIN waffe w ON b.waffe_id = w.waffe_id
            JOIN zieltyp z ON b.zieltyp_id = z.zieltyp_id
            WHERE b.einschlag_id = ?
        """, (impact_id,))

    row = cur.fetchone()

    if row:
      # Als Dictionary zurückgeben, damit Anvil-Bindings (self.item) funktionieren
      return dict(row)
    return None