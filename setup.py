from setuptools import setup, find_packages
import sys
sys.path.append('./robotapp')
sys.path.append('./robotapp/tests')


setup(
    name = "robotapp",
    version = "0.1",
    packages = find_packages(),
    test_suite = 'test'
)
