class RelationField:
    def __init__(self, relation_model):
        self.relation_model = relation_model
        self.__value = None

    # def get_mode

    def __get__(self, obj, objtype=None):
        print("Get value", obj)

        return self.__value

    def __set__(self, obj, value):
        print("set value")

        self.__value = value
