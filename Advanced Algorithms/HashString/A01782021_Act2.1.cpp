//Lucía Barrenechea
// 16 de octubre del 2023
//Hash a text adding each column and turning into hexadecimal.
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
using namespace std;
//This function has a big o notation of O(n^2) since there is a for loop inside a while loop.
vector <string> hashFunction(string file, int num){
    num=num-1;
    vector<char>characters;
    int count=0;
    ifstream myfile;
    myfile.open(file);
    if(myfile.is_open()){
        char c;
        char x;
        while(myfile.get(c)) {
            x= toupper(c); //turn to uppercase
            characters.push_back(x);
            count++;
        }
    }
    else{
        cout<<"Not able to open the file"<<endl;
        return;
    }
    int remainder=count%num; //numbers to complete last line.
    int total= count+remainder;//total chars with the extra.
    int fila= total/num; //finds number of rows.
    int times=total/fila;//finds columns.
    for(int i=0; i<=remainder; i++){
        characters.push_back(num);//insert missing char to string
    }
    vector<string>hexa; //will store already in hexadecimal values
    int x=0;
    int ASCCI=0;
    int value=0;
    //Big O notation of O(n^2)
    while(x<=times){ //until there is still an available row.
        for(int i=x; i<total; i+=times){
            ASCCI+=static_cast<int>(characters[i]); //finds ascci
        }
        value=ASCCI%256;
        stringstream stream;
        stream << hex << uppercase << value; //converts int value to hexadecimal using uppercases. Stores in stream.
        string hexadecimal= stream.str(); //converts stream to a string named hhexadecimal
        hexa.push_back(hexadecimal);//adds to vector
        ASCCI=0;
        x++;
    }
    //Big O notation of O(n). Prints vector
    for (int c=0; c<= hexa.size(); c++) {
        cout << hexa[c]<<""; 
    }
    return hexa;
}
int main(){
    hashFunction("hash.txt",24);
    return 0;
}