# setup.py
import setuptools

setuptools.setup(
    name="PyGJK",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "pyqt6",
        "scipy",
        "pyqtgraph",
    ]
)
