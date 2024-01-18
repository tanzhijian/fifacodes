import csv

from httpx import Client, Response
from parsel import Selector

from fifacodes import _DEFAULT_DATA_PATH as EXPORT_PATH
from fifacodes import Member

URL = "https://en.m.wikipedia.org/wiki/List_of_FIFA_country_codes"


MembersTypes = list[Member]


def fetch(client: Client) -> Response:
    response = client.get(URL)
    response.raise_for_status()
    return response


def parse(response: Response) -> MembersTypes:
    selector = Selector(response.text)
    members: MembersTypes = []
    tables = selector.xpath('//*[@id="mf-section-1"]/table')
    for table in tables:
        trs = table.xpath(".//tr")
        for tr in trs[1:]:
            code = tr.xpath("./td[2]/text()").get()
            name = tr.xpath("./td[1]//a/text()").get()
            if code and name:
                members.append(Member(code=code.strip(), name=name.strip()))
    return members


def export(members: MembersTypes) -> None:
    with open(EXPORT_PATH, "w") as f:
        writer = csv.writer(f)
        writer.writerow(Member._fields)
        writer.writerows(members)


def main() -> None:
    client = Client()
    response = fetch(client)
    members = parse(response)
    export(members)


if __name__ == "__main__":
    main()
