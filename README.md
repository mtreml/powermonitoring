# Power Monitoring
Webserver to monitor power consumption with live data from Kyoritsu KEW 6305

## Bokeh dashboard
Bokeh dashboard to visualize live power data from Kyoritsu KEW 6305

## USB driver

### Start wireshark USB stream monitoring

```bash
sudo modprobe usbmon
sudo setfacl -m u:$USER:r /dev/usbmon*
```
