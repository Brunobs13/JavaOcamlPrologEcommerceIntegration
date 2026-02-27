import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;



public class Store {
    private List<Cliente> clientes; //lista de clientes

    public Store() {//construtor da classe
        this.clientes = new ArrayList<>();
    }

    public void addCliente(Cliente cliente) {//metodo para adicionar clinetes a lista 
        this.clientes.add(cliente);
    }

    public List<Cliente> getClientes() {//obter lista de clientes da loja 
        return this.clientes;
    }
}