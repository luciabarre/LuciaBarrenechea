//Lucía Barrenechea
//23 de noviembre del 2023
#include <iostream>
#include <vector>
#include <fstream>
#include <limits>
#include <queue>
#include <cmath>
#include <utility>
#include <climits>
using namespace std;
//How to execute: g++ -std=c++11 astar.cpp -o astar 

struct VectorComparator {
    bool operator()(const vector<int>& v1, const vector<int>& v2) const {
        return v1[5] > v2[5]; // Compare based on the value at index 5
    }
};

//Has a big o of (n)
bool isNodeInOpenList(priority_queue<vector<int>, vector<vector<int> >, VectorComparator>& openList, int x, int y, int newF) {
    priority_queue<vector<int>, vector<vector<int> >, VectorComparator> temp;

    bool found = false;

    while (!openList.empty()) {
        vector<int> tempNode = openList.top();
        openList.pop();

        if (tempNode[0] == x && tempNode[1] == y) {
            found = true;
            if (tempNode[3] < newF) {
                // The node in the OPEN list has a smaller f value
                found = false;
            }
        }

        temp.push(tempNode);
    }
    // Restore the original order of the priority queue
    while (!temp.empty()) {
        openList.push(temp.top());
        temp.pop();
    }
    return found;
}


int heuristicManhattan(int x, int y, int goalX, int goalY) {
    return abs(x - goalX) + abs(y - goalY);
}

//HAs a Big O complexity of O(c)
bool checkvalidity(int x, int y, int num){
    if(x>=0 and x<num){
        if(y>=0 and y<num){
            //cout<<"valid neighbor"<<x<<y<<endl;
            return 1;
        }
        //cout<<"invalid neighbor"<<x<<y<<endl;
    }
    return 0;
}

//Has a Big O complexity of O(n^2)
vector<vector<int> > createMatrix(vector<vector<int> > matrix) {
    for (size_t i = 0; i < matrix.size(); ++i) {
        vector<int> line;
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            line.push_back(0);
        }
        matrix.push_back(line);
    }

    for (size_t i = 0; i < matrix.size(); ++i) {
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            cout << matrix[i][j] << i << j << " ";
        }
        cout << endl;
    }

    return matrix;
}

//Has a big O of O(c)
string directions(const vector<pair<int, int> >& path) {
    string directions;

    for (int i = 1; i < path.size(); ++i) {
        int x1 = path[i - 1].first;
        int x2 = path[i].first;
        int y1 = path[i - 1].second;
        int y2 = path[i].second;
        // cout<<x1<<", "<<y1<<endl;
        // cout<<x2<<", "<<y2<<endl;
        //Calcula Que dirección due la que se hizo comparando el nodo anterior con el siguiente.
        if (x2 == x1 + 1) {
            directions += 'R';  // Move Right
            //cout<<"R"<<endl;
        } else if (x2 == x1 - 1) {
            directions += 'L';  // Move Left
            //cout<<"L"<<endl;
        } else if (x2 == x1) {
            if (y2 == y1 + 1) {
                directions += 'U';  // Move Up
                //cout<<"U"<<endl;
            } else if (y2 == y1 - 1) {
                directions += 'D';  // Move Down
                //cout<<"D"<<endl;
            }
        }
        // Handle other cases as needed
    }
    cout << directions << endl;

    return directions;
}

//Has a Big O complexity of O(n^2)
vector <int> astar(vector<vector <vector <int> > > matrix, vector<vector <int> > matrix1, vector <int> inicio, vector <int> objetivo, int N){
    vector <int> order;
    //Create priority queue for exploration
    priority_queue<vector<int>, vector<vector<int> >, VectorComparator > openList;
    vector<vector<int> > cost(N, vector<int>(N, 11000));
    vector<vector<vector<int> > > cameFrom(N, vector<vector<int> >(N, vector<int>(2, 0)));
    
    cameFrom[inicio[1]][inicio[0]][0]=inicio[0]; //added x value of beginning
    cameFrom[inicio[1]][inicio[0]][1]=inicio[1]; //added y value of beggining

    for (size_t i = 0; i < cost.size(); ++i) {
        for (size_t j = 0; j < cost[i].size(); ++j) {
            cout << cost[i][j] << " ";
        }
        cout << endl;
    }
    openList.push(inicio);
    vector<pair<int, int> > neighbors;
    neighbors.push_back(make_pair(-1, 0)); 
    neighbors.push_back(make_pair(1, 0));
    neighbors.push_back(make_pair(0, -1));
    neighbors.push_back(make_pair(0, 1));
    vector<pair<int,int> > path;
    while(!openList.empty()){
        vector <int> actual=openList.top();//el nodo con f mas pequeño
        openList.pop();//sacarlo ya que se esta explorando
        //Explore neighbors to see if valid
        for(int i=0; i<neighbors.size();i++){
            int x1=neighbors[i].first+actual[0];//sum of x
            //cout<<x1<<endl;
            int y1=neighbors[i].second+actual[1];//sum of y
            if(checkvalidity(x1,y1,N)==1){
                if (x1 == objetivo[0] && y1 == objetivo[1]) {
    //You have reached the goal
                    while (!(actual[0] == inicio[0] && actual[1] == inicio[1])) {
                        path.push_back(make_pair(actual[0], actual[1]));
                        int tempX = actual[0];
                        actual[0] = cameFrom[actual[1]][tempX][0];
                        actual[1] = cameFrom[actual[1]][tempX][1];
                    }
                    //path.push_back(make_pair(0, 0));
}
                else{
                    if(matrix1[x1][y1]==1){
                        int h=heuristicManhattan(x1,y1,N-1,N-1);
                        for (size_t i = 0; i < cost.size(); ++i) {
                        for (size_t j = 0; j < cost[i].size(); ++j) {
                            cout << cost[i][j] << " ";
                        }
                        cout << endl;
                            }
                        int g;
                        if(cost[x1][y1]==11000){
                            int g=+1; //cost of predecessor plus one
                            cout<<g;
                        }
                        else{
                            int g=cost[x1][y1]+1; //cost of predecessor plus one
                            cout<<g;
                        }
                         //cost of predecessor plus one
                        int f=h+g;
                        
                        if (f < cost[x1][y1]) {//if the cost is less than what already exists in that position
                            
                            if(isNodeInOpenList(openList, x1,y1,f)==false){//if a node with the same position is already in openlist and has a bigger f
                                cost[x1][y1] = f;
                                cameFrom[y1][x1][0]=actual[0]; //added x value of beginning
                                cameFrom[y1][x1][1]=actual[1];
                                vector <int> neighbor;
                                neighbor.push_back(x1);//x value
                                neighbor.push_back(y1);//y value
                                neighbor.push_back(h); //heuristic
                                neighbor.push_back(f); //total cost
                                openList.push(neighbor);
                            }
                        }
                     }
                    }
            }
        }
    }
    
    cout<<endl;
    cout<<endl;
    cout<<endl;
    cout<<endl;
    path.push_back(make_pair(0, 0));
    //Used to calculate directions
    directions(path);

    return order;
}



int main(){
    int num=4;
  
   vector<vector<int> > matrix;
   vector<int> line;
   line.push_back(1);
   line.push_back(0);
   line.push_back(0);
   line.push_back(0);
   matrix.push_back(line);
   vector<int> line2;
   line2.push_back(1);
   line2.push_back(1);
   line2.push_back(0);
   line2.push_back(1);
   matrix.push_back(line2);
   vector<int> line3;
   line3.push_back(1);
   line3.push_back(1);
   line3.push_back(0);
   line3.push_back(0);
   matrix.push_back(line3);
   vector<int> line4;
   line4.push_back(0);
   line4.push_back(1);
   line4.push_back(1);
   line4.push_back(1);
   matrix.push_back(line4);


    vector<vector<vector<int> > > matrix3;
    for (int y = 0; y < matrix.size(); y++) {
        vector<vector<int> > lines;
        for (int x = 0; x < matrix[y].size(); x++) {
            vector<int> coordinates;
            coordinates.push_back(x);          // x coordinate
            coordinates.push_back(y);          // y coordinate
            // coordinates.push_back(matrix[y][x]); // node value
            //coordinates.push_back(0); //stores cost
            coordinates.push_back(0); //stores heuristic
            coordinates.push_back(0); //stores f

            lines.push_back(coordinates);
        }
        matrix3.push_back(lines);
    }
 
    cout<<matrix[3][1]<<endl;
    vector<int>start;
    start.push_back(0);
    start.push_back(0);
    start.push_back(0);
    start.push_back(0);
    vector<int>end;
    end.push_back(num-1);
    end.push_back(num-1);
    end.push_back(0);
    end.push_back(0);

    astar(matrix3,matrix,start,end,num);





    return 0;
}