open Str

let read_file filename =
  let lines = ref [] in
  let channel = open_in filename in
  try
    while true do
      lines := input_line channel :: !lines
    done; []
  with End_of_file ->
    close_in channel;
    List.rev !lines

let parse_category_discount line =
  let regexp = Str.regexp "discount('\\(.*\\)', \\(.*\\))." in
  if Str.string_match regexp line 0 then
    let category = Str.matched_group 1 line in
    let discount = float_of_string (Str.matched_group 2 line) in
    Some (category, discount)
  else
    None

let parse_item line =
  let regexp = Str.regexp "item(\\(.*\\), '\\(.*\\)', '\\(.*\\)', \\(.*\\), \\(.*\\))." in
  if Str.string_match regexp line 0 then
    Some (int_of_string (Str.matched_group 1 line), Str.matched_group 2 line, Str.matched_group 3 line, float_of_string (Str.matched_group 4 line), int_of_string (Str.matched_group 5 line))
  else
    None

    let parse_loyalty_discount line =
      let regexp = Str.regexp "loyalty_discount(\\(.*\\), \\(.*\\))." in
      if Str.string_match regexp line 0 then
        let years_str = Str.matched_group 1 line in
        let discount = float_of_string (Str.matched_group 2 line) in
        try
          let years = int_of_string years_str in
          Some (years, discount)
        with Failure _ -> None
      else
        None
    
    


let parse_shipping_cost line =
  let regexp = Str.regexp "shipping_cost('\\(.*\\)', \\(.*\\))." in
  if Str.string_match regexp line 0 then
    Some (Str.matched_group 1 line, float_of_string (Str.matched_group 2 line))
  else
    None

(* calcular o preço total sem descontos *)
let calculate_total_price cart_items items =
  List.fold_left (fun acc (id, _, _, quantity) ->
    let _, _, _, price, _ = List.find (fun (item_id, _, _, _, _) -> item_id = id) items in
    acc +. price *. float_of_int quantity
  ) 0.0 cart_items

(* calcular os descontos por categoria *)
let calculate_category_discounts cart_items items category_discounts =
  List.fold_left (fun acc (id, _, category, quantity) ->
    let _, _, _, price, _ = List.find (fun (item_id, _, _, _, _) -> item_id = id) items in
    let discount = List.assoc category category_discounts in
    acc +. price *. float_of_int quantity *. discount
  ) 0.0 cart_items


(* calcular o desconto de lealdade *)
let calculate_loyalty_discount years total_price loyalty_discounts =
  let discount = List.assoc years loyalty_discounts in
  total_price *. discount

(* Função para calcular o custo de envio *)
let calculate_shipping_cost district shipping_costs =
  List.assoc district shipping_costs

(* Função para calcular o preço final do carrinho *)
let calculate_final_price total_price category_discounts loyalty_discount shipping_cost =
  total_price -. category_discounts -. loyalty_discount +. shipping_cost

(* Função para exibir o carrinho de compras *)
let display_cart cart_items items =
  let sorted_cart_items = List.sort (fun (_, _, category1, _) (_, _, category2, _) -> compare category1 category2) cart_items in
  List.iter (fun (id, name, category, quantity) ->
    let _, _, _, price, _ = List.find (fun (item_id, _, _, _, _) -> item_id = id) items in
    Printf.printf "Item: %s, Categoria: %s, Quantidade: %d, Preço: %f\n" name category quantity price
  ) sorted_cart_items

  let main () =
    (* Leitura do arquivo e parsing dos dados *)
    let file_lines = read_file "store.pl" in
    let category_discounts = List.filter_map parse_category_discount file_lines in  (* Use parse_category_discount aqui *)
    let items = List.filter_map parse_item file_lines in
    let loyalty_discounts = List.filter_map parse_loyalty_discount file_lines in
    let shipping_costs = List.filter_map parse_shipping_cost file_lines in
  
    (* Exibição das informações parseadas *)
    List.iter (fun (category, discount) -> Printf.printf "Desconto para categoria %s: %f\n" category discount) category_discounts;  
    List.iter (fun (id, name, category, price, quantity) -> Printf.printf "Item: %d, %s, %s, %f, %d\n" id name category price quantity) items;
    List.iter (fun (years, discount) -> Printf.printf "Desconto de lealdade para %d ano(s): %f\n" years discount) loyalty_discounts;
    List.iter (fun (district, cost) -> Printf.printf "Custo de envio para o distrito %s: %f\n" district cost) shipping_costs;
  
    (* lista de clientes *)
    let cart_items = [(1, "Potion of Healing", "potions", 2); 
                  (2, "Wand of Fireball", "wands", 1);
                  (3, "Enchanted Spellbook", "enchanted_books", 1);
                  (4, "Crystal of Clairvoyance", "crystals", 1);
                  (5, "Amulet of Protection", "amulets", 1)] in
    let years = 3 in
    let district = "Aveiro" in
  
    (* Cálculos *)
    let total_price = calculate_total_price cart_items items in
    let category_discounts = calculate_category_discounts cart_items items category_discounts in  
    let loyalty_discount = calculate_loyalty_discount years total_price loyalty_discounts in
    let shipping_cost = calculate_shipping_cost district shipping_costs in
    let final_price = calculate_final_price total_price category_discounts loyalty_discount shipping_cost in
  
    (* Exibicao dos resultados *)
    Printf.printf "Preço total sem descontos: %f\n" total_price;
    Printf.printf "Descontos por categoria: %f\n" category_discounts;
    Printf.printf "Desconto de lealdade: %f\n" loyalty_discount;
    Printf.printf "Custo de envio: %f\n" shipping_cost;
    Printf.printf "Preço final: %f\n" final_price;
    Printf.printf "Carrinho de compras:\n";
    display_cart cart_items items
  
let () = main ()
  