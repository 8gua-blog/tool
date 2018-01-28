#!/usr/bin/env xonsh

import re
from os.path import dirname, join, abspath, exists, basename
from json import load, dump
import toml
import sys

__dirname = dirname(abspath(__file__))
sys.path.append(__dirname)
from dnspod import Dnspod
from config import CONFIG

VERSION_INCR = 1

def main():

    root = dirname(dirname(__dirname))
    version_toml_path = join(root, '.release.version.toml')
    package_path = join(
        root,
        "package.json"
    )

    release_path = join(dirname(root), "release/srv")

    if not exists(release_path):
        print(release_path, '不存在')
        return

    cd @(root)
    git add -u

    try:
        version_toml = toml.load(version_toml_path)
    except:
        version_toml = {}

    if re.findall("nothing.* to commit", $(git st), re.S):
        last_commit = $(git log -1).split("\n",1)[0].split(" ",1)[-1]
        if last_commit in version_toml:
            print(f"commit {last_commit} released version {version_toml[last_commit]}")
            return

    with open(package_path) as f:
        package = load(f)
        version = package['version']
        version = list(map(int, version.split(".")))
        version[-1]+=VERSION_INCR
        version = ".".join(map(str, version))
        package['version'] = version

    with open(package_path,"w") as f:
        dump(package, f, indent=4, sort_keys=True)

    comment = f"PUBLISH VERSION {version}"

    print(comment)


    cd @(release_path)
    find . | grep -vE '\.git/|.git$|\.$|\.\.$' | xargs rm -rf

    cd @(root)
    print(f">> cd {root}")
    git add -u
    git commit -m @(comment)
    last_commit = $(git log -1).split("\n",1)[0].split(" ",1)[-1]

    git archive master | tar -x -C @(release_path)

    print(f">> cd {release_path}")
    cd @(release_path)

    rm -rf nodemon.json .gitignore dev py *.md test LICENSE release.sh
    git add .

    gitignore = join(root, ".gitignore")
    cp @(gitignore) .
    git add .gitignore

    git commit -m @(comment)
    git push origin master
    git push github master

    version_toml[last_commit] = version

    with open(version_toml_path, "w") as f:
        toml.dump(version_toml, f)

    dnspod_update(version)

def dnspod_update(version):
    domain = CONFIG.HOST.TXT
    dnspod = Dnspod(*CONFIG.DNSPOD)
    dnspod.update(domain, "cli-v", version)
    dnspod.update(domain, "cli-git", " ".join(CONFIG.GIT))


if __name__ == "__main__":
    main()
