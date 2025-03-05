import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sonnenbackup",
    use_scm_version=True,
    author="@MarkusBiggus",
    author_email="",
    description="SonnenBackup Batterie V2 API component",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/markusbiggus/sonnenbackup",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "tzlocal",
        "sonnen_api_v2>=0.5.14",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
