import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.stream.Collectors;




public class Cart {
    private List<Item> items;
    
    public Cart() {
        this.items = new ArrayList<>();
        
        //  fictícios ao carrinho
        //this.items.add(new Item(1, "Potion of Healing", "potions", 10.0, 2));
        //this.items.add(new Item(2, "Wand of Fireball", "wands", 20.0, 1));
        //this.items.add(new Item(3, "Enchanted Spellbook", "enchanted_books", 30.0, 1));
        //this.items.add(new Item(4, "Crystal of Clairvoyance", "crystals", 15.0, 1));
        //this.items.add(new Item(5, "Amulet of Protection", "amulets", 25.0, 1));
    }
    
    public void addItem(Item item) {
        this.items.add(item);
    }
    
    public List<Item> getItems() {
        return this.items;
    }
    
    public String toOCamlString() {
        return items.stream()
                    .map(Item::toString)
                    .collect(Collectors.joining(","));
    }
}
