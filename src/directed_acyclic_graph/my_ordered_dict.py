from collections import OrderedDict
import numpy as np


class MyOrderedDict(OrderedDict):
    """
    Extended OrderedDict with the ability to safely delete entries, get the
    last added key and get the key with highest value containing any desired
    word or filtering it.
    """


    def delete_entry(self, entry):
        try:
            del self[entry]
        except KeyError:
            print("Key '{0}' not found.".format(entry))


    def get_key_with_highest_value(self, having_any=[], without=[], how="random"):
        if not having_any:
            try:
                sorted_items = sorted(self.items(), key=lambda kv: -kv[1])
                highest_item = sorted_items[0][0]

                return highest_item
            except TypeError:
                print("Not all values are numeric.")


        keys = []
        keys = [k for k in self.keys() if \
                ((k[0] in having_any) or (k[1] in having_any)) \
                and (k[0] not in without) \
                and (k[1] not in without)]

        if keys:
            filtered_dict = {k: self[k] for k in keys}
            highest_value = max(list(filtered_dict.values()))
            highest_items = [k for k in keys if self[k] == highest_value]
            if how == "first":
                highest_item = highest_items[0]
            elif how == "random":
                random_index = np.random.choice(range(len(highest_items)))
                highest_item = highest_items[random_index]
                

            return highest_item
        else:
            print("Could'n find any key with required values.")


    def get_highest_value(self):
        return max(list(self.values()))
        
        
    def get_lowest_value(self):
        return min(list(self.values()))
        
    
    def get_last_added_key(self):
        return list(self.keys())[-1]



