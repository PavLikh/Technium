class MyDict:
    def __init__(self):
        self.my_items = []
        self.my_keys = []

    def __setitem__(self, key, value):
        index = self.get_index(key)
        if index is not None:
            self.my_items[index] = value
        else:
            self.my_keys.append(key)
            self.my_items.append(value)

    def __getitem__(self, key):
        index = self.get_index(key)
        if index is None:
            return None
        return self.my_items[index]

    def __delitem__(self, key):
        index = self.get_index(key)
        if index is not None:
            self.my_keys.pop(index)
            self.my_items.pop(index)

    def __contains__(self, key) -> bool:
        return key in self.my_keys
    
    def get_index(self, key) -> int | None:
        if key not in self.my_keys:
            return None
        return self.my_keys.index(key)
    
    def keys(self):
        return self.my_keys

    def values(self):
        return self.my_items

    def items(self):
        res = []
        length = len(self.my_keys)
        if length > 0:
            for i in range(length):
                res.append([self.my_keys[i], self.my_items[i]])
        return res

    def __str__(self) -> str:
        s = ''
        length = len(self.my_keys)
        if length > 0:
            for i in range(length):
                if not i:
                    s = f'{self.my_keys[i]}: {self.my_items[i]}'
                else:
                    s = s + f', {self.my_keys[i]}: {self.my_items[i]}'
        return s
        



my_dict = MyDict()
my_dict['name'] = 'Alice'
my_dict['age'] = 30
print(my_dict['name'])  # Вернет 'Alice'
print('city' in my_dict)  # Вернет False
del my_dict['age']
my_dict['city'] = 'Tomsk'
print(my_dict.keys())  # Вернет ['name']
print(my_dict.values())  # Вернет ['Alice']
print(my_dict.items())
print(my_dict['name'])
print(my_dict)