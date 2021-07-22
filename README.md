# galaxy-ansible

An Ansible playbook to init a Galaxy dev server.

Refer to the [Galaxy tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible-galaxy/tutorial.html) for additional guidance.

---

This playbook enables interactive tools, which require a wildcard DNS for the host machine - [more info.](https://training.galaxyproject.org/training-material/topics/admin/tutorials/interactive-tools/tutorial.html)

---

```sh
# Install dependancies
sudo apt install -y ansible python3 python3-pip

echo "export EDITOR=nano" >> ~/.bashrc  # Otherwise defaults to vi

# Clone this repo
git clone https://github.com/neoformit/galaxy-ansible.git
cd galaxy-ansible

# Create vault password and enter secrets
rm group_vars/secrets.yml
openssl rand -base64 24 > ~/.ansible.vault.pass
ansible-vault create group_vars/secrets.yml --vault-password=~/.ansible.vault.pass

    # Enter secrets, save and exit:
    # > vault_secret_key: mysecretkeystring37465
    # > vault_dns_cloudflare_api_token: myapikey12345

ansible-galaxy install -p roles -r requirements.yml
ansible-playbook galaxy.yml
```
