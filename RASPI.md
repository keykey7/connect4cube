# Raspberry PI Quirks

### Headless Setup
Flash a Raspian on an SDCard, then mount it and
```bash
# enable SSH (pi:raspberry)
touch /run/media/$USER/boot/ssh

# fallback to a static IP
sudo tee -a /run/media/$USER/rootfs/etc/dhcpcd.conf > /dev/null <<EOT
# define static profile
profile static_eth0
static ip_address=10.0.0.23/24
static routers=10.0.0.1
static domain_name_servers=10.0.0.1

# fallback to static profile on eth0
interface eth0
fallback static_eth0
EOT

sudo umount /run/media/$USER/boot
```

### PI Bootstrapping
* Direct LAN connection with static IP in same network, then `ssh-copy-id pi@10.0.0.23`.   
* `sudo raspi-config`:   
  1 - change password   
  2 - N1, N2 - change hostname, setup WiFi   
  5 - P4, P5 - enable SPI, enable I2C   
* `sudo apt install unattended-upgrades sshfs python3-pip`
* `sudo reboot`

### connect4cube installation
I2C access requires [root permissions](https://raspberrypi.stackexchange.com/questions/51375/) (sic).
```bash
sudo pip3 install pipenv
sudo pipenv install
sudo pipenv shell
```
