from setuptools import setup, find_packages

setup(
    name='albatross_project',
    version='0.1',
    description='Implementación del protocolo ALBATROSS con simulación de red distribuida',
    author='Tu Nombre',
    author_email='tuemail@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask==2.0.1',
        'numpy==1.21.0',
        'pytest==6.2.4',
    ],
    entry_points={
        'console_scripts': [
            'albatross=main:main',
        ],
    },
)