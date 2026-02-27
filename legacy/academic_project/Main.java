import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


public class Main {
    public static void main(String[] args) {
        // nova loja
        Store store = new Store();
        
        // novo cliente
        Cliente cliente = new Cliente(1, "Lisboa", "Lisboa", 3);
        
        // items ficticios de teste
        Item item1 = new Item(1, "Potion of Healing", "potions", 10.0, 2);
        Item item2 = new Item(2, "Wand of Fireball", "wands", 20.0, 1);
        Item item3 = new Item(3, "Enchanted Spellbook", "enchanted_books", 30.0, 1);
        Item item4 = new Item(4, "Crystal of Clairvoyance", "crystals", 15.0, 1);
        Item item5 = new Item(5, "Amulet of Protection", "amulets", 25.0, 1);
        
        cliente.getCarrinho().addItem(item1);
        cliente.getCarrinho().addItem(item2);
        cliente.getCarrinho().addItem(item3);
        cliente.getCarrinho().addItem(item4);
        cliente.getCarrinho().addItem(item5);
        
        // inicializa cliente
        store.addCliente(cliente);
        
        // preço total do carrinho
        double precoTotal = OperacoesCarrinho.calcularPrecoTotal(cliente.getCarrinho().getItems());
        
        //  desconto por categoria
        double descontoCategoria = OperacoesCarrinho.calcularDescontoCategoria(cliente.getCarrinho().getItems());
        
        //  os descontos de lealdade
        double descontoLealdade = OperacoesCarrinho.calcularDescontoLealdade(Integer.toString(cliente.getAnosDeLealdade()), Double.toString(precoTotal - descontoCategoria));
        
        // o custo de envio
        double custoEnvio = OperacoesCarrinho.calcularCustoEnvio(cliente.getDistrito()); 
        
        // preço final do carrinho
        double precoFinal = OperacoesCarrinho.calcularPrecoFinal(precoTotal, descontoCategoria, descontoLealdade, custoEnvio);
        
        // o carrinho de compras
        System.out.println("Carrinho de compras:\n");
        String carrinho = OperacoesCarrinho.exibirCarrinho(cliente.getCarrinho().toOCamlString());
        System.out.println(carrinho);
                        
        //o desconto de lealdade
        System.out.println("Desconto de lealdade: " + descontoLealdade);
        
        // o custo de envio
        System.out.println("Custo de envio: " + custoEnvio);
        
        System.out.println("Desconto por categoria: " + descontoCategoria);
        
        
        System.out.println("Preço total sem descontos: " + precoTotal);
        
        
        System.out.println("Preço final do carrinho: " + precoFinal);
    }
}
