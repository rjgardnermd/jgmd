# jgmd: A general-purpose utility package

For learning how to create your own python package, this article is great:
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56


## Notes to self:
### To update this package:
- update the code
- ACTIVATE THE VENV: . ./venv/bin/activate
- update release version in setup.py (two spots)
- ENSURE THAT ANY NEW FOLDERS HAVE __init__.py (bc they won't be picked up otherwise -> package will silently fail to update)
- run the following script with commitMsg and version as params
    ./runToUpdate.sh "commitMsg" "4.0.5"
- then upgrade the package to test the new version: pip install jgmd --upgrade





## OLD
### To update this package:
- update the code
- update release version in setup.py (two spots)
- push to repo
    git add .
    git commit -m "some commit message"
    git push
- cut a new release
    git tag -a v2.0.1 -m "Minor change"
    git push origin v2.0.1
- python setup.py sdist
- twine upload dist/*
- then upgrade the package to test the new version: pip install jgmd --upgrade