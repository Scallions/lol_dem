/*
 * Read data in dir and find cross point ouput to a file
 * change old c++ style to c++11 and more modern
 */

#include <iomanip>
#include <string>
//#include <stdio.h>
#include <fstream>
#include <iostream>
#include <map>
#include <cmath>
#include <vector>
//#include <stdlib.h>
#include <boost/filesystem.hpp>
#include "threadpool.h"
#include "progressbar.hpp"

using namespace std;
using namespace indicators;

// 点数据
struct point
{
	double lon, lat, alt;
	int t1,t2;
};

// 交叉点
struct crosspoint
{
	double lon, lat, alt1, alt2;
	double ta, td;
	int i,j;
	bool tag; // 标记是否找到交叉点 false表示无
	string f1, f2;
};

// Deprecated
// struct cross_line{
// 	string  f1, f2;
// };

double mult(point a, point b, point c)      //??
{
	return (a.lon - c.lon)*(b.lat - c.lat) - (b.lon - c.lon)*(a.lat - c.lat);
}

bool intersect(point aa, point bb, point cc, point dd)  
{
    // find lien ab line cd intersect pint ??
	// 排斥
	if ((max(aa.lon, bb.lon)) < (min(cc.lon, dd.lon)))
	{
        // ab upder cd
		return false;
	}
	if ((max(aa.lat, bb.lat)) < (min(cc.lat, dd.lat)))
	{
        // ab left cd
		return false;
	}
	if ((max(cc.lon, dd.lon)) < (min(aa.lon, bb.lon)))
	{
        // cd upder ab
		return false;
	}
	if ((max(cc.lat, dd.lat)) < (min(aa.lat, bb.lat)))
	{
        // cd left ab
		return false;
	}
	// 结束排斥实验

	// 判断是否在同一侧
	if (mult(cc, bb, aa)*mult(bb, dd, aa) < 0)
	{
		// cd 在 ab同一侧
		return false;
	}
	if (mult(aa, dd, cc)*mult(dd, bb, cc) < 0)
	{
		// ab 在 cd同一侧
		return false;
	}
	return true;
}

inline bool in_rectangle(double lon, double lat, double lon_down, double lon_up, double lat_down, double lat_up)//判断点是否在矩形里
{
    // in rectangle = =
	if ((lon<lon_up) && (lon>lon_down) && (lat<lat_up) && (lat>lat_down))
		return true;
	else
		return false;
}

crosspoint intersection(point u1, point u2, point v1, point v2)                 //求交叉点坐标
{
    // find intersection point lon lat pos
	// ref https://www.cnblogs.com/ZQUACM-875180305/p/10149769.html
	crosspoint ret;
	ret.lon = -999;
	ret.lat = -999;
	// double d = (u2.lon-u1.lon)*(v2.lat-v1.lat) - (u1.lon-u2.lon)*(v1.lat-v2.lat);
	// double b1 = (u2.lat-u1.lat)*u1.lon + (u1.lon-u2.lon)*u1.lat;
	// double b2 = (v2.lat-v1.lat)*v1.lon + (v1.lon-v2.lon)*v1.lat;
	// double d1 = b2*(u2.lon-u1.lon) - b1*(v2.lon-v1.lon);
	// double d2 = b2*(u2.lat-u1.lat) - b1*(v2.lat-v1.lat);
	// ret.lon = d1/d;
	// ret.lat = d2/d;
	double t = ((u1.lon - v1.lon)*(v1.lat - v2.lat) - (u1.lat - v1.lat)*(v1.lon - v2.lon))
		/ ((u1.lon - u2.lon)*(v1.lat - v2.lat) - (u1.lat - u2.lat)*(v1.lon - v2.lon));
	ret.lon = u1.lon + (u2.lon - u1.lon)*t;
	ret.lat = u1.lat + (u2.lat - u1.lat)*t;
	return ret;
}

double distan(point a, point b){
	// 单位球面距离
	double t = 3.1415926/180;
	double d = acos(cos(a.lat*t) * cos(b.lat*t) * cos(a.lon*t - b.lon*t) + sin(a.lat*t) * sin(b.lat*t));
	return d;
}

double insert_h(point r1, point r2, crosspoint& p_r){
    // insert height with distance weight
	point p_t = {p_r.lon, p_r.lat,0};
	double d1 = distan(p_t, r1);
	double d2 = distan(p_t, r2);
	double h = d2*r1.alt / (d1 + d2) + d1*r2.alt / (d1 + d2);
	// set time
	return h;
}

crosspoint calc_crossover(const vector<point> &l1, const vector<point> &l2, int begin1, int end1, int begin2, int end2, bool &tag){
	point line1[11];
	point line2[11];
	int gap1, gap2;
    if(end1 < 2 || end2 < 2){
        crosspoint p_w = { -999, -999, -999 };
        return p_w;
    }
	int num = 0;
	while ((end1 - begin1) > 10 || (end2 - begin2) > 10){
		num++;
		
		// 采样
		if ((end1 - begin1) > 10){
			gap1 = (end1 - begin1) / 10;
			for (int i = 0; i <= 10; i++){
				if (i == 10){
					line1[10] = l1[end1];
					break;
				}
				line1[i] = l1[begin1 + i*gap1];
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
			}
		}
		// end 采样

        // update begine end to some range
		if ((end1 - begin1) > 10){
			if ((end2 - begin2) > 10){
                // length1 > 10 and length2 > 10
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
                // length 1 > 10 and length2 < 10
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
			// length 1 < 10 
			for (int i = 0; i < 10; i++){
				if (intersect(l1[begin1], l1[end1], line2[i], line2[i + 1])){
					if (i != 9)
						end2 = begin2 + gap2*(i + 1);
					begin2 = begin2 + gap2*i;
					break;
				}
			}
		}

		if (num >= 10){
			break;
		}
	}

	

	for (int i = begin1; i < end1; i++){
		for (int j = begin2; j < end2; j++){
			double ta = (l1[i+1].t1+l1[i+1].t2/28.0 - l1[i].t1 - l1[i].t2/28.0);
			double td = (l2[j+1].t1+l2[j+1].t2/28.0 - l2[j].t1 - l2[j].t2/28.0);
			// if(ta > 20.0 / 28 || td > 20.0 / 28) break;
			if (intersect(l1[i], l1[i + 1], l2[j], l2[j + 1])){
				tag = true;
				crosspoint p_r = intersection(l1[i], l1[i + 1], l2[j], l2[j + 1]);
				p_r.i = i, p_r.j = j;
				// point p_t = {p_r.lon, p_r.lat,0};
				p_r.alt1 = insert_h(l1[i], l1[i + 1], p_r);
				p_r.alt2 = insert_h(l2[j], l2[j + 1], p_r);
				double dta = (p_r.alt1 - l1[i].alt) / (l1[i+1].alt - l1[i].alt);
				double dtd = (p_r.alt2 - l2[j].alt) / (l2[j+1].alt - l2[j].alt);
				p_r.ta = l1[i].t1 + l1[i].t2/28.0 + ta*dta;
				p_r.td = l2[j].t1 + l2[j].t2/28.0 + td*dtd;
				return p_r;
			}			
		}
	}
	crosspoint p_w = { -999, -999, -999 , -1, -1, -1};
	return p_w;

}

crosspoint get_crossover(const string &f1, const string &f2, map<string, vector<point>>& lmap){// if find crossover set tage to true and return point

	bool tag = false;

	vector<point> l1 = lmap[f1];
	vector<point> l2 = lmap[f2];

	crosspoint cp =  calc_crossover(l1, l2,0,l1.size()-1,0,l2.size()-1, tag);
	cp.f1 = f1;
	cp.f2 = f2;
	cp.tag = tag;

	// 检查 nan
	if(isnan(cp.ta) || isnan(cp.td) || isnan(cp.alt1) || isnan(cp.alt2)){
		cp.tag = false;
	}

	return cp;

}

int main(int argc, char** argv)
{
	double lon_down, lon_up, lat_down, lat_up;
    lon_down = 48.285536, lon_up = 211.296789, lat_down = -90, lat_up = -89.322266;
	string  filename;

    if(argc<2)
    {
        cout << "Usage:" << endl;
        cout << "   ./crossover <dat_dir> [O]" << endl;
        return 1;
    }
	string dir = argv[1];
	string ext = argc==7?argv[6]:argc==3?argv[2]:"O";

	if(argc >= 6){
		lon_down = atof(argv[2]);
		lon_up = atof(argv[3]);
		lat_down = atof(argv[4]);
		lat_up = atof(argv[5]);
	}

    boost::filesystem::path dir_path(dir);
    if(!boost::filesystem::exists(dir_path))  //推断文件存在性
    {
        cout << "Directory doesn't exists: " << dir_path << endl;
        return 1;
    }

    cout << "++++++++++++++++++++++++++++++" << endl;
    cout << "       Start crossover        " << endl;
    cout << "++++++++++++++++++++++++++++++" << endl;
	cout << "\tRead dir: " << dir_path.string() << endl;
	cout << "\tRead area: " << lon_down << "," << lon_up << "," << lat_down << "," << lat_up << endl;


	cout << "Finding all file." << endl;
	vector<string> afilepaths;
	vector<string> dfilepaths;
    boost::filesystem::recursive_directory_iterator itEnd;
	map<string, vector<point>> lmap;
    for(boost::filesystem::recursive_directory_iterator itor( dir_path ); itor != itEnd ;++itor)
    {
        // 遍历文件夹
        if((itor->path().extension() == ".A"+ext) && (itor->path().stem().string().substr(0,7) == "LOLARDR")) // 找到 dat 数据文件
        {
			afilepaths.push_back(itor->path().string());
			vector<point> l1;

			point tem;
			ifstream ff1(itor->path().string().c_str());
			int t;
			while (ff1 >> tem.lon >> tem.lat >> tem.alt>>tem.t1>>tem.t2)
				l1.push_back(tem);
			ff1.close();
			lmap[itor->path().string()] = l1;
		}
		if((itor->path().extension() == ".D"+ext) && (itor->path().stem().string().substr(0,7) == "LOLARDR")) // 找到 dat 数据文件
        {
			dfilepaths.push_back(itor->path().string());
			vector<point> l1;

			point tem;
			ifstream ff1(itor->path().string().c_str());
			int t;
			while (ff1 >> tem.lon >> tem.lat >> tem.alt>>tem.t1>>tem.t2)
				l1.push_back(tem);
			ff1.close();
			lmap[itor->path().string()] = l1;
		}
	}
	cout << "\tAscend orbits: " << afilepaths.size() << endl;
	cout << "\tDscend orbits: " << dfilepaths.size() << endl;

	crosspoint crossover;
	// multiple thread
	vector<future<crosspoint>> result_fs;
	ThreadPool pool(48);

	boost::filesystem::path out_path = dir_path / ("crossover" + ext + ".txt");
	ofstream result(out_path.string().c_str());
    int nums = afilepaths.size();
	cout << "Finding crossover." << endl;
	for(int i=0; i<afilepaths.size(); i++){
		for(int j=0; j<dfilepaths.size(); j++){
			result_fs.emplace_back(pool.enqueue([&lmap](string f1, string f2) {
				return get_crossover(f1, f2, lmap);
			}, afilepaths[i], dfilepaths[j]));
		}
	}
	cout << "\tTask size: " << result_fs.size() << endl;
	int count_t = 0;
	int count_all = result_fs.size();
	int count_ct = 0;
	ProgressBar bar{
		option::BarWidth{100},
		option::Start{"["},
		option::Fill{"■"},
		option::Lead{"■"},
		option::Remainder{"-"},
		option::End{" ]"},
		option::ForegroundColor{Color::cyan},
		option::PostfixText{"Finding crossover..."},
		option::ShowElapsedTime{true},
		option::ShowRemainingTime{true},
		// option::MaxProgress{count_all},
		option::FontStyles{std::vector<FontStyle>{FontStyle::bold},
		}
	};
	for(auto && result_f: result_fs){
		crossover = result_f.get();
		if (crossover.tag == true && abs(crossover.alt1 - crossover.alt2) < 5){  // filter gate
			result<< fixed << setprecision(7) << crossover.f1 <<" "<< crossover.f2 <<" " <<crossover.i<<" "<<crossover.j<<" "<<crossover.ta<<" "<<crossover.td<<" "<< crossover.lon << " " << crossover.lat << " " << crossover.alt1 - crossover.alt2 << endl;
			++count_t;
		}
		++count_ct;
		// bar.tick();
		if(count_ct % (count_all / 100) == 0){
			bar.set_progress(count_ct * 100 / count_all);
		}
	}
	bar.mark_as_completed();
	cout << "\tFind crosspoint: " << count_t << endl;
    result.close();
	cout << endl;
	return 0;
}

