from setuptools import setup, find_packages

setup(
    # info
    name='dynamic_docs_server',
    version='0.0.1',
    url='http://github.com/andrewmfiorillo/dynamic-docs-server',
    license='MIT',
    author='Andrew Fiorillo',
    author_email='andrewmfiorillo@gmail.com',
    description="A versatile server for documentation written in static HTML and Markdown.",

    # code info
    packages=find_packages(),

    install_requires=[
        'flask', 'pathlib2', 'mistune'
    ],
    dependency_links=[
    ],
    entry_points={
        'console_scripts': [
            'dynamic_docs_server = dds.cli:main'
        ],
    },

    # required binaries, reflected in MANIFEST.in too
    include_package_data=True,
    package_data={
        '': ['*.*'],
    },
    exclude_package_data={
        '': ['*.jpg', '*.png', '*.pdf'],
    },
)
