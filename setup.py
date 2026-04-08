from setuptools import setup, find_packages

setup(
    name="email-agent-env",
    version="0.1.2",
    packages=find_packages(include=["env", "env.*", "server", "server.*"]),
)
