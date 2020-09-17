from flask_restful import abort
import os


class RestrictionHelper():
    """
    Helper class for restriction
    """
    def is_allowed(self, path):
        """
        Function that return True / False depends on restriction
        """
        allowed_paths = self.get_allowed_paths()
        for allowed_path in allowed_paths:
            if allowed_path in path:
                return True

        return False

    def get_allowed_paths(self):
        """
        Return allowed paths for check if user allowed
        """
        paths = []
        try:
            with open("allowedPaths.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    paths.append(line.strip())
        except IOError:
            pass

        if not paths:
            abort(
                400,
                message=
                "Allowed paths were not set, you are not allowed to any path.")
        else:
            return paths

    def change_all_slashes(self, string):
        """
        Helping function for use right separator by OS
        """
        result = string.replace("/", os.path.sep)
        result = result.replace("\\", os.path.sep)
        return result