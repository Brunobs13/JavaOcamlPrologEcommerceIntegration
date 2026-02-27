% Item em inventário 
item(1, 'Potion of Healing', 'potions', 10.0, 50).
item(2, 'Wand of Fireball', 'wands', 20.0, 30).
item(3, 'Enchanted Spellbook', 'enchanted_books', 30.0, 20).
item(4, 'Crystal of Clairvoyance', 'crystals', 15.0, 40).
item(5, 'Amulet of Protection', 'amulets', 25.0, 25).


% Descontos por categoria de item
discount('potions', 0.1).
discount('wands', 0.2).
discount('enchanted_books', 0.3).
discount('crystals', 0.15).
discount('amulets', 0.25).

% Desconto de lealdade por ano
loyalty_discount(1, 0.05).
loyalty_discount(2, 0.1).
loyalty_discount(3, 0.15).
loyalty_discount(4, 0.2).
loyalty_discount(5, 0.25).
loyalty_discount(>5, 0.3).

% Custos de envio por distrito
shipping_cost('Aveiro', 5.0).
shipping_cost('Lisboa', 7.0).
shipping_cost('Porto', 10.0).
