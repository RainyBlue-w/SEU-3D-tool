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

from seu3d_tool.config_colormap import config_colormap
import pkg_resources
import sys
import yaml

import shutil

parser = argparse.ArgumentParser(description='Run the web server')
parser.add_argument('--host', default='0.0.0.0', required=False, help='Host to run the server on (default: 0.0.0.0)')
parser.add_argument('--port', default=8050, required=False, help='Port to run the server on (default: 8050)')

subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
config_parser = subparsers.add_parser('config', help='Server configuration')
config_group = config_parser.add_mutually_exclusive_group(required=True)
config_group.add_argument('--new', action='store_true' ,help='Generate a new config file')
config_group.add_argument('--update', type=str, help='Path to finished configure file. This will updatd server config with given file')
config_group.add_argument(
  '--current', action='store_true',
  help= '''Print current configuration file. 
    You could modify and use it to update server configuration.
  '''
)
args = parser.parse_args()

seu3d_dist = pkg_resources.get_distribution("seu3d-tool")
pkg_path = os.path.join(seu3d_dist.location, 'seu3d_tool')

def run_app():
  
  if args.subcommand == 'config':
    if args.new:
      try:
        shutil.copy(os.path.join(pkg_path, 'config_template.yaml'), './seu3d_config.yaml')
        print('Configuration file generated, filling in the necessary information and start the server using it.')
      except IOError as e:
        print("Unable to create configuration file. %s" % e)
        exit(1)
      except:
        print("Unexpected error:", sys.exc_info())
        exit(1)
    elif args.current:
      if os.path.exists(os.path.join(pkg_path, 'seu3d_config.yaml')):
        with open(os.path.join(pkg_path, 'seu3d_config.yaml'), 'r') as f:
          for lines in f.readlines():
            print(lines, end='')
      else: 
        print('No configuration yet.')
    else:
      try:
        shutil.copy(args.update, os.path.join(pkg_path, 'seu3d_config.yaml')) # 覆盖
        print('Configuration updated.')
      except:
        print('Configuration failed:', sys.exc_info())
        exit(1)
      
  else:
    config_pth = os.path.join(pkg_path, 'seu3d_config.yaml')
    with open(config_pth, 'r') as f:
      config = yaml.safe_load(f)

    if 'colormap' not in config:
      config_colormap(config_pth)

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
        ServersideOutputTransform(backends=[FileSystemBackend(config['cache_dir'])]), 
        MultiplexerTransform()
      ],
      use_pages = True,
      pages_folder = os.path.join(pkg_path, 'pages'),
      requests_pathname_prefix = '/',
      background_callback_manager = DiskcacheManager(
        diskcache.Cache(config['cache_dir'])
      )
    )

    app.layout = html.Div([
        dash.page_container
    ])

    app.run(
      host=args.host,
      port=args.port,
    )