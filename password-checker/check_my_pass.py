import requests
import hashlib
import sys


def request_pwned_api_data(range_param) -> requests.Response:
    """Request pwned password range"""
    url = f"https://api.pwnedpasswords.com/range/{range_param}"
    res = requests.get(url, timeout=5)

    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}, check the pwned API and try again"
        )

    return res


def get_password_leeks_count(hashes: requests.Response, hash_to_check: str):
    """Check password if it exists in API response"""
    hashes = (line.split(":") for line in hashes.text.splitlines())

    print(hash_to_check)

    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password: str):
    """Check password if it exists in API response"""
    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    sha1_password_prefix, sha1_password_tail = sha1_password[:5], sha1_password[5:]

    response = request_pwned_api_data(sha1_password_prefix)

    return get_password_leeks_count(response, sha1_password_tail)


def main(args):
    """Main function"""
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f"{password} was found {count} times... you should probably change your password!"
            )
        else:
            print(f"{password} was NOT found. Carry on!")

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit()
