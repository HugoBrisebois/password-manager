from setuptools import setup

setup(
    name='generator_password',
    version='1.0.0',
    description='A modern password manager with Tkinter UI and SQLite storage',
    author='Hugo Brisebois',
    packages=['generator_password'],
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'generator_password=generator_password.main:main'
        ],
        'gui_scripts': [
            'generator_password-gui=generator_password.__main__:main'
        ]
    },
)
