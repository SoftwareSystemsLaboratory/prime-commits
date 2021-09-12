from setuptools import setup

from ssl_metrics_git_commits_loc import version

setup(
    name="ssl-metrics-git-commits-loc",
    packages=["ssl_metrics_git_commits_loc"],
    version=version.version(),
    description="SSL Metrics - Git History (LOC/KLOC) Analysis",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="Apache License 2.0",
    url="https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc",
    keywords=["git", "software engineering", "metrics", "commits"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
    install_requires=["matplotlib", "numpy", "pandas", "progress", "python-dateutil"],
    entry_points={
        "console_scripts": [
            "ssl-metrics-git-commits-loc = ssl_metrics.git_commits_loc:main",
            "ssl-metrics-git-commits-graph = ssl_metrics.create_graph:main",
        ]
    },
)
