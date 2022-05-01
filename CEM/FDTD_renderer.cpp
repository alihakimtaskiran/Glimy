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
    uint32_t i=0;
    uint32_t shapes[5]={0};//Rectangle, Circle, RectPrism, Sphere, Cylinder
    while(read!=""){
        getline(io,read);
        if(i%5==0)
        {
            if (read=="RECTANGLE")
            {
                shapes[0]+=1;
            }
            else if(read=="CIRCLE")
            {
                shapes[1]+=1;
            }
            else if(read=="RECTPRISM")
            {
                shapes[2]+=1;
            }
            else if(read=="SPHERE")
            {
                shapes[3]+=1;
            }
            else if(read=="CYLINDER")
            {
                shapes[4]+=1;
            }
        }        
        i++;
    }

    io.close();

    double rectangle[shapes[0]][8]={0.};//A_x, A_y, A_z, B_x, B_y, B_z, n, k
    double circle[shapes[1]][6]={0.};//C_x, C_y,C_z, r, n, k
    double rectprism[shapes[2]][8]={0.};//A_x, A_y, A_z, B_x, B_y, B_z, n, k
    double sphere[shapes[3]][6]={0.};//C_x, C_y,C_z, r, n, k
    double cylinder[shapes[4]][7]={0.};//C_x, C_y, C_z, r, h, n, k

    io.open("structure.tgf");

    for (int i=0; i<5;i++){
        getline(io, read);

    }

    uint32_t i=0;
    uint8_t shapes=0;
    while(read!=""){
        getline(io,read);
        if(i%5==0)
        {
            if (read=="RECTANGLE")
            {
                shapes=0;
            }
            else if(read=="CIRCLE")
            {
                shapes=1;
            }
            else if(read=="RECTPRISM")
            {
                shapes=2;
            }
            else if(read=="SPHERE")
            {
                shapes=3;
            }
            else if(read=="CYLINDER")
            {
                shapes=4;
            }
        }   


        i++;
    }


    io.close();
    return 0;

}
