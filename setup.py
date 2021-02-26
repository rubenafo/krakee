from setuptools import setup, find_packages

setup(
    name="krapanda",
    version="0.5",
    author="Ruben Afonso",
    author_email="rbfrancos@gmail.com",
    description="Kraken Exchange API with a thin pandas Dataframe wrap",
    url="https://github.com/rubenafo/krapanda",
    keywords = ["kraken", "cryptocurrencies", "exchange", "python", "bitcoin"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = ['krakenex', 'pandas']
)
