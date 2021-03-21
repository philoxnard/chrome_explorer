from urllib.parse import urlparse
import validators

#########################################################################
### Library for taking the url from the player and returning a domain ###
#########################################################################

# General handler for receiving a new url from the player
### Needs something to validate that self.url is actually a url
def handle_new_url(self):
    valid = validators.url(self.player.url)
    if valid:
        full_domain = get_domain(self.player.url)
        domain = snip_domain(full_domain)
        region = get_region(domain, self.region_dict)
        self.region = region
        self.determine_encounter()

# Takes the url and returns the full domain
def get_domain(url):
    domain = urlparse(url).netloc
    return domain

# Takes the full domain and returns a snipped domain
def snip_domain(domain):
    domain = domain.split('.')
    snipped_domain = domain[1]
    return snipped_domain

# Takes the snipped domain and returns a region
def get_region(domain, region_dict):
    for region, region_list in region_dict.items():
        if domain in region_list:
            return region