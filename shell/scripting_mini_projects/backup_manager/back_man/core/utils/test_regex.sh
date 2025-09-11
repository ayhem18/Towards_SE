#!/bin/bash

# Test the actual regex behavior
test_hostname_regex() {
    local hostname="$1"
    local hostname_regex="^(([a-zA-Z0-9]([a-zA-Z0-9-]+\.)+([a-zA-Z0-9-]+))|([a-zA-Z0-9-]*[a-zA-Z-]+[a-zA-Z0-9-]*))$"
    
    if [[ "$hostname" =~ $hostname_regex ]]; then
        echo "✅ VALID: $hostname"
        return 0
    else
        echo "❌ INVALID: $hostname"
        return 1
    fi
}

echo "Testing IP addresses:"
test_hostname_regex "192.168.1.1"
test_hostname_regex "10.0.0.1"
test_hostname_regex "127.0.0.1"

echo -e "\nTesting IPv6:"
test_hostname_regex "::1"
test_hostname_regex "2001:db8::1"

echo -e "\nTesting all numbers:"
test_hostname_regex "123"
test_hostname_regex "456"

echo -e "\nTesting double dots:"
test_hostname_regex "server..com"
test_hostname_regex "web..example.com"

echo -e "\nTesting underscores:"
test_hostname_regex "server_name"
test_hostname_regex "web_server"

echo -e "\nTesting hyphens at start/end:"
test_hostname_regex "-server"
test_hostname_regex "server-"
test_hostname_regex "-web-server-"
