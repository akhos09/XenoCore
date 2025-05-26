#!/bin/bash
# SSH CONFIG ROOT MASTERNODE------------------------------------------------------------------------------------------------------------------------------------
sudo apt-get update && sudo apt-get upgrade -y
echo "PubkeyAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
echo "AuthorizedKeysFile .ssh/authorized_keys" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
mkdir -p /root/.ssh
chmod 700 /root/.ssh
cd /root/.ssh
wget http://192.168.30.3/id_rsa.pub
# wget http://192.168.30.3/id_rsa2.pub
cat id_rsa.pub >> authorized_keys
chmod 600 authorized_keys
# USER ANSIBLE CONFIG (delete the # if you want an independent and additional ansible user)---------------------------------------------------------------------
# useradd -m ansible -s /bin/bash
# echo "ansible:vagrant" | sudo chpasswd
# sudo chage -d 0 ansible
# mkdir -p /home/ansible/.ssh
# chmod 700 /home/ansible/.ssh
# mv /root/.ssh/id_rsa2.pub /home/ansible/.ssh
# cat /home/ansible/.ssh/id_rsa2.pub >> /home/ansible/.ssh/authorized_keys
# chmod 600 /home/ansible/.ssh/authorized_keys
# chown -R ansible:ansible /home/ansible/.ssh
# echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# ssh -i id_rsa2 ansible@192.168.30.4-6