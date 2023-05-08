""" created by Ricky Lai 2022.5.26 """

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """initialize"""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], \
            'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view(self):
        """recursively view categories"""
        def n(L, prefix = ()):
            if type(L) in {list, tuple}:
                i = 0
                for v in L:
                    if type(v) not in {list, tuple}:
                        i += 1
                    n(v, prefix+(i, ))
            else:
                s = " "*2*(len(prefix)-1)
                s += ". " + L
                print(s)
        n(self._categories)
 
    def is_category_valid(self, cat_name):
        """check if cat_name is in categories"""
        def n(L, name):
            if type(L) in {list, tuple}:
                for v in L:
                    p = n(v, cat_name)
                    if p == True:
                       return True
            return L == cat_name
        return n(self._categories, cat_name)

    def find_subcategories(self, cat_name):
        """use yield to implement find_subcategories"""
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found == True:
                    yield categories
        return [i for i in find_subcategories_gen(cat_name, self._categories)]  