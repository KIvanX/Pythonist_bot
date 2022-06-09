
class Homework:
    global global_per # global

    def first_metod(self, change_2: float = 3, change_3: float = 5) -> float:
        encl_per: float = 12         # enclosing

        def first_metod_in_menod() -> float:
            local_per: float = 20             # local
            return global_per + encl_per + local_per

        first_metod_in_menod()
        return change_2 + change_3


global_per: int = 1 # global
sc = Homework()
sc.first_metod()