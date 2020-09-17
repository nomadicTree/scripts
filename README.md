# tnl
Quickly check to see if a tunnel is open, list available tunnels, or access a tunnel.

# Requirements
You need python3 for this script to run.

Additionally, you must add a couple of lines to your ~/.ssh/config file.
You should probably have these lines anyway.

```
Host tunnel
  ProxyCommand ssh -p 1022 bassenthwaite nc localhost %p
  User <YOUR LDAP USERNAME>
```

Next, you should ensure you can connect to bassenthwaite via SSH without a password.

Finally, you should probably add the script to your path.

You must be on the Opsview network for this script to work.

# Usage
For full usage information, run `tnl -h`.

There are three main modes: list (default), check (c), and access (a).

For help with each mode, run `tnl <mode> -h` e.g. `tnl a -h`.

## List
`tnl`
Lists open ssh tunnels.

## Check
`tnl c <port>`
Checks to see if a tunnel is open on the given port.
Returns details of the tunnel if it exists.

## Access
`tnl a <port> <user>`
Access the tunnel on port <port> as <user>.

By default, binds the remote port 80 to local port 5000 and remote port 443 to local port 5001.

These port bindings can be overridden using the option `-H` (remote 80) or `-S` (remote 443) options.
