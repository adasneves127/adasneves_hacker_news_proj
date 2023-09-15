apt-get update # Update your APT Cache
apt-get install -y ca-certificates curl gnupg # Make sure our required packages are installed for our keyring
mkdir -p /etc/apt/keyrings # Make a keyring directory
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg # download the nodeJS Keyring


# Get the deb file for the version specified
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list

# Update and install apt
apt-get update
apt-get install nodejs -y