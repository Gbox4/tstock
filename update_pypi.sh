python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf build dist tstock.egg-info
