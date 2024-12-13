from ruamel.yaml import YAML
import os
import anndata
from typing import Dict
import plotly.express.colors as pxcolors
import pkg_resources

seu3d_dist = pkg_resources.get_distribution("seu3d-tool")
pkg_path = os.path.join(seu3d_dist.location, 'seu3d_tool')

def config_colormap(config_pth: str):
    seq_colors = pxcolors.qualitative.Alphabet

    yaml = YAML()
    
    with open(config_pth, 'r') as f:
        config = yaml.load(f)

    dataset: Dict[str, anndata.AnnData] = {}
    new_celltypes: set[str] = set()

    for name, path in config['Dataset'].items():
        dataset[name] = anndata.read_h5ad(path, backed='r')
        for celltype in dataset[name].obs[config['annotation']]:
            celltype = str(celltype)
            if ( config['colormap'] is None 
                or celltype not in config['colormap'] ):
                new_celltypes.add(celltype)

    target_len = len(new_celltypes)
    seq_colors = seq_colors*(target_len // len(seq_colors) + 1)
    seq_colors = seq_colors[0:target_len]

    colormap_append = dict(zip(new_celltypes, seq_colors))
    if config['colormap']:
        config['colormap'].update(colormap_append)
    else:
        config['colormap'] = colormap_append

    with open(config_pth, 'w') as f:
        yaml.dump(config, f)