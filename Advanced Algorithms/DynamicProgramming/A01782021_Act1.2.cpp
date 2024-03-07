//Lucía Barrenechea
//28 de septiembre del 2023
#include <iostream>
#include <vector>
using namespace std;

//variables globales
vector <int> monedas;
int numero;

//Esta función tiene una complejidad Big(O) de O(n^2).
vector <int>minNumMonGR(int total, vector <int> monedas){
    vector <int> numeroMonedas(numero);
    for(int i=0; i<numero; i++){//Loop que se recorre para cada tipo de moneda. longitud de vector monedas.
         while(total>=monedas[i]){//Cambia cuando la resta de esa moneda daría un número negativo.
            total=total-monedas[i];//resta el total de moneda al total
            numeroMonedas[i]=numeroMonedas[i]+1;//agrega 1 al vector cuando se utiliza la moneda.
        }
    }
    return numeroMonedas;
}

//La función minNumMonDP tiene una complejidad Big(O) de O(n^2).
//Calcula de forma dinamica el calculo de monedas
vector <int> minNumMonDP(int total, vector <int> monedas ){
    int NumMon;
    vector<int> memory(total + 1, numeric_limits<int>::max());//guarda cantidad de monedas para formar x cantidad.
    memory[0] = 0;
    vector<int> usedCoins(total+1);//guarda que moneda se utilizo para llegar a ese total.
    vector<int> coinlist(numero);//vector que guarda cantidad de cada moneda que fue utilizada.
    for(int m = 1; m <= total; m++){//Calcula cada numero hasta llegar al total
        for(int n=0; n <= monedas.size(); n++){//itera sobre las monedas para ver cuantas se necesitan
            if (m-monedas[n] >=0){
                NumMon= memory[m - monedas[n]]+1;
                if(NumMon <= memory[m]){ //Si el calculo es mas chico que el pasado, sustituir.
                    usedCoins[m]=monedas[n];
                    memory[m]=NumMon;
                }
            }
        }
    }
    int count=0; //Cuenta las monedas. Tiene que ser igual a memory[total]
    int contar=total;
    int start=usedCoins[total];
    //while loop va a recorrer usedCoins para determinar que monedas forman el total.
     while (count<=memory[total]){
        for(int i=0;i<=monedas.size();i++){
            if(start == monedas[i]){
                coinlist[i]= coinlist[i]+1;
                contar= contar-monedas[i];
                start= usedCoins[contar];
                count= count+1;
            }
        }
     }
    return coinlist;
};

//La función escribeRespuesta tiene una complejidad Big(O) de O(n^2) ya que las dos funciones que llaman tienen complejidad de O(n^2)
void escribeRespuesta(int total){
    //Imprime los valores de programación dinamica y programación greedy.
    cout<<"Implementación Dinamica"<<endl;
    vector <int> dinamico=minNumMonDP(total, monedas);
    for (int i = 0; i < dinamico.size(); i++) {
            cout <<"Hay: "<< dinamico[i] <<" monedas de "<<monedas[i]<< endl;
     }
    cout<<endl;
    cout<<"Implementación Greedy"<<endl;
    vector <int> greedy= minNumMonGR(total, monedas);
    for (int i = 0; i < greedy.size(); i++) {
            cout <<"Hay: "<< greedy[i] <<" monedas de "<<monedas[i]<< endl;
     }
}

//El main realiza un for loop de complejidad O(n) y llama a la función escribeRespuesta que tiene de complejidad O(n^2)
//Por lo tanto, la complejidad Big O de este programa es O(n^2)
int main(){
    int total;
    int P;
    int Q;
    int moneda;
    cout<<"¿Cuantos tipos de monedas hay? ";
    cin>>numero;
    for(int i=0; i<numero; i++){
        cout<<"Inserta la moneda "<<i+1<<": ";
        cin>>moneda;
        monedas.push_back(moneda);
    }
    cout<<"¿Cual es el precio del producto que vas a comprar (P)?"<<endl;
    cin>>P;
     cout<<"¿Cuanto estas pagando (Q)?"<<endl;
    cin>>Q;
    total=Q-P;
    if(total<=0){
        cout<<"Debes dinero por lo que no se te regresara cambio. ERROR";
    }
    else{
        cout<<"Tu cambio es: "<<total<<endl;
        escribeRespuesta(total);
    }
    return 0;
}