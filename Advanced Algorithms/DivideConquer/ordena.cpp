//Lucía Barrenechea
// Sept. 7, 2023
//Advanced Algorithms
//Program that implements quickSort and mergeSort in a vector with values that come from file "file2.txt"
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

//This function reads the first line of the code (size)
//BIG O Notation: O(1): will only read the first line of the file
int readSize(){
    int arraysize;
     ifstream myfile;
     myfile.open("file2.txt");
     if(myfile.is_open()){
        string size;
        getline(myfile, size);
        arraysize= stoi(size);
     };
     return arraysize-1; //Subtracts 1 because array index includes 0
}
//BIG O Notation: O(n): n increases depending on the number of values of the original file.
//Prints the vector
void imprimeDatos( vector <int> sample){
    for (int i = 0; i < sample.size(); i++) {
        cout << sample[i] << " ";
    }
};

//BIG O Notation: O(n): n increases depending on the size of values in the file.
//This function reads all of the file and stores the values in a vector called sample.
vector <int> leeDatos(string archive){
    vector<int> sample;
    ifstream myfile;
    myfile.open(archive); //opening file.
    int counter = 0;
    if (myfile.is_open()){
        string value, first;
        getline(myfile, first);
        int condition= stoi(first);
        for(int x=0; x<condition; x++){
            if(getline(myfile, value)){
                int vectorvalue= stoi(value);
                sample.push_back(vectorvalue); 
            }
            else{
                cout<<"The vector is to big for the values.\n";
                //imprimeDatos(sample);
                myfile.close();
                cout << "Incorrect File Format: The program won't work correctly.\n";
                break;
                //return sample;
            }
        }

        myfile.close();
    };
    return sample;
};

//BIG O Notation: O(1): Only switches 2 values each time.
void change(int*num1, int*num2){
    int change= *num1;
    *num1= *num2;
    *num2= change;
};

//BIG O Notation: O(n): time complexity increases as n increases. while loop will increase iterations the bigger the vector.
//partition function to divide and separate QuickSort
int Sort_element(vector <int> &sample, int start, int end){ //start(0) y end(size).
   int i=start +1;
   int j=end;
   int pivot= sample[start]; //el primer valor de cada vector
   int temp;
   int count=0; //indica que la variable i ya ha parado
   int count2=0; //indica que la variable j ya ha parado
   while (i<=j){ //While loop continues until j passes i
        if(sample[i] <= pivot){
            i++;
        }
        else{
            count=1;
        }
        if(sample[j] >= pivot){
            j--;
        }
        else{
            count2=1;
        }
        if(count == 1 && count2 == 1){
            count=0;
            count2=0;
            change(&sample[i], &sample[j]);//Swaps values when they both stop
        }
   }
   change(&sample[start], &sample[j]);
   return j; //returns the pivot index
};

//BIG O Notation: O(n): tiem complexity increases as n increases. Recursion creates a loop that depends on n values of the vector
//REvisar como se va a calcular el pivot y la size cuando empieza la recursividad.
vector <int> quickSort(vector <int> &sample, int start, int size){ //size=end of vector
    if(start < size){
        int pivot= Sort_element(sample, start, size);
        //line 92/93 are in charge of using recursion to sort both sides of the vector uisng the pivot as a midpoint.
        quickSort(sample, start, pivot - 1); // sorting left side array
        quickSort(sample, pivot + 1, size); //sorting right side array
    };
    return sample;
};

//BIG O Notation: O(n): time complexity increases as n increases. while loop will increase iterations the bigger the vector.
//Sorts values depending on size for Merge Sort.
void SortMerge(vector <int> &sample, vector <int> &left, vector <int> &right){
    int index = 0; //keeps count of sample index
    int x = 0; //keeps count of right
    int y = 0; //keeps count of left
    int sizeLeft= left.size();
    int sizeRight= right.size();
    //until both sides have been all sorted out
    while (y < sizeLeft && x < sizeRight) { //until both sides have been all sorted out
        if (left[y] <= right[x]) { //compares the first elements of the vectors and adds the left if smallest.
            sample[index] = left[y];
            y++; //since an element was added, the index increments to compare next element
        } 
        else { // Compares the first elements of the vectors and adds the right if smallest.
            sample[index] = right[x];
            x++; // Since an element was added, the index increments to compare the next element
        }
        index++; // Original vector index increased since an element was added
    }
    while(x < sizeRight){ //adds elements of right in case that left is empty first
        sample[index]= right[x];
        x++;
        index++;
    }
    while(y < sizeLeft){ //adds elements of left in case that right is empty first
        sample[index]= left[y];
        y++;
        index++;
    }
};

//BIG O Notation: O(n): time complexity increases as n increases. Recursion creates a loop that depends on n values of the vector
//Recursive Function that divides vector into vector right and vvector left.
void mergeSort(vector <int> &sample){
    //int his function the vector will be separated until sample.size()<2
    if(sample.size()<2){
        return;
    }
    int midPoint= sample.size()/2;
    //creates temporary right vector
    vector<int> right( sample.begin(), sample.begin()+ midPoint); //Creates vector that starts form beginning to center
   // Creates temporary left vector
    vector<int> left( sample.begin() + midPoint, sample.end()); //Creates vector that starts from center to end
    mergeSort(left); //Will separate the left side of the array using recursion
    mergeSort(right); //Will separate the right side of the array using recursion
    SortMerge(sample , left, right); //This function merges the separate sides in order.
    return;
};

//BIG O Notation: O(1):  main only calls on functions.
int main(){
    int size = readSize(); //Indicates amount of numbers in the file
    cout<<"The file contains: "<<size+1<<" numbers\n";
    vector<int> sample = leeDatos("file2.txt"); //you can change file name HERE
    vector <int> sample2= sample;

    cout << "Data Before QuickSort" << "\n ";
    imprimeDatos(sample);
    cout << "\n ";
    vector <int> imprimir= quickSort(sample, 0 , size);
    cout << "Data After QuickSort" << "\n ";
    imprimeDatos(imprimir);
    cout << "\n ";

    cout << "Data Before MergeSort" << "\n ";
    imprimeDatos(sample2);//prints list before applying mergeSort
    cout << "\n ";
    mergeSort(sample2);
    cout << "Data After MergeSort" << "\n ";
    imprimeDatos(sample2); //prints list after applying mergeSort
    return 0;
};


