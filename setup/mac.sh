#!/usr/bin/env bash
if [ "$(uname)" != "Darwin" ]; then
exit 0
fi

touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress;
PROD=$(softwareupdate -l |
  grep "\*.*Command Line" |
  tail -n 1 | awk -F"*" '{print $2}' |
  sed -e 's/^ *//' |
  tr -d '\n')
softwareupdate -i "$PROD" --verbose;

export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles

if ! [ -x "$(command -v brew)" ]; then
    echo "安装 brew"
    ruby \
-e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" \
</dev/null
fi

if [ -x "$(command -v brew)" ]; then
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

brew update
brew install node
brew upgrade node
brew install git
brew upgrade git
fi

npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install -g 8gua
8gua
