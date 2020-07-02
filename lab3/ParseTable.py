class ParseTable:
    def __init__(self):
        self.table = dict()

    def put(self, key, value):
        try:
            success = self.table[key] == value
        except Exception as e:
            success = True
            pass
        self.table[key] = value
        if not success:
            print("Given Grammar is not LL(1)")

    def get(self, key):
        for current_key, current_value in self.table.items():
            if current_value is not None:
                if current_key[0] == key[0] and current_key[1] == key[1]:
                    return current_value
        return None

    def contains_key(self, key):
        result = False
        for current_key in self.table.keys():
            if current_key[0] == key[0] and current_key[1] == key[1]:
                result = True
        return result

    def __str__(self):
        s = ""
        for key, value in self.table.items():
            if value is not None:
                s = s + "M[" + str(key[0]) + ", " + str(key[1]) + "] = [" + str(value[0]) + ", " + str(
                    value[1]) + "]\n"
        return s
