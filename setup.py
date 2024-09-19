from setuptools import setup, find_packages

setup(
    name="pybatch",
    author="Max Melin",
    author_email="mmelin@ucla.edu",
    description="A library for rapid execution of python scripts via batch submission systems",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "argparse",
    ],
    packages=find_packages(where="."),
    package_dir={"": "."},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pybatch = pybatch.cli:main",
        ],
    },
    # version could be dynamically retrieved here if needed
    # version="0.0.1"  # Uncomment this or use the dynamic approach if necessary
)