from setuptools import setup, find_packages

setup(
    # info
    name='dds',
    version='0.1.0',
    url='http://github.com/andrewmfiorillo/dds',
    license='MIT',
    author='Andrew Fiorillo',
    author_email='andrewmfiorillo@gmail.com',
    description="A versatile server for documentation written in static HTML and Markdown.",

    # code info
    packages=find_packages(),

    install_requires=[
        'flask', 'pathlib2', 'mistune',
    ],
    dependency_links=[
    ],
    entry_points={
        'console_scripts': [
            'dds = dds.cli:main',
            'dds_bootstrap = dds.bootstrap:main',
        ],
    },

    # required binaries, reflected in MANIFEST.in too
    include_package_data=True,
    package_data={
        '': ['*.*'],
    },
    exclude_package_data={
        '': ['*.jpg', '*.png', '*.pdf', '*.jinja', '*.css'],
    },
)
