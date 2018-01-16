import requests

class Dnspod:
    _URL = "https://dnsapi.cn/"

    def __init__(self, dns_id, dns_key):
        self._token = f"{dns_id},{dns_key}"

    def api(self, action, data={}):
        url = f"{self._URL}{action}"
        data['login_token'] = self._token
        data['format'] = 'json'
        return requests.post(url, data).json()

    def update(self, domain, name, value, dns_type="TXT"):
        dnspod = self.api
        li = dnspod("Record.List", dict(domain=domain))
        li = li['records']

        for i in li:
            if i['type'] == 'TXT':
                if i['name'] == name:
                    value = str(value)
                    if value != i['value']:
                        print(f'设置DNSPOD记录 {dns_type} {i["name"]}.{domain} = {value}')
                        dnspod("Record.Modify", dict(
                            domain=domain,
                            record_id=i['id'],
                            sub_domain=i['name'],
                            record_type=i['type'],
                            record_line="默认",
                            value=value,
                        ))
                        break

if __name__ == "__main__":
    from config import CONFIG
    domain = CONFIG.HOST.TXT

    dnspod = Dnspod(*CONFIG.DNSPOD)

    dnspod.update(domain, "cli-v", 32)

