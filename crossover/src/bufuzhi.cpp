#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>


using namespace std;

struct point{
    double lon;
    double lat;
    double high;
    double t;
};

istream& operator>> (istream &in, point &p){
    in >> p.lon >> p.lat >> p.high >> p.t;
    return in;
}

struct line{
    vector<point> ps;
    string filename;
};

struct cross_over
{
    line *l1;
    line *l2;
    double bufu;
    int n1; // l1 number
    int n2; // l2 number
    double t1; // l1 time
    double t2; // l2 time
};


line read_line(string filename){
    ifstream fstream(filename);
    line l;
    l.filename = filename;
    point p;
    while(fstream >> p){
        l.ps.push_back(p);
    }
    return l;
}

double bufuzhi_of_twoline(line &l1, line &l2){

}

void bufuzhi(vector<line> &lines){
    int n = lines.size();
    // 遍历求交叉点 = = 感觉可以优化
    vector<double> bufus;
    for(int i=0;i<n;++i){
        for(int j=i+1;j<n;++j){
            line &l1 = lines[i];
            line &l2 = lines[j];
            double bufu = bufuzhi_of_twoline(l1, l2);
            if(bufu > 0){
                bufus.push_back(bufu);
            }
        }
    }
}

void cross_over_adjustment(vector<cross_over> cs){
    int N = 100; // lines count
    int M = cs.size(); 
    vector<vector<double>> coefficient(M*2, vector<double>(2*N,0));
    vector<double> x(N*2,0);
    vector<double> v(M*2,0);
    // build coefficient matrix
    for(int i=0;i<M;++i){
        cross_over cv = cs[i];
        v[2*i] = cv.bufu/2;
        v[2*i+1] = -cv.bufu/2;
        coefficient[2*i][2*cv.n1] = 1;
        coefficient[2*i][2*cv.n1+1] = cv.t1;  
        coefficient[2*i+1][2*cv.n2] = 1;
        coefficient[2*i+1][2*cv.n2+1] = cv.t2;
    }

    // solve x
    // x = (A^T \times P A)^{-1} \times A^T \times P \times v;    

    // adjustment
}

int main()
{

    return 0;    
}