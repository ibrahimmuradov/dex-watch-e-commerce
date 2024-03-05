class Uploader:
    @staticmethod
    def upload_profile_photo(objName, fileName):
        return f"user/{objName.username}/{fileName}"

    @staticmethod
    def upload_watch_photo(objName, fileName):
        return f"watch/{objName.watch.name}/{fileName}"

    @staticmethod
    def upload_watch_header_photo(objName, fileName):
        return f"watch/{objName.name}/{fileName}"

    @staticmethod
    def upload_watch_basket_photo(objName, fileName):
        return f"watch_basket/{objName.watch.name}/{fileName}"
