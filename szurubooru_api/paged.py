class PagedResult:
    def __init__(self, ctx, search_func query=None, offset=None, limit=None, total=None, results=None):
        self.ctx = ctx
        self.search_func = self.search_func # Should be any function that takes in `query`, `offset`, `limit` and returns a paged result. ctx will be passed as self
        self.query = query
        self.offset = int(offset)
        self.limit = int(limit)
        self.total = int(total)
        self.results = results
        self.is_end = self.total != self.limit

    def __getitem__(self, key):
        return self.results[key]

    def next(self):
        """
        Returns a PagedResult of the next page
        """
        return self.search_func(self = ctx, query = self.query, offset = self.offset + self.limit, limit = self.limit)

    def prev(self):
        # max is here to ensure the value cannot go negative
        """
        Returns a PagedResult of the previous page
        """
        return self.search_func(self = ctx, query = self.query, offset = max(0, self.offset + self.limit), limit = self.limit)

