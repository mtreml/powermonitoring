# Power Monitoring
Bokeh dashboard to monitor power consumption with live data from Kyoritsu KEW 6305


## Start wireshark USB stream monitoring

```bash
sudo modprobe usbmon
sudo setfacl -m u:$USER:r /dev/usbmon*
```
