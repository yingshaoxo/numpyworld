#!/usr/bin/env /usr/bin/python3

from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()


class Tools():
    def push(self, comment):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def reset(self):
        t.run("""
git reset --hard HEAD^
""")

    def test(self):
        t.run("""
cd numpyworld
pytest -s --disable-pytest-warnings
        """)

    def install(self):
        t.run("""
sudo rm -fr dist
sudo rm -fr build
sudo -H python3 setup.py sdist bdist_wheel
cd dist
sudo pip3 uninstall -y numpyworld
sudo pip3 install *
""")

    def publish(self):
        t.run("""
sudo rm -fr dist
sudo rm -fr build
sudo pip3 install -U twine wheel setuptools
sudo -H python3 setup.py sdist bdist_wheel
twine upload dist/*
""")


py.make_it_runnable()
py.fire(Tools)
