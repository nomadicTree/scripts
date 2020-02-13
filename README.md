# scripts
Quickly check to see if a tunnel is open, list available tunnels, or open a tunnel.

# Requirements
All you need to do is add a couple of lines to your ~/.ssh/config file.
You should probably have these lines anyway.

```
Host tunnel
  ProxyCommand ssh -p 1022 jcussen@bassenthwaite nc localhost %p
  User <YOUR LDAP USERNAME>
```

Then, you should probably add the script to your path.

You must be on the Opsview network for this script to work.

# Usage
For full usage information, run `tnl h`.

There are three main modes: check (c), list (l), and open (o).

For help with each mode, run `tnl <mode> h` e.g. `tnl o h`.


## Check
`tnl c <port>`
Checks to see if a tunnel is open on the given port.
It returns details of the tunnel if it exists.

## List
`tnl l`
List all open tunnels.

## Open
`tnl o <port> <user>`
Access the tunnel on port <port> as <user>.

By default, binds the remote port 80 to local port 5000 and remote port 443 to local port 5001.

These port bindings can be overridden using the option `-H` (remote 80) or `-S` (remote 443) options.
