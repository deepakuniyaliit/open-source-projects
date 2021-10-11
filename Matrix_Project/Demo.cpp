#include"Matrix.h"
#include<iostream>
using namespace std;
int main(){
    vector<vector<int> > vec={
        {1,1},
        {1,0}
    };
    Matrix mat(vec);
    mat=Pow(mat,10);
    cout<<mat;
    return 0;

}