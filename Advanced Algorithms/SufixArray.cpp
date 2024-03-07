//Lucía Barrenechea
//13 de octubre del 2023
//Sufix Analisis
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

//This function has a Big O notation of: O(n). depends on how big the initial string is.
vector <int>sufix(string word){
    vector <int> order;
    vector<pair<string, int> > mixedArray;//Creates a vector that accept a pair (string, int)
    int size=word.size(); //finds size of string.
    string sufix="$"; //starts the sufiz with money sign
    //Notation of O(n)
    for(int i=0; i<=size; i++){
        sufix=word[size-i]+sufix; //adds new char to sufix
        mixedArray.push_back(make_pair(sufix, size-i+1)); //adds new sufix, "size"
    }
    sort(mixedArray.begin(), mixedArray.end());//sorts lexographically using the sufix
    //Notation of O(n)
    for (int i = 0; i < mixedArray.size(); i++) {//creates vector with the "sizes" already sorted lexographically.
        order.push_back(mixedArray[i].second);
        //cout << "sufix: " << mixedArray[i].first << ", order: " << mixedArray[i].second << endl;
    }
    return order;
}

int main(){
    vector <int> order;
    string word;
    cout<<"Enter string"<<endl;
    cin>>word;
    order=sufix(word);
    for (int i = 0; i < order.size(); i++) {
       cout<<order[i]<<" ";
    }
    return 0;
}