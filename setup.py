
#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.5'

setup(name='seu3d-tool',
      version=VERSION,
      description="A web server for visualization of spatial-temporal single cell transcriptomics data",
      long_description='A test release',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python single cell transcriptomics 3D visualization spatial temporal',
      author='wuc',
      author_email='1078497976@qq.com',
      url='https://github.com/RainyBlue-w/STOmics-3D',
      license='GNU GPLv3',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        'seu3d_tool': ['*.yaml', 'pages/*', 'assets/*']
      },
      install_requires=[
        'dash==2.16.1',
        'dash-bootstrap-components',
        'dash-extensions==1.0.14',
        'dash-iconify==0.1.2',
        'dash-mantine-components==0.12.1',
        'feffery-antd-components==0.2.11',
        'feffery-utils-components==0.1.29',
        'plotly',
        'scanpy',
        'squidpy',
        'typing',
        'typing_extensions',
        'diskcache',
        'fastapi',
        'uvicorn',
        'multiprocess',
        'ruamel.yaml==0.18.6'
      ],
      zip_safe=False,
      entry_points={
        'console_scripts':[
            'seu3d-tool = seu3d_tool:run_app',
        ]
      },
)
 