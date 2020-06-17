import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-cube",
    version="0.0.1",
    author="Extra-P project",
    author_email="extra-p@lists.parallel.informatik.tu-darmstadt.de",
    description="Python Cube file reader for the Cube 4.x file format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/extra-p/py-cube",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
