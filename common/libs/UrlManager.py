class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        path = '/static' + path + "?ver=" + "2024101211"
        return UrlManager.buildUrl(path)
