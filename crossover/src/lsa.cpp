// 求解交叉点坐标及高程.cpp : Defines the entry point for the console application.
//

// #include "stdafx.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <sstream>
#include <process.h>
#include <time.h>//计算程序运行时间
#include "math.h"
#include <malloc.h>
#include <cmath>

#define PI 3.14159265358979
#define  N_MAX  20                //定义方阵的最大阶数为20
#define  N_MARK  13  //一共有N_MARK期数据可供计算
#define  YEAR  365  //规定一年近似为365天

using namespace std;

//函数的声明部分
float MatDet(float *p, int n);                    //求矩阵的行列式
float Creat_M(float *p, int m, int n, int k);    //求矩阵元素A(m, n)的代数余之式
void print(float *p, int n);                    //输出矩阵n*n
bool Gauss(float A[][N_MAX], float B[][N_MAX], int n);    //采用部分主元的高斯消去法求方阵A的逆矩阵B
bool transpose (double A[N_MAX][N_MAX],double C[N_MAX][N_MAX], int m, int n); //矩阵转置运算
bool matmul (double A[N_MAX][N_MAX],double B[N_MAX][N_MAX],double C[N_MAX][N_MAX], int m, int n, int l);//矩阵相乘运算
bool LSA (double B_in[N_MAX][N_MAX], double L_in[N_MAX], int m, int n, double x[N_MAX], double Dxx[N_MAX][N_MAX] ) ;   //最小二乘平差算法
double Bessel_inverse(double B01,double B02,double L01,double L02);//白塞尔大地主题反算函数

double lagrange(double x_in,double *x,double *y)
{
	double y_in;
	y_in=y[1]*(x_in-x[2])*(x_in-x[3])/((x[1]-x[2])*(x[1]-x[3]))+y[2]*(x_in-x[1])*(x_in-x[3])/((x[2]-x[1])*(x[2]-x[3]))+y[3]*(x_in-x[1])*(x_in-x[2])/((x[3]-x[1])*(x[3]-x[2]));
	return y_in;
}//拉格朗日插值函数
void todouble(double *lon, double *lat,double *elev,string s)
{
	int k,i=0;
	double res[3]={0.0};
	int flag[3]={0},xs[3]={0},ws[3]={0};
	int jc[3]={1,1,1},iden=0;
	for(k=0;k<3;k++)
	{
		while(s[i]==' ')
		{i++;}//空格情况
		for( ;i<s.size();i++)
		{
			if(s[i]==' ')//如果是空格进入下一条数据
			{
				i++;
				break;
			}
			if(s[i]=='.')//小数分界线标记
			{
				flag[k]=1;
				continue;
			}
			if(s[i]=='-')
			{
				iden=1;
				continue;
			}//标识是否为负数
			if(flag[k]==0)//整数部分
			{
				res[k]*=10;
				res[k]+=s[i]-'0';
			}
			else//flag=1时为小数部分
			{
				ws[k]++;
				xs[k]*=10;
				xs[k]+=s[i]-'0';
			}
		}
		for(int j=0;j<ws[k];j++)
		{
			jc[k]*=10;
		}
		res[k]+=xs[k]*1.0/jc[k];
		if(iden==1)
		{
			res[k]=0-res[k];
			iden--;
		}
	}
	*lon=res[0];
	*lat=res[1];
	*elev=res[2];
	//	return res;
}
int countline(string filepath)
{
	std::ifstream ReadFile;
	int linenumber=0;
	string temp;
	ReadFile.open(filepath.c_str(),ios::in);//ios::in 表示以只读的方式读取文件
	if( ReadFile.fail () )
		linenumber=-1;
	else
	{
		while(getline(ReadFile,temp))
		{
			linenumber++;
		}//linenum文件行数统计
	}
	ReadFile.close();
	return linenumber;
}
double linear_regression(double *x,double *y,int n_point )
{
	double a,b;
	double av_x,av_y,L_xx,L_xy,L_yy;
	av_x = 0.0;
	av_y = 0.0;
	L_xx = 0.0;
	L_yy = 0.0;
	L_xy = 0.0;
	for (int i=0; i<n_point; i++)           //计算XY的平均值
	{
		av_x += x[i]/n_point;
		av_y += y[i]/n_point;
	}
	for (int i=0; i<n_point; i++)               //计算LxyLyy和Lxy
	{
		L_xx += (x[i] - av_x) * (x[i] - av_x);
		L_yy += (y[i] - av_y) * (y[i] - av_y);
		L_xy += (x[i] - av_x) * (y[i] - av_y);
	}
	b=L_xy/L_xx;
	a=av_y-b*av_x;
	return b;
}

struct POINTF {float x; float y;};
bool Equal(float f1, float f2) 
{
    return (abs(f1 - f2) < 1e-4f);
}
//判断两点是否相等
bool operator==(const POINTF &p1, const POINTF &p2) 
{
    return (Equal(p1.x, p2.x) && Equal(p1.y, p2.y));
}
//比较两点坐标大小，先比较x坐标，若相同则比较y坐标
bool operator>(const POINTF &p1, const POINTF &p2) 
{
    return (p1.x > p2.x || (Equal(p1.x, p2.x) && p1.y > p2.y));
}
//计算两向量外积
float operator^(const POINTF &p1, const POINTF &p2) 
{
    return (p1.x * p2.y - p1.y * p2.x);
}
//判定两线段位置关系，并求出交点(如果存在)。返回值列举如下：
//[有重合] 完全重合(6)，1个端点重合且共线(5)，部分重合(4)
//[无重合] 两端点相交(3)，交于线上(2)，正交(1)，无交(0)，参数错误(-1)
int Intersection(POINTF p1, POINTF p2, POINTF p3, POINTF p4, POINTF &Int) 
{
    //保证参数p1!=p2，p3!=p4
    if (p1 == p2 || p3 == p4) 
	{
        return -1; //返回-1代表至少有一条线段首尾重合，不能构成线段
    }
    //为方便运算，保证各线段的起点在前，终点在后。
    if (p1 > p2) 
	{
        swap(p1, p2);
    }
    if (p3 > p4) 
	{
        swap(p3, p4);
    }
    //判定两线段是否完全重合
    if (p1 == p3 && p2 == p4) 
	{
        return 6;
    }
    //求出两线段构成的向量
    POINTF v1 = {p2.x - p1.x, p2.y - p1.y}, v2 = {p4.x - p3.x, p4.y - p3.y};
    //求两向量外积，平行时外积为0
    float Corss = v1 ^ v2;
    //如果起点重合
    if (p1 == p3) 
	{
        Int = p1;
        //起点重合且共线(平行)返回5；不平行则交于端点，返回3
        return (Equal(Corss, 0) ? 5 : 3);
    }
    //如果终点重合
    if (p2 == p4) 
	{
        Int = p2;
        //终点重合且共线(平行)返回5；不平行则交于端点，返回3
        return (Equal(Corss, 0) ? 5 : 3);
    }
    //如果两线端首尾相连
    if (p1 == p4) 
	{
        Int = p1;
        return 3;
    }
    if (p2 == p3) 
	{
        Int = p2;
        return 3;
    }//经过以上判断，首尾点相重的情况都被排除了
    //将线段按起点坐标排序。若线段1的起点较大，则将两线段交换
    if (p1 > p3) 
	{
        swap(p1, p3);
        swap(p2, p4);
        //更新原先计算的向量及其外积
        swap(v1, v2);
        Corss = v1 ^ v2;
    }
    //处理两线段平行的情况
    if (Equal(Corss, 0)) 
	{
        //做向量v1(p1, p2)和vs(p1,p3)的外积，判定是否共线
        POINTF vs = {p3.x - p1.x, p3.y - p1.y};
        //外积为0则两平行线段共线，下面判定是否有重合部分
        if (Equal(v1 ^ vs, 0)) 
		{
            //前一条线的终点大于后一条线的起点，则判定存在重合
            if (p2 > p3) 
			{
                Int = p3;
                return 4; //返回值4代表线段部分重合
            }
        }//若三点不共线，则这两条平行线段必不共线。
        //不共线或共线但无重合的平行线均无交点
        return 0;
    } //以下为不平行的情况，先进行快速排斥试验
    //x坐标已有序，可直接比较。y坐标要先求两线段的最大和最小值
    float ymax1 = p1.y, ymin1 = p2.y, ymax2 = p3.y, ymin2 = p4.y;
    if (ymax1 < ymin1) 
	{
        swap(ymax1, ymin1);
    }
    if (ymax2 < ymin2) 
	{
        swap(ymax2, ymin2);
    }
    //如果以两线段为对角线的矩形不相交，则无交点
    if (p1.x > p4.x || p2.x < p3.x || ymax1 < ymin2 || ymin1 > ymax2) 
	{
        return 0;
    }//下面进行跨立试验
    POINTF vs1 = {p1.x - p3.x, p1.y - p3.y}, vs2 = {p2.x - p3.x, p2.y - p3.y};
    POINTF vt1 = {p3.x - p1.x, p3.y - p1.y}, vt2 = {p4.x - p1.x, p4.y - p1.y};
    float s1v2, s2v2, t1v1, t2v1;
    //根据外积结果判定否交于线上
    if (Equal(s1v2 = vs1 ^ v2, 0) && p4 > p1 && p1 > p3) 
	{
        Int = p1;
        return 2;
    }
    if (Equal(s2v2 = vs2 ^ v2, 0) && p4 > p2 && p2 > p3) 
	{
        Int = p2;
        return 2;
    }
    if (Equal(t1v1 = vt1 ^ v1, 0) && p2 > p3 && p3 > p1) 
	{
        Int = p3;
        return 2;
    }
    if (Equal(t2v1 = vt2 ^ v1, 0) && p2 > p4 && p4 > p1) 
	{
        Int = p4;
        return 2;
    } //未交于线上，则判定是否相交
    if(s1v2 * s2v2 > 0 || t1v1 * t2v1 > 0) 
	{
        return 0;
    } //以下为相交的情况，算法详见文档
    //计算二阶行列式的两个常数项
    float ConA = p1.x * v1.y - p1.y * v1.x;
    float ConB = p3.x * v2.y - p3.y * v2.x;
    //计算行列式D1和D2的值，除以系数行列式的值，得到交点坐标
    Int.x = (ConB * v1.x - ConA * v2.x) / Corss;
    Int.y = (ConB * v1.y - ConA * v2.y) / Corss;
    //正交返回1
    return 1;
}

int main()
{
	int i,j,k;
	
	int Col = 4;
	std::ifstream fpin;
	std::ofstream fpout;
	string filepatha,filepathd,filepath_out;
	system("dir /a-d /b D:\\Study\\AltimetryData\\ERS\\ERS1Ascend\\199506\\*.* >D:\\Study\\AltimetryData\\ERS\\ERS1Ascend\\199506TrkN.txt");
	//将文件夹2003091011中的子文件文件名写入到2003091011TrkN.txt文件中

	ifstream ReadFile;
	int LMaFN=0;
	string temp;
	ReadFile.open("D:\\Study\\AltimetryData\\ERS\\ERS1Ascend\\199506TrkN.txt",ios::in);//ios::in 表示以只读的方式读取文件
	//   ReadFile.open("G:\\ICESat\\GLA12_633\\2003_10_11FN.txt",ios::in);//ios::in 表示以只读的方式读取文件
	while(getline(ReadFile,temp))
	{
		LMaFN++;
	}//LMaFN代表文件个数，即文件名文件中的行数
	ReadFile.close();

	ifstream namefile;
	namefile.open("D:\\Study\\AltimetryData\\ERS\\ERS1Ascend\\199506TrkN.txt");
	
	string fna;

	while(LMaFN!=0)
	{
		int LMa;
		getline(namefile,fna);//将文件名赋给fna
		filepatha="D:\\Study\\AltimetryData\\ERS\\ERS1Ascend\\199506\\"+fna;//filename为文件路径
		filepath_out="D:\\Study\\AltimetryData\\CorssPoint\\ERS1_ERS2\\Ascend\\199506\\"+fna;//filepath_out为输出文件的文件路径

		cout<<filepath_out<<endl;
		
		string line;
		fpin.open(filepatha.c_str(), ios::in );//根据文件路径读取文件
		LMa = countline(filepatha);
		fpin.close ();//计算数据行数
		
		double **data_a;//存储升轨数据
    
		data_a = new double *[LMa];
		for(int i = 0;i < LMa;i++)
		{
			data_a[i]=new double[Col];
		}

		//////////////////////////////////////////申请二维动态数组

		fpin.open(filepatha.c_str(), ios::in );//根据文件路径读取文件
	
		for (i=0;i<LMa;i++)
		{
			for (j=0;j<Col;j++)
			{fpin >> data_a[i][j];}
		}//分别读取行列数据

		fpin.close ();//输入数据
		/////////////////////////////data input////////////////////////////////////////////////////////////////////////////

		///////////////////////////////////////////////////////升降轨数据文件与上文相反////////////////////////////////////////////////////////////////////////////
		system("dir /a-d /b D:\\Study\\AltimetryData\\ERS\\ERS2Descend\\199506\\*.* >D:\\Study\\AltimetryData\\ERS\\ERS2Descend\\199506TrkN.txt");
		//将文件夹2003091011中的子文件文件名写入到2003091011TrkN.txt文件中

	//	ifstream ReadFile;
		int LMdFN=0;
	//	string temp;
		ReadFile.open("D:\\Study\\AltimetryData\\ERS\\ERS2Descend\\199506TrkN.txt",ios::in);//ios::in 表示以只读的方式读取文件
		//   ReadFile.open("G:\\ICESat\\GLA12_633\\2003_10_11FN.txt",ios::in);//ios::in 表示以只读的方式读取文件
		while(getline(ReadFile,temp))
		{
			LMdFN++;
		}//LMaFN代表文件个数，即文件名文件中的行数
		ReadFile.close();

		ifstream namefiled;
		namefiled.open("D:\\Study\\AltimetryData\\ERS\\ERS2Descend\\199506TrkN.txt");
	
		string fnd;
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		while (LMdFN!=0)
		{
			int LMd;
			getline(namefiled,fnd);//将文件名赋给fna
			if (fnd!=fna)
			{
				filepathd="D:\\Study\\AltimetryData\\ERS\\ERS2Descend\\199506\\"+fnd;//filename为文件路径

				fpin.open(filepathd.c_str(), ios::in );//根据文件路径读取文件
				LMd = countline(filepathd);
				fpin.close ();//计算数据行数
		
				double **data_d;//存储降轨数据
    
				data_d = new double *[LMd];
				for(int i = 0;i < LMd;i++)
				{
					data_d[i]=new double[Col];
				}

				//////////////////////////////////////////申请二维动态数组

				fpin.open(filepathd.c_str(), ios::in );//根据文件路径读取文件
	
				for (i=0;i<LMd;i++)
				{
					for (j=0;j<Col;j++)
					{fpin >> data_d[i][j];}
				}//分别读取行列数据

				fpin.close ();//输入数据
				/////////////////////////////data input////////////////////////////////////////////////////////////////////////////

				/////////////////////////////计算两条轨道是否相交，若不想交，则计算下一条，若相交，再寻找交叉点////////////////////////////////////////////
				POINTF p1, p2, p3, p4, Int;
				p1.x=data_a[0][0];
				p1.y=data_a[0][1];
				p2.x=data_a[LMa-1][0];
				p2.y=data_a[LMa-1][1];

				p3.x=data_d[0][0];
				p3.y=data_d[0][1];
				p4.x=data_d[LMd-1][0];
				p4.y=data_d[LMd-1][1];
				int nr_t = Intersection(p1, p2, p3, p4, Int);
				if (nr_t == 1)//nr为1表示两轨道相交，则进一步寻找交叉点
				{
					
					for (int i_a=0;i_a<LMa-2;i_a++)
					{
						//if (i_a==1300)
						//	int ajlkfjlka=0;
						p1.x=data_a[i_a][0];
						p1.y=data_a[i_a][1];
						p2.x=data_a[i_a+1][0];
						p2.y=data_a[i_a+1][1];
						double Dis_a=Bessel_inverse(p1.y,p2.y,p1.x,p2.x);
						//数值太小，计算时容易误认为是零，将经纬度各扩大1000倍再进行计算，然后将经纬度缩小1000倍
						POINTF p_k_1, p_k_2, p_k_3, p_k_4, Int_k;
						p_k_1.x=data_a[i_a][0]*1000;
						p_k_1.y=data_a[i_a][1]*1000;
						p_k_2.x=data_a[i_a+1][0]*1000;
						p_k_2.y=data_a[i_a+1][1]*1000;

						if (Dis_a<2000)//相邻点距离在2km以内才进行计算
						{
							for (int j_d=0;j_d<LMd-2;j_d++)
							{
								//if (j_d==2640)
								//	int djlkyoafjk=9;
								p3.x=data_d[j_d][0];
								p3.y=data_d[j_d][1];
								p4.x=data_d[j_d+1][0];
								p4.y=data_d[j_d+1][1];
								double Dis_d=Bessel_inverse(p3.y,p4.y,p3.x,p4.x);

								p_k_3.x=data_d[j_d][0]*1000;
								p_k_3.y=data_d[j_d][1]*1000;
								p_k_4.x=data_d[j_d+1][0]*1000;
								p_k_4.y=data_d[j_d+1][1]*1000;
								//扩大1000倍

								if (Dis_d<2000)//相邻点距离在2km以内才进行计算
								{
									int nr_c = Intersection(p_k_1, p_k_2, p_k_3, p_k_4, Int_k);
									Int.x=Int_k.x/1000;
									Int.y=Int_k.y/1000;//缩小1000倍
									if (nr_c == 1 || nr_c == 2 || nr_c == 3)//nr为1、2、3时表示有交点
									{
										double Da1,Da2,Da;//求解距离，利用线性插值计算交叉点处高程,升轨
										Da1=Bessel_inverse(data_a[i_a][1],Int.y,data_a[i_a][0],Int.x);
										Da2=Bessel_inverse(data_a[i_a+1][1],Int.y,data_a[i_a+1][0],Int.x);
										Da=Da1+Da2;
										double elev_a,time_a;
										elev_a=(Da1*data_a[i_a][2]+Da2*data_a[i_a+1][2])/Da;
										time_a=(Da1*data_a[i_a][3]+Da2*data_a[i_a+1][3])/Da;

										double Dd1,Dd2,Dd;//求解距离，利用线性插值计算交叉点处高程，降轨
										Dd1=Bessel_inverse(data_d[j_d][1],Int.y,data_d[j_d][0],Int.x);
										Dd2=Bessel_inverse(data_d[j_d+1][1],Int.y,data_d[j_d+1][0],Int.x);
										Dd=Dd1+Dd2;
										double elev_d,time_d;
										elev_d=(Dd1*data_d[j_d][2]+Dd2*data_d[j_d+1][2])/Dd;
										time_d=(Dd1*data_d[j_d][3]+Dd2*data_d[j_d+1][3])/Dd;

										double del_e,del_t;
										if (time_a<time_d)
										{
											del_e=elev_d-elev_a;
											del_t=time_d-time_a;
										}
										else if (time_a>=time_d)
										{
											del_e=elev_a-elev_d;
											del_t=time_a-time_d;
										}//均以时间为序，时间靠后的数据减去时间靠前的数据
							
										//int sel=data_a[i_a][4]+data_d[j_d][4];//sel=0则两期数据都不准确，=1则其中一期数据不准确，=2则两期数据都较好

										double lon_c,lat_c;
										lon_c = Int.x;
										lat_c = Int.y;
										/////////////////数据输出///////////////////////////////////////////////////////////////////////////////////////////
										if (del_e<50 && del_e>-50)//高程相差太大表示有错误，需要剔除
										{
											fpout.open(filepath_out.c_str(), ios::app );//打开要写入文件
											fpout<<setprecision(9)<<lon_c<<" "<<setprecision(9)<<lat_c<<" "<<setprecision(11)<<time_a<<" "<<setw(8)<<elev_a<<" "<<setprecision(11)<<time_d<<" "<<setw(8)<<elev_d<<"\n";
											  //输出经度、纬度、时间、高程、时间、高程，高程与时间前者先写入，后者后写入
											fpout.close();//////关闭输出数据文件//
										}
							
	
										//////////////////////////////////////////////////
									}
								}//ifDis_d<2000相邻点距离在2km以内才进行计算，对应条件
							}
						}//if (Dis_a<2000)//相邻点距离在2km以内才进行计算，对应条件						
					}
					
				}
				for(int i = 0;i < LMd;i++)
				{
					delete data_d[i];
				}//清除内存
			}
			LMdFN--;//while循环
		}
		
		for(int i = 0;i < LMa;i++)
		{
			delete data_a[i];
		}//清除内存
		LMaFN--;//while循环
	}

	return 0;
}

//-----------------------------------------------
//功能: 求矩阵(n*n)的行列式
//入口参数: 矩阵的首地址，矩阵的行数
//返回值: 矩阵的行列式值
//----------------------------------------------
float MatDet(float *p, int n)
{
    int r, c, m;
    int lop = 0;
    float result = 0;
    float mid = 1;


    if (n != 1)
    {
        lop = (n == 2) ? 1 : n;            //控制求和循环次数,若为2阶，则循环1次，否则为n次
        for (m = 0; m < lop; m++)
        {
            mid = 1;            //顺序求和, 主对角线元素相乘之和
            for (r = 0, c = m; r < n; r++, c++)
            {
                mid = mid * (*(p+r*n+c%n));
            }
            result += mid;
        }
        for (m = 0; m < lop; m++)
        {
            mid = 1;            //逆序相减, 减去次对角线元素乘积
            for (r = 0, c = n-1-m+n; r < n; r++, c--)
            {
                mid = mid * (*(p+r*n+c%n));
            }
            result -= mid;
        }
    }
    else 
        result = *p;
    return result;
}


//----------------------------------------------------------------------------
//功能: 求k*k矩阵中元素A(m, n)的代数余之式
//入口参数: k*k矩阵的首地址，矩阵元素A的下标m,n,矩阵行数k
//返回值: k*k矩阵中元素A(m, n)的代数余之式
//----------------------------------------------------------------------------
float Creat_M(float *p, int m, int n, int k)
{
    int len;
    int i, j;
    float mid_result = 0;
    int sign = 1;
    float *p_creat, *p_mid;


    len = (k-1)*(k-1);            //k阶矩阵的代数余之式为k-1阶矩阵
    p_creat = (float*)calloc(len, sizeof(float)); //分配内存单元
    p_mid = p_creat;
    for (i = 0; i < k; i++)
    {
        for (j = 0; j < k; j++)
        {
            if (i != m && j != n) //将除第i行和第j列外的所有元素存储到以p_mid为首地址的内存单元
            {
                *p_mid++ = *(p+i*k+j);
            }
        }
    }
    sign = (m+n)%2 == 0 ? 1 : -1;    //代数余之式前面的正、负号
    mid_result = (float)sign*MatDet(p_creat, k-1);
    free(p_creat);
    return mid_result;
}


//-----------------------------------------------------
//功能: 打印n*n矩阵
//入口参数: n*n矩阵的首地址,矩阵的行数n
//返回值: 无返回值
//-----------------------------------------------------
void print(float *p, int n)
{
    int i, j;
    for (i = 0; i < n; i++)
    {
        cout << setw(4);
        for (j = 0; j < n; j++)
        {
            cout << setiosflags(ios::right) << *p++ << setw(10);
        }
        cout << endl;
    }
}


//------------------------------------------------------------------
//功能: 采用部分主元的高斯消去法求方阵A的逆矩阵B
//入口参数: 输入方阵，输出方阵，方阵阶数
//返回值: true or false
//-------------------------------------------------------------------
bool Gauss(double A[][N_MAX], double B[][N_MAX], int n)
{
    int i, j, k;
    double max, temp;
    double t[N_MAX][N_MAX];                //临时矩阵
    //将A矩阵存放在临时矩阵t[n][n]中
    for (i = 0; i < n; i++)        
    {
        for (j = 0; j < n; j++)
        {
            t[i][j] = A[i][j];
        }
    }
    //初始化B矩阵为单位阵
    for (i = 0; i < n; i++)        
    {
        for (j = 0; j < n; j++)
        {
            B[i][j] = (i == j) ? (float)1 : 0;
        }
    }
    for (i = 0; i < n; i++)
    {
        //寻找主元
        max = t[i][i];
        k = i;
        for (j = i+1; j < n; j++)
        {
            if (fabs(t[j][i]) > fabs(max))
            {
                max = t[j][i];
                k = j;
            }
        }
        //如果主元所在行不是第i行，进行行交换
        if (k != i)
        {
            for (j = 0; j < n; j++)
            {
                temp = t[i][j];
                t[i][j] = t[k][j];
                t[k][j] = temp;
                //B伴随交换
                temp = B[i][j];
                B[i][j] = B[k][j];
                B[k][j] = temp; 
            }
        }
        //判断主元是否为0, 若是, 则矩阵A不是满秩矩阵,不存在逆矩阵
        if (t[i][i] == 0)
        {
            cout << "There is no inverse matrix!";
            return false;
        }
        //消去A的第i列除去i行以外的各行元素
        temp = t[i][i];
        for (j = 0; j < n; j++)
        {
            t[i][j] = t[i][j] / temp;        //主对角线上的元素变为1
            B[i][j] = B[i][j] / temp;        //伴随计算
        }
        for (j = 0; j < n; j++)        //第0行->第n行
        {
            if (j != i)                //不是第i行
            {
                temp = t[j][i];
                for (k = 0; k < n; k++)        //第j行元素 - i行元素*j列i行元素
                {
                    t[j][k] = t[j][k] - t[i][k]*temp;
                    B[j][k] = B[j][k] - B[i][k]*temp;
                }
            }
        }
    }
    return true;
}

//------------------------------------------------------------------
//功能: 矩阵转置运算
//入口参数: 输入矩阵B，输出矩阵BT
//返回值: true or false
//-------------------------------------------------------------------
bool transpose (double A[N_MAX][N_MAX],double C[N_MAX][N_MAX], int m, int n)
{
//	double C[N_MAX][N_MAX];
	int i,j;
	for ( i=0; i<n; i++)
	{
		for(j=0; j<m; j++)
		{
			C[i][j]=A[j][i];
		}
	}
	return true;
}

//------------------------------------------------------------------
//功能: 矩阵相乘运算
//入口参数: 输入矩阵A(m*n)、B(n*l)，输出矩阵C，其中C=A*B(m*l)
//返回值: true or false
//-------------------------------------------------------------------
bool matmul (double A[N_MAX][N_MAX],double B[N_MAX][N_MAX],double C[N_MAX][N_MAX], int m, int n, int l)
{
	//A为m行n列，B为n行l列，C=AB,为m行l列的方阵
	int i,j,k;
	//初始化C矩阵
	for ( i=0; i<m; i++)
	{
		for(j=0; j<l; j++)
		{
			C[i][j]=0;
		}
	}

	for (i=0; i<m; i++)
	{
		for(j=0; j<l; j++)
		{
			for(k=0; k<n; k++)
			{
				C[i][j]+=A[i][k]*B[k][j];
			}
		}
	}
	return true;
}

//------------------------------------------------------------------
//功能: 进行平差运算，求得平差结果以及做精度评定
//入口参数: 输入矩阵B、L，输出矩阵x、v
//返回值: true or false
//-------------------------------------------------------------------
bool LSA (double B_in[N_MAX][N_MAX], double L_in[N_MAX], int m, int n, double x[N_MAX], double Dxx[N_MAX][N_MAX] )
//bool LSA ( float **& B, int m_B, int n_B , float **& L, int m_L, int n_L ) 
{
	double B[N_MAX][N_MAX], L[N_MAX], Bt[N_MAX][N_MAX], BT[N_MAX][N_MAX];
	double Nbb[N_MAX][N_MAX],NBB[N_MAX][N_MAX], W[N_MAX];
	double Nbb_1[N_MAX][N_MAX], NBB_1[N_MAX][N_MAX],v[N_MAX];
	double Qxx[N_MAX][N_MAX];
	double sig=0.0;
	int i, j;
	//m表示行数，n表示列数
	for ( i=0; i<m; i++)
	{
		for(j=0; j<n; j++)
		{
			B[i][j]=B_in[i][j];
		}
	}
	for ( i=0; i < m; i++)
	{
		L[i] = L_in[i];
	}
	if (transpose (B, BT, m, n))
	{
		cout<<"求得B转置BT\n";
		//for ( i=0; i<n_B; i++)
		//{
		//	for(j=0; j<m_B; j++)
		//	{
		//		BT[i][j]=Bt[i][j];
		//	}
		//}
	}//BT此时为n*m矩阵

	if (matmul (BT, B, NBB, n, m, n))
	{
		cout<<"求得NBB\n";
		//for ( i=0; i<n_B; i++)
		//{
		//	for(j=0; j<n_B; j++)
		//	{
		//		NBB[i][j]=Nbb[i][j];
		//	}
		//}
	}//NBB此时为n*n矩阵
	for (i=0; i<m; i++)
	{
		W[i]=0.0;
	}
	for (i=0; i<n; i++)
	{
		for(j=0; j<m; j++)
		{
			W[i]+=BT[i][j]*L[j];
		}
	}//W此时为n_B*1矩阵
	if (Gauss(NBB, NBB_1, n))
	{
		cout<<"求得NBB的逆矩阵NBB_1\n";
		//for ( i=0; i<n_B; i++)
		//{
		//	for(j=0; j<n_B; j++)
		//	{
		//		NBB_1[i][j]=Nbb_1[i][j];
		//	}
		//}
	}//求NBB的逆矩阵NBB_1
	for (i=0; i<n; i++)
	{
		x[i]=0.0;
	}
	for (i=0; i<n; i++)
	{
		for(j=0; j<n; j++)
		{
			x[i]+=NBB_1[i][j]*W[j];
		}
	}//x此时为n列
	for (i=0; i<m; i++)
	{
		v[i]=0.0;
	}
	for (i=0; i<m; i++)
	{
		for (j=0; j<n; j++)
		{
			v[i]+=B[i][j]*x[j];
		}
		v[i] = v[i]-L[i];
	}//求观测误差v
	for (i=0; i<m; i++)
	{
		sig+=v[i]*v[i];
	}
	sig=sig/(m-n);//求中误差
	for ( i=0; i<n; i++)
	{
		for(j=0; j<n; j++)
		{
			Dxx[i][j]=sig*NBB_1[i][j];
		}
	}//误差情况Dxx

	return true;
}


//-----------------------------------------------------
//功能: 利用白塞尔大地主题反算求解大地线长度
//入口参数: 两点经纬度数值,单位为°
//返回值: 大地线长度
//-----------------------------------------------------
double Bessel_inverse(double B01,double B02,double L01,double L02)
{
	double B1,B2,L1,L2;
	B1 = B01*PI/180;
	B2 = B02*PI/180;
	L1 = L01*PI/180;
	L2 = L02*PI/180;
	//将输入经纬度单位转换为弧度
	double S; //outnumber
	if (B1-B2 <= 0.00001 && B1-B2 >= -0.00001 && L1-L2 <= 0.00001 && L1-L2 >= -0.00001)
		S = 0.0;
	//如果经纬度相同，则距离为0
	else
	{
		double a,b,c,e1_2,e2_2;
		a = 6378137.0;
		b = 6356752.3142;
		c = 6399593.6258;
		e1_2 = 0.0066943799013;
		e2_2 = 0.00673949674227;//WGS84椭球参数赋值
		//a = 6378245.0;
		//b = 6356863.0187730473;
		//c = 6399698.901782711;
		//e1_2 = 0.006693421622966;
		//e2_2 = 0.006738525414683;//克拉索夫斯基椭球参数赋值
		double row = 206264.806;//row秒
		double deltL,W1,W2,sinu1,sinu2,cosu1,cosu2,a1,a2,b1,b2;//定义常用辅助函数
		deltL = L2-L1;
		W1 = sqrt(1-e1_2*sin(B1)*sin(B1));
		W2 = sqrt(1-e1_2*pow(sin(B2),2));
		sinu1 = ( sin(B1)*sqrt(1-e1_2) )/W1;
		sinu2 = ( sin(B2)*sqrt(1-e1_2) )/W2;
		cosu1 = cos(B1)/W1;
		cosu2 = cos(B2)/W2;
		a1 = sinu1*sinu2;
		a2 = cosu1*cosu2;
		b1 = cosu1*sinu2;
		b2 = sinu1*cosu2;
		double delta[2]={0.0,0.0},delta_second[2]={0.0,0.0};
		double p,q,A1,sinA0,cosA0_2,lambda;
		int mark;
		mark = 0;//第一次循环标记
		double sinsigma,cossigma, sigma, alpha, beta2,x;
		while (mark==0 || delta_second[1]-delta_second[0] <= -0.00001 || delta_second[1]-delta_second[0] >= 0.00001)
		{
			lambda = deltL+delta[1];
			p = cosu2*sin(lambda);
			q = b1-b2*cos(lambda);
			A1 = atan(p/q);
			if (p>0 && q>0)
				A1 = fabs(A1);
			else if (p>0 && q<0)
				A1 = PI-fabs(A1);
			else if (p<0 && q<0)
				A1 = PI+fabs(A1);
			else if (p<0 && q>0)
				A1 = 2*PI-fabs(A1);
			sinsigma = p*sin(A1) +q*cos(A1);
			cossigma = a1+a2*cos(lambda);
			sigma = atan(sinsigma/cossigma);
			if (cossigma >= 0)
				sigma = fabs(sigma);
			else sigma = PI-fabs(sigma);
			sinA0 = cosu1*sin(A1);
			cosA0_2 = 1-pow(sinA0,2);
			x = 2*a1-cosA0_2*cos(sigma);
	//		alpha = (33523299-(281890-70*cosA0_2)*cosA0_2)*pow(10.0,-10);
	//		beta2 = (28189-94*cosA0_2)*pow(10.0,-10);
			alpha = (e1_2/2+pow(e1_2,2)/8+pow(e1_2,3)/16)-(pow(e1_2,2)/16+pow(e1_2,3)/16)*cosA0_2+(3*pow(e1_2,3)/128)*pow(cosA0_2,2);
			beta2 = (pow(e1_2,2)/32+pow(e1_2,3)/32)*cosA0_2-(pow(e1_2,3)/64)*pow(cosA0_2,2);
	//		alpha = alpha*180/PI;
	//		beta2 = beta2*180/PI;

			delta[0] = delta[1];
			delta[1] = (alpha*sigma-beta2*sin(sigma))*sinA0;
			delta_second[0] = delta[0]*180*3600/PI;
			delta_second[1] = delta[1]*180*3600/PI;
			mark++;

		}
		double k_2;
		k_2 = e2_2*cosA0_2;
		double A,B,C,B_second,C_second;
		A = b*(1+k_2/4-3*pow(k_2,2)/64+5*pow(k_2,3)/256);
		B = b*(k_2/8-pow(k_2,2)/32+15*pow(k_2,3)/1024);
		C = b*(pow(k_2,2)/128-3*pow(k_2,3)/512);

		B_second = 2*B/cosA0_2;
		C_second = 2*C/pow(cosA0_2,2);//转换为秒单位
	/*	A = 6356863+(10708.949-13.474*cosA0_2)*cosA0_2;
		B = (5354.469-8.978*cosA0_2)*cosA0_2;
		C = (2.238*cosA0_2)*cosA0_2+0.006;
		B_second = B;
		C_second = C;
	*/
	//	B_second = B*180*3600/PI;
	//	C_second = C*180*3600/PI;//转换为秒单位

		double y;
		y = cossigma*(pow(cosA0_2,2)-2*x*x);

		S = A*sigma+sinsigma*(B_second*x+C_second*y);//求解大地线长度
	}
	return S;
}



