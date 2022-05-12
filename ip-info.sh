#!/bin/bash

network_devices=$(ip addr | grep -E -c "[0-9]+: ")
for ((device = 1; device <= $network_devices; device++))
do
  network_info=$(ip addr | grep -A5 "$device:")
  device_name_=$(echo "$network_info" \
                | grep -P -o "[\w]+" \
                | head -2 \
                | tail -1)

  ip_addresses=$(echo "$network_info" \
                | grep "inet")

  dev_mac_addr=$(echo "$network_info" \
                | grep "link" \
                | head -1 \
                | grep -P -o "([\w]+[:]){5}[\w]{2}" \
                | head -1)

  ipv4_addr=$(echo "$ip_addresses" \
            | grep -E -o "([0-9]+\.){3}[0-9]+" | head -1)

  ipv6_addr=$(echo "$ip_addresses" \
            | grep -P -o "([\w]+)?::(([\w]+:){3})?[\w]{1,4}")

  echo "Device: $device_name_"
  echo "IPv4: $ipv4_addr"
  echo "IPv6: $ipv6_addr"
  echo "MAC: $dev_mac_addr"; echo
done

echo "Outside ip address: $(wget -qO- ident.me)"
