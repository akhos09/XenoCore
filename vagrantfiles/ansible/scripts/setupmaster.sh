#!/bin/bash
# ANSIBLE INSTALL-----------------------------------------------------------------------------------------------------------------------------------------------
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip pipx
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
cd /root/.ssh/
# echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
python3 -m http.server 80 &
mkdir -p /root/ansible/
echo -e "192.168.30.4 node1\n192.168.30.5 node2\n192.168.30.6 node3" >> /etc/hosts
echo -e "[clients]\nnode1\nnode2\nnode3" > /root/ansible/machines.ini
echo -e "[defaults]\ninventory=./machines.ini" > /root/ansible/ansible.cfg
# ansible -i machines.txt -m shell -a "ls -la /root/ | grep 'file'" /with/bin/bash
# ansible -i machines.txt -m command -a "ls -la /root/ | grep 'file'" /without/bin/bash
# all changes here