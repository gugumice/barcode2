# barcode2 setup

#Disable WIFI&Bluetooth in /boot/config.txt
dtoverlay=pi3-disable-wifi
dtoverlay=pi3-disable-bt

#Install CUPS
sudo apt-get install cups cups-bsd libcups2-dev
#Enable CUPS access
sudo cupsctl --remote-admin --remote-any
#Add user (pi) to lpadmin group
sudo usermod -a -G lpadmin pi
sudo service cups restart

#Create watchdog group & add user (pi) to it
sudo addgroup watchdog
sudo usermod -a -G watchdog pi

#Enable acces to /dev/watchdog for default user (pi)
sudo nano /etc/udev/rules.d/60-watchdog.rules
>KERNEL=="watchdog", MODE="0660", GROUP="watchdog"

#Install python3-pip and libs
sudo apt-get install python3-pip
sudo pip3 install pycups
sudo pip3 install pyserial
sudo pip3 install zebra

#Using barcode.service
https://www.raspberrypi.org/documentation/linux/usage/systemd.md
