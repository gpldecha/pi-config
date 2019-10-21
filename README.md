# pi-config
Different configuration steps for raspberry pi

### Zero W

## USB

#### ssh
1. Use the HDMI montior and keyboard to login the pi.
2. Run sudo raspi-config and enable the interfaces (SSH, etc..), update and reboot.
3. Add the line 'dtoverlay=dwc2' in the file /boot/config.txt
4. Add 'modules-load=dwc2,g_ether' after 'rootwait' in the file /boot/cmdline.txt
5. Edit /etc/dhcpcd.conf and add:
```bash
interface usb0
static ip_address=192.168.2.2/24
static routers=192.168.2.1
static domain_name_servers=8.8.8.8
```
6. On your PC edit the connection of the usb with a static ip:
```bash
Address       Netmask          Gateway
192.168.2.1   255.255.255.0    192.168.2.1   
```
The last step made it possible to ssh via the usb, steps adapted from [here](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget).

7. Network-manager -> connection -> Ethernet select for the Device: the usb device name, for 
instance (enp0s20u1). When you reconnect the usb, it will reuse this networking setting and not 
create a new one as it ususally does by default.

#### internet forwarding
On your pc run the following:
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 192.168.2.0/24

```
## Wirless video streaming

* download onto the pie [streameye](https://github.com/ccrisan/streameye) 

```bash
  python3 raspimjpeg.py -w 640 -h 480 -q 5 -awb=off -r 60 | streameye 
```

To remove the auto white balancing the code has to be edited:
**for the standard pi camera**
```bash
  camera.awb_gains = (1.4, 2.1)
```
**for the fish eye camera**
```bash
  camera.awb_gains = (1.4, 2.1)
```

## Run program on startup

copy the file picam.service to /lib/systemd/system

```bash
sudo chmod 644 /lib/systemd/system/picam.service
sudo systemctl daemon-reload
sudo systemctl enable picam.service
sudo reboot
```


## Notes

* The static ip for the usb ethernet device seems to restrict some of the packages which can be downloaded.

