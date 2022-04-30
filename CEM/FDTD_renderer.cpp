#include<fstream>
#include<iostream>
#include<cmath>
#include<string>
using namespace std;

void print(string arg){

    cout<<arg<<endl;
}
void print(double arg){
        cout<<arg<<endl;

}


int main(){
    fstream io;
    string read;

    io.open("structure.tgf");
    getline(io,read);
    getline(io,read);

    static uint8_t dim=stoi(read);
    getline(io,read);
    static bool curvilinear=false;
    if (read=="1")
    {
        curvilinear=true;
    }
    getline(io,read);
    static double deltaS=stod(read);    
    getline(io,read);
    static double deltaT=stod(read);
    //the preamble is read

    

    io.close();

    return 0;

}
