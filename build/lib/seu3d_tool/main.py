import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_extensions.enrich import html, DashProxy, LogTransform, ServersideOutputTransform, MultiplexerTransform
import feffery_antd_components as fac
from dash import DiskcacheManager
import diskcache
from dash_extensions.enrich import FileSystemBackend
import os
import argparse

from config_colormap import config_colormap

if not os.path.exists('./colormap.yaml'):
  config_colormap()

background_callback_manager = DiskcacheManager(diskcache.Cache("./cache"))

app = DashProxy(
  __name__, 
  external_stylesheets=[
    dbc.themes.BOOTSTRAP
  ],
  external_scripts = [
    {'src': 'https://deno.land/x/corejs@v3.31.1/index.js', 'type': 'module'}
  ],
  transforms=[
    LogTransform(), 
    ServersideOutputTransform(backends=[FileSystemBackend("./cache")]), 
    MultiplexerTransform()
  ],
  use_pages=True,
  requests_pathname_prefix='/',
  background_callback_manager=background_callback_manager
)

app.layout = dmc.NotificationsProvider(html.Div([
    dash.page_container
]))


def run_app():
  parser = argparse.ArgumentParser(description='Run the web server')
  parser.add_argument('--host', default='0.0.0.0', required=False, help='Host to run the server on (default: 0.0.0.0)')
  parser.add_argument('--port', default=8050, required=False, help='Port to run the server on (default: 8050)')
  args = parser.parse_args()
      
  app.run(
    host=args.host,
    port=args.port,
  )
