import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Item { 
    private int id;     //criaçao do items de compras,
    private String nome;
    private String categoria;
    private double preco;
    private int quantidade;
    
    public Item(int id, String nome, String categoria, double preco, int quantidade) {
        this.id = id;
        this.nome = nome;
        this.categoria = categoria;
        this.preco = preco;
        this.quantidade = quantidade;
    }
    
    // getters e setters
    public int getId() {
        return this.id;
    }
    
    public String getNome() {
        return this.nome;
    }
    
    public String getCategoria() {
        return this.categoria;
    }
    
    public double getPreco() {
        return this.preco;
    }
    
    public int getQuantidade() {
        return this.quantidade;
    }
    
    @Override
    public String toString() {
        return id + ";" + nome + ";" + categoria + ";" + preco + ";" + quantidade;
    }
}

