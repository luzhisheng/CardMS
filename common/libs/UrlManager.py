class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        path = '/static' + path + "?ver=" + "2024101211"
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildAccountImageUrl(image_path):
        # account 管理员图片地址
        return f'/static/upload/account/{image_path}'

    @staticmethod
    def buildCardImageUrl(image_path):
        # card 图片地址
        return f'/static/upload/card/{image_path}'

    @staticmethod
    def buildMemberImageUrl(image_path):
        # member 图片地址
        return f'/static/upload/member/{image_path}'

