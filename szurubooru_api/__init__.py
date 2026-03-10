import szurubooru_api.request
import szurubooru_api.url
import szurubooru_api.paged
import os

class Szurubooru:
    def __init__(self, api_endpoint, username=None, api_token=None):
        self.api_endpoint = api_endpoint # Should be http(s)://booru.host.tld/api... 
        self.username = username
        self.api_token = api_token

        self.request = szurubooru_api.request.Request(username, api_token)

    def is_error(self, data):
        # TODO: Implement errors
        if "name" in data.keys():
            return True
        return False

    # Tag categories
    def list_tag_categories(self):
        """
        Returns a list of tag categories as dicts 
        {
            "version": "...",
            "name": "...",
            "color": "...",
            "usages": "...",
            "order": "...",
            "default": "...",
        }
        """
        url = os.path.join(self.api_endpoint, "tag-categories")
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data["result"]

    def create_tag_category(self, name, color, order):
        """
        Creates a tag category. Requires name, color, order. Returns a tag category
        """
        data = { # Pains me to use en-US spelling of colour but sacrifices must be made
            "name": name,
            "color": color,
            "order": order
        }
        url = os.path.join(self.api_endpoint, "tag-categories")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def update_tag_category(self, name, version color=None, order=None):
        """
        Updates a tag category. Requires name, version. Returns a tag category
        """
        data = {
            "version": version,
            "name": name
        }
        if color:
            data["color"] = color
        if order:
            data["order"] = order

        url = os.path.join(self.api_endpoint, "tag-category", name)
        data = self.request.put(url, data=data).json()

        if not self.is_error(data):
            return data

    def get_tag_category(self, name):
        """
        Get a tag category. Requires name. Returns a tag cateogry.
        """
        url = os.path.join(self.api_endpoint, "tag-category", name)
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data
    
    def delete_tag_category(self, name, version):
        """
        Delete a tag category. Requires name, version. Returns None"
        """
        url = os.path.join(self.api_endpoint, "tag-category", name)
        data = self.request.delete(url).json()

        self.is_error(data)

    def set_default_tag_category(self, name):
        """
        Sets the board's default tag category. Requires name. Returns a tag category
        """
        url = os.path.join(self.api_endpoint, "tag-category", name, "default")
        data = self.request.put(url).json()

        if not self.is_error(data):
            return data

    # Tags
    def list_tags(self, query="*", offset=0, limit=50):
        # TODO: Implement category, sort, etc.
        """
        List tags given a query. Returns a paged list of tags. query can be '*' to list all tags.
        """
        url = os.path.join(self.api_endpoint, "tags", szurubooru_api.url.get_opts(query=query, offset=offset, limit=limit))
        data = self.request.get(url).json()

        if not self.is_error(data):
            return szurubooru_api.paged.PagedResult(
                ctx = self,
                search_func = self.list_tags,
                offset = data["offset"],
                limit = data["limit"],
                total = data["total"],
                results = data["results"]
            )
    
    def create_tag(self, names, category, description=None, implications=None, suggestions=None):
        """
        Creates a new tag. Requires names, category. Names should be list. Returns a tag
        """
        data = {
            "names": names,
            "category": category
        }
        if description:
            data["description"] = description
        if implications:
            data["implications"] = implications
        if suggestions:
            data["suggestions"] = suggestions

        url = os.path.join(self.api_endpoint, "tags")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def update_tag(self, name, version, names=None, category=None, description=None, implications=None, suggestions=None):
        """
        Updates an existing tag. Requires name, version. Returns a tag
        """
        data = {
            "version": version
        }
        if names:
            data["names"] = names
        if category:
            data["category"] = category
        if description:
            data["description"] = description
        if implications:
            data["implications"] = implications
        if suggestions:
            data["suggestions"] = suggestions

        url = os.path.join(self.api_endpoint, "tag", name)
        data = self.request.put(url, data=data).json()
        
        if not self.is_error(data):
            return data

    def get_tag(self, name):
        """
        Get a tag. Requires name. Returns a tag
        """
        url = os.path.join(self.api_endpoint, "tag", name)
        data = self.request.get(url).json()
        
        if not self.is_error(data):
            return data

    def delete_tag(self, name, version):
        """
        Delete a tag. Requires name, version. Returns None
        """
        data = {
            "version": version 
        }
        url = os.path.join(self.api_endpoint, "tag", name)
        data = self.request.delete(url, data=data).json()

        self.is_error(data)
