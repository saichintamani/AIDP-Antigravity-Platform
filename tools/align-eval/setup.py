from setuptools import setup, find_packages

setup(
    name="align-eval",
    version="1.0.0",
    description="Administer historical replay baselines for epistemic alignment evaluation.",
    author="Antigravity Research",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ]
)
