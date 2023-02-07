from scrapy.dupefilters import RFPDupeFilter

SEEN_URL_FILE = 'seen_urls.txt'

class SeenUrlFilter(RFPDupeFilter):
    def __init__(self, *args, **kwargs):
        self.urls_seen = set()
        try:
            with open(SEEN_URL_FILE, 'r') as f:
                self.urls_seen = {s.strip() for s in f.readlines()}
        except:
            pass

        RFPDupeFilter.__init__(self, *args, **kwargs)

    def request_seen(self, request):
        if request.url in self.urls_seen:
            return True

        self.urls_seen.add(request.url)
        return False

    def close(self, *args, **kwargs) -> None:
        with open(SEEN_URL_FILE, 'w') as f:
            f.write('\n'.join(sorted(self.urls_seen)))

        super().close(*args, **kwargs)
