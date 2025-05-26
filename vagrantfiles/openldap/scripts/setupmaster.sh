#!/bin/bash
# ANSIBLE INSTALL-----------------------------------------------------------------------------------------------------------------------------------------------
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip pipx git ansible
git clone https://github.com/akhos09/alacrittyforge.git
python3 --version
pipx ensurepath
pip3 install ansible --user --no-warn-script-location
# SSH ROOT------------------------------------------------------------------------------------------------------------------------------------------------------
mkdir -p /root/.ssh && cd /root/.ssh
echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
echo -e "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config
sudo ssh-keygen -t rsa -b 2048 -f id_rsa
# SSH ANSIBLE USER (delete the # if you want an independent and additional ansible user)------------------------------------------------------------------------
# useradd -m ansible -s /bin/bash
# echo "ansible:vagrant" | sudo chpasswd
# sudo chage -d 0 ansible
# sudo -u ansible mkdir -p /home/ansible/.ssh
# cd /home/ansible/.ssh
# sudo -u ansible ssh-keygen -f id_rsa2
# sudo mv ./id_rsa2.pub /root/.ssh/id_rsa2.pub
chmod 700 /root/.ssh
cd /root/.ssh/
# echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
nohup python3 -m http.server 80 &
echo -e "192.168.30.4 client1ldap\n192.168.30.5 client2ldap" >> /etc/hosts
echo -e "[clients]\nclient1ldap\nclient2ldap" > /root/openldap/machines.ini
# echo -e "[defaults]\ninventory=./machines.ini" > /root/openldap/ansible.cfg

# ansible -i machines.txt -m shell -a "ls -la /root/ | grep 'file'" /with/bin/bash
# ansible -i machines.txt -m command -a "ls -la /root/ | grep 'file'" /without/bin/bash
# all changes here