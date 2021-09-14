from setuptools import setup

from ssl_metrics_git_commits_loc import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ssl-metrics-git-commits-loc",
    packages=["ssl_metrics_git_commits_loc"],
    version=version.version(),
    description="SSL Metrics - Git History (LOC/KLOC) Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc",
    },
    keywords=["github", "software engineering", "metrics", "issues"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
    install_requires=["matplotlib", "numpy", "pandas", "progress", "python-dateutil"],
    entry_points={
        "console_scripts": [
            "ssl-metrics-git-commits-loc = ssl_metrics_git_commits_loc.git_commits_loc:main",
            "ssl-metrics-git-commits-graph = ssl_metrics_git_commits_loc.create_graph:main",
        ]
    },
)
