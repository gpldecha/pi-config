# pi-config
Different configuration steps for raspberry pi

### Zero W

#### ssh via usb
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
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o XXX -j MASQUERADE
```
replace XXX with the name of your usb interface (run ifconfig, usually something like enp0s20u1)
