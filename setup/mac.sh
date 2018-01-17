
if [ ! -f "/usr/local/bin/npm" ]; then
if [ ! -f "/usr/local/bin/brew" ]; then
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi
brew install node
fi
