import yaml
import os
import anndata
from typing import Dict
import plotly.express.colors as pxcolors
import pkg_resources

seu3d_dist = pkg_resources.get_distribution("seu3d-tool")
pkg_path = os.path.join(seu3d_dist.location, 'seu3d_tool')

def config_colormap(config_pth: str):
    seq_colors = pxcolors.qualitative.Alphabet

    with open(config_pth, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    dataset: Dict[str, anndata.AnnData] = {}
    all_celltypes: set[str] = set()

    for name, path in config['Dataset'].items():
        dataset[name] = anndata.read_h5ad(path, backed='r')
        for celltype in dataset[name].obs[config['annotation']]:
            all_celltypes.add(celltype)

    target_len = len(all_celltypes)
    seq_colors = seq_colors*(target_len // len(seq_colors) + 1)
    seq_colors = seq_colors[0:target_len]

    colormap = {'colormap': dict(zip(all_celltypes, seq_colors))}

    with open(config_pth, 'a') as f:
        yaml.dump(colormap, f)