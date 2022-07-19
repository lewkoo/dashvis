import json
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

package_author = package['author']
package_author_name = package_author.split(" <")[0]
package_author_email = package_author.split(" <")[1][:-1]

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=package["version"],
    author=package_author_name,
    author_email=package_author_email,
    description=package.get('description', package_name),
    keywords='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=package['homepage'],
    project_urls={
        'Documentation': 'https://github.com/lewkoo/dashvis/wiki',
        'Bug Reports': 'https://github.com/lewkoo/dashvis/issues',
        'Source Code': 'https://github.com/lewkoo/dashvis',
        'Discussions': 'https://github.com/lewkoo/dashvis/discussions',
        'Pull Requests': 'https://github.com/lewkoo/dashvis/pulls'
    },
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    readme="README.md",
    install_requires=[],
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Dash',
        'Intended Audience :: Developers',        
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
