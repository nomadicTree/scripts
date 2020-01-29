#!/usr/bin/python3
import argparse
import subprocess
import sys

default_http_local_port  = 5000
default_https_local_port = 5001
bassenthwaite_port       = 1022
ldap_user                = "jcussen"

def open_tunnel(args):
    print("open sesame")

def find_tunnels():
    HOST = "bassenthwaite"
    PORT = "-p %s" % bassenthwaite_port
    COMMAND = "/usr/bin/whot"
    LDAP_USER = "-l %s" % ldap_user

    ssh = subprocess.Popen(["ssh", LDAP_USER, HOST, PORT, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    tunnels = ssh.stdout.readlines()
    if tunnels == []:
        error = ssh.stderr.readlines()
        print("ERROR: %s" % error, file=sys.stderr)
        sys.exit()
    else:
        return tunnels

def list_tunnels(args):
    tunnels = find_tunnels()
    for tunnel in tunnels[1:]: #skip first line as it is never a tunnel
        print(tunnel.decode("ascii").rstrip())

def check_port(args):
    found = False
    tunnels = find_tunnels()

    for tunnel in tunnels[1:]: #skip first line as it is never a tunnel
        cur = tunnel.decode("ascii").rstrip()
        if str(args.port) in cur:
            found = True
            print(cur)
    if not found:
        print("No tunnel open on port %s." % args.port)
        print("To see a list of open tunnels, use \'tnl l\'.")


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="subcommand help")

# Open a tunnel
parser_tunnel = subparsers.add_parser("open", aliases=["o"], help="open a tunnel")
parser_tunnel.add_argument("port", type=int, help="port of tunnel")
parser_tunnel.add_argument("remote-user", type=str, help="user on remote host")
parser_tunnel.add_argument("-H", "--http-local", type=int, default=default_http_local_port,
    help="local port to bind remote port 80 to (default %s)" % default_http_local_port)
parser_tunnel.add_argument("-S", "--https-local", type=int, default=default_https_local_port,
    help="local port to bind remote port 443 to (default %s)" % default_https_local_port)
parser_tunnel.set_defaults(func=open_tunnel)

# List open tunnels
parser_list = subparsers.add_parser("list", aliases=["l"], help="list open tunnels")
parser_list.set_defaults(func=list_tunnels)

# Check a port for open tunnels
parser_check_port = subparsers.add_parser("check", aliases=["c"], help="check to see if a port has a tunnel open on it")
parser_check_port.add_argument("port", type=int, help="port to check")
parser_check_port.set_defaults(func=check_port)

args = parser.parse_args()
args.func(args)
