import requests
import hashlib
import sys

def request_api_data(query_hash):
    url = "https://api.pwnedpasswords.com/range/" + query_hash
    res = requests.get(url)
    #print(res)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and run again!')
    return res

def password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    #print(hashes)
    for h, c in hashes:
        #print(h,c)
        if h == hash_to_check:
            return c
    return 0

def pwned_api_check(password):
    sha1password = (hashlib.sha1(password.encode('utf-8')).hexdigest()).upper()
    #print(sha1password)
    head, tail = sha1password[:5], sha1password[5:]
    res = request_api_data(head)
    count = password_leak_count(res, tail)
    return count

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} found {count} times. Change the password!')
        else:
            print(f'{password} not hacked. All good!')

if __name__ == '__main__':
    main(sys.argv[1:])
 