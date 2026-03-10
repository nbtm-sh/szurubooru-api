import szurubooru_api.request
import szurubooru_api.url
import szurubooru_api.paged
import os, json

class Szurubooru:
    def __init__(self, api_endpoint, username=None, api_token=None):
        self.api_endpoint = api_endpoint # Should be http(s)://booru.host.tld/api... 
        self.username = username
        self.api_token = api_token

        self.request = szurubooru_api.request.Request(username, api_token)

    def is_error(self, data):
        # TODO: Implement errors
        if "name" in data.keys():
            print(data)
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

    def update_tag_category(self, name, version, color=None, order=None):
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

    def merge_tag(self, remove_name, remove_version, merge_version, merge_name):
        """
        Merges two tags together. remove_name -> merge_name. Requires remove_name, remove_version, merge_version, merge_name. Returnes a tag
        """
        data = {
            "removeVersion": remove_version,
            "remove": remove_name,
            "mergeToVersion": merge_version,
            "mergeTo": merge_name
        }
        url = os.path.join(self.api_endpoint, "tag-merge")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    # Tag siblings
    def get_tag_siblings(self, name):
        """
        Get tag siblings. Requires name. Returns tag siblings
        """
        url = os.path.join(self.api_endpoint, "tag-siblings", name)
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    # Posts
    def list_posts(self, query="*", offset=0, limit=50):
        # TODO: Implement category, sort, etc.
        """
        List posts given a query. Returns a paged list of posts. query can be '*' to list all posts.
        """
        url = os.path.join(self.api_endpoint, "posts", szurubooru_api.url.get_opts(query=query, offset=offset, limit=limit))
        data = self.request.get(url).json()

        if not self.is_error(data):
            return szurubooru_api.paged.PagedResult(
                ctx = self,
                search_func = self.list_posts,
                offset = data["offset"],
                limit = data["limit"],
                total = data["total"],
                results = data["results"]
            )

    def create_post(self, tags, safety, source=None, relations=None, notes=None, flags=None, anonymous=None, file=None, url=None, content_token=None):
        """
        Creates a post. Requires tags, safety, file OR url. File should be file handler. Returns a post
        """
        data = {
            "tags": tags,
            "safety": safety
        }
        if source:
            data["source"] = source
        if relations:
            data["relations"] = relations
        if notes:
            data["notes"] = notes
        if flags:
            data["flags"] = flags
        if anonymous:
            data["anonymous"] = anonymous
        if content_token:
            data["contentToken"] = content_token

        if content_token:
            url = os.path.join(self.api_endpoint, "posts")
            # Not sure why but this spesifically needs to be in string first
            data = self.request.post(url, data=json.dumps(data)).json()

            if not self.is_error(data):
                return data
        # TODO: Implement URL upload

    def update_post(self, post_id, version, tags=None, safety=None, source=None, relations=None, notes=None, flags=None):
        # TODO: Implement file updates
        """ 
        Updates an existing post. Requires post_id, version. Returns a post object
        """
        data = {
            "version": version
        }
        if tags:
            data["tags"] = tags
        if safety:
            data["safety"] = safety
        if source:
            data["source"] = source
        if relations:
            data["relations"] = relations
        if notes:
            data["notes"] = notes
        if flags:
            data["flags"] = flags
        if anonymous:
            data["flags"] = anonymous

        url = os.path.join(self.api_endpoint, "post", str(post_id))
        data = self.request.put(url, data=data).json()
        if not self.is_error(data):
            return data

    def get_post(self, post_id):
        """
        Get a post. Requires id. Returns a post
        """
        url = os.path.join(self.api_endpoint, "post", str(post_id))
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    def get_around_post(self, post_id):
        """
        Get the post IDs around a post. Requires post_id. Returns prev, and next post.
        """
        url = os.path.join(self.api_endpoint, "post", str(post_id), "around")
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    def delete_post(self, post_id, version):
        """
        Delete a post. Requires post_id, version. Returns None
        """
        data = {
            "version": version
        }
        url = os.path.join(self.api_endpoint, "post", str(post_id))
        data = self.request.delete(url, data=data).json()

        self.is_error(data)

    def merge_post(self, remove_name, remove_version, merge_version, merge_name, replace_content=False):
        """
        Merges two posts together. remove_name -> merge_name. Requires remove_name, remove_version, merge_version, merge_name. Returnes a post
        """
        data = {
            "removeVersion": remove_version,
            "remove": remove_name,
            "mergeToVersion": merge_version,
            "mergeTo": merge_name,
            "replaceContent": replace_content
        }
        url = os.path.join(self.api_endpoint, "post-merge")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def rate_post(self, post_id, score):
        """
        Rates a post. Requires post_id, score. Score must be an integer value -1,0,1. Returns a post
        """
        data = {
            "score": score
        }
        url = os.path.join(self.api_endpoint, "post", str(post_id), "score")
        data = self.request.put(url, data=data).json()

        if not self.is_error(data):
            return data

    def favourite_post(self, post_id):
        """
        Adds a post to your favourites. Returns a post
        """

        url = os.path.join(self.api_endpoint, "post", str(post_id), "favourite")
        data = self.request.post(url).json()

        if not self.is_error(data):
            return data

    def remove_favourite_post(self, post_id):
        """
        Removes a post from your favourites. Requires post_id. Returns a post
        """

        url = os.path.join(self.api_endpoint, "post", str(post_id), "favourite")
        data = self.request.delete(url).json()

        if not self.is_error(data):
            return data
    
    def get_featured_post(self):
        """
        Get featured post. Returns a post
        """
        url = os.path.join(self.api_endpoint, "featured-post")
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    def feature_post(self, post_id):
        """
        Feature a post. Requires post_id. Returns a post
        """
        data = {
            "id": post_id
        }
        url = os.path.join(self.api_endpoint, "featured-post")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def reverse_image_search(self, file):
        """
        Performs a reverse image search. Requires file. File should be a file handler.
        """
        # TODO: Implement image search result
        files = {
            "content": file 
        }

        url = os.path.join(self.api_endpoint, "reverse-search")
        data = self.request.post(url, files=files).json()

        if not self.is_error(data):
            return data

    # Pools
    def list_pool_categories(self):
        """
        Lists pool categories. Returnes a list of pool categories
        """

        url = os.path.join(self.api_endpoint, "pool-categories")
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data
    
    def create_pool_category(self, name, color):
        """
        Create a pool. Requires name, color. Returns a pool
        """
        data = {
            "name": name,
            "color": color
        }

        url = os.path.join(self.api_endpoint, "pool-categories")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def update_pool_category(self, version, name=None, color=None):
        """
        Update a pool cateogory. Requires version. Returns a pool category
        """
        data = {
            "version": version
        }
        if name:
            data["name"] = name
        if color:
            data["color"] = color

        url = os.path.join(self.api_endpoint, "pool-categories")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data

    def get_pool_category(self, name):
        """
        Get a pool category. Requires name. Returns a pool cateogry
        """
        url = os.path.join(self.api_endpoint, "pool-category", name)
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    def delete_pool_category(self, name, version):
        """
        Delete a pool category. Requires name, version. Returns None
        """
        data = {
            "version": version
        }
        url = os.path.join(self.api_endpoint, "pool-category", name)
        data = self.request.delete(url, data=data).json()

        if not self.is_error(data):
            return data

    def set_default_pool_category(self, name):
        """
        Set a pool category as the default. Requires name. Returns a pool category
        """
        url = os.path.join(self.api_endpoint, "pool-category", name, "default")
        data = self.request.put(url, data=data).json()

        if not self.is_error(data):
            return data

    def list_pools(self, query="*", offset=0, limit=50):
        # TODO: Implement category, sort, etc.
        """
        List pools given a query. Returns a paged list of pools. query can be '*' to list all pools.
        """
        url = os.path.join(self.api_endpoint, "pools", szurubooru_api.url.get_opts(query=query, offset=offset, limit=limit))
        data = self.request.get(url).json()

        if not self.is_error(data):
            return szurubooru_api.paged.PagedResult(
                ctx = self,
                search_func = self.list_posts,
                offset = data["offset"],
                limit = data["limit"],
                total = data["total"],
                results = data["results"]
            )

    def create_pool(self, names, category, description=None, posts=None):
        """
        Creates a new pool. Requires names, category. Returns a pool
        """
        data = {
            "names": names,
            "category": category
        }
        if description:
            data["description"] = description
        if posts:
            data["posts"] = posts
        url = os.path.join(self.api_endpoint, "pool")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data
    
    def update_pool(self, pool_id, version, names=None, category=None, description=None, posts=None):
        """
        Update an existing post. Requires pool_id, version. Returns a pool
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
        if posts:
            data["posts"] = posts

        url = os.path.join(self.api_endpoint, "pool", str(pool_id))
        data = self.request.put(url, data=data).json()

        if not self.is_error(data):
            return data

    def get_pool(self, pool_id):
        """
        Get a pool. Requires pool_id. Returns a pool
        """

        url = os.path.join(self.api_endpoint, "pool", str(pool_id))
        data = self.request.get(url).json()

        if not self.is_error(data):
            return data

    def delete_pool(self, pool_id):
        """
        Delete a pool. Requires pool_id. Returns None
        """

        url = os.path.join(self.api_endpoint, "pool", str(pool_id))
        data = self.request.delete(url).json()

        self.is_error(data)

    def merge_pool(self, remove_name, remove_version, merge_version, merge_name):
        """
        Merges two pools together. remove_name -> merge_name. Requires remove_name, remove_version, merge_version, merge_name. Returnes a pool
        """
        data = {
            "removeVersion": remove_version,
            "remove": remove_name,
            "mergeToVersion": merge_version,
            "mergeTo": merge_name
        }
        url = os.path.join(self.api_endpoint, "pool-merge")
        data = self.request.post(url, data=data).json()

        if not self.is_error(data):
            return data
    
    def get_upload_token(self, file):
        """
        Get the upload token for a given file. Requires file. File should be a file handler. Returns a token
        """
        file_name = os.path.basename(file.name)
        file_ext = file_name.split(".")[-1].lower()
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'mp4': 'video/mp4',
            'webm': 'video/webm' 
        }
        mime_type = mime_types[file_ext] if file_ext in mime_types.keys() else "application/octet-stream"

        files = {
            "content": (file_name, file.read(), mime_type)
        }
        url = os.path.join(self.api_endpoint, "uploads")
        data = self.request.post(url, files=files).json()

        if not self.is_error(data):
            return data["token"]
