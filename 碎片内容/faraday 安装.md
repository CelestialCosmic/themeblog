su root
usermod -aG sudo sirius
sudo usermod -aG faraday sirius
sudo apt install postgresql
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo faraday-manage initdb
