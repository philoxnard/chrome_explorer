from urllib.parse import urlparse
import validators

#########################################################################
### Library for taking the url from the player and returning a domain ###
#########################################################################

# General handler for receiving a new url from the player
def new_url_handler(self):
    for phox in self.player.party:
        phox.RAM = phox.max_RAM
    if self.state == "explore":
        valid = validators.url(self.player.url)
        if valid:
            full_domain = get_domain(self.player.url)
            sanitized_domain = sanitize_domain(full_domain)
            domain = snip_domain(sanitized_domain)
            region = get_region(domain, self.region_dict)
            self.region = region
            if self.region == "phoxtrot":
                self.handle_phoxtrot_site()
            else:
                self.determine_encounter()

# Takes the url and returns the full domain
def get_domain(url):
    domain = urlparse(url).netloc
    return domain

# Checks to see if the domain leads with www. and adds it if not
def sanitize_domain(full_domain):
    if not full_domain[3] == ".":
        full_domain = "www." + full_domain
    return full_domain

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