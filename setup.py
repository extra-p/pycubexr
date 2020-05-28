import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycube_parser",
    version="0.0.1",
    author="David Gengenbach",
    author_email="info@davidgengenbach.de",
    description="Parser for *.cubex files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidgengenbach/pycube_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
