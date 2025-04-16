"""
Setup script for the Financial Reports MCP server.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="financial-reports-mcp-server",
    version="0.1.0",
    author="Alex Isaev",
    author_email="your.email@example.com",
    description="An MCP server for accessing financial reports data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itisaevalex/financial-reports-mcp-server",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.json"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastmcp>=2.0.0",
        "httpx>=0.26.0",
        "pydantic>=2.5.3",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "financial-reports-mcp-server=src.financial_reports_mcp:run_cli",
        ],
    },
)
