import dns_formatted_name

CERT_PREFIX = "cert_"
CERT_SUFFIX = ".crt"

PUBLIC_KEY_PREFIX = "public_"
PRIVATE_KEY_PREFIX = "private_"

KEY_SUFFIX = ".pem"


def get_certificate_name(name):
    total_name = CERT_PREFIX + dns_formatted_name.get_dns_formatted_subdomain(name) + CERT_SUFFIX
    return total_name


def get_public_key_name(name):
    total_name = PUBLIC_KEY_PREFIX + dns_formatted_name.get_dns_formatted_subdomain(name) + KEY_SUFFIX
    return total_name

def get_private_key_name(name):
    total_name = PRIVATE_KEY_PREFIX + dns_formatted_name.get_dns_formatted_subdomain(name) + KEY_SUFFIX
    return total_name


if __name__ == "__main__":
    print(get_certificate_name("ram teja"), get_public_key_name("ram teja"), get_private_key_name("ram teja"))
