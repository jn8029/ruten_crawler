import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rutencrawler",
    version="0.0.5",
    author="jn8029",
    author_email="warren.y.cheng@gmail.com",
    description="A crawler for product information of sellers on Ruten.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jn8029/ruten_crawler",
    packages=setuptools.find_packages(),
    install_requires=['bs4', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
