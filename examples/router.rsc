# Representative RouterOS export and scripting constructs; documentation IPs only.
/interface bridge
add name=bridge-lan protocol-mode=rstp
/ip address
add address=192.0.2.1/24 interface=bridge-lan
/ipv6 address
add address=2001:db8::1/64 interface=bridge-lan advertise=yes
/interface ethernet
set [ find default-name=ether1 ] mac-address=02:00:00:00:00:01

:local gateway 192.0.2.254
:global retryCount 3
:local "interface-name" "bridge-lan"
:if ($retryCount > 0) do={
    :put "Gateway: $gateway"
    :put $"interface-name"
    :foreach item in=[/ip address find] do={
        :put [/ip address get $item address]
    }
} else={
    :log warning "No retries\n"
}
:delay 1h30m
:put "Result: $($retryCount + 1)"
/ip route add dst-address=0.0.0.0/0 \
    gateway=192.0.2.254 disabled=no
