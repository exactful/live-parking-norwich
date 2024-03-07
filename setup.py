from setuptools import setup, find_packages

VERSION = "0.0.2"

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="live_parking_norwich", 
        version=VERSION,
        author="Daniel Cooper",
        url="https://github.com/exactful/live-parking-norwich",
        description="This package provides real-time information about available parking spaces in car parks and park & ride sites around Norwich.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages('app'),
        package_dir={'': 'app'},
        keywords="parking parking-spaces park-and-ride Norwich",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers"])
