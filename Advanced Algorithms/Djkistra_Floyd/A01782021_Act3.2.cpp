//Lucía Barrenechea
//A01782021
//Programa para implementar el algoritmo de Floyd y el algoritmo de diijkistra.
#include <iostream>
#include <vector>
#include <fstream>
#include <limits>
using namespace std;

// vector<int> distance;
// vector<int> visited;

vector<vector<pair<int, int> > > readGraph(const string& filename) {
    ifstream file(filename);
    vector<vector<pair<int, int> > > listaAdj(0);

    if (file.is_open()) {
        int n, m;
        file >> n >> m;

        vector<vector<pair<int, int> > > listaAdj(n);
        
        for (int i = 0; i < m; ++i) {
            int inicio, fin, peso;
            file >> inicio >> fin >> peso;
            listaAdj[inicio].push_back(make_pair(fin, peso));
        }
        file.close();
        return listaAdj;
    } else {
        cout << "ERROR" << endl;
    }
    return listaAdj;
}

vector<vector< int> > readMatrix(const string& filename) {
    vector<vector<int> >matrix;
    ifstream file(filename);
    if (file.is_open()) {
        int n, m;
        file >> n >> m;
        matrix.resize(n, vector<int>(n,numeric_limits<int>::max() ));

        for (int i = 0; i < m; ++i) {
            int inicio, fin, peso;
            file >> inicio >> fin >> peso;
            matrix[inicio][fin] = peso;
        }
       
        file.close();
        return matrix;
    } else {
        cout << "ERROR" << endl;
    }
    return matrix;
}

//Esta función tiene una complejidad algoritmmica de Big O(n).
int distanciaMinima(vector <int> pesos, vector <bool> visitado){
    int chico=INT_MAX;
    int vector;
    for(int i=0; i<visitado.size();i++){ //Itera sobre la lista de visitado (true, false)
        if(visitado[i]==false && pesos[i]<chico){//Si no ha sido visitado y su peso actual es mas chico que el chico
            vector=i;//el num del vector.
            chico=pesos[i];// el nuevo chico es el peso de i.
        }
    }
    //cout<<"checking min:"<<vector;
    return vector; //regresa el num de vector
}

//Esta función tiene una complejidad de Big O (n^2) ya que tiene un for loop anidado
vector<int> dijkstra(const vector<vector<pair<int, int> > >& graph, int start) {
    //cout<<"hola"<<endl;
    vector <int>pesos;//guarda las distancias de las aristas.
    vector<bool>visitado;//guarda que vectores ya fueron visitados y cuales no.
    int size=graph.size();//numero de vertices
    for(int i=0; i<size; i++){//inicializa los vectores.
        pesos.push_back(10000); //representa el valor INF
        visitado.push_back(false);
    }
    pesos[start]=0;//inicializar a cero.
    for(int i=0; i<graph.size();i++){
        int indexMin=distanciaMinima(pesos,visitado);//guarda el vector mas pequeño de los pesos disponibles
        visitado[indexMin]=true;//agregar a visitado.
        for (int k = 0; k < graph[indexMin].size(); k++) {
            int objetivo = graph[indexMin][k].first;//el nodo que se va a llegar.
            int weight = graph[indexMin][k].second;//el peso para llegar
            if (!visitado[k] && pesos[indexMin] != 10000) {//si no se ha visitado y el peso no es el inicial
                if(pesos[indexMin] + weight < pesos[k]) {//si el nuevo peso es menor al actual.
                    pesos[objetivo] = pesos[indexMin] + weight;
                }
            }
}
    }
    return pesos;
}

//Esta función tiene una complejidad de Big O (n^2)
void imprimirMatrix( vector<vector<int> >& matrix) {
    cout<<"Floyd"<<endl;
    for (int i = 0; i < matrix.size(); ++i) {
        for (int j = 0; j < matrix.size(); ++j) {
                cout << matrix[i][j] << " ";
            }
             cout << endl;
        }
       
    }

//Esta función tiene una complejidad de Big O(n^3) ay que hay 3 for loops anidados.
vector<vector<int> > Floyd(vector<vector<int> >matrix){
    int size=matrix.size();
    for (int i=0; i<size; i++){
        for (int x=0; x<size; x++){
            if(i==x){
                matrix[i][x]=0;
            }
        }
    }
    
    for (int x = 0; x < size; ++x) {//Itera sobre los nodos de matrix
        for (int y = 0; y < size; ++y) {//Itera sobre eje x
            for (int j = 0; j < size; ++j) { //Itera sobre eje y
                if (matrix[y][x] != numeric_limits<int>::max() && matrix[x][j] != numeric_limits<int>::max()) {
                    if (matrix[y][j] > matrix[y][x] + matrix[x][j]  ) {//Si el valor disminuye al usar x
                        matrix[y][j] = matrix[y][x] + matrix[x][j];
                    }
                }
            }
        }
    }
    return matrix;
}

int main() {
    string filename = "dijkistra.txt";
    vector<vector<pair<int, int> > > grafo = readGraph(filename);
    vector<vector< int> >  matriz = readMatrix(filename);

    cout<<"Dijkstra"<<endl;
    for(int i=0; i<grafo.size(); i++){
        vector<int> dijkstraDistances = dijkstra(grafo, i);
        for(int k = 0; k<dijkstraDistances.size(); k++)                      
        { 
            if (dijkstraDistances[k]!=10000){
                cout<<"node "<<i<<" to node "<<k<<": "<<dijkstraDistances[k]<<endl;
            }
        }

    }

    vector<vector< int> >  Printmatriz =Floyd(matriz);
    imprimirMatrix(Printmatriz);

    return 0;
}
