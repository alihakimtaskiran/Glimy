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

    for (int i=0; i<5;i++)
    {
        getline(io, read);
    }

    i=0;
    uint8_t shape=0;
    uint32_t sc[5]={0,0,0,0,0};//shape_counts
    while(getline(io,read)){
        if(i%5==0)
        {
            if (read=="RECTANGLE")
            {
                shape=0;
            }
            else if(read=="CIRCLE")
            {
                shape=1;
            }
            else if(read=="RECTPRISM")
            {
                shape=2;
            }
            else if(read=="SPHERE")
            {
                shape=3;
            }
            else if(read=="CYLINDER")
            {
                shape=4;
            }
        }   

        else if(i%5==1)
        {
            
            
                if (shape== 0)
                {
                    uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    rectangle[0][0]=stod(read.substr(1, spaces[0]));
                    rectangle[sc[0]][1]=stod(read.substr(spaces[0], spaces[1]));
                    rectangle[sc[0]][2]=stod(read.substr(spaces[1],_));
                    
                }

                else if (shape==1 )
                {   
                    uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    circle[sc[1]][0]=stod(read.substr(1, spaces[0]));
                    circle[sc[1]][1]=stod(read.substr(spaces[0], spaces[1]));
                    circle[sc[1]][2]=stod(read.substr(spaces[1],_));
                }
                else if (shape==2 )
                {   uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    rectprism[sc[2]][0]=stod(read.substr(1, spaces[0]));
                    rectprism[sc[2]][1]=stod(read.substr(spaces[0], spaces[1]));
                    rectprism[sc[2]][2]=stod(read.substr(spaces[1],_));
                }
                else if (shape== 3)
                {   uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    sphere[sc[3]][0]=stod(read.substr(1, spaces[0]));
                    sphere[sc[3]][1]=stod(read.substr(spaces[0], spaces[1]));
                    sphere[sc[3]][2]=stod(read.substr(spaces[1],_));
                }
                else if (shape== 4)
                {   
                    uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    cylinder[sc[4]][0]=stod(read.substr(1, spaces[0]));
                    cylinder[sc[4]][1]=stod(read.substr(spaces[0], spaces[1]));
                    cylinder[sc[4]][2]=stod(read.substr(spaces[1],_));
                    
                }


            }

        

        else if(i%5==2)
        {
            
            switch(shape)
            {
                case 0:
                {
                    uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                    if(read[j]==' ')
                    {   
                        spaces[space_count]=j;
                            space_count++;
                        }
                    }

                    rectangle[sc[0]][3]=stod(read.substr(1, spaces[0]));
                    rectangle[sc[0]][4]=stod(read.substr(spaces[0], spaces[1]));
                    rectangle[sc[0]][5]=stod(read.substr(spaces[1],_));

                    break;
                }
                case 1:
                {
                    circle[sc[1]][3]=stod(read);
                    break;
                }
                case 2:
                {
                    uint16_t spaces[2]={0};
                    uint8_t space_count=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                    if(read[j]==' ')
                    {   
                        spaces[space_count]=j;
                            space_count++;
                        }
                    }
                    rectprism[sc[2]][3]=stod(read.substr(1, spaces[0]));
                    rectprism[sc[2]][4]=stod(read.substr(spaces[0], spaces[1]));
                    rectprism[sc[2]][5]=stod(read.substr(spaces[1],_));
                    break;
                }
                case 3:
                {
                    sphere[sc[3]][3]=stod(read);
                    break;
                }
                case 4:
                {
                    uint8_t space=0;
                    uint8_t _=read.length()-1;
                    for(uint16_t j=1;j<_;j++)
                    {
                        if(read[j]==' ')
                        {   
                            space=j;
                            break;
                        }

                    }
                    cylinder[sc[4]][3]=stod(read.substr(1, space));
                    cylinder[sc[4]][4]=stod(read.substr(space,_));
                    break;
                }
        }
        
    }


        else if(i%5==3)//refractive indexes
        {
            if (shape==0)
            {
               rectangle[sc[0]][6]=stod(read);
            }
            else if(shape==1)
            {
               circle[sc[1]][4]=stod(read);
            }
            else if(shape==2)
            {
               rectprism[sc[2]][6]=stod(read);
            }
            else if(shape==3)
            {
                sphere[sc[3]][4]=stod(read);   
            }
            else if(shape==4)
            {
                cylinder[sc[4]][5]=stod(read);
            }
        }   
         else if(i%5==4)//extiniction coefficients
        {
            if (shape==0)
            {
                rectangle[sc[0]][7]=stod(read);

               
            }
            else if(shape==1)
            {
                circle[sc[1]][5]=stod(read);
            }
            else if(shape==2)
            {
                rectprism[sc[2]][7]=stod(read);
            }
            else if(shape==3)
            {
                sphere[sc[3]][5]=stod(read);
            }
            else if(shape==4)
            {
                cylinder[sc[4]][6]=stod(read);
            }
            sc[shape]++;
        }   
        i++;

    }

    io.close();
    //Metric Topology import done

    return 0;

}
