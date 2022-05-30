#include<fstream>
#include<iostream>
#include<cmath> 
#include<string>
using namespace std;

void print(string arg){

    cout<<arg<<endl;
}
void print(float arg){
        cout<<arg<<endl;

}

float Z_0=376.730313;
float c=299792458;
float pi_2=2*M_PI;
float sqrt_2=pow(2,.5);
float sqrt_3=pow(3, .5);

int main()
{

    fstream io;
    string read;
    io.open("/tmp/MemoriesWillFade/counts.tgf");
    std::getline(io,read);
    int n_of_types=stoi(read);

    //As the new geometries are defined, add here new shapes
    unsigned long shapes[6]={0,0,0,0,0,0};//Lines, Rectangles, Circles, RectPrisms, Sphere, Cylinder

    unsigned long *pt_shapes=&shapes[0];

    std::getline(io,read);
    shapes[0]=stol(read);
    float lines[*pt_shapes][7];//A, B, layer, Re(e), Im(e), Re(mu), Im(mu)

    std::getline(io,read);
    shapes[1]=stol(read);
    float rectangles[*(pt_shapes+1)][9]; //A1, A2, B1, B2, layer, Re(e), Im(e), Re(mu), Im(mu)

    std::getline(io,read);
    shapes[2]=stol(read);
    float circles[*(pt_shapes+2)][8]; //A1, A2, r, layer, Re(e), Im(e), Re(mu), Im(mu)



    io.close();



    io.open("/tmp/MemoriesWillFade/structure.tgf");//topological geometry file
    std::getline(io, read);//reading preamble

    std::getline(io, read);
    int16_t dim=stoi(read);
    std::getline(io, read);
    unsigned long n_of_geometries=stoi(read);
    std::getline(io, read);
    bool ANC=bool(stoi(read));
    std::getline(io, read);
    float ds=stof(read);
    float dt=ds/c;

    unsigned long grid_size[dim];
    for(uint8_t i=0;i<dim;i++)
    {
        std::getline(io, read);
       
        grid_size[i]=stoi(read);
    }
    std::getline(io, read);

    for(unsigned long i=0;i<n_of_geometries; i++)
    {   
        std::getline(io, read);
        uint8_t space_count=0;
        uint16_t __=read.length();
        for(uint8_t j=0;j<__;j++)
        {
            if(read[j]==' ')
            {
                space_count+=1;
            }
        }
        uint16_t spaces[space_count+2];
        spaces[0]=0;
        uint16_t si=1;
        for(uint8_t j=0;j<__;j++)
        {
            if(read[j]==' ')
            {   
                spaces[si]=j;
                si+=1;
            }
        }
        spaces[space_count+1]=__-1;
        uint8_t _=space_count+1;
 
        uint8_t type=stoi(read.substr(spaces[0],spaces[1]));
        
        switch(type){
            case 0:

                for(uint8_t j=1;j<_;j++)
                {   
                    lines[i][j-1]=stof(read.substr(spaces[j], spaces[j+1]));
                    //cout<<lines[i][j-1]<<"||";


                }
                //print("");
                break;
            
            case 1:

                for(uint8_t j=1;j<_;j++)
                {   
                    rectangles[i][j-1]=stof(read.substr(spaces[j], spaces[j+1]));
                    //cout<<rectangles[i][j-1]<<"||";


                }
                //print("");
                break;
            
            case 2:

                for(uint8_t j=1;j<_;j++)
                {   
                    circles[i][j-1]=stof(read.substr(spaces[j], spaces[j+1]));
                    //cout<<circles[i][j-1]<<"||";


                }
                //print("");
                break;

        }
        
    }
    io.close();
    
    io.open("/tmp/MemoriesWillFade/energizers.wm");
    std::getline(io,read);
    unsigned long n_of_energizers=stol(read);
    uint8_t ___=dim+5;
    float energizers[n_of_energizers][___];//[location], [presence], amplitude, frequency, phase
    for(unsigned long i=0; i<n_of_energizers; i++)
    {
        std::getline(io,read);
        int8_t _=dim+6;
        uint32_t spaces[_];
        spaces[0]=0;
        uint32_t len=read.length();
        spaces[dim+5]=len;
        uint8_t sc=1;
        for(uint32_t j=0;j<len;j++)
        {
            if(read[j]==' ')
            {   
                spaces[sc]=j;
                sc++;
            }
        }

        for(uint8_t j=0;j<___;j++)
        {
            energizers[i][j]=stof(read.substr(spaces[j],spaces[j+1]));

        }
    }

    io.close();




    io.open("/tmp/MemoriesWillFade/renderer.dat");
    std::getline(io,read);
    unsigned long n_time_iter=stol(read);
    unsigned long observer[dim];
    for(uint8_t i=0;i<dim;i++)
    {
        std::getline(io,read);
        observer[i]=stol(read);
    }
    std::getline(io,read);
    string savedir=read;
    io.close();


    if(dim==1)
    {
  
        float E_z[grid_size[0]]={0.};
        float H_y[grid_size[0]]={0.};

        float e_r[grid_size[0]][2];
        float mu_r[grid_size[0]][2];


        for(unsigned long li=0;li<grid_size[0];li++)
        {
            float current_layer=lines[0][2];
            unsigned long current_shape=0;
           
           for(unsigned long sh=0; sh<n_of_geometries; sh++)
           {
               if(lines[sh][2]<current_layer && lines[sh][0]<=li &&li<=lines[sh][1])
               {
                   current_layer=lines[sh][2];
                   current_shape=sh;
               }
            
           }
           e_r[li][0]=lines[current_shape][3];
           e_r[li][1]=lines[current_shape][4];
           mu_r[li][0]=lines[current_shape][5];
           mu_r[li][1]=lines[current_shape][6];
          // cout<<li<<":"<<e_r[li][0]<<"**"<<mu_r[li][0]<<endl;
        }
       
        float sampler[n_time_iter];

        for(unsigned long ti=0; ti<n_time_iter; ti++)
        {
            for(unsigned long source=0; source<n_of_energizers; source++)
            {

                float *pt=&energizers[source][0];

                if(*(pt+1)<=ti&&ti<*(pt+2))
                {   
                    int __=*pt;
                    E_z[__]=(*pt+3)*sin(pi_2*ti*dt*(*(pt+4))+(*pt+5));
                }


            }

            for(unsigned long li=0;li<grid_size[0]-1;li++)
            {
                H_y[li]+=(E_z[li+1]-E_z[li])/(Z_0*mu_r[li][0]);
            }
            
            for(unsigned long li=0;li<grid_size[0];li++)
            {
                E_z[li]+=(H_y[li]-H_y[li-1])*Z_0/e_r[li][0];
            }

            sampler[ti]=E_z[observer[0]];

        }

        io.open(savedir+"/wave.wm");
        for(unsigned long ti=0; ti<n_time_iter; ti++)
        {
            io<<to_string(sampler[ti])<<" ";
        }
        io.close();
        
    
        
    }

    else if(dim==2)
    {
        float E_z[grid_size[0]][grid_size[1]]={0.};
        float H_x[grid_size[0]][grid_size[1]]={0.};
        float H_y[grid_size[0]][grid_size[1]]={0.};

        float e_r[grid_size[0]][grid_size[1]][2];
        float mu_r[grid_size[0]][grid_size[1]][2];

        float sampler[n_time_iter];

        for(unsigned long x=0;x<grid_size[0];x++)
        {
            for(unsigned long y=0; y<grid_size[1];y++)
            {
                for(unsigned long i=0; i<*(pt_shapes+1); i++)
                {
                    int current_layer=1001;
                    int current_shape[2]={0,0};
                    if(rectangles[i][4]<current_layer)
                    {
                        if (((rectangles[i][0]>=x&&x>=rectangles[i][2])||(rectangles[i][0]<=x&&x<=rectangles[i][2]))&&( (rectangles[i][3]>=y&&y>=rectangles[i][1])||(rectangles[i][3]<=y&&y<=rectangles[i][1])))

                        {
                            //cout<<x<<","<<y<<" is in Rect "<<i<<endl;
                            current_layer=rectangles[i][4];
                            current_shape[0]=0;
                            current_shape[1]=i;
                        }
                    }
                    if(circles[i][3]<current_layer){
                        if( pow((circles[i][0]-x),2)+pow((circles[i][1]-y),2)<=pow(circles[i][3],2)  )
                        {
                            current_layer=circles[i][3];
                            current_shape[0]=1;
                            current_shape[1]=i;
                            //cout<<x<<","<<y<<" is in Circle "<<i<<endl;
                        }
                    }
                    if(current_layer==1001)
                    {
                        e_r[x][y][0]=1;
                        e_r[x][y][1]=1;
                        mu_r[x][y][0]=1;
                        mu_r[x][y][1]=1;

                    }
                    else
                    {
                        switch (current_shape[0])
                        {
                        case 0:
                            e_r[x][y][0]=rectangles[current_shape[1]][5];
                            e_r[x][y][1]=rectangles[current_shape[1]][6];
                            mu_r[x][y][0]=rectangles[current_shape[1]][7];
                            mu_r[x][y][1]=rectangles[current_shape[1]][8];
                            break;
                        case 1:
                            e_r[x][y][0]=circles[current_shape[1]][4];
                            e_r[x][y][1]=circles[current_shape[1]][5];
                            mu_r[x][y][0]=circles[current_shape[1]][6];
                            mu_r[x][y][1]=circles[current_shape[1]][7];
                        default:
                            break;
                        }
                    
                    }
                    //cout<<e_r[x][y][0]<<" "<<e_r[x][y][1]<<"**"<<mu_r[x][y][0]<<" "<<mu_r[x][y][1]<<endl;
                   
                }

                


                   
            }
        }

        for(unsigned long ti=0;ti<n_time_iter;ti++)
        {   

            

            for(unsigned long x=0;x<grid_size[0]-1;x++)
            {
                for(unsigned long y=0;y<grid_size[1]-1;y++)
                {
                    H_x[x][y]-=(E_z[x][y+1]-E_z[x][y])/Z_0/sqrt_2*mu_r[x][y][0];
                    H_y[x][y]+=(E_z[x+1][y]-E_z[x][y])/Z_0/sqrt_2*mu_r[x][y][0];
                }
            }

            for(unsigned long x=0;x<grid_size[0];x++)
            {
                for(unsigned long y=0;y<grid_size[1];y++)
                {
                    E_z[x][y]+=(H_y[x][y]-H_y[x-1][y]-H_x[x][y]+H_x[x][y-1])*Z_0/sqrt_2/e_r[x][y][0];
                }
            }

            for(unsigned long source=0; source<n_of_energizers; source++)
            {   
                float *pt=&energizers[source][0];
               
                if(*(pt+2)<=ti&&ti<*(pt+3))
                {   
                    int _=*pt;
                    int __=*(pt+1);
                    
                    E_z[_][__]+=(*pt+4)*sin(pi_2*ti*dt*(*(pt+5))+(*pt+6));
                }

            }

            sampler[ti]=E_z[observer[0]][observer[1]];


        }
        io.open(savedir+"/wave.wm");
        for(unsigned long ti=0; ti<n_time_iter; ti++)
        {
            io<<to_string(sampler[ti])<<" ";
        }
        io.close();

    }


    return 0;
}
