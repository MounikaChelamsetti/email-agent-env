from setuptools import setup, find_packages

setup(
    name="email-agent-env",
    version="0.1.1",
    packages=find_packages(include=["env", "env.*"]),
)
