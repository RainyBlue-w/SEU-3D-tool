# SEU-3D-tool

Tool for building SEU-3D-like spatial-temporal omics web browser.

# Installation

It's recommended to install the seu3d-tool in a conda enviroment.  

```bash
conda create -n seu3d python=3.11
conda activate seu3d
pip install seu3d-tool
```

# Usage

### Server configuration

If you don't have a config file, you should first generate one use:

```bash
# Generating a configuration file named `seu3d_config.yaml` in current directory.
seu3d-tool config --new
```

The configuration file `seu3d_config.yaml` looks like:

```bash
# -------
# data to show on the server, in .h5ad format
# a unique name for each file, and the path to the file
# e.g. 
# Dataset:
#   E7.5: /path/to/E7.5.h5ad
#   E8.0: /path/to/E8.0.h5ad
Dataset:

# -------
# name for the celltype annotation stored in the .h5ad files (adata.obs[annotation]), default: 'celltype'
annotation: celltype

# -------
# name for the 3D embedding stored in the .h5ad files (adata.obsm[3D_embedding]), default: 'X_spatial'
3D_embedding: X_3D

# -------
# dir to store cache files, default: './cache'
cache_dir: ./cache

# -------
# colormap:
# Colormap will be auto generated when first startup. After that, you could use
# 'seu3d-tool config --current > seu3d_config.yaml' to get updated config file and modify the colormap,
# and use 'seu3d-tool config --update seu3d_config.yaml' to update server configuration.
```

You should fill all the configuration items except the `colormap` (server will auto generate it). Then you could update the server configuration use:

```bash
seu3d-tool config --update seu3d_config.yaml
```

If you want to check the current configuration, you could use:

```bash
seu3d-tool config --current
```

It will print the current configuration file of server, you could export it to a file and modify it.

```bash
seu3d-tool config --current > seu3d_config.yaml
```

### Start the server

Now the configuration is completed, you could start the server by:

```bash
seu3d-tool
```

If you want to change the port(default: 8050) and host (default: 0.0.0.0) of the server, you could start it with some extra parameters:

```bash
seu3d-tool --port=8051 --host=xxx.xx.xx.x
```

### Customized colormap

For each unique cell type annotation of all the data in dataset, a initial color will be assigned. The the colormap will be stored into server configuration after server startup, you could get the updated configuration file and customize the colormap by yourself.

```bash
seu3d-tool config --current > seu3d_config.yaml
vim seu3d_config.yaml
seu3d-tool config --update seu3d_config.yaml
```