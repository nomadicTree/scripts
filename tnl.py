#!/usr/bin/python3
import argparse
import subprocess
import sys
import re

default_http_local_port  = 5000
default_https_local_port = 5001
bassenthwaite_port       = 1022
ldap_user                = "jcussen"


def tunnel_maker(port, user, local_http_port, local_https_port):
    HOST = "tunnel"
    PORT = "-p %s" % port
    LDAP_USER = "-l %s" % ldap_user
    HTTP_PORT = "-L%s:localhost:80" % local_http_port
    HTTPS_PORT = "-L%s:localhost:443" % local_https_port

    subprocess.run(["ssh", LDAP_USER, HOST, PORT, HTTP_PORT, HTTPS_PORT])

def open_tunnel(args):
    if args.check:
        if not port_checker(args.port):
            sys.exit()
    tunnel_maker(args.port, args.remoteuser, args.httplocal, args.httpslocal)

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
        errors = ssh.stderr.readlines()
        for error in errors:
            print("ERROR: %s" % error.decode("ascii").rstrip(), file=sys.stderr)
        sys.exit()
    else:
        return tunnels

def list_tunnels(args):
    tunnels = find_tunnels()
    for tunnel in tunnels[1:]: #skip first line as it is never a tunnel
        print(tunnel.decode("ascii").rstrip())

def is_tunnel_open(port):
    port = " %s " % str(port)
    found = ""
    tunnels = find_tunnels()

    for tunnel in tunnels[1:]: #skip first line as it is never a tunnel
            found = cur
            break
    return found

def check_port(args):
    return port_checker(args.port)

def port_checker(port):
    result = False
    tunnel = is_tunnel_open(args.port)
    if tunnel:
        print(tunnel)
        result = True
    else:
        print("No tunnel open on port %d.\nTo see available tunnels, use \'tnl l\'." % args.port)
    return result

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", help="command help")

# Open a tunnel
parser_tunnel = subparsers.add_parser("open", aliases=["o"], help="open a tunnel")
parser_tunnel.add_argument("port", type=int, help="port of tunnel")
parser_tunnel.add_argument("remoteuser", type=str, help="user on remote host")
parser_tunnel.add_argument("-H", "--httplocal", type=int, default=default_http_local_port,
                           help="local port to bind remote port 80 to (default %s)" % default_http_local_port)
parser_tunnel.add_argument("-S", "--httpslocal", type=int, default=default_https_local_port,
                           help="local port to bind remote port 443 to (default %s)" % default_https_local_port)
parser_tunnel.add_argument("-c", "--check", default=False, action="store_true",
                           help="check if tunnel is open before attempting connection")
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
