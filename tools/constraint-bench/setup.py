from setuptools import setup, find_packages

setup(
    name="constraint-bench",
    version="1.0.0",
    description="Evaluating LLM adherence to negative epistemic constraints.",
    author="Antigravity Research",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.0.0",
        "pydantic>=2.0.0"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ]
)
