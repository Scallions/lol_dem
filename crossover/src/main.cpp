#include <iomanip>
#include <string>
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <cmath>
#include <vector>
#include <stdlib.h>
using namespace std;

#define min(a,b) a<b?a:b  
#define max(a,b) a>b?a:b 

struct point
{
	double lon, lat, alt;
};

struct line_p2{
	string filename;
	point p1, p2;
};

struct cross_line{
	string  f1, f2;
};

int in_lat(double lat, double lat_down, double lat_up){
	if ((lat >= lat_down) && (lat <= lat_up)){
		return 1;
	}
	else
		return -1;
}

line_p2 get_p2(string filename, double lat_down, double lat_up){
	ifstream dat(filename.c_str());
	line_p2 pp;
	pp.filename = filename;
	pp.p1.lon = -99999;
	int sum = 0;
	point  r1, r2, r;
	int tag1 = 0, tag2 = 0;
	string tem;
	while (dat >> r1.lon >> r1.lat >> r1.alt>>tem){
		tag1 = in_lat(r1.lat, lat_down, lat_up);
		if (tag1 == 1){
			sum++;
			break;
		}
	}
	while (dat >> r2.lon >> r2.lat >> r2.alt>>tem){
		tag2 = in_lat(r2.lat, lat_down, lat_up);
		if (tag2 == 1)
			sum++;
		else{
			r2 = r;
			break;
		}
		r = r2;
	}
	dat.close();
	pp.p1 = r1;
	pp.p2 = r2;
	return pp;

}
double mult(point a, point b, point c)      //??  
{
	return (a.lon - c.lon)*(b.lat - c.lat) - (b.lon - c.lon)*(a.lat - c.lat);
}

bool intersect(point aa, point bb, point cc, point dd)  //??????? 
{
	if ((max(aa.lon, bb.lon)) < (min(cc.lon, dd.lon)))
	{
		return false;
	}
	if ((max(aa.lat, bb.lat)) < (min(cc.lat, dd.lat)))
	{
		return false;
	}
	if ((max(cc.lon, dd.lon)) < (min(aa.lon, bb.lon)))
	{
		return false;
	}
	if ((max(cc.lat, dd.lat)) < (min(aa.lat, bb.lat)))
	{
		return false;
	}
	if (mult(cc, bb, aa)*mult(bb, dd, aa) < 0)
	{
		return false;
	}
	if (mult(aa, dd, cc)*mult(dd, bb, cc) < 0)
	{
		return false;
	}
	return true;
}

bool in_triangl(double lon, double lat, double lon_down, double lon_up, double lat_down, double lat_up)//??????????? 
{
	if ((lon<lon_up) && (lon>lon_down))
	{
		if ((lat<lat_up) && (lat>lat_down))
			return true;
		else
			return false;

	}
	else
	{
		return false;
	}
}

point intersection(point u1, point u2, point v1, point v2)                 //?????????
{
	point ret;
	ret.lon = -999;
	ret.lat = -999;
	double t = ((u1.lon - v1.lon)*(v1.lat - v2.lat) - (u1.lat - v1.lat)*(v1.lon - v2.lon))
		/ ((u1.lon - u2.lon)*(v1.lat - v2.lat) - (u1.lat - u2.lat)*(v1.lon - v2.lon));
	ret.lon = u1.lon + (u2.lon - u1.lon)*t;
	ret.lat = u1.lat + (u2.lat - u1.lat)*t;
	return ret;
}

double distan(point a, point b){
	double d = sqrt((a.lat - b.lat)*(a.lat - b.lat) + (a.lon - b.lon)*(a.lon - b.lon));
	return d;
}

double chazhi_h(point r1, point r2, point p){
	double d1 = distan(p, r1);
	double d2 = distan(p, r2);
	double h = d1*r1.alt / (d1 + d2) + d2*r2.alt / (d1 + d2);
	return h;
}

point calc_crossover(vector<point> &l1, vector<point> &l2, int begin1, int end1, int begin2, int end2, bool & tag){

	point line1[11];
	point line2[11];
	int gap1, gap2;

	int num = 0;
	while ((end1 - begin1) > 10 || (end2 - begin2) > 10){
		num++;
		
		

		//ofstream out(to_string(num).c_str());

		if ((end1 - begin1) > 10){
			gap1 = (end1 - begin1) / 10;
			for (int i = 0; i <= 10; i++){
				if (i == 10){
					line1[10] = l1[end1];
					break;
				}
				line1[i] = l1[begin1 + i*gap1];
				//out << fixed << setprecision(7) << line1[i].lon << " " << line1[i].lat << endl;
			}
		}

		if ((end2 - begin2) > 10){
			gap2 = (end2 - begin2) / 10;
			for (int i = 0; i <= 10; i++){
				if (i == 10){
					line2[10] = l2[end2];
					break;
				}
				line2[i] = l2[begin2 + i*gap2];
				//out << fixed << setprecision(7) << line2[i].lon << " " << line2[i].lat << endl;
			}
		}

		//out.close();
		
	
		if ((end1 - begin1) > 10){
			if ((end2 - begin2) > 10){
				int mark = 0;
				for (int i = 0; i < 10; i++){
					for ( int j = 0; j < 10; j++){
						if (intersect(line1[i], line1[i + 1], line2[j], line2[j + 1])){
							if (i != 9)
								end1 = begin1 + gap1*(i + 1);
							if (j != 9)
								end2 = begin2 + gap2*(j + 1);
							begin1 = begin1 + gap1*i;
							begin2 = begin2 + gap2*j;
							mark = 1;
							break;
						}
					}
					if (mark == 1)
						break;

				}
			}
			else{
				for (int i = 0; i < 10; i++){
					if (intersect(line1[i], line1[i + 1], l2[begin2], l2[end2])){
						if (i != 9)
							end1 = begin1 + gap1*(i + 1);
						begin1 = begin1 + gap1*i;
						break;
					}
				}
			}
		}
		else{
			
			for (int i = 0; i < 10; i++){
				if (intersect(l1[begin1], l1[end1], line2[i], line2[i + 1])){
					if (i != 9)
						end2 = begin2 + gap2*(i + 1);
					begin2 = begin2 + gap2*i;
					break;
				}
			}
		}
		
		//cout << num << endl;
		//cout << begin1 << " " << end1 << " " << begin2 << " " << end2 << endl;

		if (num >= 10){
			cout << "??????" << endl;
			break;
			/*point p_w = { -999, -999, -999 };
			return p_w;*/
		}
	}

	

	for (int i = begin1; i < end1; i++){
		for (int j = begin2; j < end2; j++){
			if (intersect(l1[i], l1[i + 1], l2[j], l2[j + 1])){
				tag = true;
				point p_r = intersection(l1[i], l1[i + 1], l2[j], l2[j + 1]);
				p_r.alt = chazhi_h(l1[i], l1[i + 1], p_r) - chazhi_h(l2[j], l2[j + 1], p_r);
				return p_r;
			}			
		}
	}
	cout << "error" << endl;
	point p_w = { -999, -999, -999 };
	return p_w;

}

point get_crossover(string f1, string f2, bool & tag){

	cout << f1 << " " << f2 << endl;

	tag = false;

	vector<point> l1;
	vector<point> l2;

	point tem;
	string str;
	ifstream ff1(f1.c_str());
	while (ff1 >> tem.lon >> tem.lat >> tem.alt >> str)
		l1.push_back(tem);
	ff1.close();

	ifstream ff2(f2.c_str());
	while (ff2 >> tem.lon >> tem.lat >> tem.alt >> str)
		l2.push_back(tem);
	ff2.close();

	//cout << l1.size() - 1 << " " << l2.size() - 1 << endl;

	return calc_crossover(l1, l2,0,l1.size()-1,0,l2.size()-1, tag);

}

int main(int argc, char argv[])
{
	double lon_down, lon_up, lat_down, lat_up;
	lon_down = 294, lon_up = 309, lat_down = 33, lat_up = 48;
	string  filename;
	/////////////////////////////////////////////////////////////////////////////////////////////////////
	
	//system("dir D:\\1111\\data\\in_r /s /b  >filelist.txt");
	
	//ifstream filelist("filelist.txt");
	//vector<line_p2> p2;
	//int num1 = 0;
	//while (filelist >> filename){
	//	cout << "????" << filename << endl;
	//	num1++;
	//	line_p2 ppp = get_p2(filename, lat_down, lat_up);
	//	p2.push_back(ppp);
	//}
	//cout << p2.size() << endl;
	//
	//ofstream p2_out("p2_out.txt");
	//
	//for (int i = 0; i< p2.size(); i++)
	//	p2_out << p2[i].filename << " " << fixed << setprecision(7) << p2[i].p1.lon << " " << p2[i].p1.lat << " " << p2[i].p2.lon << " " << p2[i].p2.lat << endl;
	////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////
	//vector<cross_line> cross;
	//ifstream p2_out("p2_out.txt");
	//line_p2 ppp;
	//vector<line_p2> p2;
	//while (p2_out >> ppp.filename >> ppp.p1.lon  >> ppp.p1.lat >> ppp.p2.lon >> ppp.p2.lat )
	//	p2.push_back(ppp);
	//cout << p2.size() << endl;
	//for (int i = 0; i< p2.size(); i++)
	//{
	//	for (int j = i + 1; j < p2.size(); j++){
	//		//cout << p2[i].filename.substr(16, 17).c_str() << endl;
	//		if (strcmp(p2[i].filename.substr(16, 17).c_str(), p2[j].filename.substr(16, 17).c_str()) != 0)
	//		{
	//			if (intersect(p2[i].p1, p2[i].p2, p2[j].p1, p2[j].p2))
	//			{
	//				cross_line tem;
	//				tem.f1 = p2[i].filename;
	//				tem.f2 = p2[j].filename;
	//				cross.push_back(tem);
	//			}
	//		}
	//	}

	//}

	//cout << "????:" << cross.size() << endl;

	//ofstream cross_l("cross_line.txt");
	//for (int i = 0; i< cross.size(); i++)
	//	cross_l << cross[i].f1 << " " << cross[i].f2 << endl;
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	ifstream cross_l("cross_line.txt");
	cross_line cross_p;
	point crossover;
	ofstream result("crossover.txt",ios::app);
	ofstream result_r("crossover_r.txt",ios::app);
	ofstream result_w("crossover_w.txt");
	bool tag;
	while (cross_l >> cross_p.f1 >> cross_p.f2){
		crossover = get_crossover(cross_p.f1, cross_p.f2,tag);
		if (tag == false)
			result_w << cross_p.f1 << "?" << cross_p.f2 << endl;
		else{
			result_r << cross_p.f1 << "?" << cross_p.f2 << "  " << fixed << setprecision(7) << crossover.lon << " " << crossover.lat << " " << crossover.alt << endl;
			result<< fixed << setprecision(7) << crossover.lon << " " << crossover.lat << " " << crossover.alt << endl;
		}
			
	}
	  


	return 0;
}

