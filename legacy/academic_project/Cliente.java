import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


public class Cliente {
    private int id;
    private String cidade;
    private String distrito;
    private int anosDeLealdade;
    private Cart carrinho;
    
    public Cliente(int id, String cidade, String distrito, int anosDeLealdade) {
        this.id = id;
        this.cidade = cidade;
        this.distrito = distrito;
        this.anosDeLealdade = anosDeLealdade;
        this.carrinho = new Cart();  //carrinho inicializado 
    }
    
    // getters
    public int getId() {
        return this.id;
    }
    
    public String getCidade() {
        return this.cidade;
    }
    
    public String getDistrito() {
        return this.distrito;
    }
    
    public int getAnosDeLealdade() {
        return this.anosDeLealdade;
    }
    
    public Cart getCarrinho() {
        return this.carrinho;
    }
    
    // setters
    public void setId(int id) {
        this.id = id;
    }
    
    public void setCidade(String cidade) {
        this.cidade = cidade;
    }
    
    public void setDistrito(String distrito) {
        this.distrito = distrito;
    }
    
    public void setAnosDeLealdade(int anosDeLealdade) {
        this.anosDeLealdade = anosDeLealdade;
    }
    
    public void setCarrinho(Cart carrinho) {
        this.carrinho = carrinho;
    }
}
