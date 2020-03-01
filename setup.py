from setuptools import setup, find_packages

setup(
    name='flexchain',
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'mysql-connector',
        'pandas',
        'matplotlib',
        'statsmodels'
    ]
)
