from setuptools import setup, find_packages

setup(
    name='ctkchart',  # Replace with your package name
    version='2.2.1',  # Replace with your package version
    author='Thisal-D',  # Replace with your name
    author_email='',  # Replace with your email
    description='Line-chart Widget for customtkinter, Python library for creating live updating line charts in CustomTkinter.',
    long_description=open('README.md').read(),  # Ensure you have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/Thisal-D/ctkchart',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    install_requires=[
        'customtkinter',  # List your package dependencies here
    ],
    include_package_data=True,
)
