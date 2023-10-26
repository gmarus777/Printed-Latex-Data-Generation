from setuptools import setup, find_packages

setup(
    name='latex-generator',
    version='0.2',
    package_dir={'': 'src'},  # Tell setuptools that your package (source code) resides in the 'src' directory
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        # List your Python dependencies here, if any.
    ],
    entry_points={
        'console_scripts': [
            'latex-generator=main:main',  # Point to the 'main' function in 'main_module'
        ],
    },
)
